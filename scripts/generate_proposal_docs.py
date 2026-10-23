"""
================================================================================
Script: scripts/generate_proposal_docs.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates the formal, publication-grade client proposal and quotation
             for Shri Shripad Kulkarni in both PDF and DOCX formats.
             Includes:
             - Detailed explanation of the 3-Agent AI architecture (Narada, Shandilya, Sutrakar).
             - Option 1 (ChatGPT + Gemini Sutrakar): ₹48,000 INR (₹18,000 LLM/infra + ₹30,000 dev).
             - Option 2 (Pure Google DeepMind Gemini Specialized): ₹75,000 INR (₹45,000 LLM/infra + ₹30,000 dev).
             - Sutrakar Agent original Sanskrit shloka formulation capability.
             - Proofreading PDF book delivery and iterative revision commitment.
             - Mandatory confidentiality footer: "Proprietory and Confidential- Hiranyam AI Labs".
================================================================================
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. ReportLab PDF Generation
# ------------------------------------------------------------------------------
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw exact total page numbers,
    running headers, and the mandatory Hiranyam AI confidentiality footer on every page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        page_width, page_height = letter

        # Running Top Header (Pages > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#7A1818"))
            self.drawString(54, page_height - 36, "HIRANYAM AI LABS")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.drawString(145, page_height - 36, "|   Project Proposal & Quotation: SK Sutras (Udyoga Sutras)")
            self.drawRightString(page_width - 54, page_height - 36, "Client: Shri Shripad Kulkarni")

            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, page_height - 42, page_width - 54, page_height - 42)

        # Mandatory Standardized Confidentiality Footer (On EVERY Page)
        self.setStrokeColor(colors.HexColor("#D4C5B9"))
        self.setLineWidth(0.75)
        self.line(54, 46, page_width - 54, 46)

        footer_text = "Proprietory and Confidential- Hiranyam AI Labs"
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#8B0000"))
        self.drawCentredString(page_width / 2.0, 32, footer_text)

        # Page numbering on right
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#666666"))
        self.drawRightString(page_width - 54, 32, f"Page {self._pageNumber} of {page_count}")

        # Verification tag on left
        self.drawString(54, 32, "Doc ID: HAIL-PROP-2026-SKS01")

        self.restoreState()


def build_pdf_proposal(output_pdf_path: Path):
    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_maroon = colors.HexColor("#800000")
    c_dark_maroon = colors.HexColor("#5c0000")
    c_navy = colors.HexColor("#0B5394")
    c_charcoal = colors.HexColor("#222222")
    c_gray = colors.HexColor("#555555")
    c_light_bg = colors.HexColor("#FAF7F2")
    c_card_bg = colors.HexColor("#FDFCF9")
    c_border = colors.HexColor("#D4C5B9")

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=c_maroon,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=c_navy,
        spaceAfter=14,
    )
    meta_style = ParagraphStyle(
        "DocMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=c_charcoal,
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=c_maroon,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=c_dark_maroon,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14.5,
        textColor=c_charcoal,
        spaceAfter=7,
    )
    body_bold = ParagraphStyle(
        "Body_Bold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4,
    )
    callout_style = ParagraphStyle(
        "Callout_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#443322"),
    )

    story = []

    # --------------------------------------------------------------------------
    # Document Header / Banner
    # --------------------------------------------------------------------------
    header_data = [
        [
            Paragraph("<b>HIRANYAM AI LABS</b><br/><font size='8' color='#555555'>Advanced Agentic AI & Cognitive Computing Solutions<br/>Official Portal: <font color='#0B5394'><u>https://hiranyamai.com/</u></font></font>", meta_style),
            Paragraph("<b>PROPOSAL & QUOTATION</b><br/><font size='8.5' color='#555555'><b>Date:</b> October 23, 2026<br/><b>Document Ref:</b> HAIL-PROP-2026-SKS01<br/><b>Valid Through:</b> 30 Days</font>", ParagraphStyle("RightMeta", parent=meta_style, alignment=2)),
        ]
    ]
    t_header = Table(header_data, colWidths=[3.25 * inch, 3.75 * inch])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_header)
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_maroon, spaceBefore=4, spaceAfter=14))

    # Title & Metadata
    story.append(Paragraph("Project Proposal & Commercial Quotation", title_style))
    story.append(Paragraph("Autonomous Tri-Agent AI Synthesis & Publication Framework for <i>SK Sutras: Udyoga Sutras</i>", subtitle_style))

    client_info_data = [
        [
            Paragraph("<b>Client / Primary Author:</b>", meta_style),
            Paragraph("Shri Shripad Kulkarni", ParagraphStyle("BoldVal", parent=meta_style, fontName="Helvetica-Bold", textColor=c_maroon)),
            Paragraph("<b>Technology Partner:</b>", meta_style),
            Paragraph("Hiranyam AI Labs (notifications@hiranyamai.com)", meta_style),
        ],
        [
            Paragraph("<b>Project Title:</b>", meta_style),
            Paragraph("SK Sutras (Udyoga Sutras Treatise)", meta_style),
            Paragraph("<b>Target Deliverable:</b>", meta_style),
            Paragraph("Print-Ready Publication PDF & Proofreading Drafts", meta_style),
        ],
    ]
    t_client = Table(client_info_data, colWidths=[1.6 * inch, 2.1 * inch, 1.4 * inch, 2.1 * inch])
    t_client.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 14))

    # --------------------------------------------------------------------------
    # 1. Executive Summary
    # --------------------------------------------------------------------------
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Hiranyam AI Labs is privileged to submit this formal proposal and quotation to <b>Shri Shripad Kulkarni</b> "
        "for the complete research, synthesis, multi-agent AI engineering, and pre-press publication workflow of the monumental "
        "philosophical treatise: <b><i>SK Sutras: Udyoga Sutras</i></b>.",
        body_style
    ))
    story.append(Paragraph(
        "The objective of this project is to orchestrate a pioneering doctrinal synthesis between two foundational canons of Indian spiritual philosophy—the "
        "<b>84 Narada Bhakti Sutras</b> (representing ecstatic, experiential devotion) and the <b>100 Shandilya Bhakti Sutras</b> (representing rational, "
        "epistemological Vedantic inquiry). Through an autonomous Tri-Agent AI architecture, these traditions are systematically cross-examined, "
        "filtered against false overlaps, and unified into an authoritative new treatise featuring <b>original Sanskrit shlokas</b> and in-depth classical "
        "<b>Marathi Udyoga Bhashya</b> tailored for modern workplace ethics and human duty.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # --------------------------------------------------------------------------
    # 2. The Three-Agent AI Architecture
    # --------------------------------------------------------------------------
    story.append(Paragraph("2. The Autonomous Three-Agent Architecture", h1_style))
    story.append(Paragraph(
        "Traditional single-model prompts fail when addressing complex scriptural literature because a single model inevitably agrees with itself, producing superficial syncretism. "
        "Our proprietary solution deploys three distinct, specialized autonomous agents with contrasting cognitive perspectives that debate, cross-examine, and arbitrate each verse:",
        body_style
    ))

    agents_table_data = [
        [
            Paragraph("<b>Agent Name</b>", meta_style),
            Paragraph("<b>Specialized Domain Canon</b>", meta_style),
            Paragraph("<b>Cognitive Role & Capabilities</b>", meta_style),
        ],
        [
            Paragraph("<b>1. Narada Bhakti Sutra Specialist Agent</b>", ParagraphStyle("AN1", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("<b>84 Narada Sutras</b><br/>(Experiential Devotion)", meta_style),
            Paragraph("Adopts the perspective of Devarshi Narada. Focuses on <i>Parama-Prema</i> (unconditional divine love), ecstatic surrender, and practical heart-centered devotion. Formulates formal philosophical propositions to challenge the rational school.", meta_style),
        ],
        [
            Paragraph("<b>2. Shandilya Bhakti Sutra Specialist Agent</b>", ParagraphStyle("AN2", parent=meta_style, textColor=c_navy, fontName="Helvetica-Bold")),
            Paragraph("<b>100 Shandilya Sutras</b><br/>(Epistemological Vedanta)", meta_style),
            Paragraph("Adopts the perspective of Maharshi Shandilya. Maintains all 100 sutras in ChromaDB vector storage. Conducts mathematical semantic searches and defends the rational Vedantic inquiry (<i>Bhakti-Jijnasa, Tarka</i>) with rigorous scriptural citations.", meta_style),
        ],
        [
            Paragraph("<b>3. Sutrakar Agent</b><br/>(Master Coordinator, Arbiter & Creative Synthesizer)", ParagraphStyle("AN3", parent=meta_style, textColor=c_dark_maroon, fontName="Helvetica-Bold")),
            Paragraph("<b>Vedic Synthesis & New Udyoga Sutras</b>", meta_style),
            Paragraph("Acts as the supreme philosophical arbiter and compiler:<br/>"
                      "• <b>Strict Non-Compulsory Logic:</b> Rejects forced or superficial mappings (67 non-matches omitted).<br/>"
                      "• <b>Anti-Duplicate Intelligence:</b> Scans memory to eliminate repeated themes or recycled sutras.<br/>"
                      "• <b>Original Shloka Formulation:</b> When authentic correspondence is verified, the Sutrakar Agent <b>composes brand-new Sanskrit shlokas</b> (new <i>Udyoga Sutras</i>).<br/>"
                      "• <b>Bespoke Marathi Commentary:</b> Authors multi-paragraph <i>Udyoga Bhashya</i> (Doctrinal Harmony, Applied Enterprise & Ethics, and Culminating Realization).", meta_style),
        ],
    ]
    t_agents = Table(agents_table_data, colWidths=[1.8 * inch, 1.6 * inch, 3.6 * inch])
    t_agents.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EFE8DE")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_agents)
    story.append(Spacer(1, 14))

    # Page Break for clean multi-page presentation
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 3. Two Deployment Options
    # --------------------------------------------------------------------------
    story.append(Paragraph("3. Detailed Deployment Options & LLM Selection Rationale", h1_style))
    story.append(Paragraph(
        "To provide full strategic and financial flexibility, we present two distinct deployment architectures based on commercial frontier Large Language Models (LLMs):",
        body_style
    ))

    # Option 1 Callout Box
    opt1_box_data = [
        [
            Paragraph("<b>OPTION 1: Hybrid Architecture (ChatGPT + Google Gemini)</b>", ParagraphStyle("Opt1Title", parent=h2_style, textColor=c_navy, spaceBefore=0)),
        ],
        [
            Paragraph(
                "<b>Agent-to-Model Configuration:</b><br/>"
                "• <b>Narada Agent:</b> OpenAI ChatGPT (GPT-4o)<br/>"
                "• <b>Shandilya Agent:</b> OpenAI ChatGPT (GPT-4o)<br/>"
                "• <b>Sutrakar Agent:</b> Google DeepMind Gemini (Gemini 1.5 Pro)<br/><br/>"
                "<b>Architectural Rationale:</b><br/>"
                "In Option 1, OpenAI's GPT-4o provides rapid conversational parsing and structured dialectic discourse for the individual source books. "
                "The <b>Sutrakar Agent is powered by Google Gemini 1.5 Pro</b> because of Gemini's unmatched training corpus on ancient Indian Vedic literatures, "
                "native classical Sanskrit grammar, Sanskrit-to-Marathi translation nuance, and massive context window (up to 2,000,000 tokens) which enables "
                "the Sutrakar to hold the entire treatise in active memory to prevent duplicate verses and repeated explanations.<br/><br/>"
                "<b>Commercial Breakdown:</b><br/>"
                "• AI Compute & Cloud Token Infrastructure: <b>₹18,000 INR</b> (approx. $215 USD)<br/>"
                "• Hiranyam AI Development, Publication & Proofreading Service Fee: <b>₹30,000 INR</b><br/>"
                "• <b>Total Investment (Option 1): ₹48,000 INR</b> (approx. $570 USD)",
                body_style
            )
        ]
    ]
    t_opt1 = Table(opt1_box_data, colWidths=[7.0 * inch])
    t_opt1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1.5, c_navy),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_opt1)
    story.append(Spacer(1, 12))

    # Option 2 Callout Box
    opt2_box_data = [
        [
            Paragraph("<b>OPTION 2: Pure Google DeepMind Gemini Specialized Architecture (Recommended)</b>", ParagraphStyle("Opt2Title", parent=h2_style, textColor=c_maroon, spaceBefore=0)),
        ],
        [
            Paragraph(
                "<b>Agent-to-Model Configuration:</b><br/>"
                "• <b>Narada Agent:</b> Google Gemini (Gemini 1.5 Pro Specialized)<br/>"
                "• <b>Shandilya Agent:</b> Google Gemini (Gemini 1.5 Pro Specialized)<br/>"
                "• <b>Sutrakar Agent:</b> Google Gemini (Gemini 1.5 Pro / Advanced High-Reasoning)<br/><br/>"
                "<b>Architectural Rationale & Superiority:</b><br/>"
                "Option 2 provides specialized in-depth Vedic and Sanskrit mastery across <b>all three agents</b>:<br/>"
                "1. <b>Deepest Vedic & Indic Corpus:</b> Google possesses the world's most comprehensive scanned repository of ancient Indian scriptures, Vedantic commentaries, and Marathi literature via Google Books digitization.<br/>"
                "2. <b>Original Sanskrit Shloka Formulation:</b> With all agents on Gemini, the Sutrakar Agent can formulate <b>completely original, grammatically precise, metered Sanskrit shlokas</b> (new <i>Udyoga Sutras</i>) that synthesize the spiritual essence of Narada and Shandilya into a brand-new canonical work.<br/>"
                "3. <b>Nuanced Marathi Translation:</b> Generates scholarly, classical Marathi prose (*भावार्थ*) free from crude English transliterations.<br/>"
                "4. <b>Unified Context Caching:</b> Eliminates multi-vendor API latency and guarantees seamless, zero-duplicate harmonization across all 50 full cycles of canon re-generation.<br/><br/>"
                "<b>Commercial Breakdown:</b><br/>"
                "• AI Compute, Deep Contextual Caching, High-Reasoning & Infrastructure: <b>₹45,000 INR</b> (approx. $535 USD)<br/>"
                "• Hiranyam AI Development, Publication & Proofreading Service Fee: <b>₹30,000 INR</b><br/>"
                "• <b>Total Investment (Option 2): ₹75,000 INR</b> (approx. $895 USD)",
                body_style
            )
        ]
    ]
    t_opt2 = Table(opt2_box_data, colWidths=[7.0 * inch])
    t_opt2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FDF9F5")),
        ('BOX', (0, 0), (-1, -1), 2, c_maroon),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_opt2)
    story.append(Spacer(1, 14))

    # --------------------------------------------------------------------------
    # 4. Hiranyam AI Scope of Services (The ₹30,000 Fee)
    # --------------------------------------------------------------------------
    story.append(Paragraph("4. Scope of Services Covered under Hiranyam AI Fee (₹30,000 INR)", h1_style))
    story.append(Paragraph(
        "Our fixed development and publication service charge of <b>₹30,000 INR</b> provides exhaustive end-to-end engineering, editorial, and pre-press support until final sign-off:",
        body_style
    ))

    scope_points = [
        "<b>Multi-Agent Engineering & LangGraph DAG:</b> Custom construction of the inter-agent state machine coordinating Narada, Shandilya, and Sutrakar agents.",
        "<b>ChromaDB Vector Retrieval Setup:</b> Embedding and indexing all 100 Shandilya sutras and 84 Narada sutras for mathematical semantic matching.",
        "<b>Senior Citizen (65+ Mode) Web Review Portal:</b> Interactive digital workspace designed specifically for Shri Shripad Kulkarni with large touch targets, high-contrast typography, and 1-click approval.",
        "<b>Proofreading Book PDF Delivery:</b> Generating beautifully typeset A4/book-format PDF drafts with Devanagari Sanskrit verses and Marathi commentary for author proofreading.",
        "<b>50 Cycles of Re-running & Editorial Corrections:</b> Unlimited re-synthesis, re-evaluations, author-directed revisions, and tone adjustments till the copy is finalized.",
        "<b>Pre-Press Printing Preparation:</b> Formatting print-ready master files with proper margins, page numbers, cover branding, and publishing headers ready for immediate physical printing.",
    ]
    for pt in scope_points:
        story.append(Paragraph(f"• {pt}", bullet_style))

    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 5. Milestone Schedule & Payment Terms
    # --------------------------------------------------------------------------
    story.append(Paragraph("5. Milestone Schedule & Delivery Roadmap", h1_style))

    roadmap_data = [
        [
            Paragraph("<b>Milestone</b>", meta_style),
            Paragraph("<b>Deliverable Description</b>", meta_style),
            Paragraph("<b>Target Timeline</b>", meta_style),
            Paragraph("<b>Payment Due</b>", meta_style),
        ],
        [
            Paragraph("<b>Milestone 1: Project Kickoff & Agent Setup</b>", meta_style),
            Paragraph("Ingestion of 84 Narada and 100 Shandilya sutras into ChromaDB. Deployment of Tri-Agent state machine.", meta_style),
            Paragraph("Week 1", meta_style),
            Paragraph("<b>40%</b> of Service Fee + LLM Infra Deposit", meta_style),
        ],
        [
            Paragraph("<b>Milestone 2: First Complete Proofreading PDF</b>", meta_style),
            Paragraph("Batch execution of canon cross-examination. Generation of the first complete <i>Udyoga Sutra</i> book draft PDF for author review.", meta_style),
            Paragraph("Week 2", meta_style),
            Paragraph("<b>30%</b> of Service Fee", meta_style),
        ],
        [
            Paragraph("<b>Milestone 3: Portal Review & Editorial Rework</b>", meta_style),
            Paragraph("Author reviews verses in Senior Citizen portal. Multi-agent revisions and re-runs executed per author guidance.", meta_style),
            Paragraph("Weeks 3 – 4", meta_style),
            Paragraph("—", meta_style),
        ],
        [
            Paragraph("<b>Milestone 4: Final Sign-off & Print-Ready Master</b>", meta_style),
            Paragraph("Final approval by Shri Shripad Kulkarni. Delivery of publication-grade print-ready PDF and archival master files.", meta_style),
            Paragraph("Week 5", meta_style),
            Paragraph("<b>30%</b> Final Balance", meta_style),
        ],
    ]
    t_roadmap = Table(roadmap_data, colWidths=[1.7 * inch, 2.7 * inch, 1.1 * inch, 1.5 * inch])
    t_roadmap.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EFE8DE")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_roadmap)
    story.append(Spacer(1, 14))

    # --------------------------------------------------------------------------
    # 6. Commercial Quotation Summary Table
    # --------------------------------------------------------------------------
    story.append(Paragraph("6. Commercial Quotation Summary", h1_style))

    quotation_data = [
        [
            Paragraph("<b>Cost Element</b>", meta_style),
            Paragraph("<b>Option 1: Hybrid Architecture<br/>(ChatGPT + Gemini Sutrakar)</b>", meta_style),
            Paragraph("<b>Option 2: Gemini Specialized<br/>(All Agents on Google Gemini)</b>", meta_style),
        ],
        [
            Paragraph("<b>Autonomous Agentic AI Infrastructure & Compute</b><br/>(50 full canon passes, multi-million token volume, vector hosting)", meta_style),
            Paragraph("₹18,000 INR<br/><font size='8' color='#666'>($215 USD approx.)</font>", meta_style),
            Paragraph("₹45,000 INR<br/><font size='8' color='#666'>($535 USD approx.)</font>", meta_style),
        ],
        [
            Paragraph("<b>Hiranyam AI Engineering & Publication Service Fee</b><br/>(LangGraph DAG, Senior Citizen portal, proofreading PDFs, corrections)", meta_style),
            Paragraph("₹30,000 INR<br/><font size='8' color='#666'>($357 USD approx.)</font>", meta_style),
            Paragraph("₹30,000 INR<br/><font size='8' color='#666'>($357 USD approx.)</font>", meta_style),
        ],
        [
            Paragraph("<b>Sanskrit Shloka Formulation & Bespoke Bhashya</b>", meta_style),
            Paragraph("Included (Standard Synthesis)", meta_style),
            Paragraph("<b>Included (Original Sanskrit Shlokas)</b>", meta_style),
        ],
        [
            Paragraph("<b>Proofreading PDF Deliveries & 50 Rework Cycles</b>", meta_style),
            Paragraph("Included till Final Sign-off", meta_style),
            Paragraph("Included till Final Sign-off", meta_style),
        ],
        [
            Paragraph("<b>TOTAL PROPOSED INVESTMENT</b>", ParagraphStyle("TotalLabel", parent=meta_style, fontName="Helvetica-Bold", fontSize=10.5, textColor=c_maroon)),
            Paragraph("<b>₹48,000 INR</b><br/><font size='8.5' color='#555'>($572 USD)</font>", ParagraphStyle("TotalVal1", parent=meta_style, fontName="Helvetica-Bold", fontSize=11, textColor=c_navy)),
            Paragraph("<b>₹75,000 INR</b><br/><font size='8.5' color='#555'>($892 USD)</font>", ParagraphStyle("TotalVal2", parent=meta_style, fontName="Helvetica-Bold", fontSize=11, textColor=c_maroon)),
        ],
    ]
    t_quote = Table(quotation_data, colWidths=[2.6 * inch, 2.2 * inch, 2.2 * inch])
    t_quote.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EFE8DE")),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#FDF9F5")),
        ('BOX', (0, 0), (-1, -1), 1.5, c_maroon),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_quote)
    story.append(Spacer(1, 18))

    # --------------------------------------------------------------------------
    # 7. Acceptance & Authorization Block
    # --------------------------------------------------------------------------
    story.append(KeepTogether([
        Paragraph("7. Proposal Acceptance & Project Authorization", h1_style),
        Paragraph(
            "By signing below, the client confirms the selection of either Option 1 or Option 2 and authorizes Hiranyam AI Labs "
            "to commence work according to the milestone schedule outlined herein.",
            body_style
        ),
        Spacer(1, 10),
        Table([
            [
                Paragraph("<b>Accepted Option (Please Circle):</b>", meta_style),
                Paragraph("<b>[  ] Option 1 (₹48,000)</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>[  ] Option 2 (₹75,000)</b>", meta_style),
            ],
            [
                Paragraph("<b>For the Client / Author:</b><br/><br/><br/>_____________________________________<br/><b>Shri Shripad Kulkarni</b><br/>Date: ________________________", meta_style),
                Paragraph("<b>For Hiranyam AI Labs:</b><br/><br/><br/>_____________________________________<br/><b>Authorized Signatory</b><br/>Hiranyam AI Labs (<a href='https://hiranyamai.com/'>https://hiranyamai.com/</a>)", meta_style),
            ]
        ], colWidths=[3.5 * inch, 3.5 * inch], style=[
            ('BOX', (0, 0), (-1, -1), 1, c_border),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ])
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated Proposal PDF at: {output_pdf_path.resolve()}")


# ------------------------------------------------------------------------------
# 2. Python-Docx Generation with OpenXML Confidentiality Footer
# ------------------------------------------------------------------------------
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def build_docx_proposal(output_docx_path: Path):
    doc = docx.Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        # Standardized OpenXML Confidentiality Footer on EVERY Page
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_run = f_p.add_run("Proprietory and Confidential- Hiranyam AI Labs")
        f_run.font.name = "Arial"
        f_run.font.size = Pt(8.5)
        f_run.font.bold = True
        f_run.font.color.rgb = RGBColor(139, 0, 0)  # Maroon

    # Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("PROJECT PROPOSAL & COMMERCIAL QUOTATION")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(128, 0, 0)
    p_title.space_after = Pt(2)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Autonomous Tri-Agent AI Synthesis & Publication Framework for SK Sutras (Udyoga Sutras)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(12)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(11, 83, 148)
    p_sub.space_after = Pt(12)

    # Client Info Box
    p_meta = doc.add_paragraph()
    p_meta.add_run("Client: ").bold = True
    p_meta.add_run("Shri Shripad Kulkarni\t\t\t\t")
    p_meta.add_run("Date: ").bold = True
    p_meta.add_run("October 23, 2026\n")
    p_meta.add_run("Provider: ").bold = True
    p_meta.add_run("Hiranyam AI Labs (https://hiranyamai.com/)\t")
    p_meta.add_run("Doc Ref: ").bold = True
    p_meta.add_run("HAIL-PROP-2026-SKS01")
    p_meta.paragraph_format.space_after = Pt(14)

    # Section 1
    doc.add_heading("1. Executive Summary", level=1)
    doc.add_paragraph(
        "Hiranyam AI Labs is pleased to present this formal proposal to Shri Shripad Kulkarni for the autonomous agentic AI "
        "synthesis and publication of the authoritative comparative treatise: SK Sutras (Udyoga Sutras). This framework orchestrates "
        "the 84 Narada Bhakti Sutras and the 100 Shandilya Bhakti Sutras into a unified publication draft, formulating original "
        "Sanskrit shlokas and comprehensive Marathi Udyoga Bhashya commentary for modern enterprise and life-duty."
    )

    # Section 2
    doc.add_heading("2. The Three Specialized Agents", level=1)
    doc.add_paragraph(
        "1. Narada Bhakti Sutra Specialist Agent: Represents Devarshi Narada's experiential, devotional school (84 sutras).\n"
        "2. Shandilya Bhakti Sutra Specialist Agent: Represents Maharshi Shandilya's epistemological, Vedantic school (100 sutras in ChromaDB).\n"
        "3. Sutrakar Agent (Master Arbiter & Creative Synthesizer): Enforces non-compulsory matching, eliminates duplicate explanations, "
        "formulates original Sanskrit shlokas for verified correspondences, and authors the multi-paragraph Marathi Udyoga Bhashya."
    )

    # Section 3
    doc.add_heading("3. Two Deployment Options & Quotation", level=1)
    doc.add_paragraph(
        "Option 1: Hybrid Architecture (ChatGPT + Gemini Sutrakar)\n"
        "• Narada Agent on ChatGPT (GPT-4o), Shandilya Agent on ChatGPT (GPT-4o), Sutrakar Agent on Google Gemini (Gemini 1.5 Pro).\n"
        "• Sutrakar Agent uses Gemini for expert knowledge in Vedic literatures, classical Sanskrit translation, and huge context memory.\n"
        "• Model & Infrastructure Cost: ₹18,000 INR\n"
        "• Hiranyam AI Development, Publication & Proofreading Service Fee: ₹30,000 INR\n"
        "• Total Option 1 Investment: ₹48,000 INR\n\n"
        "Option 2: Pure Google DeepMind Gemini Specialized Architecture (Recommended)\n"
        "• All three agents deployed on Google Gemini (Gemini 1.5 Pro Specialized).\n"
        "• Deepest native corpus of Vedic literature, Sanskrit grammar, and nuanced Marathi translation.\n"
        "• Native formulation of brand-new, original metered Sanskrit shlokas (new Udyoga Sutras) for approved pairs.\n"
        "• Unified context caching ensuring zero duplicate explanations across 50 full cycles of canon re-generation.\n"
        "• Model, Deep Caching & Infrastructure Cost: ₹45,000 INR\n"
        "• Hiranyam AI Development, Publication & Proofreading Service Fee: ₹30,000 INR\n"
        "• Total Option 2 Investment: ₹75,000 INR"
    )

    # Section 4
    doc.add_heading("4. Scope of Hiranyam AI Service Commitment (₹30,000 Fee)", level=1)
    doc.add_paragraph(
        "• Full multi-agent software engineering, vector database setup, and prompt calibration.\n"
        "• Senior Citizen (65+ Mode) Web Review Portal for Shri Shripad Kulkarni with dynamic font scaling and large touch affordances.\n"
        "• Generating publication-ready PDF books for author proofreading and review.\n"
        "• Up to 50 cycles of testing, re-communication, author revisions, and corrections until the finalized print-ready copy is achieved.\n"
        "• Final pre-press typesetting and formatting ready for physical printing."
    )

    # Section 5: Quotation Table
    doc.add_heading("5. Commercial Summary Table", level=1)
    table = doc.add_table(rows=5, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Light Shading Accent 1'

    headers = ["Cost Component", "Option 1 (Hybrid)", "Option 2 (Gemini Dedicated)"]
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h

    row1 = ["AI Compute & Token Infrastructure (50 Cycles)", "₹18,000 INR", "₹45,000 INR"]
    row2 = ["Hiranyam AI Development & Publication Fee", "₹30,000 INR", "₹30,000 INR"]
    row3 = ["Proofreading PDF Delivery & Iterative Revisions", "Included", "Included (with Original Shlokas)"]
    row4 = ["TOTAL INVESTMENT", "₹48,000 INR", "₹75,000 INR"]

    for row_idx, r_data in enumerate([row1, row2, row3, row4], start=1):
        for col_idx, cell_data in enumerate(r_data):
            table.rows[row_idx].cells[col_idx].text = cell_data

    # Section 6: Acceptance
    doc.add_heading("6. Acceptance & Authorization", level=1)
    doc.add_paragraph(
        "\nClient Signature: _______________________      Date: _______________\n"
        "Shri Shripad Kulkarni\n\n"
        "Provider Signature: ____________________      Date: _______________\n"
        "Hiranyam AI Labs (https://hiranyamai.com/)"
    )

    doc.save(str(output_docx_path))
    print(f"[+] Successfully generated Proposal DOCX at: {output_docx_path.resolve()}")


def main():
    print("=" * 80)
    print(" HIRANYAM AI LABS: GENERATING FORMAL CLIENT PROPOSAL & QUOTATION")
    print(" Client: Shri Shripad Kulkarni | Project: SK Sutras (Udyoga Sutras)")
    print("=" * 80)

    pdf_path = DOCS_DIR / "PROPOSAL_SK_SUTRAS_UDYOGA_SUTRAS.pdf"
    docx_path = DOCS_DIR / "PROPOSAL_SK_SUTRAS_UDYOGA_SUTRAS.docx"

    build_pdf_proposal(pdf_path)
    build_docx_proposal(docx_path)

    print("=" * 80)
    print(" PROPOSAL GENERATION COMPLETE!")
    print(f" PDF:  {pdf_path.resolve()}")
    print(f" DOCX: {docx_path.resolve()}")
    print("=" * 80)


if __name__ == "__main__":
    main()
