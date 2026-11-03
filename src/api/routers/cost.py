"""
================================================================================
Module: src.api.routers.cost
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: FastAPI route handlers for token consumption telemetry, 4-agent
             cost visibility, budget management, and CSV reporting.
================================================================================
"""

from typing import Any, Dict
from fastapi import APIRouter, Response
from pydantic import BaseModel, Field

from src.cost.budget import BudgetManager, get_budget_manager
from src.cost.reporting import CostReporter
from src.database.repository import ManuscriptRepository

router = APIRouter(prefix="/api/cost", tags=["Cost & Budget Explorer"])


class ConfigureBudgetRequest(BaseModel):
    scope_type: str = Field(..., description="Scope: 'project_monthly', 'provider', 'agent'")
    scope_name: str = Field(..., description="Scope Name: 'sk_sutras_total', 'google', 'openai', etc.")
    monthly_limit_inr: float = Field(..., description="Monthly expenditure limit in INR")


@router.get("/summary", summary="Four-Agent Cost Telemetry")
def get_cost_summary() -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: get_cost_summary
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves granular cost and token consumption breakdown across:
        - Agent 1: Narada Specialist (Google Gemini)
        - Agent 2: Shandilya Specialist (OpenAI GPT)
        - Agent 3: Sutrakar Master Author (Anthropic Claude)
        - Agent 4: Independent Validator (OpenAI GPT)
    ----------------------------------------------------------------------------
    """
    reporter = CostReporter()
    return reporter.get_four_agent_breakdown()


@router.get("/budget", summary="Budget Status & Hard Stop Telemetry")
def get_budget_status() -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: get_budget_status
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves project monthly budget utilization in INR and hard stop alerts.
    ----------------------------------------------------------------------------
    """
    budget_mgr = get_budget_manager()
    return budget_mgr.get_budget_status(scope_type="project_monthly", scope_name="sk_sutras_total")


@router.post("/budget", summary="Configure Administrative Budget")
def set_budget(payload: ConfigureBudgetRequest) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: set_budget
    ----------------------------------------------------------------------------
    Purpose:
        Sets or updates an administrative spending cap in INR.
    ----------------------------------------------------------------------------
    """
    budget_mgr = get_budget_manager()
    budget_mgr.configure_budget(
        scope_type=payload.scope_type,
        scope_name=payload.scope_name,
        monthly_limit_inr=payload.monthly_limit_inr,
    )
    return {
        "status": "success",
        "message": f"Budget for [{payload.scope_type}:{payload.scope_name}] configured to ₹{payload.monthly_limit_inr:,.2f} INR.",
    }


@router.get("/export", summary="Export Token Usage CSV")
def export_usage_csv() -> Response:
    """
    ----------------------------------------------------------------------------
    Function: export_usage_csv
    ----------------------------------------------------------------------------
    Purpose:
        Exports complete chronological token consumption audit log as a downloadable CSV.
    ----------------------------------------------------------------------------
    """
    reporter = CostReporter()
    csv_content = reporter.export_csv()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sk_sutras_token_usage.csv"},
    )
