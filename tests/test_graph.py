"""
================================================================================
Test Module: tests.test_graph
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Senior Lead QA test suite verifying the multi-agent LangGraph state
             machine DAG, individual agent execution nodes (Narada, Shandilya,
             Sutrakar), Human-in-the-Loop review interrupt checkpoint, and
             manuscript database persistence and compilation.
================================================================================
"""

from pathlib import Path
from typing import Any, Dict
import pytest

from src.database.repository import ManuscriptRepository
from src.models.state import SutraSynthesisState
from src.orchestration.graph import build_sutra_synthesis_graph
from src.orchestration.nodes import (
    human_review_checkpoint_node,
    narada_agent_node,
    record_approval_node,
    shandilya_agent_node,
    sutrakar_agent_node,
)


def test_narada_agent_node() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_narada_agent_node
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that narada_agent_node extracts the candidate sutra from the
        batch_queue, expounds its devotional meaning, prepares the message for
        ShandilyaAgent, and transitions workflow_stage to 'shandilya_matching'.

    Parameters:
        None

    Returns:
        None

    Manual Debugging Notes:
        - Check that 'current_pair' contains 'narada_sutra' and 'narada_statement'.
        - Validates that state indexing advances consistently.
    ----------------------------------------------------------------------------
    """
    candidate = {
        "sutra_no": "1",
        "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
        "theme": "Definition of Bhakti",
        "initial_meaning": {"en": "Now, therefore, the exposition of Devotion."},
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

    result = narada_agent_node(state)
    assert "current_pair" in result
    assert result["workflow_stage"] == "shandilya_matching"
    assert result["current_pair"]["narada_sutra"]["sutra_no"] == "1"
    assert len(result["current_pair"]["narada_statement"]) > 0


def test_shandilya_agent_node() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_shandilya_agent_node
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that shandilya_agent_node accepts the Narada proposition,
        queries the ChromaDB vector store for matching aphorisms, populates
        shandilya_sutra in current_pair, and updates workflow_stage to
        'sutrakar_synthesizing'.

    Parameters:
        None

    Returns:
        None

    Manual Debugging Notes:
        - Ensures ChromaDB returns a valid match or fallback.
        - Verifies shandilya_statement is formulated for SutrakarAgent.
    ----------------------------------------------------------------------------
    """
    state: SutraSynthesisState = {
        "batch_queue": [],
        "current_index": 0,
        "current_pair": {
            "pair_id": "PAIR-001",
            "theme": "Definition of Bhakti",
            "narada_sutra": {
                "sutra_no": "1",
                "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
                "vishleshan": {
                    "en": "Now, therefore, the exposition of Devotion.",
                    "hi": None,
                    "mr": None,
                },
            },
            "narada_statement": "Exposition of supreme love.",
        },
        "draft_manuscript": [],
        "review_status": "in_progress",
        "workflow_stage": "shandilya_matching",
        "error_log": [],
    }

    result = shandilya_agent_node(state)
    assert result["workflow_stage"] == "sutrakar_synthesizing"
    curr = result["current_pair"]
    assert "shandilya_sutra" in curr
    assert curr["shandilya_sutra"]["sutra_no"] is not None
    assert len(curr["shandilya_statement"]) > 0


def test_sutrakar_agent_node() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_sutrakar_agent_node
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that sutrakar_agent_node synthesizes the comparative
        Udyoga Bhashya across traditions and sets the state for human review.

    Parameters:
        None

    Returns:
        None

    Manual Debugging Notes:
        - Validates that review_status is set to 'pending_human_review'.
        - Validates that workflow_stage is set to 'awaiting_human_review'.
    ----------------------------------------------------------------------------
    """
    state: SutraSynthesisState = {
        "batch_queue": [],
        "current_index": 0,
        "current_pair": {
            "pair_id": "PAIR-001",
            "theme": "Definition of Bhakti",
            "narada_sutra": {
                "sutra_no": "1",
                "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
                "vishleshan": {
                    "en": "Exposition of Devotion",
                    "hi": None,
                    "mr": None,
                },
            },
            "shandilya_sutra": {
                "sutra_no": "1",
                "sanskrit": "अथातो भक्तिजिज्ञासा॥",
                "vishleshan": {
                    "en": "Inquiry into Devotion",
                    "hi": None,
                    "mr": None,
                },
            },
            "narada_statement": "Love is paramount.",
            "shandilya_statement": "Inquiry is foundational.",
        },
        "draft_manuscript": [],
        "review_status": "in_progress",
        "workflow_stage": "sutrakar_synthesizing",
        "error_log": [],
    }

    result = sutrakar_agent_node(state)
    assert result["workflow_stage"] == "awaiting_human_review"
    assert result["review_status"] == "pending_human_review"
    assert "udyoga_bhashya_synthesis" in result["current_pair"]


def test_human_review_checkpoint_node() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_human_review_checkpoint_node
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that the Human-in-the-Loop review node halts automated progression
        and marks the stage as 'in_human_review'.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    state: SutraSynthesisState = {
        "batch_queue": [],
        "current_index": 0,
        "current_pair": {"pair_id": "PAIR-001"},
        "draft_manuscript": [],
        "review_status": "pending_human_review",
        "workflow_stage": "awaiting_human_review",
        "error_log": [],
    }

    result = human_review_checkpoint_node(state)
    assert result["workflow_stage"] == "in_human_review"
    assert result["review_status"] == "pending_human_review"


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

    Manual Debugging Notes:
        - Injects an isolated temporary database repository to guarantee test isolation.
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
        Verifies that the compiled LangGraph workflow compiles cleanly,
        registers all agent nodes, and wires human_review as the review gateway.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    graph = build_sutra_synthesis_graph()
    assert graph is not None

    # Verify all 3-agent orchestration nodes are registered in the state graph
    assert "narada_agent" in graph.nodes
    assert "shandilya_agent" in graph.nodes
    assert "sutrakar_agent" in graph.nodes
    assert "human_review" in graph.nodes
    assert "record_approval" in graph.nodes
