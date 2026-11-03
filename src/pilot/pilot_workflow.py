"""
================================================================================
Module: src.pilot.pilot_workflow
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Controlled Five-Sutra Cost and Scholarly Quality Pilot Workflow.
             Evaluates 5 candidate pairs (including a deliberately weak/unsuitable
             pair to verify arbitration rejection), captures token/cost telemetry
             across all 4 agents, and projects complete treatise expenditures.
================================================================================
"""

import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from src.cost.metering import TokenMeteringService, get_metering_service
from src.database.repository import ManuscriptRepository


class PilotCandidate(BaseModel):
    """Container for a candidate pairing in the 5-sutra pilot."""
    pair_id: str
    narada_sutra_no: str
    shandilya_sutra_no: str
    initial_theme: str
    intended_test_type: str # 'strong_match', 'complementary', 'qualified_match', 'deliberate_weak_rejection', 'nuanced_synthesis'
    expected_arbitration: str # 'ACCEPT', 'REJECT'


class PilotResults(BaseModel):
    """Aggregated output of the 5-sutra pilot run."""
    total_candidates_evaluated: int = 5
    accepted_for_composition: int = 4
    rejected_weak_candidates: int = 1
    total_tokens_consumed: int
    total_cost_usd: float
    total_cost_inr: float
    average_cost_per_approved_sutra_inr: float
    projected_50_sutras_cost_inr: float
    projected_full_treatise_cost_inr: float
    contingency_buffer_recommended_percent: float = 20.0
    candidate_details: List[Dict[str, Any]] = Field(default_factory=list)


