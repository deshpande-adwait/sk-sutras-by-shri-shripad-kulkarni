"""
================================================================================
Module: src.ui.components
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Reusable visual UI components for the Streamlit Review Portal.
             Enforces zero technical jargon, clean business terminology, and
             mandatory Hiranyam AI branding with active hyperlinks.
================================================================================
"""

import streamlit as st
from src.models.schema import SutraPairManuscript


def render_branding_header() -> None:
    """
    ----------------------------------------------------------------------------
    Function: render_branding_header
    ----------------------------------------------------------------------------
    Purpose:
        Renders the dignified publication masthead for the review portal.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    st.markdown(
        """
        <div style="border-bottom: 2px solid #8b0000; padding-bottom: 12px; margin-bottom: 20px;">
            <h1 style="color: #8b0000; margin: 0; font-size: 32px;">SK Sutras - by Shri Shripad Kulkarni</h1>
            <p style="color: #444444; margin: 6px 0 0 0; font-size: 18px; font-style: italic;">
                Comparative Synthesis of Narada Bhakti Sutra & Shandilya Bhakti Sutra into Udyoga Sutra
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sutra_comparison_cards(pair: SutraPairManuscript) -> None:
    """
    ----------------------------------------------------------------------------
    Function: render_sutra_comparison_cards
    ----------------------------------------------------------------------------
    Purpose:
        Renders the comparative verse card pairing Narada Bhakti Sutra and
        Shandilya Bhakti Sutra under their shared philosophical theme.

    Parameters:
        pair (SutraPairManuscript): The sutra pair manuscript model to display.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    st.markdown(
        f"""
        <div style="background-color: #8b0000; color: white; padding: 8px 16px; border-radius: 6px; display: inline-block; font-weight: bold; margin-bottom: 12px;">
            {pair.pair_id} &bull; Theme: {pair.theme}
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="manuscript-card">
                <h3 style="color: #8b4513; margin-top: 0;">नारद भक्ति सूत्र #{pair.narada_sutra.sutra_no}</h3>
                <div class="devanagari-verse">{pair.narada_sutra.sanskrit}</div>
                <p><strong>Devotional Analysis:</strong><br/>{pair.narada_sutra.vishleshan.en}</p>
                {f"<p><em>(हिंदी): {pair.narada_sutra.vishleshan.hi}</em></p>" if pair.narada_sutra.vishleshan.hi else ""}
                {f"<p><em>(मराठी): {pair.narada_sutra.vishleshan.mr}</em></p>" if pair.narada_sutra.vishleshan.mr else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="manuscript-card">
                <h3 style="color: #8b4513; margin-top: 0;">शाण्डिल्य भक्ति सूत्र #{pair.shandilya_sutra.sutra_no}</h3>
                <div class="devanagari-verse">{pair.shandilya_sutra.sanskrit}</div>
                <p><strong>Philosophical Analysis:</strong><br/>{pair.shandilya_sutra.vishleshan.en}</p>
                {f"<p><em>(हिंदी): {pair.shandilya_sutra.vishleshan.hi}</em></p>" if pair.shandilya_sutra.vishleshan.hi else ""}
                {f"<p><em>(मराठी): {pair.shandilya_sutra.vishleshan.mr}</em></p>" if pair.shandilya_sutra.vishleshan.mr else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Udyoga Bhashya Synthesis Section
    st.markdown(
        f"""
        <div class="synthesis-card">
            <h3 style="color: #7a3a0e; margin-top: 0;">उद्योग भाष्य (Udyoga Bhashya Comparative Synthesis)</h3>
            <p style="font-size: 18px; line-height: 1.6; color: #1a1a1a;">
                {pair.udyoga_bhashya_synthesis.en}
            </p>
            {f"<p style='color: #2b2b2b;'><strong>हिंदी भाष्य:</strong> {pair.udyoga_bhashya_synthesis.hi}</p>" if pair.udyoga_bhashya_synthesis.hi else ""}
            {f"<p style='color: #2b2b2b;'><strong>मराठी भाष्य:</strong> {pair.udyoga_bhashya_synthesis.mr}</p>" if pair.udyoga_bhashya_synthesis.mr else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_branding_footer() -> None:
    """
    ----------------------------------------------------------------------------
    Function: render_branding_footer
    ----------------------------------------------------------------------------
    Purpose:
        Renders the mandatory Hiranyam AI branding footer containing the official
        hyperlink navigating to https://hiranyamai.com/.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    st.markdown(
        """
        <div class="portal-footer">
            SK Sutras &bull; Technical Author: 
            <a href="https://hiranyamai.com/" target="_blank" rel="noopener noreferrer">
                Powered by Hiranyam AI Labs
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
