"""
================================================================================
Script: scripts/generate_architecture_summary_docs.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Generates the comprehensive architectural summary document for the
             Autonomous Three-Agent AI framework for authoring the new canonical
             treatise: 'SK Sutras (Udyoga Sutras)'.
             Produces:
             1. PDF Document: docs/THREE_AGENT_BOOK_ARCHITECTURE_SUMMARY.pdf
             2. Word Document: docs/THREE_AGENT_BOOK_ARCHITECTURE_SUMMARY.docx
             3. Markdown Source: docs/THREE_AGENT_BOOK_ARCHITECTURE_SUMMARY.md
             Includes:
             - Mandatory confidentiality footer: "Proprietory and Confidential- Hiranyam AI Labs".
             - Clickable links to https://hiranyamai.com/.
             - Dynamic file-locking resilience (get_writable_path) for Windows.
             - Thorough explanations of the three specialized agents, dialectic loop,
               vector database, Sanskrit meter formulation, and senior review portal.
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
            self.drawString(145, page_height - 36, "|   Architectural Summary: Three-Agent AI Treatise Authoring Framework")
            self.drawRightString(page_width - 54, page_height - 36, "Author: Shri Shripad Kulkarni")

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
        self.drawString(54, 32, "Doc Ref: HAIL-ARCH-2026-SKS01")

        self.restoreState()


def build_pdf_architecture_summary(output_pdf_path: Path):
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
    c_green = colors.HexColor("#1e7e34")

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=25,
        textColor=c_maroon,
        spaceAfter=5,
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15.5,
        textColor=c_navy,
        spaceAfter=12,
    )
    meta_style = ParagraphStyle(
        "DocMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=c_charcoal,
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=17.5,
        textColor=c_maroon,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14.5,
        textColor=c_navy,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=c_charcoal,
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4,
    )

    story = []

    # Header / Top Banner
    header_data = [
        [
            Paragraph("<b>HIRANYAM AI LABS</b><br/><font size='8' color='#555555'>Advanced Agentic AI & Cognitive Computing Solutions<br/>Official Portal: <font color='#0B5394'><u>https://hiranyamai.com/</u></font></font>", meta_style),
            Paragraph("<b>SYSTEM ARCHITECTURE SUMMARY</b><br/><font size='8.5' color='#555555'><b>Date:</b> November 03, 2026<br/><b>Document Ref:</b> HAIL-ARCH-2026-SKS01<br/><b>Classification:</b> Technical & Conceptual Treatise Specification</font>", ParagraphStyle("RightMeta", parent=meta_style, alignment=2)),
        ]
    ]
    t_header = Table(header_data, colWidths=[3.25 * inch, 3.75 * inch])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_header)
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_maroon, spaceBefore=3, spaceAfter=12))

    # Title & Metadata
    story.append(Paragraph("Autonomous Three-Agent Collaborative Architecture", title_style))
    story.append(Paragraph("Authoring the New Canonical Treatise: <i>SK Sutras (Udyoga Sutras)</i>", subtitle_style))

    client_info_data = [
        [
            Paragraph("<b>Client & Primary Author:</b>", meta_style),
            Paragraph("Shri Shripad Kulkarni", ParagraphStyle("BoldVal", parent=meta_style, fontName="Helvetica-Bold", textColor=c_maroon)),
            Paragraph("<b>Technology Partner:</b>", meta_style),
            Paragraph("Hiranyam AI Labs (notifications@hiranyamai.com)", meta_style),
        ],
        [
            Paragraph("<b>Treatise Canon:</b>", meta_style),
            Paragraph("SK Sutras (Udyoga Sutras)", meta_style),
            Paragraph("<b>System Core:</b>", meta_style),
            Paragraph("LangGraph + ChromaDB + Google Gemini 1.5 Pro", meta_style),
        ],
    ]
    t_client = Table(client_info_data, colWidths=[1.6 * inch, 2.1 * inch, 1.4 * inch, 2.1 * inch])
    t_client.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_client)
    story.append(Spacer(1, 10))

    # --------------------------------------------------------------------------
    # 1. Executive Vision & Treatise Foundation
    # --------------------------------------------------------------------------
    story.append(Paragraph("1. Executive Vision & Treatise Foundation", h1_style))
    story.append(Paragraph(
        "The visionary literary initiative conceived by <b>Shri Shripad Kulkarni</b> seeks to establish a groundbreaking "
        "philosophical bridge between ancient Indian spiritual wisdom and the contemporary ethos of enterprise, ethical commerce, "
        "and nation-building duty. The resulting treatise, <b><i>SK Sutras (Udyoga Sutras)</i></b>, synthesizes two foundational "
        "yet traditionally distinct canons of Indian spiritual philosophy:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>The 84 Narada Bhakti Sutras:</b> Representing the experiential, ecstatic, and heart-centered school of unconditional devotional surrender (<i>Parama-Prema</i>).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>The 100 Shandilya Bhakti Sutras:</b> Representing the epistemological, rational, and Vedantic school of logical inquiry and analytical devotion (<i>Bhakti-Jijnasa & Tarka</i>).",
        bullet_style
    ))
    story.append(Paragraph(
        "The ultimate deliverable is not merely a translation or commentary of old texts, but the <b>creation of a third, original canon</b>: "
        "comprising <b>brand-new metered Sanskrit shlokas</b> (new Udyoga Sutras in classical Anushtup meter) and an exhaustive, scholarly "
        "three-dimensional classical Marathi commentary (<b><i>Udyoga Bhashya</i></b>) addressing ethical entrepreneurship, corporate duty (<i>Vyavahara-Dharma</i>), and public welfare (<i>Lokasangraha</i>).",
        body_style
    ))
    story.append(Spacer(1, 6))

    # --------------------------------------------------------------------------
    # 2. Why Single-LLM Chatbots Fail (The Lesson from Mobile AI Testing)
    # --------------------------------------------------------------------------
    story.append(Paragraph("2. Why Single-LLM Chatbots Fail: The Critical Need for Three Agents", h1_style))
    story.append(Paragraph(
        "During initial conceptual prototyping on mobile phone chatbots (e.g. consumer Gemini/ChatGPT), five critical structural flaws were identified. "
        "While the core idea resonated strongly, the raw output was academically unpublishable and linguistically flawed:",
        body_style
    ))

    flaws_table_data = [
        [
            Paragraph("<b>Mobile Chatbot Failure</b>", meta_style),
            Paragraph("<b>What Happened in Practice (Real Examples)</b>", meta_style),
            Paragraph("<b>Scholarly Impact on Book</b>", meta_style),
        ],
        [
            Paragraph("<b>1. Broken Sanskrit & Grammar Blunders</b>", ParagraphStyle("FB1", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("Elementary Sandhi and declension errors (e.g. <i>'अथतो'</i> instead of <i>'अथातो'</i>, invented root forms like <i>'यल्लभध्वा'</i>, Marathi spelling <i>'मुक्ती'</i> in Sanskrit).", meta_style),
            Paragraph("Invites immediate disqualification and severe ridicule from traditional scholars (Pandits).", meta_style),
        ],
        [
            Paragraph("<b>2. Forced Compulsory 84/84 Matching</b>", ParagraphStyle("FB2", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("Forced artificial parallels across all 84 sutras (e.g. comparing sacred Vrindavan Gopikas to corporate customer retention; equating deathbed liberation to corporate mergers).", meta_style),
            Paragraph("Destroys philosophical credibility through absurd, culturally jarring analogies.", meta_style),
        ],
        [
            Paragraph("<b>3. Gross Semantic Distortion</b>", ParagraphStyle("FB3", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("Confused classical Sanskrit <i>'Vyāpāra'</i> (which means mental/physical actions) with modern shopkeeping and retail trading.", meta_style),
            Paragraph("Distorts ancient sacred scripture into crude commercial slogans.", meta_style),
        ],
        [
            Paragraph("<b>4. Context Amnesia & Cliché Recycling</b>", ParagraphStyle("FB4", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("Because sliding context memory was narrow, mobile AI repeated identical corporate figures (Satya Nadella, Jamsetji Tata) over 20 times across the chat.", meta_style),
            Paragraph("Creates repetitive, tedious reading for serious book buyers.", meta_style),
        ],
        [
            Paragraph("<b>5. Hallucinatory Instability</b>", ParagraphStyle("FB5", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("When asked to re-generate or compile all sutras at the end, the chatbot completely replaced previous verses with brand-new, unrelated text.", meta_style),
            Paragraph("Zero editorial reproducibility or stable manuscript canon.", meta_style),
        ],
    ]
    t_flaws = Table(flaws_table_data, colWidths=[2.1 * inch, 2.8 * inch, 2.1 * inch])
    t_flaws.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2EAE4")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_flaws)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>The Fundamental Solution:</b> Authoring an authoritative treatise requires an <b>autonomous team of dedicated digital specialists</b>, "
        "grounded in a strict vector database, overseen by a high-reasoning academic arbiter with full context memory.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # --------------------------------------------------------------------------
    # 3. The Three Dedicated Book Specialist AI Agents
    # --------------------------------------------------------------------------
    story.append(Paragraph("3. The Three Dedicated Book Specialist AI Agents: Personas & Roles", h1_style))
    story.append(Paragraph(
        "To achieve true scholarly depth, our architecture establishes three distinct, specialized AI personas who interact, debate, and collaborate:",
        body_style
    ))

    # Agent 1 Box
    agent1_data = [
        [
            Paragraph("<b>AGENT 1: Narada Bhakti Sutra Specialist Agent</b>", ParagraphStyle("A1Title", parent=h2_style, textColor=c_maroon, spaceBefore=0)),
        ],
        [
            Paragraph(
                "• <b>Canonical Territory:</b> The 84 Narada Bhakti Sutras.<br/>"
                "• <b>Scholarly Persona:</b> Devarshi Narada — Experiential, heart-centered devotion, supreme love (<i>Parama-Prema</i>), surrender, emotional purity, and ethical selflessness.<br/>"
                "• <b>Core Mission in Treatise:</b> Analyzes Narada's sutra with textual fidelity, extracts its devotional essence, and poses an active philosophical inquiry (<i>Udyoga Jijnasa</i>) asking how this spiritual virtue translates into human duty and courageous enterprise.",
                body_style
            )
        ]
    ]
    t_a1 = Table(agent1_data, colWidths=[7.0 * inch])
    t_a1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1.25, c_maroon),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_a1)
    story.append(Spacer(1, 6))

    # Agent 2 Box
    agent2_data = [
        [
            Paragraph("<b>AGENT 2: Shandilya Bhakti Sutra Specialist Agent</b>", ParagraphStyle("A2Title", parent=h2_style, textColor=c_navy, spaceBefore=0)),
        ],
        [
            Paragraph(
                "• <b>Canonical Territory:</b> The 100 Shandilya Bhakti Sutras (Indexed with embeddings in a ChromaDB vector store).<br/>"
                "• <b>Scholarly Persona:</b> Maharshi Shandilya — Epistemological rigor, logical Vedanta (<i>Tarka</i>), rational analysis of devotion as ultimate attachment to Ishvara (<i>Paranurakti</i>), and alignment with Vedic metaphysics.<br/>"
                "• <b>Core Mission in Treatise:</b> Performs semantic vector searches across all 100 Shandilya sutras, computes mathematical cosine distance metrics, defends the rational doctrine against weak parallels, and provides critical counter-arguments.",
                body_style
            )
        ]
    ]
    t_a2 = Table(agent2_data, colWidths=[7.0 * inch])
    t_a2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1.25, c_navy),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_a2)
    story.append(Spacer(1, 6))

    # Agent 3 Box
    agent3_data = [
        [
            Paragraph("<b>AGENT 3: Sutrakar Agent (Master Vedic Arbiter & Creative Synthesizer)</b>", ParagraphStyle("A3Title", parent=h2_style, textColor=c_dark_maroon, spaceBefore=0)),
        ],
        [
            Paragraph(
                "• <b>Canonical Territory:</b> Universal Vedic Corpus, Classical Sanskrit Grammar (Panini), Meter (Chandas), and Classical Marathi.<br/>"
                "• <b>Scholarly Persona:</b> Supreme Canonical Arbiter, Classical Grammarian, and Master Compiler (in the tradition of Maharshi Veda Vyasa).<br/>"
                "• <b>Core Fourfold Function:</b><br/>"
                "  1. <b>Non-Compulsory Matching Gate:</b> Discards superficial matches (drops ~67 non-matches; curates only authentic correspondences yielding ~17 core doctrinal anchors).<br/>"
                "  2. <b>Anti-Repetition Engine:</b> Leverages a massive 2,000,000-token context cache to ensure zero duplicate themes or analogies across the book.<br/>"
                "  3. <b>Metered Sanskrit Shloka Formulation:</b> Writes <i>brand-new Sanskrit shlokas</i> (new Udyoga Sutras) strictly conforming to classical Anushtup meter.<br/>"
                "  4. <b>Tri-Fold Marathi Udyoga Bhashya:</b> Authors scholarly commentary across <i>Nirukta</i> (etymological root), <i>Vyavahara-Dharma</i> (practical duty), and <i>Lokasangraha</i> (societal welfare).",
                body_style
            )
        ]
    ]
    t_a3 = Table(agent3_data, colWidths=[7.0 * inch])
    t_a3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 1.25, c_dark_maroon),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_a3)
    story.append(Spacer(1, 10))

    # Page Break for clean section layout
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 4. Multi-Agent Collaborative Dialectic Workflow
    # --------------------------------------------------------------------------
    story.append(Paragraph("4. The Multi-Agent Collaborative Dialectic Workflow (Step-by-Step)", h1_style))
    story.append(Paragraph(
        "The three agents operate inside an autonomous dialectic state loop (orchestrated via LangGraph). "
        "Here is the precise 7-step process that executes for every verse under consideration:",
        body_style
    ))

    workflow_steps_data = [
        [
            Paragraph("<b>Workflow Phase</b>", meta_style),
            Paragraph("<b>Executing Agent</b>", meta_style),
            Paragraph("<b>Action & Operational Outcome</b>", meta_style),
        ],
        [
            Paragraph("<b>Step 1: Proposition Phase</b>", meta_style),
            Paragraph("Narada Specialist Agent", ParagraphStyle("W1", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("Selects the target Narada Bhakti Sutra. Expounds its devotional and spiritual essence. Formulates an enterprise inquiry (<i>Udyoga Jijnasa</i>) seeking rational and metaphysical corroboration.", meta_style),
        ],
        [
            Paragraph("<b>Step 2: Vector Search & Defense</b>", meta_style),
            Paragraph("Shandilya Specialist Agent", ParagraphStyle("W2", parent=meta_style, textColor=c_navy, fontName="Helvetica-Bold")),
            Paragraph("Embeds Narada's inquiry into ChromaDB vector space. Queries the 100 indexed Shandilya sutras. Retrieves top candidates with cosine distance metrics. Explains the epistemological justification and challenges shallow interpretations.", meta_style),
        ],
        [
            Paragraph("<b>Step 3: Arbiter Deliberation Gate</b>", meta_style),
            Paragraph("Sutrakar Agent (Arbiter)", ParagraphStyle("W3", parent=meta_style, textColor=c_dark_maroon, fontName="Helvetica-Bold")),
            Paragraph("Evaluates the match. If the parallel is superficial or forced, the Sutrakar Agent <b>REJECTS</b> the match, preserving canonical integrity. If the correspondence is philosophically profound, it is <b>APPROVED</b>.", meta_style),
        ],
        [
            Paragraph("<b>Step 4: Creative Synthesis</b>", meta_style),
            Paragraph("Sutrakar Agent (Synthesizer)", ParagraphStyle("W4", parent=meta_style, textColor=c_green, fontName="Helvetica-Bold")),
            Paragraph("Composes a <b>brand-new, metered Sanskrit shloka</b> (new Udyoga Sutra in Anushtup Chandas) that unifies Narada's love with Shandilya's logic. Authors the three-layer Marathi <i>Udyoga Bhashya</i> (Nirukta, Vyavahara, Lokasangraha).", meta_style),
        ],
        [
            Paragraph("<b>Step 5: Database Persistence</b>", meta_style),
            Paragraph("System Data Layer", meta_style),
            Paragraph("Saves the validated manuscript unit into SQLite (<code>data/manuscript.db</code>) with timestamps, audit logs, and vector distance scores, guaranteeing zero ephemeral data loss.", meta_style),
        ],
        [
            Paragraph("<b>Step 6: Senior Citizen Review</b>", meta_style),
            Paragraph("Author: Shri Shripad Kulkarni", ParagraphStyle("W6", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("The author reviews the generated pair in the <b>Senior Citizen (65+ Mode) Web Portal</b> with extra-large typography. Can approve, modify, or direct a revision cycle with one click.", meta_style),
        ],
        [
            Paragraph("<b>Step 7: Automated Master Typesetting</b>", meta_style),
            Paragraph("Automated Typesetting Engine", meta_style),
            Paragraph("Compiles the approved manuscript into a pre-proofreading digital book PDF and formatted Word document, ready for the author's final publication review.", meta_style),
        ],
    ]
    t_wf = Table(workflow_steps_data, colWidths=[1.8 * inch, 1.8 * inch, 3.4 * inch])
    t_wf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EFE8DE")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_wf)
    story.append(Spacer(1, 10))

    # --------------------------------------------------------------------------
    # 5. The Anatomy of an Approved Canonical Chapter
    # --------------------------------------------------------------------------
    story.append(Paragraph("5. Anatomy of an Approved Canonical Chapter (What the Reader Sees)", h1_style))
    story.append(Paragraph(
        "Unlike raw chat text, every chapter in <b><i>SK Sutras (Udyoga Sutras)</i></b> is structured into a rigorous, publication-grade academic layout:",
        body_style
    ))

    anatomy_table_data = [
        [
            Paragraph("<b>Chapter Component</b>", meta_style),
            Paragraph("<b>Scholarly Content & Purpose</b>", meta_style),
        ],
        [
            Paragraph("<b>1. Foundational Reference I</b>", meta_style),
            Paragraph("<b>Original Narada Bhakti Sutra</b> in Devanagari Sanskrit with exact canonical numbering and literal Marathi translation.", meta_style),
        ],
        [
            Paragraph("<b>2. Foundational Reference II</b>", meta_style),
            Paragraph("<b>Original Shandilya Bhakti Sutra</b> in Devanagari Sanskrit with exact canonical numbering, ChromaDB distance metric, and Marathi translation.", meta_style),
        ],
        [
            Paragraph("<b>3. The New Udyoga Sutra</b>", ParagraphStyle("NC", parent=meta_style, textColor=c_maroon, fontName="Helvetica-Bold")),
            Paragraph("<b>Original New Sanskrit Shloka</b> composed by the Sutrakar Agent. Fully metered in classical Anushtup Chandas (8 syllables per quarter, 32 syllables total), complete with word-by-word grammatical breakdown (Anvaya).", meta_style),
        ],
        [
            Paragraph("<b>4. Tri-Fold Marathi Udyoga Bhashya</b>", ParagraphStyle("BH", parent=meta_style, textColor=c_navy, fontName="Helvetica-Bold")),
            Paragraph(
                "• <b>Nirukta (Philosophical Root):</b> Explains the etymological connection between devotional surrender and fearless duty.<br/>"
                "• <b>Vyavahara-Dharma (Enterprise Ethics):</b> Actionable principles for business leaders, workplace ethics, decision-making, and financial integrity.<br/>"
                "• <b>Lokasangraha (National Welfare):</b> How the enterprise contributes to societal harmony, self-reliance (Atmanirbharta), and nation-building.",
                meta_style
            ),
        ],
        [
            Paragraph("<b>5. Modern Leadership Synthesis</b>", meta_style),
            Paragraph("Executive reflection illustrating how the combined principle resolves modern dilemmas in management, organizational culture, and personal conduct.", meta_style),
        ],
    ]
    t_anat = Table(anatomy_table_data, colWidths=[2.2 * inch, 4.8 * inch])
    t_anat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FAF7F2")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_anat)
    story.append(Spacer(1, 10))

    # Page Break for final technical overview and deliverables
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 6. Technical Infrastructure & Model Configuration
    # --------------------------------------------------------------------------
    story.append(Paragraph("6. Underlying Technical Infrastructure & Agent Ecosystem", h1_style))
    story.append(Paragraph(
        "The multi-agent system is engineered using state-of-the-art enterprise AI frameworks to guarantee reproducibility, stability, and zero data loss:",
        body_style
    ))

    tech_box_data = [
        [
            Paragraph("<b>Core Technology Component</b>", meta_style),
            Paragraph("<b>Implementation Details & Engineering Rigor</b>", meta_style),
        ],
        [
            Paragraph("<b>Orchestration Framework</b>", meta_style),
            Paragraph("<b>LangGraph Multi-Agent StateGraph:</b> Manages state transitions, inter-agent message passing, cycle counts, and human-in-the-loop review interrupts.", meta_style),
        ],
        [
            Paragraph("<b>Vector Knowledge Base</b>", meta_style),
            Paragraph("<b>ChromaDB Vector Store:</b> Contains all 100 Shandilya Bhakti Sutras with pre-computed semantic embeddings, ensuring accurate scriptural citations without hallucination.", meta_style),
        ],
        [
            Paragraph("<b>Foundation AI Models</b>", meta_style),
            Paragraph("<b>Google Gemini 1.5 Pro Specialized:</b> Endowed with a 2,000,000-token context window, deep native Sanskrit/Marathi corpora, and advanced reasoning for classical meter formulation.", meta_style),
        ],
        [
            Paragraph("<b>Data Persistence Layer</b>", meta_style),
            Paragraph("<b>Relational SQLite Repository (data/manuscript.db):</b> Stores full version history, author feedback, review audit trails, and chapter approvals across all 50 revision cycles.", meta_style),
        ],
        [
            Paragraph("<b>Accessibility Review Interface</b>", meta_style),
            Paragraph("<b>Senior Citizen (65+ Mode) Web Portal:</b> Custom-built for Shri Shripad Kulkarni with high-contrast UI, extra-large fonts, touch-friendly 48x48dp targets, and zero technical jargon.", meta_style),
        ],
    ]
    t_tech = Table(tech_box_data, colWidths=[2.2 * inch, 4.8 * inch])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FAF7F2")),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # --------------------------------------------------------------------------
    # 7. Deliverables & Author Next Steps
    # --------------------------------------------------------------------------
    story.append(Paragraph("7. Project Deliverables & Final Output Format", h1_style))
    story.append(Paragraph(
        "Upon execution of the collaborative multi-agent framework, Shri Shripad Kulkarni receives:",
        body_style
    ))
    story.append(Paragraph(
        "1. <b>Pre-Proofreading Digital Book PDFs:</b> Beautifully typeset, publication-formatted draft volumes containing all validated sutra pairs, metered Sanskrit verses, and classical Marathi commentary.",
        bullet_style
    ))
    story.append(Paragraph(
        "2. <b>Editable Master Word Manuscript (.docx):</b> Complete editable draft formatted with standard typographical hierarchies for the author's final personal touches.",
        bullet_style
    ))
    story.append(Paragraph(
        "3. <b>Interactive Senior Citizen Review Portal:</b> Accessible web dashboard allowing the author to review, annotate, request revisions, and approve chapters at their own pace.",
        bullet_style
    ))
    story.append(Paragraph(
        "4. <b>Up to 50 Revision Cycles Included:</b> Continuous fine-tuning of commentary, translations, and shloka nuances based on author instructions until final print approval.",
        bullet_style
    ))
    story.append(Paragraph(
        "5. <b>Final Print-Ready Master PDF:</b> Formatted and delivered ready for the client's commercial printing press and publishing house (actual printing and formal publishing handled independently by client).",
        bullet_style
    ))
    story.append(Spacer(1, 14))

    # Concluding Signature Block
    sig_data = [
        [
            Paragraph("<b>Document Prepared By:</b><br/><br/><br/>_____________________________________<br/><b>Hiranyam AI Labs</b><br/>Lead Agentic Software Architect<br/>Official Portal: <a href='https://hiranyamai.com/'>https://hiranyamai.com/</a>", meta_style),
            Paragraph("<b>Presented To & Approved By:</b><br/><br/><br/>_____________________________________<br/><b>Shri Shripad Kulkarni</b><br/>Primary Author & Conceptual Creator<br/>SK Sutras: Udyoga Sutras", meta_style),
        ]
    ]
    t_sig = Table(sig_data, colWidths=[3.5 * inch, 3.5 * inch])
    t_sig.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(KeepTogether(t_sig))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated Architecture Summary PDF at: {output_pdf_path.resolve()}")


# ------------------------------------------------------------------------------
# 2. Python-Docx Generation with OpenXML Confidentiality Footer
# ------------------------------------------------------------------------------
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


def build_docx_architecture_summary(output_docx_path: Path):
    doc = docx.Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        # Mandatory Standardized OpenXML Confidentiality Footer
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
    r_title = p_title.add_run("SYSTEM ARCHITECTURAL SPECIFICATION & WORKFLOW SUMMARY")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(128, 0, 0)
    p_title.space_after = Pt(2)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Autonomous Multi-Agent AI Framework for Authoring the New Canonical Treatise: SK Sutras (Udyoga Sutras)")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(11, 83, 148)
    p_sub.space_after = Pt(10)

    # Metadata Table
    meta_table = doc.add_table(rows=2, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.style = 'Light Shading Accent 1'
    meta_cells = [
        [("Client / Primary Author:", True), ("Shri Shripad Kulkarni", False), ("Date:", True), ("November 03, 2026", False)],
        [("Technology Partner:", True), ("Hiranyam AI Labs (https://hiranyamai.com/)", False), ("Doc Ref:", True), ("HAIL-ARCH-2026-SKS01", False)]
    ]
    for r_idx, row in enumerate(meta_cells):
        for c_idx, (text, is_bold) in enumerate(row):
            cell = meta_table.rows[r_idx].cells[c_idx]
            cell.text = text
            if is_bold:
                cell.paragraphs[0].runs[0].font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Section 1
    doc.add_heading("1. Executive Vision & Treatise Foundation", level=1)
    doc.add_paragraph(
        "The visionary literary initiative conceived by Shri Shripad Kulkarni seeks to establish a groundbreaking "
        "philosophical bridge between ancient Indian spiritual wisdom and the contemporary ethos of enterprise, ethical commerce, "
        "and nation-building duty. The resulting treatise, SK Sutras (Udyoga Sutras), synthesizes two foundational yet traditionally distinct canons:\n\n"
        "• The 84 Narada Bhakti Sutras: Representing the experiential, ecstatic, and heart-centered school of unconditional devotional surrender (Parama-Prema).\n"
        "• The 100 Shandilya Bhakti Sutras: Representing the epistemological, rational, and Vedantic school of logical inquiry and analytical devotion (Bhakti-Jijnasa & Tarka).\n\n"
        "The ultimate deliverable is the creation of an authoritative third canon: comprising brand-new metered Sanskrit shlokas "
        "(new Udyoga Sutras in classical Anushtup meter) and an exhaustive classical Marathi commentary (Udyoga Bhashya) dedicated to "
        "ethical entrepreneurship, corporate duty (Vyavahara-Dharma), and public welfare (Lokasangraha)."
    )

    # Section 2
    doc.add_heading("2. Why Single-LLM Chatbots Fail: The Critical Need for Three Agents", level=1)
    doc.add_paragraph(
        "During initial conceptual prototyping on consumer mobile phone chatbots, five critical structural flaws were identified, "
        "proving that single-prompt consumer chatbots cannot author an authoritative book:"
    )

    flaws_table = doc.add_table(rows=6, cols=3)
    flaws_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    flaws_table.style = 'Light Shading Accent 1'
    flaws_headers = ["Mobile Chatbot Failure", "What Happened in Practice (Real Examples)", "Scholarly Impact on Published Book"]
    for i, h in enumerate(flaws_headers):
        cell = flaws_table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True

    flaws_data = [
        ("1. Broken Sanskrit & Grammar Blunders", "Produced elementary Sandhi and declension errors (e.g. 'अथतो' instead of 'अथातो', invented root words like 'यल्लभध्वा', Marathi spelling 'मुक्ती' in Sanskrit).", "Invites immediate disqualification and severe criticism from traditional Sanskrit scholars (Pandits)."),
        ("2. Forced Compulsory 84/84 Matching", "Forced artificial parallels across all 84 sutras where none exist (e.g. comparing sacred Vrindavan Gopikas to corporate customer retention; equating deathbed liberation to corporate mergers).", "Destroys philosophical credibility through absurd, culturally jarring analogies."),
        ("3. Gross Semantic Distortion", "Confused classical Sanskrit 'Vyāpāra' (mental/physical actions) with modern shopkeeping and retail trading.", "Distorts ancient sacred scripture into crude commercial slogans."),
        ("4. Context Amnesia & Cliché Recycling", "Sliding context limits caused repetitive recycling of identical corporate figures (Satya Nadella, Jamsetji Tata) over 20 times.", "Creates repetitive, tedious reading for serious book buyers."),
        ("5. Hallucinatory Instability", "Re-prompting the chatbot caused it to completely discard and replace previously written verses with new unrelated text.", "Zero editorial reproducibility or stable manuscript canon."),
    ]
    for r_idx, r_data in enumerate(flaws_data, start=1):
        for c_idx, text in enumerate(r_data):
            flaws_table.rows[r_idx].cells[c_idx].text = text

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Section 3
    doc.add_heading("3. The Three Dedicated Book Specialist AI Agents: Personas & Roles", level=1)
    doc.add_paragraph(
        "To achieve true scholarly depth, our architecture establishes three distinct, specialized AI personas who interact, debate, and collaborate:"
    )

    agents_table = doc.add_table(rows=4, cols=3)
    agents_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    agents_table.style = 'Light Shading Accent 1'
    agent_headers = ["Specialist AI Agent", "Canonical Scope & Persona", "Core Scholarly Responsibilities"]
    for i, h in enumerate(agent_headers):
        cell = agents_table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True

    agent_data = [
        ("Agent 1: Narada Bhakti Sutra Specialist Agent", "84 Narada Sutras\nPersona: Devarshi Narada (Experiential devotion, Parama-Prema, surrender, emotional purity)", "Analyzes Narada's sutra with textual fidelity, extracts its devotional essence, and poses an enterprise inquiry (Udyoga Jijnasa) asking how this spiritual virtue translates into human duty."),
        ("Agent 2: Shandilya Bhakti Sutra Specialist Agent", "100 Shandilya Sutras in ChromaDB\nPersona: Maharshi Shandilya (Epistemological rigor, logical Vedanta, Tarka, Paranurakti)", "Performs semantic vector searches across all 100 Shandilya sutras, computes cosine distance metrics, defends rational doctrine against weak parallels, and provides critical counter-arguments."),
        ("Agent 3: Sutrakar Agent (Master Vedic Arbiter & Synthesizer)", "Universal Vedic Corpus, Paninian Grammar & Classical Marathi\nPersona: Supreme Canonical Arbiter (in tradition of Maharshi Veda Vyasa)", "Fourfold Operation:\n1. Non-Compulsory Matching Gate: Drops ~67 non-matches; curates ~17 core anchors.\n2. Anti-Repetition Engine: 2M context cache ensuring zero duplicated themes.\n3. Metered Sanskrit Shloka Formulation: Writes original verses in Anushtup Chandas.\n4. Tri-Fold Marathi Udyoga Bhashya: Nirukta, Vyavahara-Dharma, and Lokasangraha."),
    ]
    for r_idx, r_data in enumerate(agent_data, start=1):
        for c_idx, text in enumerate(r_data):
            agents_table.rows[r_idx].cells[c_idx].text = text

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Section 4
    doc.add_heading("4. The Multi-Agent Collaborative Dialectic Workflow (Step-by-Step)", level=1)
    doc.add_paragraph(
        "The three agents operate inside an autonomous dialectic state loop (orchestrated via LangGraph). Here is the precise 7-step process that executes for every verse:"
    )

    wf_table = doc.add_table(rows=8, cols=3)
    wf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    wf_table.style = 'Light Shading Accent 1'
    wf_headers = ["Workflow Phase", "Executing Agent", "Action & Operational Outcome"]
    for i, h in enumerate(wf_headers):
        cell = wf_table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True

    wf_data = [
        ("Step 1: Proposition Phase", "Narada Specialist Agent", "Selects the target Narada Bhakti Sutra. Expounds its devotional essence. Formulates an enterprise inquiry (Udyoga Jijnasa) seeking rational and metaphysical corroboration."),
        ("Step 2: Vector Search & Defense", "Shandilya Specialist Agent", "Embeds inquiry into ChromaDB vector space. Queries the 100 indexed Shandilya sutras. Retrieves top candidates with cosine distance metrics. Explains epistemological justification."),
        ("Step 3: Arbiter Deliberation Gate", "Sutrakar Agent (Arbiter)", "Evaluates match. If the parallel is superficial or forced, the Sutrakar Agent REJECTS the match, preserving canonical integrity. If philosophically profound, it is APPROVED."),
        ("Step 4: Creative Synthesis", "Sutrakar Agent (Synthesizer)", "Composes a brand-new, metered Sanskrit shloka (new Udyoga Sutra in Anushtup Chandas) that unifies Narada's love with Shandilya's logic. Authors the three-layer Marathi Udyoga Bhashya."),
        ("Step 5: Database Persistence", "System Data Layer", "Saves the validated manuscript record into SQLite (data/manuscript.db) with timestamps, audit logs, and vector distance scores, guaranteeing zero ephemeral data loss."),
        ("Step 6: Senior Citizen Review", "Author: Shri Shripad Kulkarni", "The author reviews the generated pair in the Senior Citizen (65+ Mode) Web Portal with extra-large typography. Can approve, modify, or direct a revision cycle with one click."),
        ("Step 7: Automated Master Typesetting", "Automated Typesetting Engine", "Compiles approved manuscript into a pre-proofreading digital book PDF and formatted Word document, ready for the author's final publication review."),
    ]
    for r_idx, r_data in enumerate(wf_data, start=1):
        for c_idx, text in enumerate(r_data):
            wf_table.rows[r_idx].cells[c_idx].text = text

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Section 5
    doc.add_heading("5. Anatomy of an Approved Canonical Chapter in SK Sutras", level=1)
    doc.add_paragraph(
        "Every chapter in the treatise follows a structured scholarly layout:"
    )

    anat_table = doc.add_table(rows=6, cols=2)
    anat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    anat_table.style = 'Light Shading Accent 1'
    anat_headers = ["Chapter Component", "Scholarly Content & Purpose"]
    for i, h in enumerate(anat_headers):
        cell = anat_table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True

    anat_data = [
        ("1. Foundational Reference I", "Original Narada Bhakti Sutra in Devanagari Sanskrit with exact canonical numbering and literal Marathi translation."),
        ("2. Foundational Reference II", "Original Shandilya Bhakti Sutra in Devanagari Sanskrit with exact canonical numbering, ChromaDB distance metric, and Marathi translation."),
        ("3. The New Udyoga Sutra", "Original New Sanskrit Shloka composed by the Sutrakar Agent. Fully metered in classical Anushtup Chandas (8 syllables per quarter, 32 syllables total), complete with word-by-word grammatical breakdown (Anvaya)."),
        ("4. Tri-Fold Marathi Udyoga Bhashya", "• Nirukta: Philosophical and etymological connection between devotional surrender and fearless duty.\n• Vyavahara-Dharma: Practical principles for business leaders, workplace ethics, and financial integrity.\n• Lokasangraha: Contribution to societal harmony, self-reliance (Atmanirbharta), and nation-building."),
        ("5. Modern Leadership Synthesis", "Executive reflection illustrating how the combined principle resolves modern dilemmas in management, organizational culture, and personal conduct."),
    ]
    for r_idx, r_data in enumerate(anat_data, start=1):
        for c_idx, text in enumerate(r_data):
            anat_table.rows[r_idx].cells[c_idx].text = text

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Section 6
    doc.add_heading("6. Underlying Technical Infrastructure & Agent Ecosystem", level=1)
    tech_table = doc.add_table(rows=6, cols=2)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_table.style = 'Light Shading Accent 1'
    tech_headers = ["Technical Component", "Engineering Implementation & Academic Rigor"]
    for i, h in enumerate(tech_headers):
        cell = tech_table.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True

    tech_data = [
        ("Orchestration Framework", "LangGraph Multi-Agent StateGraph managing state, node transitions, and human-in-the-loop review interrupts."),
        ("Vector Knowledge Base", "ChromaDB storing all 100 Shandilya Sutras with pre-computed semantic embeddings, preventing scriptural hallucinations."),
        ("Foundation AI Models", "Google Gemini 1.5 Pro Specialized with 2,000,000-token context window, deep native Sanskrit/Marathi corpora, and advanced reasoning for classical meter formulation."),
        ("Persistence Layer", "Relational SQLite repository (data/manuscript.db) ensuring zero ephemeral data loss and complete revision audit trails."),
        ("Accessibility Review Interface", "Senior Citizen (65+ Mode) Web Review Portal with high-contrast UI, extra-large fonts, touch-friendly 48x48dp targets, and zero technical jargon."),
    ]
    for r_idx, r_data in enumerate(tech_data, start=1):
        for c_idx, text in enumerate(r_data):
            tech_table.rows[r_idx].cells[c_idx].text = text

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Section 7
    doc.add_heading("7. Deliverables & Next Steps for the Author", level=1)
    doc.add_paragraph(
        "1. Pre-Proofreading Digital Book PDFs: Professionally typeset draft volumes with Sanskrit verses and Marathi commentary.\n"
        "2. Editable Master Word Manuscript (.docx): Formatted for author's final personal editorial touches.\n"
        "3. Interactive Senior Citizen Review Portal: Web dashboard for chapter-by-chapter review and approvals.\n"
        "4. Up to 50 Revision Cycles Included: Complete iterative refinements based on author feedback.\n"
        "5. Final Print-Ready Master PDF: Delivered ready for commercial printing press (printing & publishing handled independently by client)."
    )

    doc.save(str(output_docx_path))
    print(f"[+] Successfully generated Architecture Summary DOCX at: {output_docx_path.resolve()}")


# ------------------------------------------------------------------------------
# 3. Markdown Document Generation
# ------------------------------------------------------------------------------
def build_markdown_architecture_summary(output_md_path: Path):
    md_content = """# Architectural Summary: Autonomous Three-Agent AI Framework