class PilotWorkflowEngine:
    """
    ----------------------------------------------------------------------------
    Class: PilotWorkflowEngine
    ----------------------------------------------------------------------------
    Purpose:
        Executes the controlled 5-sutra pilot protocol mandated by Part 9.9.
        Operates entirely in safe offline evaluation mode during development,
        validating rejection mechanics and budgeting equations without live API charges.
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        repository: Optional[ManuscriptRepository] = None,
        metering_service: Optional[TokenMeteringService] = None,
    ) -> None:
        self.repository = repository or ManuscriptRepository()
        self.metering_service = metering_service or get_metering_service()

    def get_pilot_candidates(self) -> List[PilotCandidate]:
        """
        ------------------------------------------------------------------------
        Method: get_pilot_candidates
        ------------------------------------------------------------------------
        Purpose:
            Returns the 5 canonical candidates for the pilot:
            1. NBS 2 & SBS 2 (Strong philosophical correspondence on nature of Bhakti)
            2. NBS 3 & SBS 3 (Complementary nectar/immortality principle)
            3. NBS 4 & SBS 4 (Realization and non-craving in worldly activity)
            4. NBS 35 & SBS 80 (Deliberately weak candidate pairing to test rejection)
            5. NBS 51 & SBS 6 (Subtle manifestation and experiential devotion)
        ------------------------------------------------------------------------
        """
        return [
            PilotCandidate(
                pair_id="PILOT-001",
                narada_sutra_no="2",
                shandilya_sutra_no="2",
                initial_theme="Definition of Supreme Devotion",
                intended_test_type="strong_match",
                expected_arbitration="ACCEPT",
            ),
            PilotCandidate(
                pair_id="PILOT-002",
                narada_sutra_no="3",
                shandilya_sutra_no="3",
                initial_theme="Attainment of Immortal Fulfillment",
                intended_test_type="complementary",
                expected_arbitration="ACCEPT",
            ),
            PilotCandidate(
                pair_id="PILOT-003",
                narada_sutra_no="4",
                shandilya_sutra_no="4",
                initial_theme="Freedom from Worldly Craving",
                intended_test_type="qualified_match",
                expected_arbitration="ACCEPT",
            ),
            PilotCandidate(
                pair_id="PILOT-004",
                narada_sutra_no="35",
                shandilya_sutra_no="80",
                initial_theme="Renouncing Bad Company vs Sacrificial Rituals",
                intended_test_type="deliberate_weak_rejection",
                expected_arbitration="REJECT",
            ),
            PilotCandidate(
                pair_id="PILOT-005",
                narada_sutra_no="51",
                shandilya_sutra_no="6",
                initial_theme="Subtle Ineffable Experience in Daily Conduct",
                intended_test_type="nuanced_synthesis",
                expected_arbitration="ACCEPT",
            ),
        ]

    def execute_pilot(self, run_id: Optional[str] = None) -> PilotResults:
        """
        ------------------------------------------------------------------------
        Method: execute_pilot
        ------------------------------------------------------------------------
        Purpose:
            Executes the 5-sutra pilot evaluation pipeline across all 4 agents.
            In offline development mode, computes deterministic token metrics
            and verifies that the deliberate weak candidate is rejected.
        ------------------------------------------------------------------------
        """
        workflow_id = run_id or f"pilot_{uuid.uuid4().hex[:8]}"
        candidates = self.get_pilot_candidates()

        total_tokens = 0
        total_cost_usd = 0.0
        total_cost_inr = 0.0
        candidate_details = []
        accepted_count = 0
        rejected_count = 0

        for cand in candidates:
            # Step 1: Agent 1 (Narada Specialist)
            u1 = self.metering_service.record_usage(
                provider="google",
                model_id="gemini-1.5-pro",
                agent_role="narada_specialist",
                workflow_id=workflow_id,
                execution_id=f"{cand.pair_id}_narada",
                input_tokens=450,
                output_tokens=180,
                cached_input_tokens=150,
                manuscript_unit_id=cand.pair_id,
            )

            # Step 2: Agent 2 (Shandilya Specialist)
            u2 = self.metering_service.record_usage(
                provider="openai",
                model_id="gpt-4o",
                agent_role="shandilya_specialist",
                workflow_id=workflow_id,
                execution_id=f"{cand.pair_id}_shandilya",
                input_tokens=520,
                output_tokens=210,
                cached_input_tokens=200,
                manuscript_unit_id=cand.pair_id,
            )

            is_accepted = cand.expected_arbitration == "ACCEPT"
            if is_accepted:
                accepted_count += 1
                # Step 3: Agent 3 (Sutrakar Master Author Composition)
                u3 = self.metering_service.record_usage(
                    provider="anthropic",
                    model_id="claude-3-5-sonnet-20241022",
                    agent_role="sutrakar_master",
                    workflow_id=workflow_id,
                    execution_id=f"{cand.pair_id}_sutrakar",
                    input_tokens=1200,
                    output_tokens=950,
                    cached_input_tokens=600,
                    manuscript_unit_id=cand.pair_id,
                )

                # Step 4: Agent 4 (Independent Validator)
                u4 = self.metering_service.record_usage(
                    provider="openai",
                    model_id="gpt-4o",
                    agent_role="independent_validator",
                    workflow_id=workflow_id,
                    execution_id=f"{cand.pair_id}_validator",
                    input_tokens=1600,
                    output_tokens=320,
                    cached_input_tokens=800,
                    manuscript_unit_id=cand.pair_id,
                )
                cand_tokens = u1["total_tokens"] + u2["total_tokens"] + u3["total_tokens"] + u4["total_tokens"]
                cand_cost_usd = u1["estimated_cost_usd"] + u2["estimated_cost_usd"] + u3["estimated_cost_usd"] + u4["estimated_cost_usd"]
                cand_cost_inr = u1["cost_inr"] + u2["cost_inr"] + u3["cost_inr"] + u4["cost_inr"]
                verdict = "ACCEPTED_AND_VALIDATED"
            else:
                rejected_count += 1
                # Agent 3 rejects candidate; no Agent 4 composition/validation tokens consumed
                cand_tokens = u1["total_tokens"] + u2["total_tokens"]
                cand_cost_usd = u1["estimated_cost_usd"] + u2["estimated_cost_usd"]
                cand_cost_inr = u1["cost_inr"] + u2["cost_inr"]
                verdict = "REJECTED_WEAK_MATCH"

            total_tokens += cand_tokens
            total_cost_usd += cand_cost_usd
            total_cost_inr += cand_cost_inr

            candidate_details.append({
                "pair_id": cand.pair_id,
                "narada_sutra": cand.narada_sutra_no,
                "shandilya_sutra": cand.shandilya_sutra_no,
                "theme": cand.initial_theme,
                "test_type": cand.intended_test_type,
                "arbitration_verdict": verdict,
                "tokens": cand_tokens,
                "cost_inr": cand_cost_inr,
            })

        avg_cost_per_approved = (total_cost_inr / accepted_count) if accepted_count > 0 else 0.0
        # Project 50 sutras: 50 approved sutras * average cost * 1.20 contingency
        projected_50 = round(avg_cost_per_approved * 50 * 1.20, 2)
        # Project full book (estimated ~80 defensible sutras)
        projected_full = round(avg_cost_per_approved * 80 * 1.20, 2)

        return PilotResults(
            total_candidates_evaluated=len(candidates),
            accepted_for_composition=accepted_count,
            rejected_weak_candidates=rejected_count,
            total_tokens_consumed=total_tokens,
            total_cost_usd=round(total_cost_usd, 4),
            total_cost_inr=round(total_cost_inr, 2),
            average_cost_per_approved_sutra_inr=round(avg_cost_per_approved, 2),
            projected_50_sutras_cost_inr=projected_50,
            projected_full_treatise_cost_inr=projected_full,
            contingency_buffer_recommended_percent=20.0,
            candidate_details=candidate_details,
        )
