"""
================================================================================
Test Module: tests.test_accessibility
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Senior Lead QA test suite verifying the Accessibility Engine,
             Senior Citizen (65+ Mode) CSS rules, minimum touch target heights,
             and high-contrast Devanagari legibility.
================================================================================
"""

from src.ui.theme import get_accessibility_css


def test_senior_citizen_mode_enforces_large_touch_targets() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_senior_citizen_mode_enforces_large_touch_targets
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that when Senior Citizen (65+ Mode) is active, generated CSS
        enforces button heights >= 48px to eliminate misclicks for elderly reviewers.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    css = get_accessibility_css(senior_mode=True, font_scale="large", high_contrast=True)

    # Verify minimum height rule >= 48px is injected (large is 52px)
    assert "min-height: 52px" in css
    # Verify Devanagari prominent styling is present
    assert ".devanagari-verse" in css
    # Verify touch target styling on mobile
    assert "min-height: 56px !important;" in css


def test_senior_citizen_mode_extra_large_scale() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_senior_citizen_mode_extra_large_scale
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that extra_large typography scaling elevates base fonts to 22px
        and button heights to 60px.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    css = get_accessibility_css(senior_mode=True, font_scale="extra_large", high_contrast=True)

    assert "font-size: 22px;" in css
    assert "min-height: 60px" in css


def test_standard_mode_metrics() -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_standard_mode_metrics
    ----------------------------------------------------------------------------
    Purpose:
        Verifies standard mode metrics when senior mode is disabled.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    css = get_accessibility_css(senior_mode=False, font_scale="standard", high_contrast=False)

    assert "font-size: 16px;" in css
    assert "min-height: 44px" in css
