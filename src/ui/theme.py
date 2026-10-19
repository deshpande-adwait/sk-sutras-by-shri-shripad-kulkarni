"""
================================================================================
Module: src.ui.theme
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Dynamic accessibility theming engine. Injects adaptive CSS for
             device-agnostic mobile rendering, large touch targets, high-contrast
             reading, and the dedicated Senior Citizen (65+ Mode) preset.
================================================================================
"""

from typing import Dict


def get_accessibility_css(
    senior_mode: bool = True,
    font_scale: str = "large",
    high_contrast: bool = True,
) -> str:
    """
    ----------------------------------------------------------------------------
    Function: get_accessibility_css
    ----------------------------------------------------------------------------
    Purpose:
        Generates dynamic CSS rules tailored for Streamlit components based on
        active accessibility preferences. When Senior Citizen (65+ Mode) is active,
        enforces large touch targets (>= 48px), prominent Devanagari verses,
        and high-contrast typography to eliminate eye strain for senior reviewers.

    Parameters:
        senior_mode (bool): Whether Senior Citizen (65+ Mode) is active.
        font_scale (str): Typography scale factor ('standard', 'large', 'extra_large').
        high_contrast (bool): Whether to enforce maximum visual contrast.

    Returns:
        str: Injectable HTML `<style>` block containing customized CSS.

    Manual Debugging Notes:
        - Streamlit embeds this CSS via `st.markdown(css, unsafe_allow_html=True)`.
        - Test across both mobile browser viewports (<= 480px) and wide desktop monitors.
    ----------------------------------------------------------------------------
    """
    scale_map: Dict[str, Dict[str, str]] = {
        "standard": {
            "base_font": "16px",
            "verse_font": "20px",
            "h1_font": "26px",
            "h2_font": "22px",
            "btn_padding": "10px 18px",
            "btn_height": "44px",
            "btn_font": "15px",
        },
        "large": {
            "base_font": "19px",
            "verse_font": "25px",
            "h1_font": "30px",
            "h2_font": "25px",
            "btn_padding": "14px 24px",
            "btn_height": "52px",
            "btn_font": "18px",
        },
        "extra_large": {
            "base_font": "22px",
            "verse_font": "29px",
            "h1_font": "34px",
            "h2_font": "28px",
            "btn_padding": "16px 28px",
            "btn_height": "60px",
            "btn_font": "20px",
        },
    }

    # If Senior Mode is active, override standard with at least 'large'
    resolved_scale_key = font_scale if not senior_mode else ("extra_large" if font_scale == "extra_large" else "large")
    metrics = scale_map.get(resolved_scale_key, scale_map["large"])

    bg_color = "#fbf9f5" if high_contrast else "#ffffff"
    text_color = "#111111" if high_contrast else "#222222"
    verse_color = "#7b1113" if high_contrast else "#8b0000"
    card_bg = "#ffffff" if high_contrast else "#fdfcf9"
    border_color = "#333333" if high_contrast else "#d5c9bd"

    css = f"""
    <style>
        /* Base typography & responsive container */
        html, body, [class*="css"] {{
            font-size: {metrics['base_font']};
            color: {text_color};
            background-color: {bg_color};
        }}

        /* Generous touch targets for all buttons (Senior Accessibility) */
        .stButton > button {{
            min-height: {metrics['btn_height']};
            padding: {metrics['btn_padding']};
            font-size: {metrics['btn_font']} !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            border: 2px solid {border_color} !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            transition: all 0.2s ease-in-out;
            margin-top: 6px;
            margin-bottom: 6px;
        }}

        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.14);
        }}

        /* Prominent Devanagari Sanskrit verses */
        .devanagari-verse {{
            font-family: 'Noto Serif Devanagari', 'Mangal', 'Kokila', serif;
            font-size: {metrics['verse_font']} !important;
            font-weight: 700;
            line-height: 1.6;
            color: {verse_color};
            background-color: #fff9f2;
            padding: 16px;
            border-left: 6px solid #8b0000;
            border-radius: 6px;
            margin: 12px 0;
            border: 1px solid #f0e2d5;
        }}

        /* Comparative review cards */
        .manuscript-card {{
            background-color: {card_bg};
            border: 2px solid {border_color};
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.06);
        }}

        /* Synthesis highlight card */
        .synthesis-card {{
            background-color: #f7f2ea;
            border-left: 6px solid #b85d19;
            border-radius: 8px;
            padding: 20px;
            margin: 16px 0;
            border: 1px solid #e5d8c8;
        }}

        /* Mobile layout refinements */
        @media (max-width: 768px) {{
            .stButton > button {{
                width: 100% !important;
                min-height: 56px !important;
                font-size: 20px !important;
            }}
            .devanagari-verse {{
                font-size: 22px !important;
                padding: 12px !important;
            }}
        }}

        /* Clean business-facing footer */
        .portal-footer {{
            margin-top: 50px;
            padding: 20px;
            text-align: center;
            border-top: 1px solid {border_color};
            font-size: 14px;
            color: #555555;
        }}
        .portal-footer a {{
            color: #0b5394;
            font-weight: bold;
            text-decoration: none;
        }}
    </style>
    """
    return css
