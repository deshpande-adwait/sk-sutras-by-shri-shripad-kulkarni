"""
================================================================================
Module: src.orchestration.graph
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Compiles the 3-agent LangGraph workflow engine:
             NaradaAgent -> ShandilyaAgent -> SutrakarAgent -> Human Review Checkpoint -> Approval & PDF Compilation
================================================================================
"""

from typing import Any, Literal
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from src.models.state import SutraSynthesisState
from src.orchestration.nodes import (
    human_review_checkpoint_node,
    narada_agent_node,
    record_approval_node,
    shandilya_agent_node,
    sutrakar_agent_node,
)


def _route_after_review(
    state: SutraSynthesisState,
) -> Literal["record_approval", "__end__"]:
    """
    ----------------------------------------------------------------------------
    Function: _route_after_review
    ----------------------------------------------------------------------------
    Purpose:
        Routes after the human review checkpoint. If approved, advances to
        record_approval; otherwise terminates or awaits next command.

    Parameters:
        state (SutraSynthesisState): The active state.

    Returns:
        Literal["record_approval", "__end__"]: Destination node.
    ----------------------------------------------------------------------------
    """
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
        Constructs and compiles the multi-agent LangGraph orchestration graph
        connecting:
        1. NaradaAgent (presents Narada sutra & devotional thesis)
        2. ShandilyaAgent (matches Shandilya sutra via ChromaDB & provides epistemological thesis)
        3. SutrakarAgent (synthesizes both into Udyoga Bhashya & validates schema)
        4. Human Review Checkpoint (pauses before this node via HitL interrupt)
        5. Record Approval & Publication PDF compilation

    Parameters:
        checkpointer (Any): Optional state persistence checkpointer.

    Returns:
        CompiledStateGraph: Executable multi-agent graph.
    ----------------------------------------------------------------------------
    """
    workflow = StateGraph(SutraSynthesisState)

    # 1. Register Multi-Agent Nodes
    workflow.add_node("narada_agent", narada_agent_node)
    workflow.add_node("shandilya_agent", shandilya_agent_node)
    workflow.add_node("sutrakar_agent", sutrakar_agent_node)
    workflow.add_node("human_review", human_review_checkpoint_node)
    workflow.add_node("record_approval", record_approval_node)

    # 2. Wire Multi-Agent Communication Graph
    workflow.add_edge(START, "narada_agent")
    workflow.add_edge("narada_agent", "shandilya_agent")
    workflow.add_edge("shandilya_agent", "sutrakar_agent")
    workflow.add_edge("sutrakar_agent", "human_review")

    # 3. Conditional Human Review Resolution
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
