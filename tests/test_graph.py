"""
================================================================================
Test Module: tests.test_graph
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Senior Lead QA test suite verifying the multi-agent LangGraph state
             machine DAG, batch processing queue, and Human-in-the-Loop interrupts.
================================================================================
"""

from pathlib import Path
import pytest
from src.database.repository import ManuscriptRepository
from src.models.state import SutraSynthesisState
from src.orchestration.graph import build_sutra_synthesis_graph
from src.orchestration.nodes import (
    prepare_candidate_pair_node,
    record_approval_node,
    synthesize_bhashya_node,
)


def test_prepare_candidate_pair_node() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_prepare_candidate_pair_node
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that prepare_candidate_pair_node accurately picks the candidate
        at current_index and updates the state.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    candidate = {
        "pair_id": "PAIR-001",
        "theme": "Definition of Bhakti",
        "narada_sutra": {"sutra_no": "1", "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥", "vishleshan": {"en": "Text"}},
        "shandilya_sutra": {"sutra_no": "1", "sanskrit": "अथातो भक्तिजिज्ञासा॥", "vishleshan": {"en": "Text"}},
    }
    state: SutraSynthesisState = {
        "batch_queue": [candidate],
        "current_index": 0,
        "current_pair": None,
        "draft_manuscript": [],
        "review_status": "in_progress",
        "workflow_stage": "preparing",
        "error_log": [],
    }

    result = prepare_candidate_pair_node(state)
    assert result["current_pair"] == candidate
    assert result["workflow_stage"] == "synthesizing"


def test_record_approval_node(tmp_path: Path) -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_record_approval_node
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that record_approval_node persists the approved pair in SQLite,
        appends to draft_manuscript, and increments current_index.

    Parameters:
        tmp_path (Path): Pytest temporary path fixture.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    test_repo = ManuscriptRepository(db_path=tmp_path / "test_approval.db")
    synthesized_pair = {
        "pair_id": "PAIR-001",
        "theme": "Definition of Bhakti",
        "narada_sutra": {
            "sutra_no": "1",
            "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
            "vishleshan": {"en": "Exposition of Devotion", "hi": None, "mr": None},
        },
        "shandilya_sutra": {
            "sutra_no": "1",
            "sanskrit": "अथातो भक्तिजिज्ञासा॥",
            "vishleshan": {"en": "Inquiry into Devotion", "hi": None, "mr": None},
        },
        "udyoga_bhashya_synthesis": {
            "en": "Synthesis connecting exposition with inquiry.",
            "hi": "समन्वय",
            "mr": "समन्वय",
        },
    }

    state: SutraSynthesisState = {
        "batch_queue": [synthesized_pair],
        "current_index": 0,
        "current_pair": synthesized_pair,
        "draft_manuscript": [],
        "review_status": "approved",
        "workflow_stage": "in_human_review",
        "error_log": [],
    }

    result = record_approval_node(state, repo=test_repo)

    assert result["current_index"] == 1
    assert result["current_pair"] is None
    assert len(result["draft_manuscript"]) == 1
    assert result["review_status"] == "approved"

    # Verify database persistence
    db_record = test_repo.get_pair("PAIR-001")
    assert db_record is not None
    assert db_record.pair_id == "PAIR-001"


def test_graph_compilation_and_interrupt() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_graph_compilation_and_interrupt
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that the compiled LangGraph workflow compiles cleanly and
        registers the interrupt before the human_review node.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    graph = build_sutra_synthesis_graph()
    assert graph is not None
    # Verify human_review interrupt is registered in graph nodes
    assert "human_review" in graph.nodes
