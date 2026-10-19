"""
================================================================================
Test Module: tests.test_agents
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Senior Lead QA test suite verifying the multi-agent communication
             pipeline: NaradaAgent -> ShandilyaAgent -> SutrakarAgent.
================================================================================
"""

from pathlib import Path
import pytest
from src.agents.narada_agent import NaradaAgent
from src.agents.shandilya_agent import ShandilyaAgent
from src.agents.sutrakar_agent import SutrakarAgent
from src.database.repository import ManuscriptRepository
from src.models.schema import SutraPairManuscript


def test_narada_agent_expound_sutra() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_narada_agent_expound_sutra
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that NaradaAgent loads its knowledge base, expounds a verse,
        and produces the inter-agent message for ShandilyaAgent.
    ----------------------------------------------------------------------------
    """
    agent = NaradaAgent()
    sutra_raw = agent.get_sutra_by_number("1")
    assert sutra_raw is not None
    assert sutra_raw["sutra_no"] == "1"

    result = agent.expound_sutra(sutra_raw)
    assert result["sutra_item"].sutra_no == "1"
    assert "अथातो भक्तिं व्याख्यास्यामः॥" in result["sutra_item"].sanskrit
    assert len(result["agent_message_to_shandilya"]) > 0


def test_three_agent_communication_flow(tmp_path: Path) -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_three_agent_communication_flow
    ----------------------------------------------------------------------------
    Purpose:
        Verifies the full dialogic exchange:
        1. NaradaAgent presents Sutra #1
        2. ShandilyaAgent receives, queries vector store, and matches Sutra #1
        3. SutrakarAgent compiles synthesis into Udyoga Bhashya and saves to SQLite
    ----------------------------------------------------------------------------
    """
    # 1. Narada Agent
    narada_agent = NaradaAgent()
    narada_raw = narada_agent.get_sutra_by_number("1")
    narada_exp = narada_agent.expound_sutra(narada_raw)

    # 2. Shandilya Agent
    shandilya_agent = ShandilyaAgent()
    shandilya_resp = shandilya_agent.match_and_respond(
        narada_sutra=narada_exp["sutra_item"],
        theme=narada_exp["theme"],
        narada_message=narada_exp["agent_message_to_shandilya"],
    )
    assert shandilya_resp["shandilya_sutra"].sutra_no == "1"

    # 3. Sutrakar Agent
    test_repo = ManuscriptRepository(db_path=tmp_path / "test_agents.db")
    sutrakar_agent = SutrakarAgent(repository=test_repo)
    compiled: SutraPairManuscript = sutrakar_agent.synthesize_and_compile(
        pair_id="PAIR-TEST-001",
        theme=narada_exp["theme"],
        narada_sutra=narada_exp["sutra_item"],
        shandilya_sutra=shandilya_resp["shandilya_sutra"],
        narada_statement=narada_exp["agent_message_to_shandilya"],
        shandilya_statement=shandilya_resp["agent_message_to_sutrakar"],
    )

    assert compiled.pair_id == "PAIR-TEST-001"
    assert len(compiled.udyoga_bhashya_synthesis.en) > 0

    # Verify database persistence
    saved_db = test_repo.get_pair("PAIR-TEST-001")
    assert saved_db is not None
    assert saved_db.pair_id == "PAIR-TEST-001"
