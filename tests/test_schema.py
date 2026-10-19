"""
================================================================================
Test Module: tests.test_schema
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Senior Lead QA test suite for validating Pydantic schemas against
             the extensible JSON specification required for the Udyoga Sutra.
================================================================================
"""

import pytest
from pydantic import ValidationError
from src.models.schema import MultilingualText, SutraItem, SutraPairManuscript


def test_valid_sutra_pair_manuscript() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_valid_sutra_pair_manuscript
    ----------------------------------------------------------------------------
    Purpose:
        Validates that a correctly populated dictionary matching the specification
        schema instantiates a SutraPairManuscript model without validation errors.

    Parameters:
        None

    Returns:
        None

    Errors:
        AssertionError: If fields fail to match expected types or values.

    Manual Debugging Notes:
        - Run via: `pytest tests/test_schema.py -k test_valid_sutra_pair_manuscript -v`
    ----------------------------------------------------------------------------
    """
    data = {
        "pair_id": "PAIR-001",
        "theme": "Definition of Bhakti",
        "narada_sutra": {
            "sutra_no": "1",
            "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
            "vishleshan": {
                "en": "Now, therefore, we shall expound Devotion.",
                "hi": None,
                "mr": None,
            },
        },
        "shandilya_sutra": {
            "sutra_no": "1",
            "sanskrit": "अथातो भक्तिजिज्ञासा॥",
            "vishleshan": {
                "en": "Now, therefore, the inquiry into Devotion.",
                "hi": None,
                "mr": None,
            },
        },
        "udyoga_bhashya_synthesis": {
            "en": "Unified synthesis connecting exposition with inquiry.",
            "hi": None,
            "mr": None,
        },
    }

    model = SutraPairManuscript(**data)
    assert model.pair_id == "PAIR-001"
    assert model.narada_sutra.sutra_no == "1"
    assert model.narada_sutra.sanskrit == "अथातो भक्तिं व्याख्यास्यामः॥"
    assert model.narada_sutra.vishleshan.en == "Now, therefore, we shall expound Devotion."
    assert model.narada_sutra.vishleshan.hi is None
    assert model.shandilya_sutra.sutra_no == "1"
    assert model.udyoga_bhashya_synthesis.en == "Unified synthesis connecting exposition with inquiry."


def test_multilingual_expansion() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_multilingual_expansion
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that multilingual fields correctly support Hindi and Marathi
        content alongside English.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    multi = MultilingualText(
        en="Devotion to God",
        hi="ईश्वर के प्रति भक्ति",
        mr="ईश्वराविषयी भक्ती",
    )
    assert multi.en == "Devotion to God"
    assert multi.hi == "ईश्वर के प्रति भक्ति"
    assert multi.mr == "ईश्वराविषयी भक्ती"


def test_missing_mandatory_field_raises_error() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_missing_mandatory_field_raises_error
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that omitting mandatory fields such as pair_id or sanskrit verse
        triggers a pydantic.ValidationError, preventing corrupted data ingestion.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    invalid_data = {
        "theme": "Incomplete Pair Without pair_id",
        "narada_sutra": {
            "sutra_no": "1",
            # missing sanskrit verse
            "vishleshan": {"en": "Text"},
        },
    }
    with pytest.raises(ValidationError):
        SutraPairManuscript(**invalid_data)  # type: ignore
