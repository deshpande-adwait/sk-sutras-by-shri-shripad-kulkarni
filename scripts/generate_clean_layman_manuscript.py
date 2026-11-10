"""
================================================================================
Script: scripts/generate_clean_layman_manuscript.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates the clean, authoritative, layman-friendly Word manuscript
             for the 10 Canonical Udyog Sutras with ZERO technical jargon.
             Retains all Sanskrit verses, translations, explanations, case studies,
             yoga resilience, and actionable enterprise guidance.
================================================================================
"""

import os
import shutil
import sys
from datetime import datetime
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
sys.path.insert(0, str(BASE_DIR))

from scripts.ten_new_sutras_canonical_data import TEN_NEW_UDYOG_SUTRAS_CANON

DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DOCS_DIR / "UDYOG_SUTRAS_TEN_NEW_CANONICAL_MATCHING_AND_SHLOKAS.docx"

ARTIFACT_DIR = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_FILE = ARTIFACT_DIR / "UDYOG_SUTRAS_TEN_NEW_CANONICAL_MATCHING_AND_SHLOKAS.docx"

MANDATORY_FOOTER = "Proprietory and Confidential- Hiranyam AI Labs"

# Color Palette: Classical Academic Corporate
C_MAROON = RGBColor(139, 0, 0)       # #8B0000 Primary Sacred Accent
C_NAVY = RGBColor(18, 52, 86)        # #123456 Secondary Deep Blue
C_SLATE = RGBColor(40, 45, 55)       # #282D37 Body Text
C_GOLD = RGBColor(180, 115, 20)      # Highlighting Accent
C_GREEN = RGBColor(24, 134, 75)      # Natural Accent


