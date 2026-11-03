"""
================================================================================
Module: src.models.state
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Global TypedDict state definition for the LangGraph 4-agent multi-agent
             orchestration DAG. Manages workflow progression, independent analysis
             of Narada & Shandilya, arbitration, composition, Agent 4 validation,
             bounded 3-cycle revisions, human escalation, and persistence.
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
        Directed Acyclic Graph (DAG) state machine across all 4 AI agents.

    Fields:
        batch_queue (List[Dict[str, Any]]):
            Queue of incoming paired candidate records awaiting semantic
            comparison and synthesis.
        current_index (int):
            Index pointer to active pair.
        current_pair (Optional[Dict[str, Any]]):
            The active candidate sutra pair currently undergoing processing.
        
        # 4-Agent Modular State Attributes
        agent1_narada_output (Optional[Dict[str, Any]]):
            Structured analysis output from Agent 1 (Narada Specialist / Gemini).
        agent2_shandilya_output (Optional[Dict[str, Any]]):
            Structured analysis output from Agent 2 (Shandilya Specialist / OpenAI).
        candidate_relationship (Optional[Dict[str, Any]]):
            Comparative evaluation pairing Narada and Shandilya propositions.
        arbitration_verdict (Optional[str]):
            Agent 3 arbitration decision: 'ACCEPTED' or 'REJECTED_WEAK_MATCH'.
        arbitration_notes (Optional[str]):
            Philosophical rationale explaining why candidate was accepted or rejected.
        
        agent3_composition (Optional[Dict[str, Any]]):
            The generated manuscript unit draft containing Sections A through F.
        agent4_validation_report (Optional[Dict[str, Any]]):
            Structured validation report from Agent 4 (Validator) with check statuses
            and targeted findings.
        
        # Revision Control
        revision_count (int):
            Counter tracking AI revision iterations for the current unit (bounded at 3).
        targeted_revision_feedback (Optional[Dict[str, Any]]):
            Structured, location-specific instructions sent to Agent 3.
        escalate_to_human (bool):
            Flag set to True when 3 AI revision cycles fail or critical scholar issue arises.
        
        # Human-in-the-Loop Governance
        review_status (str):
            Status flag for author review ('in_progress', 'pending_human_review', 'approved', 'revised', 'rejected').
        human_feedback (Optional[str]):
            Editorial guidance or scholarly corrections supplied by Shri Shripad Kulkarni.
        
        draft_manuscript (List[Dict[str, Any]]):
            Cumulative sequence of approved manuscript records.
        workflow_stage (str):
            Label representing current pipeline node.
        error_log (List[str]):
            Diagnostic log of non-fatal execution errors or provider warnings.
        execution_id (str):
            Unique identifier tracing this end-to-end pipeline run.
    ----------------------------------------------------------------------------
    """
    batch_queue: List[Dict[str, Any]]
    current_index: int
    current_pair: Optional[Dict[str, Any]]
    
    agent1_narada_output: Optional[Dict[str, Any]]
    agent2_shandilya_output: Optional[Dict[str, Any]]
    candidate_relationship: Optional[Dict[str, Any]]
    arbitration_verdict: Optional[str]
    arbitration_notes: Optional[str]
    
    agent3_composition: Optional[Dict[str, Any]]
    agent4_validation_report: Optional[Dict[str, Any]]
    
    revision_count: int
    targeted_revision_feedback: Optional[Dict[str, Any]]
    escalate_to_human: bool
    
    review_status: str
    human_feedback: Optional[str]
    draft_manuscript: List[Dict[str, Any]]
    workflow_stage: str
    error_log: List[str]
    execution_id: str
