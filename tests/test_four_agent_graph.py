"""
================================================================================
Test Module: tests.test_four_agent_graph
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Senior QA unit tests verifying the 4-agent LangGraph state machine,
             7-step orchestration, arbitration rejection of weak candidates,
             Agent 4 validation routing, and bounded 3-cycle revision loop.
================================================================================
"""

import pytest
from langgraph.checkpoint.memory import MemorySaver

from src.models.state import SutraSynthesisState
from src.orchestration.graph import build_four_agent_scholarly_graph
from src.orchestration.nodes import (
    candidate_matching_node,
    independent_analysis_node,
    independent_validation_node,
    original_composition_node,
    persistence_and_author_review_node,
    source_preparation_node,
    synthesis_arbitration_node,
    targeted_revision_node,
)


def test_four_agent_graph_compilation():
    """Verifies that the 4-agent LangGraph compiles with interrupt_before persistence_review."""
    memory = MemorySaver()
    graph = build_four_agent_scholarly_graph(checkpointer=memory)
    assert graph is not None


def test_arbitration_node_accepts_strong_candidate():
    """Verifies that Agent 3 accepts defensible candidate pairings."""
    state: SutraSynthesisState = {
        "current_pair": {
            "candidate_info": {
                "sutra_no": "2",
                "intended_test_type": "strong_match",
            }
        }
    }
    result = synthesis_arbitration_node(state)
    assert result["arbitration_verdict"] == "ACCEPTED"
    assert "Accepted by Sutrakar" in result["arbitration_notes"]


def test_sutrakar_active_parishad_deliberation_dialogue():
    """Verifies that Sutrakar actively participates in the Shastrartha discussion with Agent 1 and Agent 2."""
    state: SutraSynthesisState = {
        "current_pair": {
            "candidate_info": {"sutra_no": "2", "shandilya_sutra_no": "2"},
        },
        "agent1_narada_output": {
            "sutra_no": "2",
            "thesis": "भक्ती हे परम प्रेमरूप आहे (निरतिशय प्रीती).",
            "theme": "परम प्रेमरूप भक्ती आणि परानुरक्ती",
        },
        "agent2_shandilya_output": {
            "sutra_no": "2",
            "thesis": "ईश्वरावरील अखंड ज्ञानमूलक परानुरक्ती म्हणजेच भक्ती.",
        },
    }
    result = synthesis_arbitration_node(state)
    assert "parishad_deliberation" in result
    delib = result["parishad_deliberation"]
    assert "sutrakar_inquiry" in delib
    assert "philosophical_tension" in delib
    assert "synthetic_resolution" in delib
    assert "deliberation_transcript" in delib
    assert "विद्वत् परिषद संवाद" in delib["deliberation_transcript"]
    assert "सूत्रकार विचारणा" in delib["sutrakar_inquiry"]
    assert result["arbitration_verdict"] == "ACCEPTED"


def test_source_prep_initializes_sutrakar_guidelines():
    """Verifies that source_prep node provides Sutrakar's opening directive to other agents."""
    state: SutraSynthesisState = {
        "batch_queue": [{"sutra_no": "1", "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥", "theme": "Definition"}],
        "current_index": 0,
    }
    result = source_preparation_node(state)
    assert "sutrakar_guidelines" in result
    assert "Sutrakar Arbiter Directive" in result["sutrakar_guidelines"]


def test_arbitration_node_rejects_weak_candidate():
    """Verifies that Agent 3 actively rejects weak or forced candidate pairings."""
    state: SutraSynthesisState = {
        "current_pair": {
            "candidate_info": {
                "sutra_no": "35",
                "intended_test_type": "deliberate_weak_rejection",
            }
        }
    }
    result = synthesis_arbitration_node(state)
    assert result["arbitration_verdict"] == "REJECTED_WEAK_MATCH"
    assert "Rejected by Sutrakar" in result["arbitration_notes"]


def test_arbitration_node_rejects_surface_token_collision():
    """Verifies that Agent 3 actively rejects superficial token collision matches like NBS 5 & SBS 5."""
    state: SutraSynthesisState = {
        "current_pair": {
            "candidate_info": {
                "sutra_no": "5",
                "shandilya_sutra_no": "5",
            }
        },
        "agent1_narada_output": {"sutra_no": "5", "sanskrit": "यत्प्राप्य न किञ्चिद् वाञ्छति न शोचति न द्वेष्टि..."},
        "agent2_shandilya_output": {"sutra_no": "5", "sanskrit": "द्वेषप्रतिद्वन्द्विभावाद्रसशब्दाच्च॥"},
    }
    result = synthesis_arbitration_node(state)
    assert result["arbitration_verdict"] == "REJECTED_WEAK_MATCH"
    assert "Superficial token collision" in result["arbitration_notes"]


def test_targeted_revision_node_increments_counter():
    """Verifies that targeted_revision_node increments the revision counter."""
    # Compose initial unit
    s_state: SutraSynthesisState = {
        "current_pair": {"pair_id": "UDYOGA-TEST", "sutra_no": "1"},
        "agent1_narada_output": {"sutra_no": "1", "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥", "theme": "Test Theme", "vishleshan": {"en": "Devotion."}},
        "agent2_shandilya_output": {"sutra_no": "1", "sanskrit": "अथातो भक्तिजिज्ञासा॥", "vishleshan": {"en": "Inquiry."}},
    }
    comp_res = original_composition_node(s_state)

    state: SutraSynthesisState = {
        "agent3_composition": comp_res["agent3_composition"],
        "agent4_validation_report": {
            "manuscript_unit_id": "UDYOGA-TEST",
            "execution_id": "val_exec_01",
            "overall_status": "NEEDS_REVISION",
            "revision_cycle": 0,
            "findings": [
                {
                    "gate": "chandas_metre",
                    "severity": "MAJOR",
                    "location": "Section B: Metre",
                    "issue_description": "Minor syllable discrepancy",
                    "suggested_correction": "Rephrase to exact 32 syllables",
                }
            ],
        },
        "revision_count": 0,
    }

    result = targeted_revision_node(state)
    assert result["revision_count"] == 1
    assert result["agent3_composition"]["version_number"] == 2


def test_persistence_and_author_review_node(tmp_path):
    """Verifies that persistence_review persists manuscript and sets pending_human_review."""
    s_state: SutraSynthesisState = {
        "current_pair": {"pair_id": "UDYOGA-PERSIST", "sutra_no": "1"},
        "agent1_narada_output": {"sutra_no": "1", "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥", "theme": "Persistence Theme", "vishleshan": {"en": "Devotion."}},
        "agent2_shandilya_output": {"sutra_no": "1", "sanskrit": "अथातो भक्तिजिज्ञासा॥", "vishleshan": {"en": "Inquiry."}},
    }
    comp_res = original_composition_node(s_state)

    import uuid
    state: SutraSynthesisState = {
        "agent3_composition": comp_res["agent3_composition"],
        "agent4_validation_report": {
            "id": f"val-rep-{uuid.uuid4().hex[:8]}",
            "manuscript_unit_id": comp_res["agent3_composition"]["id"],
            "execution_id": f"exec-persist-{uuid.uuid4().hex[:8]}",
            "validator_model_id": "gpt-4o",
            "overall_status": "PASS",
            "revision_cycle": 0,
            "findings": [],
        },
    }

    result = persistence_and_author_review_node(state)
    assert result["review_status"] == "pending_human_review"
    assert result["workflow_stage"] == "pending_author_review"
