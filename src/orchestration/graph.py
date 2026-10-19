"""
================================================================================
Module: src.orchestration.graph
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Compiles the LangGraph StateGraph Directed Acyclic Graph (DAG) with
             a bi-directional Human-in-the-Loop (HitL) interrupt mechanism.
================================================================================
"""

from typing import Any, Dict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.models.state import SutraSynthesisState
from src.orchestration.nodes import (
    prepare_candidate_pair_node,
    synthesize_bhashya_node,
    human_review_checkpoint_node,
    record_approval_node,
)


def _route_after_prepare(state: SutraSynthesisState) -> Literal["synthesize_bhashya", "__end__"]:
    """
    ----------------------------------------------------------------------------
    Function: _route_after_prepare
    ----------------------------------------------------------------------------
    Purpose:
        Conditional routing logic following the prepare candidate node. If the
        batch queue is exhausted or no active pair is found, routes to END;
        otherwise proceeds to synthesize_bhashya.

    Parameters:
        state (SutraSynthesisState): The current graph state.

    Returns:
        Literal["synthesize_bhashya", "__end__"]: Next node destination.
    ----------------------------------------------------------------------------
    """
    if state.get("current_pair") is None:
        return "__end__"
    return "synthesize_bhashya"


def _route_after_review(
    state: SutraSynthesisState,
) -> Literal["record_approval", "prepare_candidate", "__end__"]:
    """
    ----------------------------------------------------------------------------
    Function: _route_after_review
    ----------------------------------------------------------------------------
    Purpose:
        Evaluates the review_status after human evaluation. If approved, advances
        to record_approval. If rejected, skips persistence and prepares the next
        item. If finished, terminates cleanly.

    Parameters:
        state (SutraSynthesisState): The current graph state.

    Returns:
        Literal["record_approval", "prepare_candidate", "__end__"]: Next step.
    ----------------------------------------------------------------------------
    """
    status = state.get("review_status")
    if status == "approved":
        return "record_approval"
    elif status == "rejected":
        return "prepare_candidate"
    return "__end__"


def build_sutra_synthesis_graph(checkpointer: Any = None) -> Any:
    """
    ----------------------------------------------------------------------------
    Function: build_sutra_synthesis_graph
    ----------------------------------------------------------------------------
    Purpose:
        Constructs and compiles the complete multi-agent LangGraph workflow for
        comparative manuscript synthesis. Incorporates Human-in-the-Loop (HitL)
        interrupts before the human_review node so scholars can review, refine,
        or approve the generated Udyoga Bhashya.

    Parameters:
        checkpointer (Any): State persistence checkpointer. Defaults to an
                            in-memory MemorySaver if omitted.

    Returns:
        CompiledStateGraph: The executable LangGraph workflow engine.

    Manual Debugging Notes:
        - When invoking the graph, pass a unique `thread_id` in the config dictionary:
          `config = {"configurable": {"thread_id": "session-001"}}`
        - The graph will pause right before `human_review` when `interrupt_before`
          is specified, allowing the Streamlit UI to display the pending pair.
    ----------------------------------------------------------------------------
    """
    workflow = StateGraph(SutraSynthesisState)

    # Add core processing nodes
    workflow.add_node("prepare_candidate", prepare_candidate_pair_node)
    workflow.add_node("synthesize_bhashya", synthesize_bhashya_node)
    workflow.add_node("human_review", human_review_checkpoint_node)
    workflow.add_node("record_approval", record_approval_node)

    # Establish edge routing
    workflow.add_edge(START, "prepare_candidate")

    workflow.add_conditional_edges(
        "prepare_candidate",
        _route_after_prepare,
        {
            "synthesize_bhashya": "synthesize_bhashya",
            "__end__": END,
        },
    )

    workflow.add_edge("synthesize_bhashya", "human_review")

    workflow.add_conditional_edges(
        "human_review",
        _route_after_review,
        {
            "record_approval": "record_approval",
            "prepare_candidate": "prepare_candidate",
            "__end__": END,
        },
    )

    workflow.add_edge("record_approval", "prepare_candidate")

    # Use supplied checkpointer or default MemorySaver
    resolved_checkpointer = checkpointer if checkpointer is not None else MemorySaver()

    return workflow.compile(
        checkpointer=resolved_checkpointer,
        interrupt_before=["human_review"],
    )
