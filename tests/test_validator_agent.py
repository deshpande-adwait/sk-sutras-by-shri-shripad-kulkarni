"""
================================================================================
Test Module: tests.test_validator_agent
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: QA unit tests verifying Agent 4 (Independent Validator), Anushtubh
             Chandas syllable metre analysis, multi-gate validation, and 3-cycle
             revision escalation.
================================================================================
"""

from pathlib import Path
from src.agents.sutrakar_agent import SutrakarAgent
from src.agents.validator_agent import SanskritMetreValidator, ValidatorAgent
from src.database.repository import ManuscriptRepository
from src.models.schema import MultilingualText, SutraItem


def test_anushtubh_metre_validator_success():
    """Verifies that an authentic 32-syllable Anushtubh verse passes metrical check."""
    verse = "उद्यमे संश्रिता भक्तिः कर्मयोगेन दीव्यते ।\nलोकसंग्रहमेवेह साधयेन्नित्यमुत्तमम् ॥"
    result = SanskritMetreValidator.validate_anushtubh(verse)
    assert result["is_anushtubh"] is True
    assert 30 <= result["total_syllables"] <= 34


def test_anushtubh_metre_validator_rejection_on_mismatched_length():
    """Verifies that a truncated verse (e.g. 15 syllables) fails the Anushtubh metre check."""
    bad_verse = "उद्यमे संश्रिता भक्तिः ॥"
    result = SanskritMetreValidator.validate_anushtubh(bad_verse)
    assert result["status"] == "FAIL"
    assert result["is_anushtubh"] is False
    assert "Syllable count deviation" in result["deviation_notes"]


def test_validator_agent_complete_pass(tmp_path: Path):
    """Verifies that a properly formatted manuscript unit passes all 7 validation gates."""
    repo = ManuscriptRepository(db_path=tmp_path / "test_val1.db")
    sutrakar = SutrakarAgent(repository=repo)
    narada_item = SutraItem(
        sutra_no="2",
        sanskrit="सा त्वस्मिन् परमप्रेमरूपा॥",
        vishleshan=MultilingualText(en="Devotion is supreme love.", hi="परम प्रेम", mr="परम प्रेम"),
    )
    shandilya_item = SutraItem(
        sutra_no="2",
        sanskrit="सा परानुरक्तिरीश्वरे॥",
        vishleshan=MultilingualText(en="Devotion is supreme attachment to the Divine.", hi="परम अनुरक्ति", mr="परम अनुरक्ती"),
    )

    unit = sutrakar.compose_complete_manuscript_unit(
        unit_id="UDYOGA-001",
        chapter_no=1,
        sutra_no="1",
        theme="Ethical Enterprise and Supreme Devotion",
        narada_item=narada_item,
        shandilya_item=shandilya_item,
    )

    validator = ValidatorAgent()
    report = validator.validate_manuscript_unit(unit, revision_cycle=0)

    assert report.source_authenticity_check == "PASS"
    assert report.critical_issues_count == 0
    assert report.overall_status in ("PASS", "NEEDS_REVISION")


def test_validator_escalates_to_human_after_three_revisions(tmp_path: Path):
    """Verifies Part 4.4 Rule 6: After three unsuccessful revisions, escalate to human review."""
    repo = ManuscriptRepository(db_path=tmp_path / "test_val2.db")
    sutrakar = SutrakarAgent(repository=repo)
    narada_item = SutraItem(
        sutra_no="2",
        sanskrit="सा त्वस्मिन् परमप्रेमरूपा॥",
        vishleshan=MultilingualText(en="Devotion is supreme love."),
    )
    shandilya_item = SutraItem(
        sutra_no="2",
        sanskrit="सा परानुरक्तिरीश्वरे॥",
        vishleshan=MultilingualText(en="Devotion is supreme attachment."),
    )

    unit = sutrakar.compose_complete_manuscript_unit(
        unit_id="UDYOGA-002",
        chapter_no=1,
        sutra_no="2",
        theme="Worldly Activity",
        narada_item=narada_item,
        shandilya_item=shandilya_item,
    )
    # Deliberately inject a major issue (e.g. truncate verse to fail metre)
    unit.original_sanskrit_verse = "उद्यमे संश्रिता ॥"

    validator = ValidatorAgent()
    # At revision_cycle = 3, unresolved major issue MUST trigger HUMAN_REVIEW_REQUIRED
    report = validator.validate_manuscript_unit(unit, revision_cycle=3)

    assert report.overall_status == "HUMAN_REVIEW_REQUIRED"
    assert report.major_issues_count > 0


def test_sutrakar_targeted_revision_increments_version(tmp_path: Path):
    """Verifies that applying targeted revision preserves identity while incrementing version number."""
    repo = ManuscriptRepository(db_path=tmp_path / "test_val3.db")
    sutrakar = SutrakarAgent(repository=repo)
    narada_item = SutraItem(
        sutra_no="1",
        sanskrit="अथातो भक्तिं व्याख्यास्यामः॥",
        vishleshan=MultilingualText(en="Now, therefore, we shall expound Devotion."),
    )
    shandilya_item = SutraItem(
        sutra_no="1",
        sanskrit="अथातो भक्तिजिज्ञासा॥",
        vishleshan=MultilingualText(en="Now, therefore, the inquiry into Devotion."),
    )

    unit_v1 = sutrakar.compose_complete_manuscript_unit(
        unit_id="UDYOGA-003",
        chapter_no=1,
        sutra_no="1",
        theme="Inquiry into Ethical Devotion",
        narada_item=narada_item,
        shandilya_item=shandilya_item,
    )
    assert unit_v1.version_number == 1

    validator = ValidatorAgent()
    report = validator.validate_manuscript_unit(unit_v1)

    unit_v2 = sutrakar.apply_targeted_revision(unit_v1, report)
    assert unit_v2.version_number == 2
    assert unit_v2.parent_version_id == unit_v1.id
    assert unit_v2.unit_id == unit_v1.unit_id
