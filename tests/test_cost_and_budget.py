"""
================================================================================
Test Module: tests.test_cost_and_budget
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: QA unit tests verifying central token metering, price catalog,
             budget reservations, hard stops at 100%, and the 5-sutra pilot module.
================================================================================
"""

import pytest
from src.cost.budget import BudgetManager
from src.cost.catalog import PriceCatalog, get_default_price_catalog
from src.cost.estimator import PreCallEstimator
from src.cost.metering import TokenMeteringService
from src.cost.reporting import CostReporter
from src.database.repository import ManuscriptRepository
from src.pilot.pilot_workflow import PilotWorkflowEngine
from src.providers.base import ProviderBudgetExceededError
from src.providers.openai_adapter import OpenAIAdapter


@pytest.fixture
def isolated_cost_stack(tmp_path):
    """Fixture providing isolated repository and cost managers."""
    db_file = tmp_path / "test_cost.db"
    repo = ManuscriptRepository(db_path=db_file)
    catalog = PriceCatalog()
    metering = TokenMeteringService(repository=repo, catalog=catalog, exchange_rate_inr=83.50)
    budget = BudgetManager(repository=repo)
    estimator = PreCallEstimator(catalog=catalog, budget_manager=budget, exchange_rate_inr=83.50)
    reporter = CostReporter(repository=repo)
    pilot = PilotWorkflowEngine(repository=repo, metering_service=metering)
    return {
        "repo": repo,
        "catalog": catalog,
        "metering": metering,
        "budget": budget,
        "estimator": estimator,
        "reporter": reporter,
        "pilot": pilot,
    }


def test_price_catalog_rates_and_verification(isolated_cost_stack):
    catalog = isolated_cost_stack["catalog"]
    gemini_price = catalog.get_price("google", "gemini-1.5-pro")
    assert gemini_price is not None
    assert gemini_price.input_price_per_m == 3.50
    assert gemini_price.output_price_per_m == 10.50
    assert gemini_price.is_verified is False  # Flagged provisional until explicit live check
    assert "https://ai.google.dev/pricing" in gemini_price.official_source_url

    cost = catalog.calculate_cost_usd("google", "gemini-1.5-pro", input_tokens=1000, output_tokens=500)
    assert cost > 0


def test_token_metering_and_idempotency(isolated_cost_stack):
    metering = isolated_cost_stack["metering"]
    repo = isolated_cost_stack["repo"]

    # First call
    record1 = metering.record_usage(
        provider="anthropic",
        model_id="claude-3-5-sonnet-20241022",
        agent_role="sutrakar_master",
        workflow_id="wf-001",
        execution_id="exec-001",
        input_tokens=1000,
        output_tokens=500,
    )
    assert record1["cost_inr"] > 0
    assert record1["exchange_rate_inr"] == 83.50

    # Duplicate call with identical execution_id and attempt
    metering.record_usage(
        provider="anthropic",
        model_id="claude-3-5-sonnet-20241022",
        agent_role="sutrakar_master",
        workflow_id="wf-001",
        execution_id="exec-001",
        input_tokens=1000,
        output_tokens=500,
    )

    # Verify no duplicate billing record created
    records = repo.get_token_usage_records()
    assert len(records) == 1


def test_budget_manager_hard_stop_at_100_percent(isolated_cost_stack):
    budget = isolated_cost_stack["budget"]
    # Set a tiny budget of 10 INR
    budget.configure_budget(scope_type="project_monthly", scope_name="sk_sutras_total", monthly_limit_inr=10.0)

    # Try reserving 15 INR -> Should raise ProviderBudgetExceededError
    with pytest.raises(ProviderBudgetExceededError) as exc_info:
        budget.check_and_reserve(
            scope_type="project_monthly",
            scope_name="sk_sutras_total",
            estimated_cost_inr=15.0,
            reservation_id="res-001",
        )
    assert "Budget limit of ₹10.00 INR" in str(exc_info.value)


def test_pre_call_estimator(isolated_cost_stack):
    estimator = isolated_cost_stack["estimator"]
    adapter = OpenAIAdapter(offline_mode=True)

    estimate = estimator.estimate(
        adapter=adapter,
        prompt="Analyze Shandilya Sutra 1 in detail",
        system_prompt="You are Shandilya specialist.",
        max_output_tokens=1000,
    )
    assert estimate.estimated_input_tokens > 0
    assert estimate.estimated_output_tokens == 1000
    assert estimate.estimated_cost_inr > 0
    assert estimate.is_budget_permissible is True


def test_cost_reporting_and_csv_export(isolated_cost_stack):
    metering = isolated_cost_stack["metering"]
    reporter = isolated_cost_stack["reporter"]

    metering.record_usage(
        provider="google",
        model_id="gemini-1.5-pro",
        agent_role="narada_specialist",
        workflow_id="wf-test",
        execution_id="narada-01",
        input_tokens=500,
        output_tokens=200,
    )
    metering.record_usage(
        provider="openai",
        model_id="gpt-4o",
        agent_role="independent_validator",
        workflow_id="wf-test",
        execution_id="val-01",
        input_tokens=800,
        output_tokens=150,
    )

    breakdown = reporter.get_four_agent_breakdown()
    assert len(breakdown["by_agent"]) == 2

    csv_text = reporter.export_csv()
    assert "narada_specialist" in csv_text
    assert "independent_validator" in csv_text


def test_five_sutra_pilot_workflow(isolated_cost_stack):
    pilot = isolated_cost_stack["pilot"]
    results = pilot.execute_pilot()

    assert results.total_candidates_evaluated == 5
    assert results.accepted_for_composition == 4
    assert results.rejected_weak_candidates == 1  # Crucial: NBS 35 vs SBS 80 rejected
    assert results.total_cost_inr > 0
    assert results.average_cost_per_approved_sutra_inr > 0
    assert results.projected_50_sutras_cost_inr > results.total_cost_inr
    assert results.contingency_buffer_recommended_percent == 20.0