## Collaborative Authoring System for the New Canonical Treatise: *SK Sutras (Udyoga Sutras)*

> **Client & Primary Author:** Shri Shripad Kulkarni  
> **Technology Partner:** [Hiranyam AI Labs](https://hiranyamai.com/)  
> **Document Reference ID:** `HAIL-ARCH-2026-SKS01`  
> **Date:** November 03, 2026  
> **Confidentiality Notice:** *Proprietory and Confidential- Hiranyam AI Labs*  

---

### 1. Executive Vision & Treatise Foundation

The visionary literary initiative conceived by **Shri Shripad Kulkarni** seeks to establish a groundbreaking philosophical bridge between ancient Indian spiritual wisdom and the contemporary ethos of enterprise, ethical commerce, and nation-building duty. 

The resulting treatise, **_SK Sutras: Udyoga Sutras_**, synthesizes two foundational yet traditionally distinct canons of Indian spiritual philosophy:
1. **The 84 Narada Bhakti Sutras:** Representing the experiential, ecstatic, and heart-centered school of unconditional devotional surrender (*Parama-Prema*).
2. **The 100 Shandilya Bhakti Sutras:** Representing the epistemological, rational, and Vedantic school of logical inquiry and analytical devotion (*Bhakti-Jijnasa & Tarka*).

The ultimate deliverable is not merely a translation of old texts, but the **creation of an authoritative third canon**:
* **Brand-New Metered Sanskrit Shlokas** (*new Udyoga Sutras*) composed strictly in classical Anushtup meter (*Chandas*) and Paninian grammar.
* **Exhaustive Classical Marathi Commentary** (*Udyoga Bhashya*) structured across *Nirukta* (etymology/philosophy), *Vyavahara-Dharma* (practical enterprise ethics), and *Lokasangraha* (societal welfare and nation-building).

---

### 2. Why Single-LLM Chatbots Fail: The Critical Need for Three Agents

During initial conceptual prototyping on consumer mobile phone chatbots (e.g. standard Gemini/ChatGPT), five critical structural flaws emerged, proving that single-prompt chatbots cannot author an authoritative book:

| # | Flaw Observed on Mobile Chatbot | Technical & Textual Manifestation | Scholarly Impact on Published Book |
|---|---|---|---|
| **1** | **Broken Sanskrit & Grammar Blunders** | Produced elementary Sandhi and declension errors (e.g. *'अथतो'* instead of *'अथातो'*, invented non-existent roots like *'यल्लभध्वा'*, vernacular Marathi spelling *'मुक्ती'* in Sanskrit). | Invites immediate disqualification and severe criticism from traditional Sanskrit scholars (*Pandits*). |
| **2** | **Forced Compulsory 84/84 Matching** | Forced artificial parallels across all 84 sutras where none exist (e.g. comparing sacred Vrindavan Gopikas to corporate customer retention; equating deathbed liberation to corporate mergers). | Destroys philosophical credibility through absurd, culturally jarring analogies. |
| **3** | **Gross Semantic Distortion** | Confused classical Sanskrit *'Vyāpāra'* (which means mental/physical actions) with modern shopkeeping and retail trading. | Distorts ancient sacred scripture into crude commercial slogans. |
| **4** | **Context Amnesia & Cliché Recycling** | Sliding context limits caused repetitive recycling of identical corporate figures (Satya Nadella, Jamsetji Tata) over 20 times. | Creates repetitive, tedious reading for serious book buyers. |
| **5** | **Hallucinatory Instability** | Re-prompting the chatbot caused it to completely discard and replace previously written verses with new unrelated text. | Zero editorial reproducibility or stable manuscript canon. |

**The Solution:** Authoring an authoritative treatise requires an **autonomous team of dedicated digital specialists**, grounded in a strict vector database, overseen by a high-reasoning academic arbiter with full context memory.

---

### 3. The Three Dedicated Book Specialist AI Agents: Personas & Roles

Our architecture establishes three distinct, specialized AI personas who interact, debate, and collaborate:

```
┌────────────────────────────────────────────────────────────────────────┐
│               1. Narada Bhakti Sutra Specialist Agent                   │
│   • Canon: 84 Narada Bhakti Sutras                                     │
│   • Perspective: Devarshi Narada (Experiential & Ecstatic Devotion)    │
│   • Function: Studies verses, explains devotion, poses inquiries       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼ (Philosophical Proposition: Udyoga Jijnasa)
┌────────────────────────────────────────────────────────────────────────┐
│              2. Shandilya Bhakti Sutra Specialist Agent                 │
│   • Canon: 100 Shandilya Bhakti Sutras (Indexed in ChromaDB)           │
│   • Perspective: Maharshi Shandilya (Rational Epistemology & Tarka)    │
│   • Function: Searches database, finds matches, defends logic          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼ (Candidate Matches & Cosine Distance Scores)
┌────────────────────────────────────────────────────────────────────────┐
│                        3. Sutrakar Agent                               │
│      (Master Coordinator, Arbiter & Creative Synthesizer)              │
│   • Perspective: Supreme Vedic Arbiter & Canonical Compiler            │
│   • Non-Compulsory Matching Gate: Rejects ~67 weak/forced matches      │
│   • Anti-Repetition Gate: 2M-token memory ensures zero duplicate themes│
│   • Composes Original Sanskrit Shlokas: Metered in Anushtup Chandas    │
│   • Authors Comprehensive Marathi Commentary: 3-fold Udyoga Bhashya    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼ (Validated Manuscript Record)
┌────────────────────────────────────────────────────────────────────────┐
│                  Senior Citizen (65+ Mode) Portal                      │
│   • Hosted on SQLite repository (data/manuscript.db)                   │
│   • Shri Shripad Kulkarni reviews, approves, or directs revisions      │
│   • Automated Pre-Proofreading Book PDF & Word Delivery                │
└────────────────────────────────────────────────────────────────────────┘
```

#### Detailed Agent Specifications:

1. **Agent 1: Narada Bhakti Sutra Specialist Agent**
   * **Domain:** 84 Narada Bhakti Sutras.
   * **Persona:** Devarshi Narada — Experiential, heart-centered devotion, supreme love (*Parama-Prema*), surrender, emotional purity, and ethical selflessness.
   * **Operation:** Analyzes Narada's sutra with textual fidelity, extracts its devotional essence, and poses an enterprise inquiry (*Udyoga Jijnasa*) asking how this spiritual virtue translates into human duty and courageous enterprise.

2. **Agent 2: Shandilya Bhakti Sutra Specialist Agent**
   * **Domain:** 100 Shandilya Bhakti Sutras (Indexed in ChromaDB vector store).
   * **Persona:** Maharshi Shandilya — Epistemological rigor, logical Vedanta (*Tarka*), rational analysis of devotion as ultimate attachment to Ishvara (*Paranurakti*), and alignment with Vedic metaphysics.
   * **Operation:** Performs semantic vector searches across all 100 Shandilya sutras, computes mathematical cosine distance metrics, defends the rational doctrine against weak parallels, and provides critical counter-arguments.

3. **Agent 3: Sutrakar Agent (Master Vedic Arbiter & Creative Synthesizer)**
   * **Domain:** Universal Vedic Corpus, Paninian Grammar, Classical Chandas, and Classical Marathi.
   * **Persona:** Supreme Canonical Arbiter, Classical Grammarian, and Master Compiler (in the tradition of Maharshi Veda Vyasa).
   * **Fourfold Operation:**
     - **Non-Compulsory Matching Gate:** Discards superficial matches (drops ~67 non-matches; curates only authentic correspondences yielding ~17 core doctrinal anchors).
     - **Anti-Repetition Engine:** Leverages a massive 2,000,000-token context cache to ensure zero duplicate themes or corporate analogies across the book.
     - **Metered Sanskrit Shloka Formulation:** Writes *brand-new Sanskrit shlokas* (new Udyoga Sutras) strictly conforming to classical Anushtup meter (8 syllables per quarter).
     - **Tri-Fold Marathi Udyoga Bhashya:** Authors scholarly commentary across *Nirukta* (etymological root), *Vyavahara-Dharma* (practical duty), and *Lokasangraha* (societal welfare).

---

### 4. The Multi-Agent Collaborative Dialectic Workflow (Step-by-Step)

The three agents operate inside an autonomous dialectic state loop (orchestrated via LangGraph). Here is the precise 7-step process that executes for every verse:

1. **Step 1: Proposition Phase (Narada Agent)**  
   Selects the target Narada Bhakti Sutra. Expounds its devotional and spiritual essence. Formulates an enterprise inquiry (*Udyoga Jijnasa*) seeking rational and metaphysical corroboration.
2. **Step 2: Vector Search & Defense Phase (Shandilya Agent)**  
   Embeds Narada's inquiry into ChromaDB vector space. Queries the 100 indexed Shandilya sutras. Retrieves top candidates with cosine distance metrics. Explains the epistemological justification and challenges shallow interpretations.
3. **Step 3: Arbiter Deliberation Gate (Sutrakar Agent)**  
   Evaluates the match. If the parallel is superficial or forced, the Sutrakar Agent **REJECTS** the match, preserving canonical integrity. If the correspondence is philosophically profound, it is **APPROVED**.
4. **Step 4: Creative Synthesis Phase (Sutrakar Agent)**  
   Composes a **brand-new, metered Sanskrit shloka** (new Udyoga Sutra in Anushtup Chandas) that unifies Narada's love with Shandilya's logic. Authors the three-layer Marathi *Udyoga Bhashya* (*Nirukta*, *Vyavahara-Dharma*, *Lokasangraha*).
5. **Step 5: Database Persistence Phase (System Data Layer)**  
   Saves the validated manuscript unit into SQLite (`data/manuscript.db`) with timestamps, audit logs, and vector distance scores, guaranteeing zero ephemeral data loss.
6. **Step 6: Senior Citizen Review Phase (Author: Shri Shripad Kulkarni)**  
   The author reviews the generated pair in the **Senior Citizen (65+ Mode) Web Portal** with extra-large typography. Can approve, modify, or direct a revision cycle with one click.
7. **Step 7: Automated Master Typesetting Phase**  
   Compiles the approved manuscript into a pre-proofreading digital book PDF and formatted Word document, ready for the author's final publication review.

---

### 5. Anatomy of an Approved Canonical Chapter (What the Reader Sees)

Every chapter in **_SK Sutras (Udyoga Sutras)_** is structured into a rigorous, publication-grade academic layout:

1. **Foundational Reference I:** Original Narada Bhakti Sutra in Devanagari Sanskrit with exact canonical numbering and literal Marathi translation.
2. **Foundational Reference II:** Original Shandilya Bhakti Sutra in Devanagari Sanskrit with exact canonical numbering, ChromaDB distance metric, and Marathi translation.
3. **The New Udyoga Sutra:** Original New Sanskrit Shloka composed by the Sutrakar Agent. Fully metered in classical Anushtup Chandas (8 syllables per quarter, 32 syllables total), complete with word-by-word grammatical breakdown (Anvaya).
4. **Tri-Fold Marathi Udyoga Bhashya:**
   * **Nirukta (Philosophical Root):** Explains the etymological connection between devotional surrender and fearless duty.
   * **Vyavahara-Dharma (Enterprise Ethics):** Actionable principles for business leaders, workplace ethics, decision-making, and financial integrity.
   * **Lokasangraha (National Welfare):** How the enterprise contributes to societal harmony, self-reliance (*Atmanirbharta*), and nation-building.
5. **Modern Leadership Synthesis:** Executive reflection illustrating how the combined principle resolves modern dilemmas in management, organizational culture, and personal conduct.

---

### 6. Underlying Technical Infrastructure & Agent Ecosystem

| Technology Layer | Implementation & Tools | Architectural Purpose & Rigor |
|---|---|---|
| **Agent Orchestration** | LangGraph Multi-Agent StateGraph | Manages state transitions, inter-agent dialogue loops, cycle counts, and human-in-the-loop review interrupts. |
| **Vector Knowledge Base** | ChromaDB Vector Store | Contains all 100 Shandilya Sutras with pre-computed semantic embeddings, preventing scriptural hallucinations. |
| **Foundation AI Models** | Google Gemini 1.5 Pro Specialized | 2,000,000-token context window, deep native Sanskrit/Marathi corpora, advanced reasoning for classical meter formulation. |
| **Data Persistence Layer** | SQLite (`data/manuscript.db`) | Stores immutable version history, author feedback, review audit trails, and chapter approvals across 50 revision cycles. |
| **Accessibility Portal** | Senior Citizen (65+ Mode) Web Interface | Custom-built for Shri Shripad Kulkarni with high-contrast UI, extra-large fonts, 48x48dp touch targets, and zero technical jargon. |

---

### 7. Project Deliverables & Next Steps for the Author

1. **Pre-Proofreading Digital Book PDFs:** Beautifully typeset, publication-formatted draft volumes containing all validated sutra pairs, metered Sanskrit verses, and classical Marathi commentary.
2. **Editable Master Word Manuscript (.docx):** Complete editable draft formatted with standard typographical hierarchies for the author's final personal touches.
3. **Interactive Senior Citizen Review Portal:** Accessible web dashboard allowing the author to review, annotate, request revisions, and approve chapters at their own pace.
4. **Up to 50 Revision Cycles Included:** Continuous fine-tuning of commentary, translations, and shloka nuances based on author instructions until final print approval.
5. **Final Print-Ready Master PDF:** Formatted and delivered ready for commercial printing press (actual printing and formal publishing handled independently by client).

---
*Proprietory and Confidential- Hiranyam AI Labs*
"""
    output_md_path.write_text(md_content.strip() + "\n", encoding="utf-8")
    print(f"[+] Successfully generated Architecture Summary Markdown at: {output_md_path.resolve()}")


# ------------------------------------------------------------------------------
# 4. Dynamic Path Probe for File Locking Resilience on Windows
# ------------------------------------------------------------------------------
def get_writable_path(target_path: Path) -> Path:
    """
    Resolves a safe, non-locked target file path for writing deliverables on
    Windows systems where PDF viewers (such as Adobe Acrobat Reader) or Word
    processors enforce exclusive write-locks on currently opened documents.
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
    print("=" * 80)
    print(" HIRANYAM AI LABS: GENERATING ARCHITECTURE SUMMARY DELIVERABLES")
    print(" Project: SK Sutras (Udyoga Sutras) | Author: Shri Shripad Kulkarni")
    print("=" * 80)

    base_pdf = DOCS_DIR / "THREE_AGENT_BOOK_ARCHITECTURE_SUMMARY.pdf"
    base_docx = DOCS_DIR / "THREE_AGENT_BOOK_ARCHITECTURE_SUMMARY.docx"
    base_md = DOCS_DIR / "THREE_AGENT_BOOK_ARCHITECTURE_SUMMARY.md"

    pdf_out = get_writable_path(base_pdf)
    docx_out = get_writable_path(base_docx)

    if pdf_out != base_pdf:
        print(f"[!] Primary PDF '{base_pdf.name}' is locked by a viewer. Writing to: '{pdf_out.name}'")
    if docx_out != base_docx:
        print(f"[!] Primary DOCX '{base_docx.name}' is locked. Writing to: '{docx_out.name}'")

    build_pdf_architecture_summary(pdf_out)
    build_docx_architecture_summary(docx_out)
    build_markdown_architecture_summary(base_md)

    print("=" * 80)
    print(" ARCHITECTURE SUMMARY GENERATION COMPLETE!")
    print(f" PDF Deliverable:  {pdf_out.resolve()}")
    print(f" DOCX Deliverable: {docx_out.resolve()}")
    print(f" MD Deliverable:   {base_md.resolve()}")
    print("=" * 80)


if __name__ == "__main__":
    main()
