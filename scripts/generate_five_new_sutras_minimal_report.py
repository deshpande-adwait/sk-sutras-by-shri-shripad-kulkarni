"""
================================================================================
Script: scripts/generate_five_new_sutras_minimal_report.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates the exact clean, user-friendly Word document (.docx)
             containing EXCLUSIVELY the 3 requested components:
             1. Matching Pairs (Original Narada & Shandilya Sutras in Sanskrit)
             2. Newly Derived Shloka (New Sanskrit Udyam Sutra)
             3. Translation of each of the shlokas (English & Marathi)
             Enforces the mandatory confidentiality footer on every page:
             "Proprietory and Confidential- Hiranyam AI Labs"
================================================================================
"""

import os
import shutil
import sys
from pathlib import Path

# Configure Windows UTF-8 console output
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Inches, Pt, RGBColor

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DOCS_DIR / "UDYAM_SUTRAS_MATCHING_PAIRS_AND_NEW_SHLOKAS.docx"
ARTIFACT_DIR = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc")
ARTIFACT_FILE = ARTIFACT_DIR / "UDYAM_SUTRAS_MATCHING_PAIRS_AND_NEW_SHLOKAS.docx"

MANDATORY_FOOTER = "Proprietory and Confidential- Hiranyam AI Labs"

# Color Palette: Clean Classical Academic
C_MAROON = RGBColor(139, 0, 0)       # #8B0000 Primary Sacred Accent
C_NAVY = RGBColor(18, 52, 86)        # #123456 Secondary Accent
C_SLATE = RGBColor(40, 45, 55)       # #282D37 Text dark
C_GOLD = RGBColor(180, 115, 20)      # Highlighting
C_BORDER = "D4C5B0"                  # Subtle warm border


