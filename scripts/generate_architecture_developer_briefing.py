"""
================================================================================
Script: scripts/generate_architecture_developer_briefing.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates an exhaustive, developer-ready Technical Architecture and
             Multi-Agent AI System Specification document in Word (.docx) format
             for peer architectural review and system hardening.
             Includes:
             - 5 Specialized Autonomous AI Agents & Multi-LLM Topology
             - 3 Premier Commercial Model Providers (Gemini, OpenAI, Claude)
             - Vector Store Architecture (ChromaDB 100 Shandilya & 20+ IKS Library)
             - Relational ACID Persistence & Cryptographic Execution Proofs (SQLite)
             - 13 Qualitative Verification Gates (Agent 5 Gatekeeper)
             - Complete Step-by-Step Execution Lifecycle when triggered
             - Actionable Hardening Opportunities for the Reviewing Developer
             - Mandatory Footer: "Proprietory and Confidential- Hiranyam AI Labs"
             - Clickable Hyperlink to https://hiranyamai.com/
================================================================================
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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

# Output Paths
OUTPUT_DIR = BASE_DIR / "docs" / "architecture"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FILE_NAME = "SK_Sutras_Complete_Architecture_and_Agentic_AI_Summary.docx"

TARGET_DOCS_OUTPUT = OUTPUT_DIR / FILE_NAME
DROPBOX_OUTPUT = Path(r"C:\Users\deshp\Dropbox\Hiranyam AI Labs") / FILE_NAME
ARTIFACT_OUTPUT = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc") / FILE_NAME

MANDATORY_FOOTER = "Proprietory and Confidential- Hiranyam AI Labs"

# Color Palette: Technical Architecture Publication
C_NAVY = RGBColor(18, 52, 86)        # #123456 Deep Primary Navy
C_MAROON = RGBColor(139, 0, 0)       # #8B0000 Classical Deep Accent
C_SLATE = RGBColor(40, 45, 55)       # #282D37 Charcoal Body Text
C_CHARCOAL = RGBColor(26, 32, 44)    # #1A202C High-Legibility Headings
C_GOLD = RGBColor(180, 115, 20)      # Highlighting Accent
C_GREEN = RGBColor(24, 134, 75)      # Verification / Pass Accent
C_RED = RGBColor(185, 28, 28)        # Rejection / Gate Alert Accent
C_CODE = RGBColor(30, 41, 59)        # Code snippet text


def set_cell_background(cell, hex_color: str) -> None:
    """Sets background shading of a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top: int = 80, bottom: int = 80, left: int = 120, right: int = 120) -> None:
    """Sets cell padding in dxa units (1 pt = 20 dxa)."""
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


def add_hyperlink(paragraph, url: str, text: str, color: str = "123456", underline: bool = True) -> Any:
    """Appends a clickable OpenXML hyperlink to a python-docx paragraph."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = parse_xml(
        f'<w:hyperlink {nsdecls("w")} r:id="{r_id}" '
        f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
    )
    new_run = parse_xml(f'<w:r {nsdecls("w")}/>')
    rPr = parse_xml(f'<w:rPr {nsdecls("w")}/>')

    if color:
        c = parse_xml(f'<w:color {nsdecls("w")} w:val="{color}"/>')
        rPr.append(c)
    if underline:
        u = parse_xml(f'<w:u {nsdecls("w")} w:val="single"/>')
        rPr.append(u)

    new_run.append(rPr)
    new_run_text = parse_xml(f'<w:t {nsdecls("w")} xml:space="preserve">{text}</w:t>')
    new_run.append(new_run_text)
    hyperlink.append(new_run)
    paragraph._element.append(hyperlink)
    return hyperlink


def add_section_heading(doc, text: str, level: int = 1) -> None:
    """Creates a styled section heading."""
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    if level == 1:
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = "Georgia"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = C_NAVY
    elif level == 2:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Georgia"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = C_MAROON
    elif level == 3:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = C_GOLD


def add_body_paragraph(doc, text: str, space_after: int = 5, line_spacing: float = 1.15) -> Any:
    """Adds standard body text paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    run.font.name = "Georgia"
    run.font.size = Pt(10)
    run.font.color.rgb = C_SLATE
    return p


