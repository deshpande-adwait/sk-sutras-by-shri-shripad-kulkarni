"""
================================================================================
Module: src.ui.app
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Main entry point for the Streamlit Manuscript Review Portal.
             Implements device-agnostic responsive design, admin-configurable
             Senior Citizen (65+ Mode) accessibility engine, Human-in-the-Loop
             review workflow, and publication typesetting exports.
================================================================================
"""

import os
from pathlib import Path
import streamlit as st

from src.database.repository import ManuscriptRepository
from src.models.schema import MultilingualText, SutraItem, SutraPairManuscript
from src.pdf.generator import ManuscriptPDFGenerator
from src.ui.components import (
    render_branding_footer,
    render_branding_header,
    render_sutra_comparison_cards,
)
from src.ui.theme import get_accessibility_css


def init_session_state(repo: ManuscriptRepository) -> None:
    """
    ----------------------------------------------------------------------------
    Function: init_session_state
    ----------------------------------------------------------------------------
    Purpose:
        Initializes Streamlit session variables from persistent settings stored
        in SQLite or environment defaults.

    Parameters:
        repo (ManuscriptRepository): Relational database repository instance.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    if "senior_mode" not in st.session_state:
        db_val = repo.get_setting("senior_mode_enabled", "true")
        st.session_state["senior_mode"] = db_val.lower() == "true"

    if "font_scale" not in st.session_state:
        db_val = repo.get_setting("default_font_scale", "large")
        st.session_state["font_scale"] = db_val

    if "high_contrast" not in st.session_state:
        db_val = repo.get_setting("high_contrast_theme", "true")
        st.session_state["high_contrast"] = db_val.lower() == "true"

    if "reviewer_name" not in st.session_state:
        st.session_state["reviewer_name"] = "Shri Shripad Kulkarni"


def main() -> None:
    """
    ----------------------------------------------------------------------------
    Function: main
    ----------------------------------------------------------------------------
    Purpose:
        Configures page layout, injects dynamic accessibility styles, renders
        the sidebar administrative settings, and manages the primary review tabs.

    Parameters:
        None

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    st.set_page_config(
        page_title="SK Sutras - Udyoga Sutra Review Portal",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    repo = ManuscriptRepository()
    init_session_state(repo)

    # --------------------------------------------------------------------------
    # Sidebar: Administrative Settings & Accessibility Engine
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### Accessibility & Display Settings")
        
        # Senior Citizen (65+ Mode) Toggle - Enabled by Default for this Project
        senior_toggle = st.toggle(
            "Senior Citizen (65+ Mode)",
            value=st.session_state["senior_mode"],
            help="Enlarges typography, broadens touch targets, and applies high-legibility contrasts.",
        )
        if senior_toggle != st.session_state["senior_mode"]:
            st.session_state["senior_mode"] = senior_toggle
            repo.set_setting("senior_mode_enabled", str(senior_toggle).lower())
            st.rerun()

        # Typography Scale
        font_options = ["standard", "large", "extra_large"]
        current_idx = font_options.index(st.session_state["font_scale"]) if st.session_state["font_scale"] in font_options else 1
        selected_scale = st.selectbox(
            "Reading Typography Scale",
            options=font_options,
            index=current_idx,
            format_func=lambda s: s.replace("_", " ").title(),
        )
        if selected_scale != st.session_state["font_scale"]:
            st.session_state["font_scale"] = selected_scale
            repo.set_setting("default_font_scale", selected_scale)
            st.rerun()

        # High Contrast Readability
        contrast_toggle = st.toggle(
            "High-Contrast Reading Mode",
            value=st.session_state["high_contrast"],
        )
        if contrast_toggle != st.session_state["high_contrast"]:
            st.session_state["high_contrast"] = contrast_toggle
            repo.set_setting("high_contrast_theme", str(contrast_toggle).lower())
            st.rerun()

        st.divider()

        # Reviewer Profile
        st.markdown("### Reviewer Profile")
        reviewer = st.text_input("Active Reviewer Name", value=st.session_state["reviewer_name"])
        st.session_state["reviewer_name"] = reviewer

        # Live Overview
        st.divider()
        st.markdown("### Live Manuscript Overview")
        all_pairs = repo.get_all_pairs()
        approved_count = len([p for p in all_pairs if repo.get_pair(p.pair_id)])
        st.metric(label="Total Comparative Pairs", value=len(all_pairs))
        st.caption("All changes are automatically saved to your local database.")

    # --------------------------------------------------------------------------
    # Inject Dynamic Accessibility Styles
    # --------------------------------------------------------------------------
    css = get_accessibility_css(
        senior_mode=st.session_state["senior_mode"],
        font_scale=st.session_state["font_scale"],
        high_contrast=st.session_state["high_contrast"],
    )
    st.markdown(css, unsafe_allow_html=True)

    # Render Masthead
    render_branding_header()

    # --------------------------------------------------------------------------
    # Main Navigation Tabs
    # --------------------------------------------------------------------------
    tab_review, tab_manuscript, tab_new_pair = st.tabs([
        "📖 Comparative Sutra Review",
        "📜 Compiled Udyoga Sutra Treatise",
        "➕ Add / Seed Sutra Pair",
    ])

    # TAB 1: Comparative Review (Human-in-the-Loop)
    with tab_review:
        pending_pairs = repo.get_all_pairs(status="pending_review")
        if not pending_pairs:
            # Also show approved pairs if pending list is empty for inspection
            pending_pairs = repo.get_all_pairs()

        if not pending_pairs:
            st.info("No comparative sutra pairs found. Use the 'Add / Seed Sutra Pair' tab to seed initial verses.")
        else:
            pair_options = [f"{p.pair_id} - {p.theme}" for p in pending_pairs]
            selected_idx = st.selectbox(
                "Select Sutra Pair for Review",
                options=range(len(pending_pairs)),
                format_func=lambda i: pair_options[i],
            )
            selected_pair = pending_pairs[selected_idx]

            # Display comparative cards
            render_sutra_comparison_cards(selected_pair)

            # Editorial Review Actions
            st.markdown("### Editorial Decision")
            col_act1, col_act2, col_act3 = st.columns([1, 1, 1])

            with col_act1:
                if st.button("✅ Approve Synthesis", use_container_width=True):
                    repo.record_review(
                        pair_id=selected_pair.pair_id,
                        reviewer_name=st.session_state["reviewer_name"],
                        action="approved",
                        notes="Approved by reviewer without modifications.",
                    )
                    st.success(f"Pair '{selected_pair.pair_id}' approved successfully!")
                    st.rerun()

            with col_act2:
                with st.expander("✏️ Refine / Edit Commentary"):
                    edited_bhashya = st.text_area(
                        "Modified Udyoga Bhashya (English)",
                        value=selected_pair.udyoga_bhashya_synthesis.en,
                        height=160,
                    )
                    reviewer_notes = st.text_input("Editorial Notes", placeholder="e.g. Adjusted philosophical context...")
                    if st.button("💾 Save Revisions & Approve", use_container_width=True):
                        repo.record_review(
                            pair_id=selected_pair.pair_id,
                            reviewer_name=st.session_state["reviewer_name"],
                            action="approved",
                            notes=reviewer_notes,
                            updated_bhashya_en=edited_bhashya,
                        )
                        st.success("Revisions saved and synthesis approved!")
                        st.rerun()

            with col_act3:
                if st.button("🚫 Reject Pairing", use_container_width=True):
                    repo.record_review(
                        pair_id=selected_pair.pair_id,
                        reviewer_name=st.session_state["reviewer_name"],
                        action="rejected",
                        notes="Rejected from compilation by reviewer.",
                    )
                    st.warning(f"Pair '{selected_pair.pair_id}' marked as rejected.")
                    st.rerun()

    # TAB 2: Compiled Treatise & PDF Export
    with tab_manuscript:
        all_compiled = repo.get_all_pairs()
        if not all_compiled:
            st.info("No compiled manuscript records available yet.")
        else:
            st.markdown(f"### Compiled Udyoga Sutra ({len(all_compiled)} Aphorism Pairs)")
            
            # PDF Generation Action
            pdf_gen = ManuscriptPDFGenerator()
            if st.button("📥 Generate & Download Publication PDF", use_container_width=True):
                with st.spinner("Compiling high-fidelity Devanagari PDF..."):
                    generated_path = pdf_gen.generate_pdf(
                        pairs=all_compiled,
                        output_filename="udyoga_sutra_compilation.pdf",
                    )
                    if generated_path.exists():
                        with open(generated_path, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Click Here to Download PDF Document",
                                data=pdf_file,
                                file_name=generated_path.name,
                                mime="application/pdf" if str(generated_path).endswith(".pdf") else "text/html",
                                use_container_width=True,
                            )
                        st.success(f"Manuscript compiled successfully: {generated_path.name}")

            # Browse individual entries
            for entry in all_compiled:
                with st.expander(f"{entry.pair_id}: {entry.theme}"):
                    render_sutra_comparison_cards(entry)

    # TAB 3: Add / Seed Sutra Pair
    with tab_new_pair:
        st.markdown("### Seed Canonical Pairs or Add Custom Pair")
        if st.button("🌱 Load Canonical Seed Pairs (Narada & Shandilya)", use_container_width=True):
            seed_pairs = [
                SutraPairManuscript(
                    pair_id="PAIR-001",
                    theme="Inaugural Definition of Bhakti",
                    narada_sutra=SutraItem(
                        sutra_no="1",
                        sanskrit="अथातो भक्तिं व्याख्यास्यामः॥",
                        vishleshan=MultilingualText(
                            en="Now, therefore, we shall expound the nature and philosophy of Devotion (Bhakti).",
                            hi="अब इसके बाद हम भक्ति की व्याख्या करेंगे।",
                            mr="आता यानंतर आम्ही भक्तीची सविस्तर व्याख्या करू.",
                        ),
                    ),
                    shandilya_sutra=SutraItem(
                        sutra_no="1",
                        sanskrit="अथातो भक्तिजिज्ञासा॥",
                        vishleshan=MultilingualText(
                            en="Now, therefore, arises the profound spiritual inquiry into the philosophical nature of Bhakti.",
                            hi="अब इसके बाद भक्ति के स्वरूप की दार्शनिक जिज्ञासा की जाती है।",
                            mr="आता यानंतर भक्तीच्या स्वरूपाविषयी तात्विक जिज्ञासा केली जाते.",
                        ),
                    ),
                    udyoga_bhashya_synthesis=MultilingualText(
                        en=(
                            "The Udyoga Sutra inaugurates its synthesis by uniting Narada's experiential exposition "
                            "('vyākhyāsyāmaḥ') with Shandilya's epistemological inquiry ('jijñāsā'). While Narada introduces "
                            "Bhakti as a lived devotional reality, Shandilya establishes it as an intellectual quest for "
                            "supreme spiritual knowledge. Together, they demonstrate that true devotion harmonizes ecstatic "
                            "love with rigorous discernment."
                        ),
                        hi=(
                            "उद्योग सूत्र नारद की अनुभवात्मक व्याख्या और शांडिल्य की ज्ञानात्मक जिज्ञासा का समन्वय करता है। "
                            "भक्ति केवल भाव नहीं, अपितु परम ज्ञान का अधिष्ठान भी है।"
                        ),
                        mr=(
                            "उद्योग सूत्र नारदांची अनुभवाधारित व्याख्या आणि शांडिल्यांची ज्ञानमूलक जिज्ञासा यांचा समन्वय साधतो. "
                            "भक्ती केवळ भावना नसून सर्वोच्च ज्ञानाचे अधिष्ठान आहे."
                        ),
                    ),
                ),
                SutraPairManuscript(
                    pair_id="PAIR-002",
                    theme="Supreme Love & Attachment to the Divine",
                    narada_sutra=SutraItem(
                        sutra_no="2",
                        sanskrit="सा त्वस्मिन् परमप्रेमरूपा॥",
                        vishleshan=MultilingualText(
                            en="That (Devotion) is indeed of the nature of supreme divine love directed towards the Divine.",
                            hi="वह (भक्ति) निश्चित रूप से ईश्वर के प्रति परम प्रेम स्वरूप है।",
                            mr="ती भक्ती खरोखर ईश्वराविषयी परम प्रेमरूप आहे.",
                        ),
                    ),
                    shandilya_sutra=SutraItem(
                        sutra_no="2",
                        sanskrit="सा परानुरक्तिरीश्वरे॥",
                        vishleshan=MultilingualText(
                            en="That (Bhakti) is supreme, unswerving attachment (anurakti) directed towards the Supreme Lord (Ishvara).",
                            hi="वह (भक्ति) परमेश्वर के प्रति परम अनुरक्ति (अनन्य अनुराग) है।",
                            mr="ती भक्ती परमेश्वराच्या ठिकाणी असलेली परम अनुरक्ती होय.",
                        ),
                    ),
                    udyoga_bhashya_synthesis=MultilingualText(
                        en=(
                            "In this thematic pairing, Narada defines Bhakti as 'parama-prema-rūpā' (pure, supreme love), "
                            "centering on the emotional ecstasy and selfless surrender of the devotee. Shandilya characterizes "
                            "it as 'parānuraktir-īśvare' (supreme attachment after knowing God's glory). The Udyoga synthesis "
                            "reveals that love (prema) and unshakeable attachment (anurakti) are two dimensions of the same divine connection."
                        ),
                        hi=(
                            "नारद भक्ति को 'परम प्रेम रूपा' कहते हैं, जबकि शांडिल्य इसे 'परानुरक्ति' कहते हैं। "
                            "उद्योग भाष्य सिद्ध करता है कि प्रेम और अनुरक्ति वस्तुतः एक ही चेतना के दो पहलू हैं।"
                        ),
                        mr=(
                            "नारद भक्तीला 'परम प्रेम रूप' म्हणतात, तर शांडिल्य तिला 'परानुरक्ती' म्हणतात. "
                            "उद्योग भाष्य हे दाखवून देते की प्रेम आणि अखंड आसक्ती ही एकाच भक्तीचे दोन पैलू आहेत."
                        ),
                    ),
                ),
            ]
            for p in seed_pairs:
                repo.save_pair(p, status="pending_review")
            st.success("Canonical seed pairs loaded into database!")
            st.rerun()

    # Mandatory Branding Footer
    render_branding_footer()


if __name__ == "__main__":
    main()
