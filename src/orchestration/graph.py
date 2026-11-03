"""
================================================================================
Module: src.orchestration.graph
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Compiles both the legacy 3-agent graph and the full 4-agent
             scholarly LangGraph architecture connecting Narada, Shandilya,
             Sutrakar Master Author, and Independent Validator with bounded
             3-cycle revision loop and Human-in-the-Loop interruption checkpoint.
================================================================================
"""

from typing import Any, Literal
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src.models.state import SutraSynthesisState
from src.orchestration.nodes import (
    candidate_matching_node,
    human_review_checkpoint_node,
    independent_analysis_node,
    independent_validation_node,
    narada_agent_node,
    original_composition_node,
    persistence_and_author_review_node,
    record_approval_node,
    shandilya_agent_node,
    source_preparation_node,
    synthesis_arbitration_node,
    sutrakar_agent_node,
    targeted_revision_node,
)


# ==============================================================================
# Legacy 3-Agent Routing (Maintained for Backward Compatibility)
# ==============================================================================

def _route_after_review(
    state: SutraSynthesisState,
) -> Literal["record_approval", "__end__"]:
    """Routes after the human review checkpoint in the 3-agent graph."""
    status = state.get("review_status")
    if status == "approved":
        return "record_approval"
    return "__end__"


def build_sutra_synthesis_graph(checkpointer: Any = None) -> Any:
    """
    ----------------------------------------------------------------------------
    Function: build_sutra_synthesis_graph
    ----------------------------------------------------------------------------
    Purpose:
        Constructs and compiles the 3-agent backward-compatible LangGraph workflow.
    ----------------------------------------------------------------------------
    """
    workflow = StateGraph(SutraSynthesisState)

    workflow.add_node("narada_agent", narada_agent_node)
    workflow.add_node("shandilya_agent", shandilya_agent_node)
    workflow.add_node("sutrakar_agent", sutrakar_agent_node)
    workflow.add_node("human_review", human_review_checkpoint_node)
    workflow.add_node("record_approval", record_approval_node)

    workflow.add_edge(START, "narada_agent")
    workflow.add_edge("narada_agent", "shandilya_agent")
    workflow.add_edge("shandilya_agent", "sutrakar_agent")
    workflow.add_edge("sutrakar_agent", "human_review")

    workflow.add_conditional_edges(
        "human_review",
        _route_after_review,
        {
            "record_approval": "record_approval",
            "__end__": END,
        },
    )

    workflow.add_edge("record_approval", END)

    resolved_checkpointer = checkpointer if checkpointer is not None else MemorySaver()

    return workflow.compile(
        checkpointer=resolved_checkpointer,
        interrupt_before=["human_review"],
    )


# ==============================================================================
# Comprehensive 4-Agent Routing & Graph Compilation (Parts 4, 5 & 14)
# ==============================================================================

def _route_arbitration_verdict(
    state: SutraSynthesisState,
) -> Literal["composition", "persistence_review"]:
    """
    Routes after Agent 3 arbitration:
    - If candidate is accepted -> proceed to composition.
    - If weak/forced candidate is rejected -> bypass composition and persist rejection.
    """
    verdict = state.get("arbitration_verdict")
    if verdict == "REJECTED_WEAK_MATCH":
        return "persistence_review"
    return "composition"


def _route_validation_result(
    state: SutraSynthesisState,
) -> Literal["persistence_review", "targeted_revision"]:
    """
    Routes after Agent 4 validation:
    - If PASS -> proceed to persistence & author review.
    - If NEEDS_REVISION and revision_count < 3 -> route back to targeted revision.
    - If FAIL or revision_count >= 3 -> escalate to human author review.
    """
    report = state.get("agent4_validation_report", {})
    status = report.get("overall_status", "PASS")
    rev_count = state.get("revision_count", 0)

    if status == "NEEDS_REVISION" and rev_count < 3:
        return "targeted_revision"

    return "persistence_review"


def build_four_agent_scholarly_graph(checkpointer: Any = None) -> Any:
    """
    ----------------------------------------------------------------------------
    Function: build_four_agent_scholarly_graph
    ----------------------------------------------------------------------------
    Purpose:
        Constructs and compiles the complete 7-step 4-agent LangGraph topology:
        1. Source Preparation (verify authenticated provenance)
        2. Independent Analysis (Agent 1 Narada & Agent 2 Shandilya)
        3. Candidate Identification (retrieve & present propositions)
        4. Synthesis & Arbitration (Agent 3 evaluates & can reject weak candidates)
        5. Original Composition (Agent 3 generates Sections A through F)
        6. Independent Validation (Agent 4 validates across 7 scholarly gates)
           - Targeted Revision Loop (bounded at maximum 3 AI revision cycles)
        7. Persistence and Author Review (HitL checkpoint for Shri Shripad Kulkarni)

    Parameters:
        checkpointer (Any): Optional LangGraph checkpointer for resumable state.

    Returns:
        CompiledStateGraph: Executable 4-agent state machine.
    ----------------------------------------------------------------------------
    """
    workflow = StateGraph(SutraSynthesisState)

    # 1. Register 4-Agent Nodes
    workflow.add_node("source_prep", source_preparation_node)
    workflow.add_node("independent_analysis", independent_analysis_node)
    workflow.add_node("candidate_matching", candidate_matching_node)
    workflow.add_node("arbitration", synthesis_arbitration_node)
    workflow.add_node("composition", original_composition_node)
    workflow.add_node("validation", independent_validation_node)
    workflow.add_node("targeted_revision", targeted_revision_node)
    workflow.add_node("persistence_review", persistence_and_author_review_node)

    # 2. Linear Pipeline to Arbitration
    workflow.add_edge(START, "source_prep")
    workflow.add_edge("source_prep", "independent_analysis")
    workflow.add_edge("independent_analysis", "candidate_matching")
    workflow.add_edge("candidate_matching", "arbitration")

    # 3. Conditional Arbitration Branch (Accept vs Reject Weak Candidate)
    workflow.add_conditional_edges(
        "arbitration",
        _route_arbitration_verdict,
        {
            "composition": "composition",
            "persistence_review": "persistence_review",
        },
    )

    # 4. Composition to Independent Validation
    workflow.add_edge("composition", "validation")

    # 5. Conditional Validation Branch (Pass vs Targeted Revision vs Human Escalation)
    workflow.add_conditional_edges(
        "validation",
        _route_validation_result,
        {
            "targeted_revision": "targeted_revision",
            "persistence_review": "persistence_review",
        },
    )

    # 6. Revision loop returns to validation for re-evaluation
    workflow.add_edge("targeted_revision", "validation")

    # 7. Final edge to completion
    workflow.add_edge("persistence_review", END)

    resolved_checkpointer = checkpointer if checkpointer is not None else MemorySaver()

    return workflow.compile(
        checkpointer=resolved_checkpointer,
        interrupt_before=["persistence_review"],
    )
