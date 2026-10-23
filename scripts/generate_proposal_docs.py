"""
================================================================================
Script: scripts/generate_proposal_docs.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates the formal, publication-grade client proposal and quotation
             for Shri Shripad Kulkarni in both PDF and DOCX formats.
             Includes:
             - Layman-friendly section titles (Three Book Specialists, Solution Options).
             - Option 1 (ChatGPT + Gemini Sutrakar): Exactly Rs. 45,678 INR
               (Rs. 18,000 AI Infra + Rs. 27,678 Development & Service Fee).
             - Option 2 (Pure Google Gemini Specialized): Exactly Rs. 78,910 INR
               (Rs. 45,000 AI Infra + Rs. 33,910 Development & Service Fee).
             - Separate development fees explicitly stated per option.
             - Proofreading & physical printing clarified as handled by client.
             - Pre-proofreading PDF book delivery & 50 cycles of revisions included.
             - All currency symbols rendered as 'Rs.' to guarantee zero font glyph errors.
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
        fontSize=23,
        leading=27,
        textColor=c_maroon,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16.5,
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
        fontSize=14.5,
        leading=18.5,
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
        fontSize=8.5,
        leading=13,
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
    story.append(Paragraph("Autonomous Multi-Agent AI Synthesis & Digital Draft Framework for <i>SK Sutras: Udyoga Sutras</i>", subtitle_style))

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
            Paragraph("Pre-Proofreading Digital Book PDFs & Revisions", meta_style),
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
        "Hiranyam AI Labs is privileged to present this formal proposal and quotation to <b>Shri Shripad Kulkarni</b> "
        "for the complete research, synthesis, and multi-agent AI engineering workflow of the monumental philosophical treatise: "
        "<b><i>SK Sutras: Udyoga Sutras</i></b>.",
        body_style
    ))
    story.append(Paragraph(
        "The objective of this project is to orchestrate a pioneering doctrinal synthesis between two foundational canons of Indian spiritual philosophy—the "
        "<b>84 Narada Bhakti Sutras</b> (representing experiential devotion) and the <b>100 Shandilya Bhakti Sutras</b> (representing rational, "
        "epistemological Vedantic inquiry). Through a dedicated team of three specialized AI agents, these traditions are systematically cross-examined, "
        "filtered against false overlaps, and unified into an authoritative new treatise featuring <b>original Sanskrit shlokas</b> and in-depth classical "
        "<b>Marathi Udyoga Bhashya</b> commentary dedicated to modern workplace ethics and human duty.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # --------------------------------------------------------------------------
    # 2. How the Three Dedicated Book Specialists AI Agents Work Together
    # --------------------------------------------------------------------------
    story.append(Paragraph("2. How the Three Dedicated Book Specialists AI Agents Work Together", h1_style))
    story.append(Paragraph(
        "Instead of relying on a single AI that tries to do everything at once, our system divides the work between three specialized digital scholars. "
        "Each book has its own dedicated specialist agent, and a third coordinator oversees the entire conversation to ensure deep authenticity and zero duplicate matches:",
        body_style
    ))

    agents_table_data = [
        [
            Paragraph("<b>Specialist Role</b>", meta_style),
            Paragraph("<b>Assigned Book / Domain</b>", meta_style),
            Paragraph("<b>What This Specialist Does in Plain Words</b>", meta_style),
        ],
        [
            Paragraph("<b>1. Narada Bhakti Sutra Specialist Agent</b>", ParagraphStyle("AN1", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("<b>84 Narada Sutras</b><br/>(Devotional Love & Surrender)", meta_style),
            Paragraph("Acts as the champion of pure devotion (Parama-Prema). It studies each of the 84 Narada verses, explains its emotional and spiritual meaning, and poses thoughtful philosophical questions to the Shandilya specialist.", meta_style),
        ],
        [
            Paragraph("<b>2. Shandilya Bhakti Sutra Specialist Agent</b>", ParagraphStyle("AN2", parent=meta_style, textColor=c_navy, fontName="Helvetica-Bold")),
            Paragraph("<b>100 Shandilya Sutras</b><br/>(Logic & Vedantic Inquiry)", meta_style),
            Paragraph("Acts as the master of scriptural logic (Bhakti-Jijnasa). It searches the complete 100 Shandilya sutras in our specialized database, finds the closest conceptual matches, and explains the rational philosophy behind them.", meta_style),
        ],
        [
            Paragraph("<b>3. Sutrakar Agent</b><br/>(Master Coordinator, Arbiter & Synthesizer)", ParagraphStyle("AN3", parent=meta_style, textColor=c_dark_maroon, fontName="Helvetica-Bold")),
            Paragraph("<b>Vedic Synthesis & New Udyoga Sutras</b>", meta_style),
            Paragraph("Acts as the master editor and judge between the two specialists:<br/>"
                      "• <b>Prevents Forced Matches:</b> Rejects weak parallels where verses do not truly match (67 non-matches omitted).<br/>"
                      "• <b>Prevents Repetitions:</b> Ensures no verse or explanation is repeated twice anywhere in the book.<br/>"
                      "• <b>Composes Original Sanskrit Shlokas:</b> When an authentic match is found, it <b>composes a brand-new Sanskrit shloka (new Udyoga Sutra)</b>.<br/>"
                      "• <b>Authors Comprehensive Marathi Commentary:</b> Writes in-depth Marathi Udyoga Bhashya connecting the verses to daily enterprise, workplace ethics, and inner peace.", meta_style),
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
    # 3. Technology Choices and Solution Options Explained
    # --------------------------------------------------------------------------
    story.append(Paragraph("3. Technology Choices and Solution Options Explained", h1_style))
    story.append(Paragraph(
        "To provide clear choices in capabilities and budget, we offer two distinct solution options based on leading commercial artificial intelligence engines:",
        body_style
    ))

    # Option 1 Callout Box
    opt1_box_data = [
        [
            Paragraph("<b>OPTION 1: Hybrid Solution (ChatGPT for Two Books + Google Gemini for Master Coordinator)</b>", ParagraphStyle("Opt1Title", parent=h2_style, textColor=c_navy, spaceBefore=0)),
        ],
        [
            Paragraph(
                "<b>How the Models Are Assigned:</b><br/>"
                "• <b>Narada Specialist:</b> OpenAI ChatGPT (GPT-4o)<br/>"
                "• <b>Shandilya Specialist:</b> OpenAI ChatGPT (GPT-4o)<br/>"
                "• <b>Sutrakar Master Coordinator:</b> Google Gemini (Gemini 1.5 Pro)<br/><br/>"
                "<b>Why This Setup Works:</b><br/>"
                "ChatGPT handles the active question-and-answer dialogue between the two books with speed and clarity. "
                "The <b>Sutrakar Master Coordinator is powered by Google Gemini</b> because Google Gemini has an enormous memory "
                "(up to 2,000,000 words at once). This allows the master coordinator to keep the entire book in mind continuously, "
                "ensuring that no explanation is ever repeated and that all Vedic references are carefully checked.<br/><br/>"
                "<b>Commercial Investment (Option 1):</b><br/>"
                "• AI Cloud Compute & Model Infrastructure (50 full cycles): <b>Rs. 18,000 INR</b> (approx. $215 USD)<br/>"
                "• Hiranyam AI Development and Service Fee: <b>Rs. 27,678 INR</b> (approx. $329 USD)<br/>"
                "• <b>Total Proposed Investment (Option 1): Rs. 45,678 INR</b> (approx. $544 USD)",
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
    story.append(KeepTogether(t_opt1))

    # Dedicated PageBreak for Option 2 Box to ensure it sits cleanly on its own separate page
    story.append(PageBreak())

    # Option 2 Callout Box (Consistently styled in Blue c_navy, exactly matching Option 1)
    opt2_box_data = [
        [
            Paragraph("<b>OPTION 2: Dedicated Google Gemini Vedic Specialist Solution (Recommended)</b>", ParagraphStyle("Opt2Title", parent=h2_style, textColor=c_navy, spaceBefore=0)),
        ],
        [
            Paragraph(
                "<b>How the Models Are Assigned:</b><br/>"
                "• <b>Narada Specialist:</b> Google Gemini (Gemini 1.5 Pro Specialized)<br/>"
                "• <b>Shandilya Specialist:</b> Google Gemini (Gemini 1.5 Pro Specialized)<br/>"
                "• <b>Sutrakar Master Coordinator:</b> Google Gemini (Gemini 1.5 Pro Advanced High-Reasoning)<br/><br/>"
                "<b>Why This Option Is Superior for Ancient Scriptures:</b><br/>"
                "Option 2 gives all three specialists deep Vedic and Sanskrit expertise:<br/>"
                "1. <b>Vast Knowledge of Indian Scriptures:</b> Google has digitized millions of ancient Indian books, Sanskrit commentaries, and Marathi historical texts through its global library archives.<br/>"
                "2. <b>Composes Brand-New Sanskrit Shlokas:</b> When an authentic match is approved, Gemini possesses the unique ability to <b>write brand-new, poetically metered Sanskrit verses (new Udyoga Sutras)</b> for the client's new book.<br/>"
                "3. <b>Authentic Classical Marathi:</b> Writes dignified, classical Marathi commentary (Bhavartha) naturally, without unnatural English-sounding phrasing.<br/>"
                "4. <b>Unified Memory Across 50 Full Cycles:</b> All three specialists share the exact same brain architecture, allowing completely seamless coordination across 50 full cycles of re-running and fine-tuning.<br/><br/>"
                "<b>Commercial Investment (Option 2):</b><br/>"
                "• AI Cloud Compute, Deep Caching, High-Reasoning & Infrastructure: <b>Rs. 45,000 INR</b> (approx. $535 USD)<br/>"
                "• Hiranyam AI Development and Service Fee: <b>Rs. 33,910 INR</b> (approx. $404 USD)<br/>"
                "• <b>Total Proposed Investment (Option 2): Rs. 78,910 INR</b> (approx. $939 USD)",
                body_style
            )
        ]
    ]
    t_opt2 = Table(opt2_box_data, colWidths=[7.0 * inch])
    t_opt2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1.5, c_navy),  # Blue border matching Option 1
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(KeepTogether(t_opt2))
    story.append(Spacer(1, 14))

    # --------------------------------------------------------------------------
    # 4. Scope of Services Covered under Hiranyam AI Development and Service Fees
    # --------------------------------------------------------------------------
    story.append(Paragraph("4. Scope of Services Covered under Hiranyam AI Development and Service Fees", h1_style))
    story.append(Paragraph(
        "Our development and service fees cover the complete technical software engineering, database setup, "
        "and digital draft delivery up to the stage of the client's proofreading. The specific fee applies according to the option chosen:",
        body_style
    ))

    fee_box_data = [
        [
            Paragraph("<b>Under Option 1 (Hybrid Solution):</b>", meta_style),
            Paragraph("Hiranyam AI Development and Service Fee is <b>Rs. 27,678 INR</b>", ParagraphStyle("F1", parent=meta_style, textColor=c_navy, fontName="Helvetica-Bold")),
        ],
        [
            Paragraph("<b>Under Option 2 (Gemini Specialized):</b>", meta_style),
            Paragraph("Hiranyam AI Development and Service Fee is <b>Rs. 33,910 INR</b>", ParagraphStyle("F2", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
        ],
    ]
    t_fee_box = Table(fee_box_data, colWidths=[2.8 * inch, 4.2 * inch])
    t_fee_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_fee_box)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>What Is Covered Under Our Service Fee:</b>", h2_style))
    scope_points = [
        "<b>Multi-Agent Software Engineering:</b> Building and fine-tuning the automated coordination system connecting the Narada, Shandilya, and Sutrakar specialists.",
        "<b>Scriptural Database Setup (ChromaDB):</b> Indexing all 100 Shandilya verses and 84 Narada verses for instant mathematical comparison and retrieval.",
        "<b>Senior Citizen (65+ Mode) Web Review Portal:</b> Setting up an easy-to-use digital reading portal for Shri Shripad Kulkarni with extra-large fonts, high contrast, and simple buttons.",
        "<b>Pre-Proofreading Book PDF Deliveries:</b> Generating clean, beautifully typeset digital PDF drafts containing Sanskrit verses and Marathi commentary for the client's internal proofreading.",
        "<b>Up to 50 Full Cycles of Re-running & Author Corrections:</b> Executing all adjustments, re-evaluations, and re-arbitration runs per author feedback until the final text is approved.",
        "<b>Delivery of Final Digital Master PDF:</b> Providing the finalized digital PDF manuscript ready for the client's publication and printing team.",
    ]
    for pt in scope_points:
        story.append(Paragraph(f"• {pt}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Note on Client Responsibilities: Actual proofreading, physical printing, bookbinding, and formal book publishing "
        "will be handled independently by the client. Hiranyam AI Labs delivers all digital manuscript materials ready up to the proofreading stage.</i>",
        callout_style
    ))

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
            Paragraph("<b>Milestone 1: Project Kickoff & Setup</b>", meta_style),
            Paragraph("Database indexing of 184 sutras, setup of three specialists, and launch of Senior Citizen portal.", meta_style),
            Paragraph("Week 1", meta_style),
            Paragraph("<b>40%</b> of Service Fee + AI Infra Deposit", meta_style),
        ],
        [
            Paragraph("<b>Milestone 2: Delivery of Pre-Proofreading Draft PDF</b>", meta_style),
            Paragraph("Complete batch execution of all 84 Narada verses against 100 Shandilya verses. Delivery of first complete pre-proofreading book PDF for client review.", meta_style),
            Paragraph("Week 2", meta_style),
            Paragraph("<b>30%</b> of Service Fee", meta_style),
        ],
        [
            Paragraph("<b>Milestone 3: Client Proofreading & Revisions</b>", meta_style),
            Paragraph("Author reviews verses in portal and conducts proofreading. Multi-agent revisions and re-runs executed per author guidance.", meta_style),
            Paragraph("Weeks 3 – 4", meta_style),
            Paragraph("—", meta_style),
        ],
        [
            Paragraph("<b>Milestone 4: Final Approval & Master PDF Handover</b>", meta_style),
            Paragraph("Final approval by Shri Shripad Kulkarni. Delivery of finalized master PDF manuscript ready for client's publishing team.", meta_style),
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
            Paragraph("<b>Option 1: Hybrid Solution<br/>(ChatGPT + Gemini Sutrakar)</b>", meta_style),
            Paragraph("<b>Option 2: Gemini Specialized<br/>(All Agents on Google Gemini)</b>", meta_style),
        ],
        [
            Paragraph("<b>Autonomous AI Cloud Compute & Infrastructure</b><br/>(50 full canon passes, multi-million token volume, database hosting)", meta_style),
            Paragraph("Rs. 18,000 INR<br/><font size='8' color='#666'>($215 USD approx.)</font>", meta_style),
            Paragraph("Rs. 45,000 INR<br/><font size='8' color='#666'>($535 USD approx.)</font>", meta_style),
        ],
        [
            Paragraph("<b>Hiranyam AI Development and Service Fee</b><br/>(Software engineering, portal, pre-proofreading PDFs, up to 50 revisions)", meta_style),
            Paragraph("<b>Rs. 27,678 INR</b><br/><font size='8' color='#666'>($329 USD approx.)</font>", meta_style),
            Paragraph("<b>Rs. 33,910 INR</b><br/><font size='8' color='#666'>($404 USD approx.)</font>", meta_style),
        ],
        [
            Paragraph("<b>Original Sanskrit Shloka Formulation</b>", meta_style),
            Paragraph("Standard Synthesis", meta_style),
            Paragraph("<b>Included (Original Sanskrit Shlokas)</b>", meta_style),
        ],
        [
            Paragraph("<b>Pre-Proofreading PDF Deliveries & 50 Rework Cycles</b>", meta_style),
            Paragraph("Included till Final Master Delivery", meta_style),
            Paragraph("Included till Final Master Delivery", meta_style),
        ],
        [
            Paragraph("<b>TOTAL PROPOSED INVESTMENT</b>", ParagraphStyle("TotalLabel", parent=meta_style, fontName="Helvetica-Bold", fontSize=10.5, textColor=c_maroon)),
            Paragraph("<b>Rs. 45,678 INR</b><br/><font size='8.5' color='#555'>($544 USD)</font>", ParagraphStyle("TotalVal1", parent=meta_style, fontName="Helvetica-Bold", fontSize=11, textColor=c_navy)),
            Paragraph("<b>Rs. 78,910 INR</b><br/><font size='8.5' color='#555'>($939 USD)</font>", ParagraphStyle("TotalVal2", parent=meta_style, fontName="Helvetica-Bold", fontSize=11, textColor=c_maroon)),
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
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<i>*Note: Proofreading, physical printing, bookbinding, and formal publishing will be arranged independently by the client. "
        "Hiranyam AI Labs delivers the finalized master digital PDF ready for printing upon completion of revisions.</i>",
        callout_style
    ))
    story.append(Spacer(1, 14))

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
                Paragraph("<b>[  ] Option 1 (Rs. 45,678 INR)</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>[  ] Option 2 (Rs. 78,910 INR)</b>", meta_style),
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
    r_sub = p_sub.add_run("Autonomous Multi-Agent AI Synthesis & Digital Draft Framework for SK Sutras (Udyoga Sutras)")
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
        "synthesis and digital draft preparation of the authoritative comparative treatise: SK Sutras (Udyoga Sutras). This framework orchestrates "
        "the 84 Narada Bhakti Sutras and the 100 Shandilya Bhakti Sutras into a unified digital draft, formulating original "
        "Sanskrit shlokas and comprehensive Marathi Udyoga Bhashya commentary for modern enterprise and life-duty."
    )

    # Section 2
    doc.add_heading("2. How the Three Dedicated Book Specialists AI Agents Work Together", level=1)
    doc.add_paragraph(
        "1. Narada Bhakti Sutra Specialist Agent: Represents Devarshi Narada's experiential devotional school (84 sutras).\n"
        "2. Shandilya Bhakti Sutra Specialist Agent: Represents Maharshi Shandilya's epistemological, rational school (100 sutras in ChromaDB).\n"
        "3. Sutrakar Agent (Master Coordinator & Synthesizer): Enforces non-compulsory matching, eliminates duplicate explanations, "
        "composes original Sanskrit shlokas for verified correspondences, and authors the multi-paragraph Marathi Udyoga Bhashya commentary."
    )

    # Section 3
    doc.add_heading("3. Technology Choices and Solution Options Explained", level=1)
    doc.add_paragraph(
        "Option 1: Hybrid Solution (ChatGPT for Two Books + Google Gemini for Master Coordinator)\n"
        "• Narada Agent on ChatGPT (GPT-4o), Shandilya Agent on ChatGPT (GPT-4o), Sutrakar Agent on Google Gemini (Gemini 1.5 Pro).\n"
        "• Sutrakar Agent uses Gemini for expert knowledge in Vedic literatures, classical Sanskrit, and massive context memory.\n"
        "• AI Compute & Cloud Infrastructure (50 cycles): Rs. 18,000 INR\n"
        "• Hiranyam AI Development and Service Fee: Rs. 27,678 INR\n"
        "• Total Option 1 Proposed Investment: Rs. 45,678 INR\n\n"
        "Option 2: Dedicated Google Gemini Vedic Specialist Solution (Recommended)\n"
        "• All three specialists deployed on Google Gemini (Gemini 1.5 Pro Specialized).\n"
        "• Deepest native corpus of Vedic literature, Sanskrit grammar, and classical Marathi commentary.\n"
        "• Composes brand-new, original metered Sanskrit shlokas (new Udyoga Sutras) for approved pairs.\n"
        "• Unified context caching ensuring zero duplicate explanations across 50 full cycles of canon re-generation.\n"
        "• AI Compute, Deep Caching, High-Reasoning & Infrastructure: Rs. 45,000 INR\n"
        "• Hiranyam AI Development and Service Fee: Rs. 33,910 INR\n"
        "• Total Option 2 Proposed Investment: Rs. 78,910 INR"
    )

    # Section 4
    doc.add_heading("4. Scope of Services Covered under Hiranyam AI Development and Service Fees", level=1)
    doc.add_paragraph(
        "Development and Service Fee by Option:\n"
        "• Under Option 1: Hiranyam AI Development and Service Fee is Rs. 27,678 INR\n"
        "• Under Option 2: Hiranyam AI Development and Service Fee is Rs. 33,910 INR\n\n"
        "Included in Our Service Fee:\n"
        "• Multi-agent software engineering, ChromaDB vector database setup, and prompt calibration.\n"
        "• Senior Citizen (65+ Mode) Web Review Portal for Shri Shripad Kulkarni with extra-large fonts and simple layout.\n"
        "• Pre-proofreading digital book PDF delivery with Devanagari Sanskrit verses and Marathi commentary for client review.\n"
        "• Up to 50 cycles of testing, re-communication, author revisions, and corrections until the final text is approved.\n"
        "• Delivery of finalized digital master PDF ready for client's publishing team.\n\n"
        "*Note: Actual proofreading, physical printing, bookbinding, and publishing will be handled independently by the client."
    )

    # Section 5: Quotation Table
    doc.add_heading("5. Commercial Summary Table", level=1)
    table = doc.add_table(rows=6, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Light Shading Accent 1'

    headers = ["Cost Component", "Option 1 (Hybrid Solution)", "Option 2 (Gemini Dedicated)"]
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h

    row1 = ["AI Cloud Compute & Infrastructure (50 Cycles)", "Rs. 18,000 INR", "Rs. 45,000 INR"]
    row2 = ["Hiranyam AI Development and Service Fee", "Rs. 27,678 INR", "Rs. 33,910 INR"]
    row3 = ["Original Sanskrit Shloka Formulation", "Standard Synthesis", "Included (Original Sanskrit Shlokas)"]
    row4 = ["Pre-Proofreading PDF Deliveries & 50 Revisions", "Included till Master Delivery", "Included till Master Delivery"]
    row5 = ["TOTAL PROPOSED INVESTMENT", "Rs. 45,678 INR", "Rs. 78,910 INR"]

    for row_idx, r_data in enumerate([row1, row2, row3, row4, row5], start=1):
        for col_idx, cell_data in enumerate(r_data):
            table.rows[row_idx].cells[col_idx].text = cell_data

    # Section 6: Acceptance
    doc.add_heading("6. Acceptance & Authorization", level=1)
    doc.add_paragraph(
        "\nAccepted Option:  [  ] Option 1 (Rs. 45,678 INR)       [  ] Option 2 (Rs. 78,910 INR)\n\n"
        "Client Signature: _______________________      Date: _______________\n"
        "Shri Shripad Kulkarni\n\n"
        "Provider Signature: ____________________      Date: _______________\n"
        "Hiranyam AI Labs (https://hiranyamai.com/)"
    )

    doc.save(str(output_docx_path))
    print(f"[+] Successfully generated Proposal DOCX at: {output_docx_path.resolve()}")


def get_writable_path(target_path: Path) -> Path:
    """
    =============================================================================
    FUNCTION: get_writable_path
    =============================================================================
    PURPOSE:
        Resolves a safe, non-locked target file path for writing deliverables on
        Windows systems where PDF viewers (such as Adobe Acrobat Reader) or Word
        processors enforce exclusive write-locks on currently opened documents.

    PARAMETERS:
        target_path (Path): Desired target file path.

    RETURNS:
        Path: A path guaranteed or tested to be available for write access. If the
              base path is locked, it systematically tests fallback variations
              (_REVISED, _v2, _v3, etc.) until an unlocked filename is secured.

    MANUAL DEBUGGING NOTES:
        If Adobe Acrobat or Word locks the primary proposal file, Windows raises
        PermissionError (Errno 13). This function prevents build crashes by
        gracefully redirecting the output to a versioned path while alerting the user.
    =============================================================================
    """
    if not target_path.exists():
        return target_path

    # Probe primary path with append mode
    try:
        with open(target_path, "a+"):
            pass
        return target_path
    except PermissionError:
        pass

    parent = target_path.parent
    stem = target_path.stem
    ext = target_path.suffix

    # Probe _REVISED path
    revised = parent / f"{stem}_REVISED{ext}"
    try:
        if not revised.exists():
            return revised
        with open(revised, "a+"):
            pass
        return revised
    except PermissionError:
        pass

    # Probe versioned increments: _v2, _v3, _v4...
    counter = 2
    while True:
        candidate = parent / f"{stem}_v{counter}{ext}"
        try:
            if not candidate.exists():
                return candidate
            with open(candidate, "a+"):
                pass
            return candidate
        except PermissionError:
            counter += 1


def main():
    """
    =============================================================================
    ROUTINE: main
    =============================================================================
    PURPOSE:
        Orchestrates the generation of client proposal documents in both PDF and
        Word (.docx) formats, complete with dynamic path probing for file-lock
        resilience on Windows.
    =============================================================================
    """
    print("=" * 80)
    print(" HIRANYAM AI LABS: GENERATING REVISED PROPOSAL & QUOTATION")
    print(" Client: Shri Shripad Kulkarni | Project: SK Sutras (Udyoga Sutras)")
    print("=" * 80)

    base_pdf = DOCS_DIR / "PROPOSAL_SK_SUTRAS_UDYOGA_SUTRAS.pdf"
    base_docx = DOCS_DIR / "PROPOSAL_SK_SUTRAS_UDYOGA_SUTRAS.docx"

    pdf_out = get_writable_path(base_pdf)
    docx_out = get_writable_path(base_docx)

    if pdf_out != base_pdf:
        print(f"[!] Primary PDF '{base_pdf.name}' is locked by a viewer. Writing to: '{pdf_out.name}'")
    if docx_out != base_docx:
        print(f"[!] Primary DOCX '{base_docx.name}' is locked. Writing to: '{docx_out.name}'")

    build_pdf_proposal(pdf_out)
    build_docx_proposal(docx_out)

    print("=" * 80)
    print(" REVISED PROPOSAL GENERATION COMPLETE!")
    print(f" PDF Deliverable:  {pdf_out.resolve()}")
    print(f" DOCX Deliverable: {docx_out.resolve()}")
    print("=" * 80)


if __name__ == "__main__":
    main()


