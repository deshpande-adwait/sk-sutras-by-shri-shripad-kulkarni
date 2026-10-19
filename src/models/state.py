"""
================================================================================
Module: src.models.state
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Global TypedDict state definition for the LangGraph multi-agent
             orchestration DAG. Manages workflow progression, batch queuing,
             human-in-the-loop review interruptions, and cumulative draft
             manuscripts.
================================================================================
"""

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class SutraSynthesisState(TypedDict, total=False):
    """
    ----------------------------------------------------------------------------
    TypedDict: SutraSynthesisState
    ----------------------------------------------------------------------------
    Purpose:
        Defines the global state shared across all nodes within the LangGraph
        Directed Acyclic Graph (DAG) state machine. Maintains the execution
        context, batch processing counters, human-in-the-loop (HitL) interrupt
        checkpoints, and cumulative draft manuscript records.

    Fields:
        batch_queue (List[Dict[str, Any]]):
            Queue of incoming paired candidate records awaiting semantic
            comparison and synthesis.
        current_index (int):
            Index pointer to the active sutra pair currently undergoing processing.
        current_pair (Optional[Dict[str, Any]]):
            The active candidate sutra pair currently undergoing extraction,
            comparison, or review.
        review_status (str):
            Status flag for human-in-the-loop governance:
            - 'in_progress': Node execution underway.
            - 'pending_human_review': LangGraph execution interrupted for HitL inspection.
            - 'approved': Approved by human reviewer (e.g. Shri Shripad Kulkarni).
            - 'revised': Updated with human editorial feedback.
            - 'rejected': Candidate pairing rejected.
        human_feedback (Optional[str]):
            Editorial comments, philosophical notes, or corrections supplied
            by the reviewer during HitL interruption.
        draft_manuscript (List[Dict[str, Any]]):
            Cumulative sequence of approved manuscript records conforming
            strictly to the SutraPairManuscript extensible schema.
        workflow_stage (str):
            Label representing current pipeline node (e.g., 'ingestion',
            'matching', 'synthesis', 'review', 'typesetting', 'complete').
        error_log (List[str]):
            Diagnostic log of non-fatal execution errors or provider warnings.
    ----------------------------------------------------------------------------
    """
    batch_queue: List[Dict[str, Any]]
    current_index: int
    current_pair: Optional[Dict[str, Any]]
    review_status: str
    human_feedback: Optional[str]
    draft_manuscript: List[Dict[str, Any]]
    workflow_stage: str
    error_log: List[str]