def add_callout_box(doc, title: str, text: str, hex_bg: str = "F5F7FA", border_color: str = "123456") -> None:
    """Creates a clean shaded callout box for architectural principles or keynotes."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, hex_bg)
    set_cell_margins(cell, top=70, bottom=70, left=110, right=110)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15

    r_t = p.add_run(f"★ {title}\n")
    r_t.font.name = "Arial"
    r_t.font.size = Pt(9.5)
    r_t.font.bold = True
    r_t.font.color.rgb = C_NAVY

    r_b = p.add_run(text)
    r_b.font.name = "Georgia"
    r_b.font.size = Pt(9)
    r_b.font.color.rgb = C_SLATE


def build_architecture_briefing_document() -> Path:
    """
    Builds the comprehensive technical architecture specification document in Word format.
    """
    print("=" * 80)
    print("GENERATING ARCHITECTURE & MULTI-AGENT SPECIFICATION DOCUMENT")
    print("=" * 80)

    doc = docx.Document()

    # Set Margins (0.8 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

        # Mandatory Confidentiality Footer on every page
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.text = MANDATORY_FOOTER
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in f_p.runs:
            r.font.name = "Georgia"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(120, 120, 120)

    # ==================== TITLE PAGE / HEADER ====================
    tp = doc.add_paragraph()
    tp.paragraph_format.space_before = Pt(28)
    tp.paragraph_format.space_after = Pt(4)
    tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr1 = tp.add_run("SK SUTRAS: SYSTEM ARCHITECTURE &\nMULTI-AGENT AI SPECIFICATION\n")
    tr1.font.name = "Georgia"
    tr1.font.size = Pt(22)
    tr1.font.bold = True
    tr1.font.color.rgb = C_NAVY

    tr2 = tp.add_run("Comprehensive Technical Blueprint, Multi-LLM Orchestration Council, and Live Execution Pipeline\n")
    tr2.font.name = "Georgia"
    tr2.font.size = Pt(12)
    tr2.font.color.rgb = C_MAROON

    tr3 = tp.add_run("A Developer-to-Developer Architectural Review Briefing\n")
    tr3.font.name = "Arial"
    tr3.font.size = Pt(10)
    tr3.font.italic = True
    tr3.font.bold = True
    tr3.font.color.rgb = C_GOLD

    # Metadata & Attribution Box
    m_tbl = doc.add_table(rows=1, cols=1)
    m_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_cell = m_tbl.cell(0, 0)
    set_cell_background(m_cell, "F5F2EB")
    set_cell_margins(m_cell, top=80, bottom=80, left=120, right=120)
    mp = m_cell.paragraphs[0]
    mp.paragraph_format.line_spacing = 1.25
    mp.paragraph_format.space_after = Pt(0)

    mp.add_run("Project: SK Sutras — by Shri Shripad Kulkarni\n")
    mp.add_run("Organization: Hiranyam AI Labs (Repository: Hiranyam-AI-Labs/sk-sutras-by-shri-shripad-kulkarni)\n")
    mp.add_run("Author & Principal Inquirer: Shri Shripad Kulkarni\n")
    mp.add_run("Guiding Axiom: 'सूत्र लहान, विचार महान, निरूपण सुटसुटीत, संक्षिप्त आणि आचरण व्यावहारिक'\n")
    mp.add_run("Architecture Pattern: Dynamic Multi-Provider Shastrartha Council (5 Specialized AI Agents)\n")
    mp.add_run("AI Providers: Google Cloud (Gemini 2.5/3.8 Flash), OpenAI (GPT-4o), Anthropic (Claude 3.5 Sonnet)\n")
    mp.add_run("Vector & Relational Storage: ChromaDB (100 Shandilya Sutras & 20+ IKS Texts) + SQLite (ACID Journaling)\n")
    mp.add_run("Engineering Contact & Web Portal: ")
    add_hyperlink(mp, "https://hiranyamai.com/", "Powered by Hiranyam AI Labs", color="123456", underline=True)

    doc.add_page_break()

    # ==================== TABLE OF CONTENTS ====================
    toc_p = doc.add_paragraph()
    toc_p.paragraph_format.space_before = Pt(6)
    toc_p.paragraph_format.space_after = Pt(6)
    t_run = toc_p.add_run("Document Overview & Contents")
    t_run.font.name = "Georgia"
    t_run.font.size = Pt(14)
    t_run.font.bold = True
    t_run.font.color.rgb = C_MAROON

    toc_items = [
        ("1. Executive Summary & Problem Formulation", "Treatise purpose, Sanskrit synthesis, and brevity mandate"),
        ("2. System Architecture & Multi-Provider Model Topology", "Why 3 distinct frontier LLMs prevent monoculture & confirmation bias"),
        ("3. The Five Specialized Autonomous Agents", "Personas, responsibilities, prompt models, and dialectic roles"),
        ("4. The 13 Qualitative Verification Gates (Agent 5)", "Paninian grammar, brevity audit, anti-plagiarism, and duplicate guards"),
        ("5. Data Persistence, Vector Stores & Cryptographic Audit Logs", "ChromaDB collections, SQLite manuscript journal, and SHA-256 proofs"),
        ("6. Complete Step-by-Step Execution Lifecycle", "What happens end-to-end when the generation engine is triggered"),
        ("7. The 7-Part Reader-First Chapter Architecture", "Pedagogical ordering: Source First -> Derivation -> Sutra -> Bhashya -> Action"),
        ("8. Architectural Review & System Hardening Opportunities", "6 actionable engineering recommendations for peer developer review")
    ]

    toc_tbl = doc.add_table(rows=len(toc_items), cols=2)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, desc) in enumerate(toc_items):
        c0 = toc_tbl.cell(idx, 0)
        c1 = toc_tbl.cell(idx, 1)
        c0.width = Inches(3.2)
        c1.width = Inches(3.8)
        set_cell_background(c0, "FBF9F5" if idx % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "FBF9F5" if idx % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, top=40, bottom=40, left=80, right=80)
        set_cell_margins(c1, top=40, bottom=40, left=80, right=80)

        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.space_after = Pt(0)

        r0 = p0.add_run(title)
        r0.font.name = "Arial"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r0.font.color.rgb = C_NAVY

        r1 = p1.add_run(desc)
        r1.font.name = "Georgia"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = C_SLATE

    # ==================== SECTION 1 ====================
    add_section_heading(doc, "1. Executive Summary & Problem Formulation", level=1)
    add_body_paragraph(
        doc,
        "The SK Sutras platform is an autonomous multi-agent AI research, composition, and validation engine designed to author a canonical "
        "contemporary Sanskrit treatise: 'श्रीमद् उद्योग सूत्राणि' (Shrimad Udyog Sutras). Initiated by author and researcher Shri Shripad Kulkarni, "
        "the project's overarching objective is to bridge classical Bharatiya Jnana Parampara (Indian Knowledge Systems) with 21st-century "
        "entrepreneurial leadership, enterprise ethics, and corporate governance."
    )
    add_body_paragraph(
        doc,
        "Rather than quoting ancient texts out of context or inventing speculative ideas without scriptural roots, the engine implements a "
        "strict dialectical Shastrartha council. It pairs authentic Sanskrit verses from two complementary classical schools of Bhakti:\n"
        "• Devarshi Narada's affective path of passionate surrender, emotional vision, and obsessive devotion to one's craft (Narada Bhakti Sutras).\n"
        "• Maharshi Shandilya's epistemological path of discriminative intellect (Buddhi), rational proof (Pramana), and disciplined due diligence (Shandilya Bhakti Sutras)."
    )

    add_callout_box(
        doc,
        "The Non-Negotiable Editorial Axiom (Shri Shripad Kulkarni Mandate)",
        "'सूत्र लहान, विचार महान, निरूपण सुटसुटीत, संक्षिप्त आणि आचरण व्यावहारिक'\n"
        "1. Sutra (Aphorism): Extremely short, title-like, memorable, punchy, and easy to recall (typically 2 to 5 Sanskrit words, e.g. '॥ अथातो उद्योगजिज्ञासा ॥').\n"
        "2. Bhashya (Commentary): Crisp, lucid Marathi commentary strictly between 70 and 110 words. Zero rambling, zero filler, zero repetitive bloat.\n"
        "3. Actionable Application: Real-world Eastern & Western case studies, Patanjali Yoga founder resilience frameworks, and concrete DOs & DON'Ts for founders, managers, and boards."
    )

    # ==================== SECTION 2 ====================
    add_section_heading(doc, "2. System Architecture & Multi-Provider Model Topology", level=1)
    add_body_paragraph(
        doc,
        "A foundational design decision of the SK Sutras architecture is Multi-Provider LLM Heterogeneity. Single-model multi-agent "
        "frameworks suffer from shared cognitive blindspots, lexical echo chambers, and self-reinforcing hallucination loops. If Agent 1, Agent 2, "
        "Agent 4, and Agent 5 were all powered by the same underlying model weights (e.g. only GPT-4o or only Claude), the debate would be cosmetic: "
        "the validator would share the author's stylistic biases and fail to detect subtle grammatical or doctrinal flaws."
    )
    add_body_paragraph(
        doc,
        "To enforce genuine intellectual tension and adversarial scrutiny, the 5 agents are distributed across three distinct frontier commercial AI providers:"
    )

    # Model Topology Table
    topo_tbl = doc.add_table(rows=6, cols=4)
    topo_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Agent & Council Role", "Commercial Provider", "Deployed Model ID", "Architectural Function"]
    for col_idx, h_text in enumerate(headers):
        c = topo_tbl.cell(0, col_idx)
        set_cell_background(c, "123456")
        set_cell_margins(c, top=60, bottom=60, left=80, right=80)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    rows_data = [
        ("Agent 1: Narada Specialist", "Google Cloud AI", "gemini-3.8-flash / gemini-2.5-flash", "Affective devotion, passionate vision, enterprise isomorphism"),
        ("Agent 2: Shandilya Specialist", "OpenAI", "gpt-4o", "Analytical due diligence, rational proof, ChromaDB semantic scoring"),
        ("Agent 3: Bharatiya Jnana Specialist", "Anthropic", "claude-sonnet-5-5 / claude-3-5-sonnet", "Multi-text scriptural retrieval (DOC-01..04 + 20 IKS texts)"),
        ("Agent 4: Master Sutrakar Author", "Anthropic", "claude-sonnet-5-5 / claude-3-5-sonnet", "Shastrartha arbitration, Paninian composition, crisp Bhashya"),
        ("Agent 5: Independent Verification", "OpenAI + Classical Engine", "gpt-4o + SanskritMetreValidator", "13-Gate quality audit, duplicate rejector, zero auto-approval")
    ]

    for r_idx, row_vals in enumerate(rows_data, start=1):
        for c_idx, val in enumerate(row_vals):
            c = topo_tbl.cell(r_idx, c_idx)
            set_cell_background(c, "FBF9F5" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, top=40, bottom=40, left=70, right=70)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Georgia"
            r.font.size = Pt(8)
            r.font.color.rgb = C_SLATE

    # ==================== SECTION 3 ====================
    add_section_heading(doc, "3. The Five Specialized Autonomous Agents", level=1)
    add_body_paragraph(
        doc,
        "Each of the five agents operates with an isolated, specialized system prompt, domain boundaries, and custom tooling:"
    )

    agents_detail = [
        ("Agent 1: Devarshi Narada Specialist", "Google Gemini", [
            "Domain: The 84 Sutras of the Narada Bhakti Sutra corpus.",
            "Persona: Affective, visionary, passionate. Represents the emotional driving force and unrelenting purpose of an enterprise founder.",
            "Execution Function: Evaluates candidate Narada verses, maps devotional love to modern entrepreneurial dedication (Udyamshilta), and formulates an initial thematic thesis addressed to Agent 2."
        ]),
        ("Agent 2: Maharshi Shandilya Specialist", "OpenAI GPT-4o", [
            "Domain: The 100 Sutras of the Shandilya Bhakti Sutra corpus, indexed in ChromaDB.",
            "Persona: Rigorous, epistemological, analytical. Insists that visionary passion without empirical proof (Pramana) and due diligence leads to commercial ruin.",
            "Execution Function: Dynamically queries the ChromaDB vector store across all 100 Shandilya sutras, scores semantic similarity, evaluates the top-5 candidates, and provides an adversarial due diligence review."
        ]),
        ("Agent 3: Bharatiya Jnana Specialist (IKS Auditor)", "Anthropic Claude 3.5 Sonnet", [
            "Domain: 4 Foundational Author Texts (DOC-01 to DOC-04) + 20+ Canonical Texts in ChromaDB.",
            "Persona: Traditional scriptural scholar, ethical custodian, interdisciplinary researcher.",
            "Execution Function: Retrieves complementary verses from Arthashastra, Bhagavad Gita, Patanjali Yoga, and Sant Tukaram. Ensures every sutra is anchored in lawful wealth creation (Dharmasammata Arthalabha) and social trusteeship (Lokasangraha)."
        ]),
        ("Agent 4: Master Sutrakar (Discussion Lead & Primary Author)", "Anthropic Claude 3.5 Sonnet", [
            "Domain: Classical Sanskrit grammar (Paninian Astadhyayi), aphoristic design, contemporary business synthesis.",
            "Persona: Master author, chief arbiter, and philosophical synthesizer.",
            "Execution Function: Arbitrates candidate pairings (rejects forced matches); composes a new, short Sanskrit Udyoga Sutra (2-5 words); formulates Padaccheda, Anvaya, and Nirukta; authors bilingual translations; and produces the concise Bhashya (<110 words)."
        ]),
        ("Agent 5: Independent Verification Specialist & Quality Auditor", "OpenAI GPT-4o + Classical Rule Engine", [
            "Domain: Classical Sanskrit metres, grammar validators, duplication algorithms, 13 qualitative audit gates.",
            "Persona: Uncompromising Senior Lead QA auditor, external peer reviewer.",
            "Execution Function: Audits Agent 4's composition. Enforces a strict fail-closed policy: rejects any candidate with a score < 85/100, duplicate Sanskrit text, or verbosity > 120 words, triggering mandatory re-deliberation."
        ])
    ]

    for a_title, a_prov, a_pts in agents_detail:
        add_section_heading(doc, f"{a_title} [{a_prov}]", level=2)
        for pt in a_pts:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Inches(0.2)
            r = p.add_run(f"• {pt}")
            r.font.name = "Georgia"
            r.font.size = Pt(8.5)
            r.font.color.rgb = C_SLATE

    # ==================== SECTION 4 ====================
    add_section_heading(doc, "4. The 13 Qualitative Verification Gates (Agent 5 Gatekeeper)", level=1)
    add_body_paragraph(
        doc,
        "Every candidate Udyog Sutra must clear 13 qualitative gates before Agent 5 certifies it into the canonical database. "
        "If any single gate fails, the candidate is rejected with an audit report, forcing Agent 4 to re-synthesize or re-compose:"
    )

    gates = [
        ("Gate 1: Short, Memorable Formulation", "Sutra must be an extremely short, title-like aphorism (2 to 5 words). Long 2-line metrical shlokas are strictly rejected."),
        ("Gate 2: Paninian Grammatical Soundness", "Exact word-breakdown (Padaccheda), prose order (Anvaya), and etymological roots (Nirukta) must be grammatically sound."),
        ("Gate 3: Doctrinal Fidelity to Narada", "Preserves authentic affective devotion and founder passion without dilution."),
        ("Gate 4: Doctrinal Fidelity to Shandilya", "Preserves rational due diligence, discriminative logic, and epistemological integrity."),
        ("Gate 5: Authentic Bharatiya Jnana Grounding", "Verified citation of the 4 foundational texts and canonical IKS scriptural traditions."),
        ("Gate 6: Concise Bhashya Length Audit", "Marathi Bhashya must strictly reside within 70 to 110 words (hard limit 120 words). Padding is disqualified."),
        ("Gate 7: Biographical Case Studies Authenticity", "Exactly 2 real-life case studies (1 Eastern, 1 Western) demonstrating the principle in commercial history."),
        ("Gate 8: Patanjali Yoga Psychological Resilience", "Specific Patanjali Yoga Sutra reference with actionable founder mental equilibrium guidance."),
        ("Gate 9: Ethical Enterprise & Trusteeship", "Strict adherence to Dharmasammata Arthalabha, Satya-Vyavahara, and Gandhian/Upanishadic Trusteeship."),
        ("Gate 10: Absolute Novelty & Originality", "Must be a genuine contemporary synthesis; quoting an ancient verse as a 'new sutra' is strictly barred."),
        ("Gate 11: Absence of Forced Matching", "The Narada-Shandilya conceptual pairing must be natural and philosophically resonant, not forced by keyword overlap."),
        ("Gate 12: Actionable Leadership Guidance", "Specific, non-generic operational direction for Early Founders, Operational Managers, and Boards."),
        ("Gate 13: Algorithmic Duplicate Guard", "Strict string and normalized cosine similarity check (< 0.85) against all previously approved sutras in the canon.")
    ]

    g_tbl = doc.add_table(rows=len(gates) + 1, cols=2)
    g_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    g_cell0 = g_tbl.cell(0, 0)
    g_cell1 = g_tbl.cell(0, 1)
    g_cell0.width = Inches(2.6)
    g_cell1.width = Inches(4.4)
    set_cell_background(g_cell0, "8B0000")
    set_cell_background(g_cell1, "8B0000")
    set_cell_margins(g_cell0, top=50, bottom=50, left=80, right=80)
    set_cell_margins(g_cell1, top=50, bottom=50, left=80, right=80)
    g_cell0.paragraphs[0].add_run("Verification Gate").font.color.rgb = RGBColor(255, 255, 255)
    g_cell1.paragraphs[0].add_run("Mandatory Quality Criterion").font.color.rgb = RGBColor(255, 255, 255)
    g_cell0.paragraphs[0].runs[0].font.bold = True
    g_cell1.paragraphs[0].runs[0].font.bold = True

    for idx, (g_name, g_desc) in enumerate(gates, start=1):
        c0 = g_tbl.cell(idx, 0)
        c1 = g_tbl.cell(idx, 1)
        c0.width = Inches(2.6)
        c1.width = Inches(4.4)
        set_cell_background(c0, "FBF9F5" if idx % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "FBF9F5" if idx % 2 == 0 else "FFFFFF")
        set_cell_margins(c0, top=35, bottom=35, left=70, right=70)
        set_cell_margins(c1, top=35, bottom=35, left=70, right=70)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.space_after = Pt(0)

        r0 = p0.add_run(g_name)
        r0.font.name = "Arial"
        r0.font.size = Pt(8)
        r0.font.bold = True
        r0.font.color.rgb = C_NAVY

        r1 = p1.add_run(g_desc)
        r1.font.name = "Georgia"
        r1.font.size = Pt(8)
        r1.font.color.rgb = C_SLATE

    # ==================== SECTION 5 ====================
    add_section_heading(doc, "5. Data Persistence, Vector Stores & Cryptographic Audit Logs", level=1)
    add_body_paragraph(
        doc,
        "The architecture enforces strict enterprise data persistence across relational, vector, and append-only cryptographic storage layers:"
    )

    layers = [
        ("ChromaDB Vector Store", "Collections: 'shandilya_100_sutras' and 'iks_canonical_library'. Persisted locally under data/vectorstore/chroma. Enables fast, semantic distance-based nearest-neighbor querying without hardcoded lookups."),
        ("SQLite Relational Journal (manuscript.db)", "Stores table 'manuscript_units' with 34 relational columns recording Sanskrit verses, translations, grammatical parses, and approval timestamps. Ensures ACID transactional safety."),
        ("Token Financial & Usage Ledger", "Table 'token_usage_records' logs every single API call: model ID, input tokens, output tokens, cached tokens, and exact financial cost computed in USD and INR (83.50 INR/USD rate)."),
        ("Live Cryptographic Proof Registry", "Table 'live_api_execution_logs' records HTTP 200 statuses, finish reasons, execution IDs, and SHA-256 cryptographic hashes of every raw LLM response string to guarantee audit proof against mock data."),
        ("Append-Only Consultation Ledger", "File 'data/knowledge_repository/consultation/consultation_ledger.jsonl' records every independent document lookup performed by Agent 4 for audit traceability.")
    ]

    for l_title, l_desc in layers:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        r_t = p.add_run(f"★ {l_title}: ")
        r_t.font.name = "Arial"
        r_t.font.size = Pt(8.5)
        r_t.font.bold = True
        r_t.font.color.rgb = C_NAVY
        r_d = p.add_run(l_desc)
        r_d.font.name = "Georgia"
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = C_SLATE

    # ==================== SECTION 6 ====================
    add_section_heading(doc, "6. Complete Step-by-Step Execution Lifecycle", level=1)
    add_body_paragraph(
        doc,
        "When the command 'scripts/run_dynamic_live_council.py' is executed, the following 10-step pipeline runs sequentially until exactly 10 new canonical Udyog Sutras are certified:"
    )

    steps = [
        ("Step 1: Environment & Token Hydration", "Validates Windows Credential Manager and environment API keys for Google Gemini, OpenAI, and Anthropic. Initializes SQLite tables and verifies ChromaDB index connectivity."),
        ("Step 2: Candidate Narada Dispatch (Agent 1)", "Picks the next unvisited Narada Bhakti Sutra. Invokes Google Gemini ('gemini-3.8-flash') to extract its entrepreneurial isomorphism thesis."),
        ("Step 3: Semantic Vector Retrieval & Review (Agent 2)", "Queries ChromaDB across the 100 Shandilya sutras. Invokes OpenAI GPT-4o to analyze the top candidates and produce an adversarial rational due diligence review."),
        ("Step 4: Shastrartha Arbitration & Pair Certification (Agent 4)", "Invokes Anthropic Claude 3.5 Sonnet to arbitrate the Narada-Shandilya pairing. Rejects forced matches and approves only authentic doctrinal harmony."),
        ("Step 5: Balanced Multi-Document Research (Agent 3)", "Invokes Claude 3.5 Sonnet to query the 4 foundational texts (DOC-01..04) and dynamically retrieve relevant verses from 20+ IKS texts in ChromaDB."),
        ("Step 6: Master Classical Sanskrit Composition (Agent 4)", "Invokes Claude 3.5 Sonnet to compose the short, memorable Sanskrit Sutra (2-5 words), Padaccheda, Anvaya, Nirukta, translations, and concise Bhashya (<110 words)."),
        ("Step 7: 13-Gate Audit & Duplicate Gate (Agent 5)", "Invokes OpenAI GPT-4o and runs algorithmic duplicate checks against existing canon. Rejection triggers re-deliberation; approval requires score >= 85."),
        ("Step 8: ACID Relational Commit & SHA-256 Proof Recording", "Writes the approved unit to SQLite 'manuscript_units' and logs raw response SHA-256 hashes, token counts, and cost to 'live_api_execution_logs'."),
        ("Step 9: Automated Publication Document Generation", "Compiles the full publication manuscript into 'Shrimad_Udyog_Sutras_10_Canonical_Sutras_Editorial_Refined.docx' implementing the 7-part pedagogical framework."),
        ("Step 10: Multi-Target Replication & Client Changelog Commit", "Replicates the document across Dropbox, workspace docs, and brain artifacts. Appends version release notes to CLIENT_CHANGELOG.md.")
    ]

    for s_title, s_desc in steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.15)
        r_t = p.add_run(f"[{s_title}]: ")
        r_t.font.name = "Arial"
        r_t.font.size = Pt(8.5)
        r_t.font.bold = True
        r_t.font.color.rgb = C_MAROON
        r_d = p.add_run(s_desc)
        r_d.font.name = "Georgia"
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = C_SLATE

    # ==================== SECTION 7 ====================
    add_section_heading(doc, "7. The 7-Part Reader-First Chapter Architecture", level=1)
    add_body_paragraph(
        doc,
        "Every chapter in the generated Word manuscript adheres to an identical, reader-friendly pedagogical framework designed for modern executives:"
    )

    parts = [
        ("१. मूळ आधार आणि संदर्भ श्लोक (Foundational Source Verses)", "Source First: Narada and Shandilya authentic Sanskrit shlokas, transliterations, and meanings presented first."),
        ("२. मूळ तत्त्वाकडून उद्योग सूत्राकडे (Derivation Bridge)", "Explains the philosophical bridge from devotional scripture to contemporary enterprise leadership."),
        ("३. नवीन उद्योग सूत्र व सरळ अर्थ (New Udyoga Sutra & Translation)", "Prominent golden Sanskrit box, followed by high-contrast Marathi and English translations, plus Padaccheda, Anvaya, Nirukta."),
        ("४. सविस्तर विवेचन व निरूपण (Detailed Exposition & Bhashya)", "Crisp, lucid commentary strictly under 110 words explaining core business meaning and trusteeship."),
        ("५. व्यावहारिक उपयोजन व सत्यकथा (Practical Case Studies & Yoga)", "Biographical case studies of industrial pioneers (Jamsetji Tata, Thomas Edison, etc.) + Patanjali mental peace guidance."),
        ("६. काय करावे आणि काय टाळावे (DOs & DON'Ts for Modern Enterprise)", "Actionable behavioral code: 3 concrete DOs with founder/manager guidance, and 3 specific DON'Ts / pitfalls."),
        ("७. चिंतन व अंतिम सूत्रसार (Reflection & Key Takeaway)", "Executive introspection question, one-line core takeaway mantra, and auspicious closing invocation.")
    ]

    for p_title, p_desc in parts:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(0.2)
        r_t = p.add_run(f"• {p_title}: ")
        r_t.font.name = "Arial"
        r_t.font.size = Pt(8.5)
        r_t.font.bold = True
        r_t.font.color.rgb = C_NAVY
        r_d = p.add_run(p_desc)
        r_d.font.name = "Georgia"
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = C_SLATE

    # ==================== SECTION 8 ====================
    add_section_heading(doc, "8. Architectural Review & System Hardening Opportunities", level=1)
    add_body_paragraph(
        doc,
        "For a peer architect or technical reviewer examining this codebase, here are 6 high-value engineering opportunities to critique and strengthen:"
    )

    hardening_items = [
        ("1. Asynchronous Graph Parallelism (LangGraph DAG Execution)", 
         "Currently, the execution loop is sequential. Implementing asynchronous fan-out where Agent 1 and Agent 3 pre-fetch in parallel can reduce total pipeline execution latency by ~40%."),
        ("2. Dedicated Semantic Cache Layer for Prompt Templates", 
         "Implementing Redis or SQLite-based prompt-response semantic caching for stable foundational queries (e.g. static Shandilya/Narada initial meanings) to reduce unnecessary API token costs."),
        ("3. Classical Sanskrit Morphological Parser Integration", 
         "Augmenting Agent 5's rule engine with an external computational linguistics parser (e.g. Inria Sanskrit Heritage Site engine / Heritage Platform) to automate Paninian Sandhi and Samasa verification programmatically."),
        ("4. Dynamic Temperature & Top-P Persona Calibration", 
         "Calibrating generation parameters per persona: Temperature 0.2 for Agent 2 (Analytical Due Diligence) and Agent 5 (QA Gatekeeper); Temperature 0.6 for Agent 1 and Agent 4 (Creative Classical Composition)."),
        ("5. Continuous Automated Regression Benchmark", 
         "Expanding the current 73-test suite to include synthetic semantic drift benchmarks, verifying that re-runs preserve doctrinal alignment without degradation over time."),
        ("6. Cloud-Native Webhook & Containerized Deployment", 
         "Packaging the council into a containerized FastAPI service with persistent Docker volume bind mounts for SQLite and ChromaDB, enabling scheduled cloud runs with zero data overwrite risk.")
    ]

    for h_title, h_desc in hardening_items:
        add_callout_box(doc, h_title, h_desc, hex_bg="FBF9F5", border_color="8B0000")
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # Save to Target Paths
    TARGET_DOCS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(TARGET_DOCS_OUTPUT))
    print(f"Saved workspace file: {TARGET_DOCS_OUTPUT}")

    try:
        DROPBOX_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TARGET_DOCS_OUTPUT, DROPBOX_OUTPUT)
        print(f"Copied to Dropbox: {DROPBOX_OUTPUT}")
    except Exception as e:
        print(f"Warning: Could not copy to Dropbox: {e}")

    try:
        shutil.copy2(TARGET_DOCS_OUTPUT, ARTIFACT_OUTPUT)
        print(f"Copied to Brain Artifact: {ARTIFACT_OUTPUT}")
    except Exception as e:
        print(f"Warning: Could not copy to Brain Artifact: {e}")

    print("\nArchitecture briefing document generated successfully.")
    return TARGET_DOCS_OUTPUT


if __name__ == "__main__":
    build_architecture_briefing_document()