def set_cell_background(cell, hex_color: str):
    """Sets background shading of a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def build_concise_word_document():
    doc = docx.Document()

    # Configure Margins and Mandatory Footer across all sections
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.different_first_page_header_footer = False

        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run(MANDATORY_FOOTER)
        f_run.font.name = "Arial"
        f_run.font.size = Pt(8.5)
        f_run.font.bold = True
        f_run.font.color.rgb = C_MAROON

    # --------------------------------------------------------------------------
    # Document Header & Title
    # --------------------------------------------------------------------------
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_after = Pt(2)
    r_pre = p_pre.add_run("SRI SHRIPAD KULKARNI'S CANONICAL INITIATIVE")
    r_pre.font.name = "Arial"
    r_pre.font.size = Pt(9.5)
    r_pre.font.bold = True
    r_pre.font.color.rgb = C_GOLD

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run("UDYAM SUTRAS: MATCHING PAIRS & NEW SHLOKAS")
    r_t.font.name = "Arial"
    r_t.font.size = Pt(17)
    r_t.font.bold = True
    r_t.font.color.rgb = C_MAROON

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(8)
    r_s = p_sub.add_run(
        "Source Foundations (Narada Bhakti Sutras × Shandilya Bhakti Sutras) → "
        "Newly Derived Original Shlokas with Complete Translations"
    )
    r_s.font.name = "Georgia"
    r_s.font.size = Pt(11)
    r_s.font.italic = True
    r_s.font.bold = True
    r_s.font.color.rgb = C_NAVY

    # Metadata Table
    meta_table = doc.add_table(rows=2, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    col_widths = [Inches(1.8), Inches(2.2), Inches(1.5), Inches(1.5)]
    for row in meta_table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = w

    meta_data = [
        [("Primary Author / Idea:", True), ("Shri Shripad Kulkarni", False), ("Date:", True), ("November 07, 2026", False)],
        [("Technology Partner:", True), ("Hiranyam AI Labs (https://hiranyamai.com/)", False), ("Document Format:", True), ("3 Core Elements Only", False)],
    ]
    for r_idx, row in enumerate(meta_data):
        for c_idx, (text, is_bold) in enumerate(row):
            cell = meta_table.cell(r_idx, c_idx)
            set_cell_margins(cell, top=45, bottom=45, left=70, right=70)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(text)
            run.font.name = "Arial"
            run.font.size = Pt(8.5)
            run.font.bold = is_bold
            if is_bold:
                run.font.color.rgb = C_MAROON
                set_cell_background(cell, "F5ECE1")
            else:
                run.font.color.rgb = C_SLATE
                set_cell_background(cell, "FCF9F5")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # DATA DEFINITION: ALL 5 NEWLY DERIVED ORIGINAL SUTRAS
    # Strictly matching pair + new shloka + translations of each
    # --------------------------------------------------------------------------
    sutras_data = [
        # ----------------------------------------------------------------------
        # SUTRA 1: ANTIFRAGILITY
        # ----------------------------------------------------------------------
        {
            "id": 1,
            "theme": "आघातजन्य-प्रतिभा व विपत्ति-रूपांतरण (Antifragility & Adversarial Transformation)",
            "n_ref": "Narada Bhakti Sutra 78 (NBS 78)",
            "n_sanskrit": "अहिंसासत्यशौचदयास्तिक्यादिचारित्र्याणि परिपालनीयानि ॥",
            "n_trans_en": "Virtues such as non-violence, truth, purity, compassion, and faith must be rigorously practiced and preserved.",
            "n_trans_mr": "अहिंसा, सत्य, पावित्र्य, दया आणि आस्तिकता या मूल्यांचे निष्ठेने पालन करावे.",
            
            "s_ref": "Shandilya Bhakti Sutra 61 (SBS 61)",
            "s_sanskrit": "तदैक्यान्नानात्वम् ॥",
            "s_trans_en": "Through unified alignment with the core truth, all external diversity and multiplicity resolve into singular strength.",
            "s_trans_mr": "त्या एका परमतत्त्वाशी एकरूपता असल्यामुळे सर्व बाह्य विविधतेचे पर्यवसान एकात्मिक सामर्थ्यात होते.",
            
            "new_title": "New Udyam Sutra 1",
            "new_sanskrit": "आघातोत्पीडितः प्राज्ञो दीप्यते न तु सीदति ।\nविपद्भवति सामर्थ्यं यस्योद्योगः स्वभावजः ॥",
            "new_trans_en": "Buffeted by external shocks and hostility, the wise leader blazes forth and never collapses; adversity itself transforms into enduring capability for one whose enterprise is born of innate purpose.",
            "new_trans_mr": "संकटांच्या आघाताने सुजाण उद्योजक खचून न जाता अधिक उजळून निघतो; ज्याचा उद्योग त्याच्या मूळ स्वभावातून आणि ध्येयातून जन्मला आहे, त्याच्यासाठी संकट हेच सामर्थ्य बनते."
        },
        # ----------------------------------------------------------------------
        # SUTRA 2: EPISTEMIC SOVEREIGNTY
        # ----------------------------------------------------------------------
        {
            "id": 2,
            "theme": "प्रज्ञा-स्वायत्तता व स्वदेशी नवोन्मेष (Epistemic Sovereignty & Foundational IP)",
            "n_ref": "Narada Bhakti Sutra 10 (NBS 10)",
            "n_sanskrit": "अन्याश्रयाणां त्यागोऽनन्यता ॥",
            "n_trans_en": "Single-minded dedication consists of renouncing all external reliance and borrowed crutches.",
            "n_trans_mr": "इतर सर्व बाह्य आधारांचा व उसन्या परावलंबित्वाचा त्याग करणे हीच खरी अनन्यता होय.",
            
            "s_ref": "Shandilya Bhakti Sutra 8 (SBS 8)",
            "s_sanskrit": "तद्वतः प्रपत्तिरन्यथा पातित्यात् ॥",
            "s_trans_en": "Total commitment must be anchored in authentic self-truth; relying on an alien foundation leads to downfall.",
            "s_trans_mr": "केवळ त्या स्वयंसिद्ध सत्यालाच शरण जावे; उसन्या आधारांवर विसंबल्यास पतन निश्चित असते.",
            
            "new_title": "New Udyam Sutra 2",
            "new_sanskrit": "परप्रज्ञोपजीवेन न स्वराज्यं प्रसिद्ध्यति ।\nस्वात्ममूल्यान्वेषणेन विश्वं जयति बुद्धिमान् ॥",
            "new_trans_en": "True sovereignty is never achieved by living on borrowed intellect and derivative frameworks; by originating foundational value from one's own core genius, the wise creator commands the world.",
            "new_trans_mr": "दुसऱ्यांच्या उसन्या बुद्धीवर किंवा परकीय तंत्रज्ञानावर जगून स्वावलंबन किंवा स्वराज्य साध्य होत नाही; स्वतःच्या मूळ मूल्यांचा आणि क्षमतेचा शोध घेऊनच बुद्धिमान उद्योजक जग जिंकतो."
        },
        # ----------------------------------------------------------------------
        # SUTRA 3: GENERATIONAL SUCCESSION
        # ----------------------------------------------------------------------
        {
            "id": 3,
            "theme": "ज्ञानसंक्रमण व संस्थागत सातत्य (Inter-generational Knowledge Transmission & Lineage)",
            "n_ref": "Narada Bhakti Sutra 38 (NBS 38)",
            "n_sanskrit": "महत्सङ्गस्तु दुर्लभोऽगम्योऽमोघश्च ॥",
            "n_trans_en": "The association and guidance of great masters is rare, unfathomable, and unerring in its transformative power.",
            "n_trans_mr": "महान विभूतींचा सहवास आणि मार्गदर्शन अत्यंत दुर्लभ, अगम्य आणि निश्चित फलदायी असते.",
            
            "s_ref": "Shandilya Bhakti Sutra 91 (SBS 91)",
            "s_sanskrit": "परम्परातो ज्ञानसंसिद्धिः ॥",
            "s_trans_en": "The perfection of knowledge is fulfilled and preserved exclusively through unbroken lineage and discipleship.",
            "s_trans_mr": "ज्ञानाची परिपूर्णता केवळ अखंड गुरु-शिष्य परंपरेतून आणि संस्कारातूनच साध्य होते.",
            
            "new_title": "New Udyam Sutra 3",
            "new_sanskrit": "न केवलं धनं स्थाप्यं स्थापनीया परम्परा ।\nयोग्यशिष्ये समर्पितं कार्यं तिष्ठति शाश्वतम् ॥",
            "new_trans_en": "A leader must not merely leave behind monetary wealth; one must establish an enduring lineage of wisdom and values. An enterprise entrusted to a worthy successor endures eternally.",
            "new_trans_mr": "केवळ संपत्ती किंवा पैसा मागे सोडून जाणे पुरेसे नाही, तर मूल्यांची परंपरा निर्माण केली पाहिजे; योग्य शिष्याकडे सोपवलेले कार्यच युगायुगे शाश्वत टिकून राहते."
        },
        # ----------------------------------------------------------------------
        # SUTRA 4: ECOLOGICAL SYMBIOSIS
        # ----------------------------------------------------------------------
        {
            "id": 4,
            "theme": "प्राकृतिक दोहन व संवासरूप उद्यम (Regenerative Ecological Symbiosis & Stewardship)",
            "n_ref": "Narada Bhakti Sutra 67 (NBS 67)",
            "n_sanskrit": "तन्मया हि ते ॥",
            "n_trans_en": "For the dedicated seers become deeply permeated with reverential love across all creation.",
            "n_trans_mr": "कारण ते सर्व चराचर सृष्टीशी आणि निसर्गाशी तन्मय आणि एकरूप झालेले असतात.",
            
            "s_ref": "Shandilya Bhakti Sutra 96 (SBS 96)",
            "s_sanskrit": "प्राणेषु सर्वभूतानां समत्वम् ॥",
            "s_trans_en": "Equity and reverential balance must extend across the life-breath of all living entities.",
            "s_trans_mr": "सर्व सजीवांच्या प्राणांविषयी आणि अस्तित्वाविषयी समभाव व आदर असणे आवश्यक आहे.",
            
            "new_title": "New Udyam Sutra 4",
            "new_sanskrit": "दोहनेन यथा धेनुः पालिता न तु हिंसिता ।\nतथैव प्रकृतेर्भोगाद् उद्योगः फलवान् भवेत् ॥",
            "new_trans_en": "Just as a cow is lovingly nurtured and gently milked—never harmed or destroyed—so must an enterprise utilize nature’s resources through regeneration, thereby yielding enduring fruit.",
            "new_trans_mr": "ज्याप्रमाणे गाईचे पोषण करून, तिच्यावर प्रेम करून तिचे दोहन केले जाते आणि तिला कधीही मारले जात नाही; त्याचप्रमाणे निसर्गाचे पुनरुज्जीवन करत चालवलेला उद्योगच शाश्वत फलदायी ठरतो."
        },
        # ----------------------------------------------------------------------
        # SUTRA 5: TANGIBLE UTILITY OVER SPECULATION
        # ----------------------------------------------------------------------
        {
            "id": 5,
            "theme": "वास्तविक मूल्यनिर्मिती व आभासी अर्थत्याग (Tangible Utility & Wealth Creation Over Speculation)",
            "n_ref": "Narada Bhakti Sutra 7 (NBS 7)",
            "n_sanskrit": "सा न कामयमाना निरोधरूपत्वात् ॥",
            "n_trans_en": "Devotion is not of the nature of selfish, illusory desire, because it is of the nature of restraint from falsehood.",
            "n_trans_mr": "ती भक्ती स्वार्थी कामनेची नसते, कारण ती असत्याचा आणि मोहाचा निरोध करणारी असते.",
            
            "s_ref": "Shandilya Bhakti Sutra 6 (SBS 6)",
            "s_sanskrit": "न क्रिया परप्रयोजनाभावात् ॥",
            "s_trans_en": "It is not a mere empty mechanical ritual, because it is anchored in genuine, unselfish purpose.",
            "s_trans_mr": "केवळ पोकळ बाह्य दिखावा म्हणजे भक्ती नव्हे, तर तिला निःस्वार्थ लोककल्याणाचे ठोस प्रयोजन असते.",
            
            "new_title": "New Udyam Sutra 5",
            "new_sanskrit": "आभासिकं त्यजेल्लोभं वस्तुसत्यं विचिन्तयेत् ।\nलोकस्य दुःखहारित्वाद् उद्योगो महते श्रिये ॥",
            "new_trans_en": "Let an entrepreneur renounce the illusory greed of paper speculation and concentrate upon real, tangible utility; an enterprise that alleviates the genuine suffering of the people attains monumental glory.",
            "new_trans_mr": "कागदी नफ्याचा आणि आभासी मूल्यांकनाचा लोभ सोडून प्रत्यक्ष उपयुक्त वस्तूचे निर्माण करावे; लोकांचे दुःख आणि दैन्य दूर करणारा उद्योगच खऱ्या आणि चिरंतन वैभवाला प्राप्त होतो."
        }
    ]

    for item in sutras_data:
        s_id = item["id"]

        # Unit Header Banner
        p_hdr = doc.add_paragraph()
        p_hdr.paragraph_format.space_before = Pt(14)
        p_hdr.paragraph_format.space_after = Pt(3)
        r_uh = p_hdr.add_run(f"UDYAM SUTRA {s_id}: {item['theme']}")
        r_uh.font.name = "Arial"
        r_uh.font.size = Pt(12)
        r_uh.font.bold = True
        r_uh.font.color.rgb = C_MAROON

        # ----------------------------------------------------------------------
        # COMPONENT 1: MATCHING PAIRS (Original Shlokas & Their Translations)
        # ----------------------------------------------------------------------
        p_lbl1 = doc.add_paragraph()
        p_lbl1.paragraph_format.space_after = Pt(2)
        r_l1 = p_lbl1.add_run("1. Matching Source Pair (Original Shlokas & Translations):")
        r_l1.font.name = "Arial"
        r_l1.font.size = Pt(10)
        r_l1.font.bold = True
        r_l1.font.color.rgb = C_NAVY

        tbl_pair = doc.add_table(rows=1, cols=2)
        tbl_pair.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_pair.autofit = False
        tbl_pair.columns[0].width = Inches(3.5)
        tbl_pair.columns[1].width = Inches(3.5)

        # Left Column: Narada Sutra
        c_n = tbl_pair.cell(0, 0)
        set_cell_margins(c_n, top=80, bottom=80, left=100, right=100)
        set_cell_background(c_n, "FBF6F0")

        p_n_skt = c_n.paragraphs[0]
        p_n_skt.paragraph_format.space_after = Pt(2)
        r_n_ref = p_n_skt.add_run(f"{item['n_ref']}\n")
        r_n_ref.font.name = "Arial"
        r_n_ref.font.size = Pt(9.5)
        r_n_ref.font.bold = True
        r_n_ref.font.color.rgb = C_MAROON

        r_n_verse = p_n_skt.add_run(f"{item['n_sanskrit']}\n")
        r_n_verse.font.name = "Arial"
        r_n_verse.font.size = Pt(11)
        r_n_verse.font.bold = True
        r_n_verse.font.color.rgb = C_MAROON

        p_n_tr = c_n.add_paragraph()
        p_n_tr.paragraph_format.space_after = Pt(0)
        p_n_tr.paragraph_format.line_spacing = 1.15

        r_ne_lbl = p_n_tr.add_run("English: ")
        r_ne_lbl.font.name = "Georgia"
        r_ne_lbl.font.size = Pt(8.5)
        r_ne_lbl.font.bold = True
        r_ne_lbl.font.color.rgb = C_NAVY
        r_ne_txt = p_n_tr.add_run(f"{item['n_trans_en']}\n")
        r_ne_txt.font.name = "Georgia"
        r_ne_txt.font.size = Pt(8.5)
        r_ne_txt.font.color.rgb = C_SLATE

        r_nm_lbl = p_n_tr.add_run("मराठी: ")
        r_nm_lbl.font.name = "Arial"
        r_nm_lbl.font.size = Pt(8.5)
        r_nm_lbl.font.bold = True
        r_nm_lbl.font.color.rgb = C_MAROON
        r_nm_txt = p_n_tr.add_run(f"{item['n_trans_mr']}")
        r_nm_txt.font.name = "Arial"
        r_nm_txt.font.size = Pt(8.5)
        r_nm_txt.font.color.rgb = C_SLATE

        # Right Column: Shandilya Sutra
        c_s = tbl_pair.cell(0, 1)
        set_cell_margins(c_s, top=80, bottom=80, left=100, right=100)
        set_cell_background(c_s, "F0F4F8")

        p_s_skt = c_s.paragraphs[0]
        p_s_skt.paragraph_format.space_after = Pt(2)
        r_s_ref = p_s_skt.add_run(f"{item['s_ref']}\n")
        r_s_ref.font.name = "Arial"
        r_s_ref.font.size = Pt(9.5)
        r_s_ref.font.bold = True
        r_s_ref.font.color.rgb = C_NAVY

        r_s_verse = p_s_skt.add_run(f"{item['s_sanskrit']}\n")
        r_s_verse.font.name = "Arial"
        r_s_verse.font.size = Pt(11)
        r_s_verse.font.bold = True
        r_s_verse.font.color.rgb = C_NAVY

        p_s_tr = c_s.add_paragraph()
        p_s_tr.paragraph_format.space_after = Pt(0)
        p_s_tr.paragraph_format.line_spacing = 1.15

        r_se_lbl = p_s_tr.add_run("English: ")
        r_se_lbl.font.name = "Georgia"
        r_se_lbl.font.size = Pt(8.5)
        r_se_lbl.font.bold = True
        r_se_lbl.font.color.rgb = C_NAVY
        r_se_txt = p_s_tr.add_run(f"{item['s_trans_en']}\n")
        r_se_txt.font.name = "Georgia"
        r_se_txt.font.size = Pt(8.5)
        r_se_txt.font.color.rgb = C_SLATE

        r_sm_lbl = p_s_tr.add_run("मराठी: ")
        r_sm_lbl.font.name = "Arial"
        r_sm_lbl.font.size = Pt(8.5)
        r_sm_lbl.font.bold = True
        r_sm_lbl.font.color.rgb = C_MAROON
        r_sm_txt = p_s_tr.add_run(f"{item['s_trans_mr']}")
        r_sm_txt.font.name = "Arial"
        r_sm_txt.font.size = Pt(8.5)
        r_sm_txt.font.color.rgb = C_SLATE

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

        # ----------------------------------------------------------------------
        # COMPONENTS 2 & 3: NEW SHLOKA & ITS TRANSLATIONS
        # ----------------------------------------------------------------------
        p_lbl2 = doc.add_paragraph()
        p_lbl2.paragraph_format.space_after = Pt(2)
        r_l2 = p_lbl2.add_run("2 & 3. Newly Formed Sanskrit Shloka & Its Translations:")
        r_l2.font.name = "Arial"
        r_l2.font.size = Pt(10)
        r_l2.font.bold = True
        r_l2.font.color.rgb = C_NAVY

        tbl_new = doc.add_table(rows=1, cols=1)
        tbl_new.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_new.autofit = False
        tbl_new.columns[0].width = Inches(7.0)

        c_new = tbl_new.cell(0, 0)
        set_cell_margins(c_new, top=100, bottom=100, left=140, right=140)
        set_cell_background(c_new, "FFFDF9")

        tcPr = c_new._element.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="E0D4C3"/>'
            f'<w:left w:val="single" w:sz="28" w:space="0" w:color="8B0000"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="E0D4C3"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="E0D4C3"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        # 2. Sanskrit Verse (Centred & Large)
        p_skt = c_new.paragraphs[0]
        p_skt.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_skt.paragraph_format.space_after = Pt(6)
        for line in item["new_sanskrit"].split("\n"):
            r_line = p_skt.add_run(line + "\n")
            r_line.font.name = "Arial"
            r_line.font.size = Pt(12.5)
            r_line.font.bold = True
            r_line.font.color.rgb = C_MAROON

        # 3. Translations of the New Shloka
        p_tr = c_new.add_paragraph()
        p_tr.paragraph_format.space_after = Pt(0)
        p_tr.paragraph_format.line_spacing = 1.15

        r_te_lbl = p_tr.add_run("English Translation: ")
        r_te_lbl.font.name = "Arial"
        r_te_lbl.font.size = Pt(9)
        r_te_lbl.font.bold = True
        r_te_lbl.font.color.rgb = C_NAVY
        r_te_txt = p_tr.add_run(f"{item['new_trans_en']}\n")
        r_te_txt.font.name = "Georgia"
        r_te_txt.font.size = Pt(9)
        r_te_txt.font.color.rgb = C_SLATE

        r_tm_lbl = p_tr.add_run("मराठी भाषांतर: ")
        r_tm_lbl.font.name = "Arial"
        r_tm_lbl.font.size = Pt(9)
        r_tm_lbl.font.bold = True
        r_tm_lbl.font.color.rgb = C_MAROON
        r_tm_txt = p_tr.add_run(f"{item['new_trans_mr']}")
        r_tm_txt.font.name = "Arial"
        r_tm_txt.font.size = Pt(9)
        r_tm_txt.font.color.rgb = C_SLATE

        # Separation
        if s_id < 5:
            doc.add_paragraph().paragraph_format.space_after = Pt(6)
        else:
            doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # Save & Copy to Artifact
    # --------------------------------------------------------------------------
    doc.save(str(OUTPUT_FILE))
    print(f"[+] Successfully generated Word file at: {OUTPUT_FILE.resolve()}")

    try:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(OUTPUT_FILE), str(ARTIFACT_FILE))
        print(f"[+] Successfully copied Word file to Artifact Directory: {ARTIFACT_FILE.resolve()}")
    except Exception as e:
        print(f"[!] Warning: Could not copy to artifact directory: {e}")

    return OUTPUT_FILE


if __name__ == "__main__":
    build_concise_word_document()
