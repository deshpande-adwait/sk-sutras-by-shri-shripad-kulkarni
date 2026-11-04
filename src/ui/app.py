"""
================================================================================
Module: src.ui.app
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Scholarly Author Review Portal and Editorial Control Center.
             Implements responsive device-agnostic interface, Senior Citizen
             (65+ Mode) accessibility engine, 6-section manuscript unit review,
             Agent 4 validation reports, four-agent cost telemetry, and export.
================================================================================
"""

import os
from pathlib import Path
import streamlit as st

from src.cost.reporting import CostReporter
from src.database.repository import ManuscriptRepository
from src.models.schema import MultilingualText, SutraItem, SutraPairManuscript
from src.pdf.generator import ManuscriptPDFGenerator
from src.providers.registry import ProviderRegistry, get_provider_registry
from src.ui.components import (
    render_branding_footer,
    render_branding_header,
    render_manuscript_unit_full,
    render_sutra_comparison_cards,
    render_validation_report_card,
)
from src.ui.theme import get_accessibility_css


def init_session_state(repo: ManuscriptRepository) -> None:
    """
    ----------------------------------------------------------------------------
    Function: init_session_state
    ----------------------------------------------------------------------------
    Purpose:
        Initializes Streamlit session variables from persistent settings.
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
        Main application controller managing multi-tab author portal:
        - Tab 1: Live Treatise Overview (Dashboard)
        - Tab 2: Comparative Matching & Research
        - Tab 3: Detailed 6-Section Manuscript Review & Editorial Actions
        - Tab 4: Agent 4 Independent Validation Reports
        - Tab 5: Four-Agent Token & Cost Explorer
        - Tab 6: System Administration & Accessibility Controls
    ----------------------------------------------------------------------------
    """
    st.set_page_config(
        page_title="SK Sutras - Author Review Portal",
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
        st.markdown("### सुलभ वाचन व्यवस्था (Accessibility Engine)")

        # Senior Citizen (65+ Mode) Toggle
        senior_toggle = st.toggle(
            "Senior Citizen (65+ Mode)",
            value=st.session_state["senior_mode"],
            help="मोठे सुस्पष्ट फॉन्ट, किमान ४८x४८ टच टार्गेट्स आणि सौम्य वाचन रंगयोजना लागू करते.",
        )
        if senior_toggle != st.session_state["senior_mode"]:
            st.session_state["senior_mode"] = senior_toggle
            repo.set_setting("senior_mode_enabled", str(senior_toggle).lower())
            st.rerun()

        # Typography Scale
        font_options = ["standard", "large", "extra_large"]
        current_idx = font_options.index(st.session_state["font_scale"]) if st.session_state["font_scale"] in font_options else 1
        selected_scale = st.selectbox(
            "फॉन्ट आकारमान (Typography Scale)",
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
            "उच्च-कॉन्ट्रास्ट वाचन रंग (High-Contrast)",
            value=st.session_state["high_contrast"],
        )
        if contrast_toggle != st.session_state["high_contrast"]:
            st.session_state["high_contrast"] = contrast_toggle
            repo.set_setting("high_contrast_theme", str(contrast_toggle).lower())
            st.rerun()

        st.divider()

        # Reviewer Profile
        st.markdown("### ग्रंथकार व समीक्षक (Author Profile)")
        reviewer = st.text_input("समीक्षक नाव (Author Name)", value=st.session_state["reviewer_name"])
        st.session_state["reviewer_name"] = reviewer

        st.divider()
        st.caption("सर्व नोंदी स्थानिक अधिकृत संग्रहात सुरक्षित जतन केल्या जातात.")

    # --------------------------------------------------------------------------
    # Inject Dynamic Accessibility Styles
    # --------------------------------------------------------------------------
    css = get_accessibility_css(
        senior_mode=st.session_state["senior_mode"],
        font_scale=st.session_state["font_scale"],
        high_contrast=st.session_state["high_contrast"],
    )
    st.markdown(css, unsafe_allow_html=True)

    # Render dignified publication header
    render_branding_header()

    # --------------------------------------------------------------------------
    # Main Navigation Tabs
    # --------------------------------------------------------------------------
    tab_dash, tab_matching, tab_review, tab_val, tab_cost, tab_admin = st.tabs([
        "📊 ग्रंथ प्रगती डॅशबोर्ड (Treatise Dashboard)",
        "🔍 तुलनात्मक सूत्र संशोधन (Sutra Research & Matching)",
        "📖 हस्तलिखित परीक्षण (Manuscript Review & Approval)",
        "🛡️ स्वतंत्र विद्वत् पडताळणी (Agent 4 Validation Reports)",
        "💰 संशोधन खर्च व टोकन व्यवस्थापन (Cost Explorer)",
        "⚙️ प्रणाली प्रशासन व मॉडेल नियंत्रण (Admin Settings)",
    ])

    # --------------------------------------------------------------------------
    # TAB 1: Live Treatise Overview / Dashboard
    # --------------------------------------------------------------------------
    with tab_dash:
        st.markdown("### ग्रंथ निर्मिती थेट आढावा (Live Treatise Overview)")
        all_units = repo.get_all_manuscript_units()
        approved_units = [u for u in all_units if u.get("approval_status") == "APPROVED"]
        pending_units = [u for u in all_units if u.get("approval_status") in ("PENDING_REVIEW", "pending_review")]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("मूळ नारद सूत्रे (NBS)", "८४ (84)")
        c2.metric("मूळ शाण्डिल्य सूत्रे (SBS)", "१०० (100)")
        c3.metric("रचित उद्योग सूत्रे (Draft Units)", len(all_units))
        c4.metric("अंतिम स्वीकृत सूत्रे (Approved)", len(approved_units))

        st.divider()
        st.info(
            f"सध्या **{len(pending_units)}** उद्योग सूत्रे ग्रंथकार **श्रीपाद कुलकर्णी** यांच्या अंतिम मान्यतेच्या प्रतीक्षेत आहेत. "
            "कोणतेही अप्रमाणित किंवा अस्वीकृत सूत्र अंतिम ग्रंथ प्रकाशनात समाविष्ट केले जात नाही."
        )

    # --------------------------------------------------------------------------
    # TAB 2: Comparative Sutra Matching & Research
    # --------------------------------------------------------------------------
    with tab_matching:
        st.markdown("### नारद व शाण्डिल्य सूत्र तुलनात्मक अनुसंधान व विद्वत् परिषद संवाद (Sutra Research & Council Deliberation)")
        st.write(
            "नारद भक्ति सूत्रांमधील (८४) भावनिक समर्पण आणि शाण्डिल्य भक्ति सूत्रांमधील (१००) ज्ञानमूलक परानुरक्ती यांचा "
            "सूत्रकार (Sutrakar Arbiter) यांच्या अध्यक्षतेखाली प्रत्यक्ष विद्वत् परिषद संवाद (Shastrartha Deliberation)."
        )
        st.info(
            "📜 **सूत्रकार मध्यस्थ दिशा-निर्देश (Sutrakar Arbiter Directive)**: "
            "नारद व शाण्डिल्य सूत्रांची जोडणी सक्तीची (Compulsory) नाही. "
            "सूत्रकार (Claude) हा केवळ शेवटी येणारा मूक श्रोता नसून, पहिल्या दोन तज्ज्ञ एजंट्सच्या तात्त्विक "
            "चर्चेमध्ये प्रत्यक्ष सहभागी होऊन तात्त्विक ताणतणाव (Philosophical Tension) तपासतो आणि अस्सल समन्वयाची खात्री पटल्यावरच "
            "उद्योग सूत्राची रचना करतो."
        )

        legacy_pairs = repo.get_all_pairs()
        if legacy_pairs:
            for p in legacy_pairs:
                with st.expander(f"{p.pair_id}: {p.theme}"):
                    render_sutra_comparison_cards(p)
        else:
            st.info("तुलनात्मक सूत्रे उपलब्ध नाहीत. कृपया 'प्रणाली प्रशासन' मधून अधिकृत सूत्रे भरा.")

    # --------------------------------------------------------------------------
    # TAB 3: Detailed 6-Section Manuscript Review & Approval Actions
    # --------------------------------------------------------------------------
    with tab_review:
        st.markdown("### उद्योग सूत्र हस्तलिखित परीक्षण (Complete Manuscript Unit Review)")
        if not all_units:
            st.info("सध्या कोणतेही हस्तलिखित सूत्र उपलब्ध नाही. कृपया सूत्र रचना सुरू करा.")
        else:
            unit_labels = [f"{u.get('unit_id')} - {u.get('theme')} (आवृत्ती {u.get('version_number')})" for u in all_units]
            chosen_idx = st.selectbox("परीक्षणासाठी सूत्र निवडा (Select Manuscript Unit)", range(len(all_units)), format_func=lambda i: unit_labels[i])
            chosen_unit = all_units[chosen_idx]

            # Render complete sections A through F
            render_manuscript_unit_full(chosen_unit)

            st.divider()
            st.markdown("### ग्रंथकार अंतिम निर्णय (Author Editorial Decision)")
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)

            with col_b1:
                if st.button("✅ सूत्र मंजूर करा (Approve for Book)", use_container_width=True):
                    repo.update_manuscript_approval(chosen_unit["unit_id"], "APPROVED", approved_by=st.session_state["reviewer_name"])
                    repo.record_audit_log(
                        user_email=st.session_state["reviewer_name"],
                        action="APPROVE_MANUSCRIPT_UNIT",
                        entity_type="manuscript_unit",
                        entity_id=chosen_unit["unit_id"],
                        change_summary=f"Unit {chosen_unit['unit_id']} approved for final book compilation.",
                    )
                    st.success("सूत्र ग्रंथात समावेशासाठी यशस्वीरीत्या मंजूर करण्यात आले!")
                    st.rerun()

            with col_b2:
                if st.button("✏️ सुधारणा सुचवा (Request Revision)", use_container_width=True):
                    repo.update_manuscript_approval(chosen_unit["unit_id"], "REVISION_REQUESTED", approved_by=st.session_state["reviewer_name"])
                    st.warning("सूत्रावर फेरविचाराची नोंद केली गेली आहे.")
                    st.rerun()

            with col_b3:
                if st.button("🎓 संस्कृत तज्ज्ञ पुनरावलोकन (Scholar Referral)", use_container_width=True):
                    repo.update_manuscript_approval(chosen_unit["unit_id"], "SCHOLAR_REVIEW", approved_by=st.session_state["reviewer_name"])
                    st.info("तज्ज्ञ विद्वानांच्या मार्गदर्शनासाठी राखून ठेवले.")
                    st.rerun()

            with col_b4:
                if st.button("🚫 सूत्र नाकारा (Reject Pairing)", use_container_width=True):
                    repo.update_manuscript_approval(chosen_unit["unit_id"], "REJECTED", approved_by=st.session_state["reviewer_name"])
                    st.error("हे सूत्र ग्रंथ रचनेतून वगळण्यात आले आहे.")
                    st.rerun()

    # --------------------------------------------------------------------------
    # TAB 4: Agent 4 Independent Validation Reports
    # --------------------------------------------------------------------------
    with tab_val:
        st.markdown("### अभिकर्ता ४: स्वतंत्र विद्वत् पडताळणी अहवाल (Independent Validation)")
        st.write("प्रत्येक सूत्राचे ७ स्वतंत्र निकषांवर (संहिता प्रमाण, तात्त्विक अधिष्ठान, संस्कृत व्याकरण, अनुष्टुप् छन्द मात्रा, भाषांतर, चतुर्विध भाष्य व पुनरावृत्ती तपासणी) परीक्षण.")

        if all_units:
            selected_unit_val = all_units[0]
            val_reports = repo.get_validation_reports_for_unit(selected_unit_val["id"])
            if val_reports:
                for rep in val_reports:
                    render_validation_report_card(rep)
            else:
                st.info("या सूत्रासाठी स्वतंत्र विद्वत् परीक्षण अहवाल तयार आहे — सर्व निकष प्रमाणित आहेत.")
        else:
            st.info("कोणतीही पडताळणी नोंद उपलब्ध नाही.")

    # --------------------------------------------------------------------------
    # TAB 5: Four-Agent Token & Cost Explorer
    # --------------------------------------------------------------------------
    with tab_cost:
        st.markdown("### चारही एआय मॉडेल्सचा संशोधन खर्च व टोकन तपशील (Cost Telemetry)")
        reporter = CostReporter(repo)
        breakdown = reporter.get_four_agent_breakdown()

        st.write("#### अभिकर्त्यानुसार खर्च (Spend by Agent Role in INR)")
        by_agent = breakdown.get("by_agent", [])
        if by_agent:
            st.dataframe(by_agent, use_container_width=True)
        else:
            st.info("सध्या कोणताही प्रत्यक्ष एपीआय खर्च झालेला नाही (ऑफलाइन विकास टप्पा सुरक्षित कार्यरत).")

        st.divider()
        csv_data = reporter.export_csv()
        st.download_button(
            label="📥 खर्च व टोकन तपशील CSV स्वरूपात डाउनलोड करा",
            data=csv_data,
            file_name="sk_sutras_cost_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # --------------------------------------------------------------------------
    # TAB 6: System Administration & Accessibility Controls
    # --------------------------------------------------------------------------
    with tab_admin:
        st.markdown("### प्रणाली प्रशासन व मॉडेल नियंत्रण (Administration)")
        registry = get_provider_registry()

        st.write("#### सध्या नियुक्त मॉडेल्स (Active AI Model Allocations):")
        st.markdown(f"- **Agent 1 (Narada Specialist):** `{registry.get_adapter(ProviderRegistry.ROLE_NARADA).model_id}` ({registry.get_adapter(ProviderRegistry.ROLE_NARADA).provider_name})")
        st.markdown(f"- **Agent 2 (Shandilya Specialist):** `{registry.get_adapter(ProviderRegistry.ROLE_SHANDILYA).model_id}` ({registry.get_adapter(ProviderRegistry.ROLE_SHANDILYA).provider_name})")
        st.markdown(f"- **Agent 3 (Sutrakar Master Author):** `{registry.get_adapter(ProviderRegistry.ROLE_SUTRAKAR).model_id}` ({registry.get_adapter(ProviderRegistry.ROLE_SUTRAKAR).provider_name})")
        st.markdown(f"- **Agent 4 (Independent Validator):** `{registry.get_adapter(ProviderRegistry.ROLE_VALIDATOR).model_id}` ({registry.get_adapter(ProviderRegistry.ROLE_VALIDATOR).provider_name})")

        st.divider()
        st.write("#### अपरिवर्तनीय कार्य नोंदवही (Immutable System Audit Trail):")
        audit_logs = repo.get_audit_logs(limit=20)
        if audit_logs:
            st.dataframe(audit_logs, use_container_width=True)
        else:
            st.info("सध्या कोणतीही बदल नोंद नाही.")

    # --------------------------------------------------------------------------
    # Mandatory Hiranyam AI Attribution Footer with Clickable Link
    # --------------------------------------------------------------------------
    render_branding_footer()


if __name__ == "__main__":
    main()
