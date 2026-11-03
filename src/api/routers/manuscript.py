"""
================================================================================
Module: src.api.routers.manuscript
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: FastAPI route handlers for Author Manuscript Review, Dashboard metrics,
             canonical source lookup, and human approval governance.
================================================================================
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from src.database.repository import ManuscriptRepository

router = APIRouter(prefix="/api/manuscript", tags=["Author Manuscript Portal"])


class ReviewActionRequest(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: ReviewActionRequest
    ----------------------------------------------------------------------------
    Purpose:
        Request payload submitted by the author for editorial actions.
    ----------------------------------------------------------------------------
    """
    action: str = Field(..., description="Action: 'APPROVE', 'REJECT', 'REQUEST_REVISION', 'SCHOLAR_REFERRAL', 'HOLD'")
    reviewer_name: str = Field(default="Shri Shripad Kulkarni", description="Reviewer name")
    editorial_comments: Optional[str] = Field(default=None, description="Author's notes or corrections")


@router.get("/dashboard", summary="Author Dashboard Metrics")
def get_author_dashboard_metrics() -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: get_author_dashboard_metrics
    ----------------------------------------------------------------------------
    Purpose:
        Returns executive treatise authoring progress metrics:
        - Total canonical source sutras (84 Narada + 100 Shandilya)
        - Synthesized Udyoga Sutra units
        - Pending review units awaiting Shri Shripad Kulkarni's approval
        - Fully approved units ready for master book publication
        - Estimated research expenditure in INR
    ----------------------------------------------------------------------------
    """
    repo = ManuscriptRepository()
    all_units = repo.get_all_manuscript_units()
    approved_units = [u for u in all_units if u.get("approval_status") == "APPROVED"]
    pending_units = [u for u in all_units if u.get("approval_status") in ("PENDING_REVIEW", "pending_review")]

    usage_summary = repo.get_token_usage_summary(group_by="agent_role")
    total_cost_inr = sum(u.get("total_cost_inr", 0.0) for u in usage_summary)

    return {
        "platform_title": "SK Sutras Author Portal",
        "author": "Shri Shripad Kulkarni",
        "canonical_narada_sutras_count": 84,
        "canonical_shandilya_sutras_count": 100,
        "total_synthesized_units": len(all_units),
        "pending_author_review_count": len(pending_units),
        "approved_for_publication_count": len(approved_units),
        "total_research_investment_inr": round(total_cost_inr, 2),
    }


@router.get("/units", summary="List Manuscript Units")
def list_manuscript_units(
    approval_status: Optional[str] = Query(None, description="Filter by approval status: 'APPROVED', 'PENDING_REVIEW', etc."),
) -> List[Dict[str, Any]]:
    """
    ----------------------------------------------------------------------------
    Function: list_manuscript_units
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves active manuscript units for editorial review and book compilation.
    ----------------------------------------------------------------------------
    """
    repo = ManuscriptRepository()
    return repo.get_all_manuscript_units(approval_status=approval_status)


@router.get("/units/{unit_id}", summary="Get Detailed Manuscript Unit")
def get_manuscript_unit_detail(
    unit_id: str,
    version_number: Optional[int] = Query(None, description="Optional version number. Defaults to current active version."),
) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: get_manuscript_unit_detail
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves the complete manuscript unit (Sections A through F), its latest
        Agent 4 validation report, and prior version lineage.
    ----------------------------------------------------------------------------
    """
    repo = ManuscriptRepository()
    unit = repo.get_manuscript_unit(unit_id=unit_id, version_number=version_number)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manuscript unit with identifier '{unit_id}' not found.",
        )

    val_reports = repo.get_validation_reports_for_unit(unit["id"])
    unit["validation_reports"] = val_reports
    return unit


@router.post("/units/{unit_id}/review", summary="Record Author Review Decision")
def record_author_review_decision(
    unit_id: str,
    payload: ReviewActionRequest,
) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: record_author_review_decision
    ----------------------------------------------------------------------------
    Purpose:
        Records Shri Shripad Kulkarni's formal editorial decision:
        - 'APPROVE': Qualifies unit for inclusion in master book exports.
        - 'REJECT': Rejects unit from publication.
        - 'REQUEST_REVISION': Sends unit back for targeted refinement.
        - 'SCHOLAR_REFERRAL': Marks for Sanskrit scholar external review.
        - 'HOLD': Suspends pending additional reflection.
    ----------------------------------------------------------------------------
    """
    repo = ManuscriptRepository()
    unit = repo.get_manuscript_unit(unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Manuscript unit '{unit_id}' not found.",
        )

    action_upper = payload.action.upper()
    valid_actions = {"APPROVE", "REJECT", "REQUEST_REVISION", "SCHOLAR_REFERRAL", "HOLD"}
    if action_upper not in valid_actions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action '{payload.action}'. Must be one of {valid_actions}.",
        )

    # Status mapping
    status_map = {
        "APPROVE": "APPROVED",
        "REJECT": "REJECTED",
        "REQUEST_REVISION": "REVISION_REQUESTED",
        "SCHOLAR_REFERRAL": "SCHOLAR_REVIEW",
        "HOLD": "ON_HOLD",
    }
    target_status = status_map[action_upper]

    repo.update_manuscript_approval(
        unit_id=unit_id,
        status=target_status,
        approved_by=payload.reviewer_name,
    )

    repo.record_audit_log(
        user_email=payload.reviewer_name,
        action=f"AUTHOR_{action_upper}",
        entity_type="manuscript_unit",
        entity_id=unit_id,
        change_summary=f"Author action {action_upper} recorded with notes: {payload.editorial_comments or 'None'}",
    )

    return {
        "status": "success",
        "unit_id": unit_id,
        "approval_status": target_status,
        "reviewer": payload.reviewer_name,
        "message": f"Editorial decision '{action_upper}' successfully logged.",
    }