def set_cell_background(cell, hex_color: str):
    """Sets background shading of a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
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


def _to_str(val):
    if isinstance(val, dict):
        return "; ".join(f"{k} = {v}" for k, v in val.items())
    elif isinstance(val, list):
        return ", ".join(str(x) for x in val)
    return str(val) if val is not None else ""


def build_clean_layman_document():
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

    # ==================== COVER / TITLE HEADER ====================
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(2)
    r_t1 = title_p.add_run("॥ श्रीमद् उद्योग सूत्राणि ॥\n")
    r_t1.font.name = "Georgia"
    r_t1.font.size = Pt(22)
    r_t1.font.bold = True
    r_t1.font.color.rgb = C_MAROON

    r_t2 = title_p.add_run("SHRIMAD UDYOG SUTRAS – TEN CANONICAL SUTRAS\n")
    r_t2.font.name = "Arial"
    r_t2.font.size = Pt(13)
    r_t2.font.bold = True
    r_t2.font.color.rgb = C_NAVY

    r_t3 = title_p.add_run("दस प्रामाणिक उद्योग सूत्रे : मूळ संदर्भ, सुलभ निरूपण व दैनंदिन आचरण\n")
    r_t3.font.name = "Georgia"
    r_t3.font.size = Pt(11)
    r_t3.font.italic = True
    r_t3.font.color.rgb = C_SLATE

    # Metadata Banner (Clean, Professional, Zero Technical Jargon)
    meta_tbl = doc.add_table(rows=1, cols=1)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_cell = meta_tbl.cell(0, 0)
    set_cell_background(meta_cell, "FBF9F5")
    set_cell_margins(meta_cell, top=100, bottom=100, left=160, right=160)
    m_p = meta_cell.paragraphs[0]
    m_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    m_run = m_p.add_run(
        f"ग्रंथकार (Author): श्री श्रीपाद कुलकर्णी (Shri Shripad Kulkarni)\n"
        f"मार्गदर्शक तत्त्व: 'सूत्र लहान, विचार महान, निरूपण सुटसुटीत, संक्षिप्त आणि आचरण व्यावहारिक'\n"
        f"सद्ग्रंथ प्रेरणा: नारद भक्ती सूत्रे, शांडिल्य भक्ती सूत्रे, भगवद्गीता, कौटिलीय अर्थशास्त्र, "
        f"संत तुकाराम महाराज अभंगगाथा, समर्थ रामदास दासबोध, ईशावास्योपनिषद, पतंजली योगसूत्रे आणि भर्तृहरी नीतिशतक\n"
        f"प्रकाशन: २०२६ | Powered by Hiranyam AI Labs (https://hiranyamai.com/)"
    )
    m_run.font.name = "Arial"
    m_run.font.size = Pt(9)
    m_run.font.color.rgb = C_SLATE

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==================== TEN CANONICAL SUTRAS ====================
    for item in TEN_NEW_UDYOG_SUTRAS_CANON:
        s_idx = item["sutra_no"]
        theme = item["theme"]
        mp = item["matching_pair"]
        bjf = item["bharatiya_jnana_foundation"]
        nus = item["new_udyog_sutra"]

        # Section Header Banner
        h_tbl = doc.add_table(rows=1, cols=1)
        h_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        h_cell = h_tbl.cell(0, 0)
        set_cell_background(h_cell, "123456")
        set_cell_margins(h_cell, top=80, bottom=80, left=140, right=140)
        h_p = h_cell.paragraphs[0]
        h_p.paragraph_format.space_after = Pt(0)
        hrun = h_p.add_run(f"उद्योग सूत्र {s_idx:02d} : {theme}")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(11)
        hrun.font.bold = True
        hrun.font.color.rgb = RGBColor(255, 255, 255)

        # ---------------- 1. MATCHING PAIRS ----------------
        m_title = doc.add_paragraph()
        m_title.paragraph_format.space_before = Pt(8)
        m_title.paragraph_format.space_after = Pt(2)
        r_mt = m_title.add_run("१. मूळ आधार आणि संदर्भ श्लोक (Foundational Source Verses)")
        r_mt.font.name = "Arial"
        r_mt.font.size = Pt(10)
        r_mt.font.bold = True
        r_mt.font.color.rgb = C_MAROON

        p_tbl = doc.add_table(rows=2, cols=2)
        p_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Column Widths
        for row in p_tbl.rows:
            row.cells[0].width = Inches(3.5)
            row.cells[1].width = Inches(3.5)

        # Narada Column
        c_n_hdr = p_tbl.cell(0, 0)
        set_cell_background(c_n_hdr, "8B0000")
        set_cell_margins(c_n_hdr, top=50, bottom=50, left=90, right=90)
        p1 = c_n_hdr.paragraphs[0]
        r1 = p1.add_run(f"नारद भक्ती सूत्र {mp['narada']['sutra_no']} (Narada Bhakti Sutra #{mp['narada']['sutra_no']})")
        r1.font.name = "Arial"
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(255, 255, 255)

        c_n_body = p_tbl.cell(1, 0)
        set_cell_background(c_n_body, "FBF9F5")
        set_cell_margins(c_n_body, top=60, bottom=60, left=90, right=90)
        p_nb = c_n_body.paragraphs[0]
        r_ns = p_nb.add_run(f"{mp['narada']['sanskrit']}\n\n")
        r_ns.font.name = "Georgia"
        r_ns.font.size = Pt(11)
        r_ns.font.bold = True
        r_ns.font.color.rgb = C_MAROON

        r_ne = p_nb.add_run(f"English: {mp['narada']['meaning_en']}\n\n")
        r_ne.font.name = "Arial"
        r_ne.font.size = Pt(8.5)
        r_ne.font.color.rgb = C_SLATE

        r_nm = p_nb.add_run(f"मराठी अर्थ: {mp['narada']['meaning_mr']}")
        r_nm.font.name = "Georgia"
        r_nm.font.size = Pt(8.5)
        r_nm.font.color.rgb = C_SLATE

        # Shandilya Column
        c_s_hdr = p_tbl.cell(0, 1)
        set_cell_background(c_s_hdr, "123456")
        set_cell_margins(c_s_hdr, top=50, bottom=50, left=90, right=90)
        p2 = c_s_hdr.paragraphs[0]
        r2 = p2.add_run(f"शांडिल्य भक्ती सूत्र {mp['shandilya']['sutra_no']} (Shandilya Bhakti Sutra #{mp['shandilya']['sutra_no']})")
        r2.font.name = "Arial"
        r2.font.size = Pt(9)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(255, 255, 255)

        c_s_body = p_tbl.cell(1, 1)
        set_cell_background(c_s_body, "FBF9F5")
        set_cell_margins(c_s_body, top=60, bottom=60, left=90, right=90)
        p_sb = c_s_body.paragraphs[0]
        r_ss = p_sb.add_run(f"{mp['shandilya']['sanskrit']}\n\n")
        r_ss.font.name = "Georgia"
        r_ss.font.size = Pt(11)
        r_ss.font.bold = True
        r_ss.font.color.rgb = C_NAVY

        r_se = p_sb.add_run(f"English: {mp['shandilya']['meaning_en']}\n\n")
        r_se.font.name = "Arial"
        r_se.font.size = Pt(8.5)
        r_se.font.color.rgb = C_SLATE

        r_sm = p_sb.add_run(f"मराठी अर्थ: {mp['shandilya']['meaning_mr']}")
        r_sm.font.name = "Georgia"
        r_sm.font.size = Pt(8.5)
        r_sm.font.color.rgb = C_SLATE

        # Thematic Harmony Note (Clean, Layman Terms)
        p_harm = doc.add_paragraph()
        p_harm.paragraph_format.space_before = Pt(4)
        p_harm.paragraph_format.space_after = Pt(4)
        r_hl = p_harm.add_run("दोन्ही संदर्भांचा सुंदर समन्वय (Harmonious Core Insight): ")
        r_hl.font.name = "Arial"
        r_hl.font.size = Pt(8.5)
        r_hl.font.bold = True
        r_hl.font.color.rgb = C_GOLD
        r_ht = p_harm.add_run(mp["thematic_harmony"])
        r_ht.font.name = "Georgia"
        r_ht.font.size = Pt(8.5)
        r_ht.font.color.rgb = C_SLATE

        # Bharatiya Knowledge Base Foundations (Layman Headings)
        f_tbl = doc.add_table(rows=1, cols=1)
        f_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        f_cell = f_tbl.cell(0, 0)
        set_cell_background(f_cell, "F5F2EB")
        set_cell_margins(f_cell, top=50, bottom=50, left=100, right=100)
        fp = f_cell.paragraphs[0]
        fp.paragraph_format.space_after = Pt(0)
        fr1 = fp.add_run("भारतीय ज्ञान परंपरा व सद्ग्रंथ विचार (Bharatiya Wisdom Foundations):\n")
        fr1.font.name = "Arial"
        fr1.font.size = Pt(8.5)
        fr1.font.bold = True
        fr1.font.color.rgb = C_NAVY

        fr2 = fp.add_run(
            f"• {bjf['doc01_mahadgrantha']}\n"
            f"• {bjf['doc02_karyavritti17']}\n"
            f"• {bjf['doc03_karyavritti05']}\n"
            f"• {bjf['doc04_sant_tukaram']}\n"
            f"• प्राचीन सद्ग्रंथ संदर्भ: {bjf['iks_scriptural_references']}"
        )
        fr2.font.name = "Georgia"
        fr2.font.size = Pt(8)
        fr2.font.color.rgb = C_SLATE

        # ---------------- 2. NEWLY DERIVED SUTRA ----------------
        s_title = doc.add_paragraph()
        s_title.paragraph_format.space_before = Pt(8)
        s_title.paragraph_format.space_after = Pt(2)
        r_st = s_title.add_run("२. नवीन उद्योग सूत्र (New Enterprise Aphorism — सूत्र लहान, विचार महान)")
        r_st.font.name = "Arial"
        r_st.font.size = Pt(10)
        r_st.font.bold = True
        r_st.font.color.rgb = C_MAROON

        # Shloka / Sutra Box
        sh_tbl = doc.add_table(rows=1, cols=1)
        sh_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        sh_cell = sh_tbl.cell(0, 0)
        set_cell_background(sh_cell, "FFFBF0")
        set_cell_margins(sh_cell, top=90, bottom=90, left=120, right=120)
        shp = sh_cell.paragraphs[0]
        shp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        shp.paragraph_format.space_after = Pt(0)
        sutra_verse_clean = nus['sanskrit_verse'].strip()
        shr1 = shp.add_run(f"॥ उद्योगसूत्रम् {s_idx:02d} ॥\n")
        shr1.font.name = "Georgia"
        shr1.font.size = Pt(11)
        shr1.font.bold = True
        shr1.font.color.rgb = C_GOLD
        shr2 = shp.add_run(f"{sutra_verse_clean}")
        shr2.font.name = "Georgia"
        shr2.font.size = Pt(15)
        shr2.font.bold = True
        shr2.font.color.rgb = C_MAROON

        # Padaccheda, Anvaya & Nirukta (Clean Layman Labels)
        pa_p = doc.add_paragraph()
        pa_p.paragraph_format.space_before = Pt(4)
        pa_p.paragraph_format.space_after = Pt(2)
        r_pl = pa_p.add_run("शब्द फोड (Word Breakdown / Padaccheda): ")
        r_pl.font.name = "Arial"
        r_pl.font.size = Pt(8.5)
        r_pl.font.bold = True
        r_pl.font.color.rgb = C_NAVY
        r_pv = pa_p.add_run(f"{nus['padaccheda']}\n")
        r_pv.font.name = "Georgia"
        r_pv.font.size = Pt(9)
        r_pv.font.color.rgb = C_SLATE

        r_al = pa_p.add_run("सोपा सरळ क्रम (Simple Prose Order / Anvaya): ")
        r_al.font.name = "Arial"
        r_al.font.size = Pt(8.5)
        r_al.font.bold = True
        r_al.font.color.rgb = C_NAVY
        r_av = pa_p.add_run(f"{nus['anvaya']}\n")
        r_av.font.name = "Georgia"
        r_av.font.size = Pt(9)
        r_av.font.color.rgb = C_SLATE

        r_nl = pa_p.add_run("शब्दांचे अर्थ (Word Meanings / Nirukta): ")
        r_nl.font.name = "Arial"
        r_nl.font.size = Pt(8.5)
        r_nl.font.bold = True
        r_nl.font.color.rgb = C_NAVY
        r_nv = pa_p.add_run(_to_str(nus.get("nirukta")))
        r_nv.font.name = "Georgia"
        r_nv.font.size = Pt(8.5)
        r_nv.font.color.rgb = C_SLATE

        # ---------------- 3. CONCISE EXPOSITION, CASE STUDIES & PRACTICAL GUIDANCE ----------------
        e_title = doc.add_paragraph()
        e_title.paragraph_format.space_before = Pt(8)
        e_title.paragraph_format.space_after = Pt(2)
        r_et = e_title.add_run("३. सोपे निरूपण, सत्य कथा व दैनंदिन आचरण (Simple Explanation, Real-Life Examples & Practical Action)")
        r_et.font.name = "Arial"
        r_et.font.size = Pt(10)
        r_et.font.bold = True
        r_et.font.color.rgb = C_MAROON

        t_tbl = doc.add_table(rows=5, cols=1)
        t_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Row 0: English & Marathi Translation
        c_en = t_tbl.cell(0, 0)
        set_cell_background(c_en, "FBF9F5")
        set_cell_margins(c_en, top=50, bottom=50, left=90, right=90)
        p_en = c_en.paragraphs[0]
        p_en.paragraph_format.space_after = Pt(0)
        r_enh = p_en.add_run("सरळ अर्थ (Clear Translation & Meaning):\n")
        r_enh.font.name = "Arial"
        r_enh.font.size = Pt(8.5)
        r_enh.font.bold = True
        r_enh.font.color.rgb = C_NAVY
        r_ent = p_en.add_run(f"• English: {_to_str(nus.get('translation_en'))}\n• मराठी: {_to_str(nus.get('translation_mr'))}")
        r_ent.font.name = "Georgia"
        r_ent.font.size = Pt(8.5)
        r_ent.font.color.rgb = C_SLATE

        # Row 1: Crisp Marathi Bhashya (Short & Focused)
        c_mr = t_tbl.cell(1, 0)
        set_cell_background(c_mr, "FFFFFF")
        set_cell_margins(c_mr, top=60, bottom=60, left=90, right=90)
        p_mr = c_mr.paragraphs[0]
        p_mr.paragraph_format.space_after = Pt(0)
        r_mrh = p_mr.add_run("सुटसुटीत निरूपण (Crisp & Clear Explanation — सूत्र लहान, विचार महान):\n")
        r_mrh.font.name = "Georgia"
        r_mrh.font.size = Pt(9.5)
        r_mrh.font.bold = True
        r_mrh.font.color.rgb = C_MAROON
        bhashya_text = nus.get("comprehensive_bhashya_mr") or nus.get("translation_mr", "")
        r_mrt = p_mr.add_run(bhashya_text)
        r_mrt.font.name = "Georgia"
        r_mrt.font.size = Pt(9)
        r_mrt.font.color.rgb = C_SLATE

        # Row 2: Biographical Case Studies (Eastern & Western)
        c_cs = t_tbl.cell(2, 0)
        set_cell_background(c_cs, "F5F7FA")
        set_cell_margins(c_cs, top=50, bottom=50, left=90, right=90)
        p_cs = c_cs.paragraphs[0]
        p_cs.paragraph_format.space_after = Pt(0)
        r_csh = p_cs.add_run("प्रेरणादायी सत्य कथा (Inspiring Real-Life Case Studies):\n")
        r_csh.font.name = "Arial"
        r_csh.font.size = Pt(8.5)
        r_csh.font.bold = True
        r_csh.font.color.rgb = C_NAVY
        case_studies = nus.get("biographical_case_studies", [])
        if isinstance(case_studies, list) and case_studies:
            for cs in case_studies:
                if isinstance(cs, dict):
                    p_cs.add_run(f"• {cs.get('name')} [{cs.get('category')}]: {cs.get('case_summary')}\n")
                else:
                    p_cs.add_run(f"• {cs}\n")
        else:
            p_cs.add_run("• जमशेदजी टाटा (स्वदेशी राष्ट्रउभारणी) व थॉमस एडिसन (तर्कशुद्ध प्रयोगशीलता व समर्पण)\n")

        # Row 3: Founder Psychology & Mental Resilience via Patanjali Yoga Sutras
        c_yg = t_tbl.cell(3, 0)
        set_cell_background(c_yg, "FBF9F5")
        set_cell_margins(c_yg, top=50, bottom=50, left=90, right=90)
        p_yg = c_yg.paragraphs[0]
        p_yg.paragraph_format.space_after = Pt(0)
        r_ygh = p_yg.add_run("मानसिक समतोल व ताणमुक्ती — पतंजली योगविचार (Mental Peace & Stress Relief):\n")
        r_ygh.font.name = "Georgia"
        r_ygh.font.size = Pt(8.5)
        r_ygh.font.bold = True
        r_ygh.font.color.rgb = C_GOLD
        yg_data = nus.get("mental_resilience_yoga_sutras", {})
        if isinstance(yg_data, dict) and yg_data:
            ref = yg_data.get("sutra_reference", "पतंजली योगसूत्र १.१२")
            v_sk = yg_data.get("sanskrit", "अभ्यासवैराग्याभ्यां तन्निरोधः")
            fw = yg_data.get("psychological_framework", "")
            p_yg.add_run(f"• सूत्र संदर्भ: {ref} — {v_sk}\n• मनाची शांतता: {fw}")
        else:
            p_yg.add_run("• अभ्यास व वैराग्याच्या द्वारे उद्योजकाने संकटातही मानसिक संतुलन राखावे.")

        # Row 4: Practical Enterprise Guidance
        c_pe = t_tbl.cell(4, 0)
        set_cell_background(c_pe, "FFFBF0")
        set_cell_margins(c_pe, top=50, bottom=50, left=90, right=90)
        p_pe = c_pe.paragraphs[0]
        p_pe.paragraph_format.space_after = Pt(0)
        r_peh = p_pe.add_run("दैनंदिन आचरणासाठी मार्गदर्शन (Actionable Steps for Daily Practice):\n")
        r_peh.font.name = "Arial"
        r_peh.font.size = Pt(8.5)
        r_peh.font.bold = True
        r_peh.font.color.rgb = C_MAROON
        pe_items = nus.get("practical_enterprise_guidance", [])
        if isinstance(pe_items, list) and pe_items:
            for item in pe_items:
                if isinstance(item, dict):
                    p_pe.add_run(f"• {item.get('role')}: {item.get('guidance')}\n")
                else:
                    p_pe.add_run(f"• {item}\n")
        else:
            p_pe.add_run(_to_str(nus.get("practical_enterprise_guidance")))

        # Dignified Publishing Separator (No AI badges or test scores)
        q_p = doc.add_paragraph()
        q_p.paragraph_format.space_before = Pt(6)
        q_p.paragraph_format.space_after = Pt(14)
        q_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        qr = q_p.add_run("॥ शुभं भवतु — उद्योगेनैव सिध्यन्ति कार्याणि ॥")
        qr.font.name = "Georgia"
        qr.font.size = Pt(8.5)
        qr.font.italic = True
        qr.font.color.rgb = C_GOLD

    # Save to Docs and Brain Artifacts
    doc.save(str(OUTPUT_FILE))
    shutil.copy2(OUTPUT_FILE, ARTIFACT_FILE)
    print(f"Successfully generated clean layman manuscript:")
    print(f"  Docs: {OUTPUT_FILE}")
    print(f"  Artifact: {ARTIFACT_FILE}")


if __name__ == "__main__":
    build_clean_layman_document()
