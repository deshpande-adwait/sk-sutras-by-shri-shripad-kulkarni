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


def render_manuscript_unit_full(unit: Dict[str, Any]) -> None:
    """
    ----------------------------------------------------------------------------
    Function: render_manuscript_unit_full
    ----------------------------------------------------------------------------
    Purpose:
        Renders the complete 6-section ManuscriptUnit conforming to Part 4.3 & 12:
        - Section A: Source Foundation (Narada & Shandilya original sutras)
        - Section B: New Udyoga Sutra in Sanskrit with explicit composition label
        - Section C: Granular Sanskrit Analysis (Padaccheda, Anvaya, Chandas)
        - Section D: Multilingual Translations (English, Hindi, Marathi)
        - Section E: Four-Fold Commentary (Nirukta, Vyavahara, Lokasangraha, Leadership)
        - Section F: Practical Synthesis & Historical Relevance
    ----------------------------------------------------------------------------
    """
    unit_id = unit.get("unit_id", "UDYOGA-001")
    theme = unit.get("theme", "Universal Conduct")
    version = unit.get("version_number", 1)
    status_tag = unit.get("approval_status", "PENDING_REVIEW")

    st.markdown(
        f"""
        <div style="background-color: #8b0000; color: white; padding: 10px 18px; border-radius: 8px; margin-bottom: 16px;">
            <span style="font-size: 20px; font-weight: bold;">{unit_id} &bull; {theme}</span>
            <span style="float: right; background-color: white; color: #8b0000; padding: 2px 10px; border-radius: 4px; font-size: 14px; font-weight: bold;">
                Version {version} &bull; {status_tag}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section A: Source Foundation
    st.markdown("### विभाग अ — आधारभूत मूळ संहिता (Source Foundation)")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div class="manuscript-card">
                <h4 style="color: #8b4513; margin-top: 0;">नारद भक्ति सूत्र ({unit.get('narada_sutra_ref', 'NBS')})</h4>
                <div class="devanagari-verse">{unit.get('narada_sanskrit', '')}</div>
                <p><strong>तात्त्विक अधिष्ठान:</strong> {unit.get('philosophical_relationship', '')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="manuscript-card">
                <h4 style="color: #8b4513; margin-top: 0;">शाण्डिल्य भक्ति सूत्र ({unit.get('shandilya_sutra_ref', 'SBS')})</h4>
                <div class="devanagari-verse">{unit.get('shandilya_sanskrit', '')}</div>
                <p><strong>निवडीचे प्रयोजन:</strong> {unit.get('selection_justification', '')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Section B: New Udyoga Sutra
    st.markdown("### विभाग ब — नूतन उद्योग सूत्र (Original Sanskrit Verse)")
    st.markdown(
        f"""
        <div class="synthesis-card">
            <span style="background-color: #2e7d32; color: white; padding: 3px 8px; border-radius: 4px; font-size: 13px; font-weight: bold;">
                {unit.get('composition_label', 'Original contemporary composition')}
            </span>
            <div class="devanagari-verse" style="font-size: 24px; margin: 12px 0;">
                {unit.get('original_sanskrit_verse', '')}
            </div>
            <p style="font-size: 17px; color: #1a1a1a;"><strong>तात्पर्य:</strong> {unit.get('intended_meaning', '')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Section C: Sanskrit Scholarly Analysis
    st.markdown("### विभाग क — संस्कृत भाषावैज्ञानिक अन्वय व छन्दोमीमांसा (Sanskrit Analysis)")
    with st.expander("व्याकरण, पदच्छेद व अनुष्टुप् छन्द विश्लेषण उघडा (View Details)", expanded=True):
        st.markdown(f"**पदच्छेद (Padaccheda):** {unit.get('padaccheda', '')}")
        st.markdown(f"**अन्वय (Anvaya):** {unit.get('anvaya', '')}")
        st.markdown(f"**पदार्थ (Word Meanings):** {unit.get('word_meanings', '')}")
        st.markdown(f"**व्याकरण विवरण (Grammar):** {unit.get('grammatical_explanation', '')}")
        st.markdown(f"**छन्दोमीमांसा (Chandas):** {unit.get('chandas_name', 'Anushtubh')} — {unit.get('chandas_analysis', '')}")

    # Section D: Multilingual Translations
    st.markdown("### विभाग ड — त्रैभाषिक अनुवाद (Translations: English, Hindi, Marathi)")
    t1, t2, t3 = st.tabs(["English", "हिंदी (Hindi)", "मराठी (Marathi)"])
    with t1:
        st.write(unit.get("translation_en", ""))
    with t2:
        st.write(unit.get("translation_hi", ""))
    with t3:
        st.write(unit.get("translation_mr", ""))

    # Section E: Four-Fold Commentary
    st.markdown("### विभाग इ — चतुर्विध भाष्य (Four-Fold Commentary)")
    st.markdown(f"**१. निरुक्त (Linguistic Nuance):** {unit.get('nirukta', '')}")
    st.markdown(f"**२. व्यवहार-धर्म (Professional Conduct & Ethics):** {unit.get('vyavahara_dharma', '')}")
    st.markdown(f"**३. लोकसंग्रह (Societal Welfare & Trusteeship):** {unit.get('lokasangraha', '')}")
    st.markdown(f"**४. आधुनिक नेतृत्व समन्वय (Modern Business Synthesis):** {unit.get('modern_leadership_synthesis', '')}")


def render_validation_report_card(report: Dict[str, Any]) -> None:
    """
    ----------------------------------------------------------------------------
    Function: render_validation_report_card
    ----------------------------------------------------------------------------
    Purpose:
        Renders Agent 4 (Independent Validator) scholarly validation report card.
    ----------------------------------------------------------------------------
    """
    status_str = report.get("overall_status", "PASS")
    status_color = "#2e7d32" if status_str == "PASS" else ("#d32f2f" if status_str == "FAIL" else "#f57c00")

    st.markdown(
        f"""
        <div style="border: 2px solid {status_color}; border-radius: 8px; padding: 14px; margin-top: 16px; background-color: #fafafa;">
            <h4 style="color: {status_color}; margin-top: 0;">
                अभिकर्ता ४ स्वतंत्र विद्वत् परीक्षण अहवाल (Agent 4 Validation Report) &bull; {status_str}
            </h4>
            <p><strong>परीक्षण चक्र (Revision Cycle):</strong> {report.get('revision_cycle', 0)} / 3</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    findings = report.get("findings", [])
    if findings:
        st.write("**सुधारणेसाठी सूचना (Required Scholarly Refinements):**")
        for f in findings:
            st.warning(f"[{f.get('location')}] {f.get('issue_description')} — उपाय: {f.get('suggested_correction')}")

