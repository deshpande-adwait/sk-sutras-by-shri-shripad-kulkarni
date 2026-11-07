"""
================================================================================
Test Module: tests.test_council_logger
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Unit tests verifying the CouncilLogger audit and live transcript
             mechanisms for the four-agent Vidvat Parishad dialogue.
================================================================================
"""

import json
from pathlib import Path
from src.orchestration.council_logger import CouncilLogger


def test_council_logger_initialization(tmp_path: Path):
    """Verifies that CouncilLogger initializes directories and files correctly."""
    logger = CouncilLogger(log_dir=tmp_path, session_name="test_session")
    assert tmp_path.exists()
    assert logger.log_file.exists()


def test_council_logger_event_and_dialogue(tmp_path: Path):
    """Verifies that CouncilLogger logs events and dialogue transcripts properly."""
    logger = CouncilLogger(log_dir=tmp_path, session_name="test_dialogue")

    agent1_data = {
        "sutra_no": "1",
        "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
        "thesis": "भक्ती हे मानवी जीवनातील सर्वोच्च अमृत आणि पराभक्तीचे मूळ आहे.",
    }
    agent2_data = {
        "sutra_no": "1",
        "sanskrit": "अथातो भक्तिजिज्ञासा॥",
        "thesis": "भक्ती हे केवळ भावनिक कल्लोळ नसून तात्त्विक संशोधन आहे.",
    }
    arbitration_data = {
        "sutrakar_inquiry": "How do we reconcile emotional surrender with analytical inquiry?",
        "philosophical_tension": "Affective devotion vs cognitive discernment.",
        "synthetic_resolution": "Synthesizing into ethical enterprise (Udyoga).",
        "arbitration_verdict": "ACCEPTED",
        "arbitration_notes": "Accepted authentic doctrinal alignment.",
    }
    agent4_data = {
        "overall_status": "PASS",
        "syllables_count": 32,
        "grammar_status": "PASS",
        "philosophical_status": "PASS",
        "location_specific_findings": "All 7 Gates Passed",
    }

    transcript = logger.log_dialogue(
        sutra_id="UDYOGA-TEST-001",
        theme="Inception and Diligence",
        agent1_narada=agent1_data,
        agent2_shandilya=agent2_data,
        sutrakar_arbitration=arbitration_data,
        agent4_validation=agent4_data,
        print_to_console=False,
    )

    assert "VIDVAT PARISHAD DIALOGUE TRANSCRIPT" in transcript
    assert "Agent 1 — Narada" in transcript
    assert "Agent 2 — Shandilya" in transcript
    assert "Agent 3 — Sutrakara" in transcript
    assert "Agent 4 — Independent Sanskrit & Metre Review" in transcript
    assert "UDYOGA-TEST-001" in transcript

    # Verify JSONL content
    assert logger.jsonl_file.exists()
    with open(logger.jsonl_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) >= 1
        entry = json.loads(lines[-1])
        assert entry["metadata"]["sutra_id"] == "UDYOGA-TEST-001"
        assert entry["metadata"]["verdict"] == "ACCEPTED"
