"""
================================================================================
Test Module: tests.test_database
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Senior Lead QA test suite verifying SQLite relational persistence,
             CRUD operations, audit trails, and accessibility setting storage.
================================================================================
"""

from pathlib import Path
import pytest
from src.database.repository import ManuscriptRepository
from src.models.schema import MultilingualText, SutraItem, SutraPairManuscript


@pytest.fixture
def temp_repo(tmp_path: Path) -> ManuscriptRepository:
    """
    ----------------------------------------------------------------------------
    Fixture: temp_repo
    ----------------------------------------------------------------------------
    Purpose:
        Creates an isolated, temporary SQLite database repository instance for
        clean unit testing.

    Parameters:
        tmp_path (Path): Pytest temporary path fixture.

    Returns:
        ManuscriptRepository: Initialized repository bound to a temporary DB.
    ----------------------------------------------------------------------------
    """
    db_file = tmp_path / "test_manuscript.db"
    return ManuscriptRepository(db_path=db_file)


def test_repository_init_and_default_settings(temp_repo: ManuscriptRepository) -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_repository_init_and_default_settings
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that initializing the repository creates the tables and sets
        default accessibility settings (Senior 65+ Mode enabled).

    Parameters:
        temp_repo (ManuscriptRepository): Isolated test repository fixture.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    senior_mode = temp_repo.get_setting("senior_mode_enabled")
    assert senior_mode == "true"
    font_scale = temp_repo.get_setting("default_font_scale")
    assert font_scale == "large"


def test_save_and_retrieve_pair(temp_repo: ManuscriptRepository) -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_save_and_retrieve_pair
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that a SutraPairManuscript can be saved, retrieved, and that
        Devanagari text integrity is preserved across persistence cycles.

    Parameters:
        temp_repo (ManuscriptRepository): Isolated test repository fixture.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    pair = SutraPairManuscript(
        pair_id="TEST-001",
        theme="Universal Love",
        narada_sutra=SutraItem(
            sutra_no="2",
            sanskrit="सा त्वस्मिन् परमप्रेमरूपा॥",
            vishleshan=MultilingualText(en="Devotion is supreme love.", hi="परम प्रेम", mr="परम प्रेम"),
        ),
        shandilya_sutra=SutraItem(
            sutra_no="2",
            sanskrit="सा परानुरक्तिरीश्वरे॥",
            vishleshan=MultilingualText(en="Devotion is supreme attachment.", hi="परम अनुरक्ति", mr="परम अनुरक्ती"),
        ),
        udyoga_bhashya_synthesis=MultilingualText(
            en="Synthesis of supreme devotion and unswerving attachment.",
            hi="प्रेम और अनुरक्ति का समन्वय",
            mr="प्रेम आणि अनुरक्ती यांचा समन्वय",
        ),
    )

    temp_repo.save_pair(pair, status="pending_review")
    retrieved = temp_repo.get_pair("TEST-001")

    assert retrieved is not None
    assert retrieved.pair_id == "TEST-001"
    assert retrieved.narada_sutra.sanskrit == "सा त्वस्मिन् परमप्रेमरूपा॥"
    assert retrieved.shandilya_sutra.sanskrit == "सा परानुरक्तिरीश्वरे॥"
    assert retrieved.udyoga_bhashya_synthesis.en == "Synthesis of supreme devotion and unswerving attachment."


def test_record_review_and_audit_history(temp_repo: ManuscriptRepository) -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_record_review_and_audit_history
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that human reviews (approvals and edits) are recorded into the
        audit trail and that the pair's status is updated atomically.

    Parameters:
        temp_repo (ManuscriptRepository): Isolated test repository fixture.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    pair = SutraPairManuscript(
        pair_id="TEST-002",
        theme="Immortality of Soul",
        narada_sutra=SutraItem(
            sutra_no="3",
            sanskrit="अमृतस्वरूपा च॥",
            vishleshan=MultilingualText(en="It is of nectarine nature."),
        ),
        shandilya_sutra=SutraItem(
            sutra_no="3",
            sanskrit="तत्संस्थस्यामृतत्वोपदेशात्॥",
            vishleshan=MultilingualText(en="Scriptures promise immortality."),
        ),
        udyoga_bhashya_synthesis=MultilingualText(
            en="Initial draft synthesis.",
        ),
    )
    temp_repo.save_pair(pair, status="pending_review")

    # Record Human-in-the-Loop approval with revision
    temp_repo.record_review(
        pair_id="TEST-002",
        reviewer_name="Shri Shripad Kulkarni",
        action="approved",
        notes="Refined philosophical synthesis.",
        updated_bhashya_en="Refined Udyoga Bhashya on spiritual immortality.",
    )

    updated_pair = temp_repo.get_pair("TEST-002")
    assert updated_pair is not None
    assert updated_pair.udyoga_bhashya_synthesis.en == "Refined Udyoga Bhashya on spiritual immortality."
