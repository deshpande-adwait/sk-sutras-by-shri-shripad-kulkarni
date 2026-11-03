"""
================================================================================
Module: src.doc_export.pdf_exporter
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Review and Print-Ready PDF Document Generator using ReportLab.
             Renders approved manuscript units with the mandatory confidentiality
             footer: "Proprietory and Confidential- Hiranyam AI Labs" on every page.
================================================================================
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer


class NumberedCanvas(canvas.Canvas):
    """
    ----------------------------------------------------------------------------
    Class: NumberedCanvas
    ----------------------------------------------------------------------------
    Purpose:
        Two-pass canvas that renders page numbers and the mandatory confidentiality
        footer: 'Proprietory and Confidential- Hiranyam AI Labs' centered on every page.
    ----------------------------------------------------------------------------
    """

    MANDATORY_FOOTER = "Proprietory and Confidential- Hiranyam AI Labs"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._saved_page_states: List[Any] = []

    def showPage(self) -> None:
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self) -> None:
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int) -> None:
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#777777"))

        # Mandatory footer centered
        page_width, page_height = letter
        self.drawCentredString(page_width / 2.0, 32, self.MANDATORY_FOOTER)

        # Page number on right
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(page_width - 54, 32, page_str)

        self.restoreState()


class ManuscriptPrintPDFExporter:
    """
    ----------------------------------------------------------------------------
    Class: ManuscriptPrintPDFExporter
    ----------------------------------------------------------------------------
    Purpose:
        Compiles approved Udyoga Sutra manuscript units into a formal publication-grade
        PDF document with consistent headers, margins, and confidentiality footers.
    ----------------------------------------------------------------------------
    """

    def __init__(self, output_dir: Optional[Path] = None) -> None:
        self.output_dir = output_dir or (Path(__file__).resolve().parent.parent.parent / "data" / "output" / "manuscripts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_writable_path(self, target_path: Path) -> Path:
        """Handles Windows file-locking if document is currently open in Adobe Acrobat."""
        if not target_path.exists():
            return target_path
        try:
            with open(target_path, "a+"):
                return target_path
        except (PermissionError, IOError):
            stem = target_path.stem
            ext = target_path.suffix
            for i in range(1, 100):
                alt = target_path.parent / f"{stem}_{i}{ext}"
                try:
                    with open(alt, "a+"):
                        return alt
                except (PermissionError, IOError):
                    continue
        return target_path

    def export_pdf(
        self,
        units: List[Dict[str, Any]],
        output_filename: str = "udyoga_sutra_treatise.pdf",
        approved_only: bool = True,
        title: str = "Udyoga Sutras (उद्योग सूत्राणि)",
        author: str = "Shri Shripad Kulkarni",
    ) -> Path:
        """
        Compiles the manuscript units into publication PDF.
        """
        target_path = self.output_dir / output_filename
        writable = self._get_writable_path(target_path)

        doc = SimpleDocTemplate(
            str(writable),
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#8B0000"),
            alignment=1, # Center
            spaceAfter=8,
        )

        sub_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#444444"),
            alignment=1,
            spaceAfter=14,
        )

        unit_heading_style = ParagraphStyle(
            "UnitHeading",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#8B0000"),
            spaceBefore=14,
            spaceAfter=6,
        )

        body_style = ParagraphStyle(
            "DocBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#222222"),
            spaceAfter=6,
        )

        story = []

        # Masthead
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(
            f"<b>Author & Approver:</b> {author} &bull; "
            f"<b>Technology Implementation:</b> Hiranyam AI Labs (<a href='https://hiranyamai.com/'>https://hiranyamai.com/</a>)",
            sub_style,
        ))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#8B0000"), spaceAfter=14))

        target_units = [u for u in units if u.get("approval_status") == "APPROVED"] if approved_only else units
        if not target_units:
            target_units = units

        for unit in target_units:
            u_id = unit.get("unit_id", "UDYOGA-001")
            theme = unit.get("theme", "Universal Conduct")
            s_num = unit.get("sutra_number", "1")

            story.append(Paragraph(f"उद्योग सूत्र #{s_num}: {theme} ({u_id})", unit_heading_style))
            story.append(Paragraph(
                f"<b>[Original contemporary composition]</b><br/>"
                f"<b>Sanskrit Verse:</b> {unit.get('original_sanskrit_verse', '')}<br/>"
                f"<b>Intended Meaning:</b> {unit.get('intended_meaning', '')}",
                body_style,
            ))

            story.append(Paragraph(
                f"<b>Source Narada:</b> {unit.get('narada_sutra_ref')} — {unit.get('narada_sanskrit')}<br/>"
                f"<b>Source Shandilya:</b> {unit.get('shandilya_sutra_ref')} — {unit.get('shandilya_sanskrit')}<br/>"
                f"<b>Philosophical Synthesis:</b> {unit.get('philosophical_relationship')}",
                body_style,
            ))

            story.append(Paragraph(
                f"<b>Sanskrit Analysis:</b> Padaccheda: {unit.get('padaccheda')}<br/>"
                f"Anvaya: {unit.get('anvaya')}<br/>"
                f"Chandas: {unit.get('chandas_name', 'Anushtubh')} ({unit.get('chandas_analysis')})",
                body_style,
            ))

            story.append(Paragraph(
                f"<b>Translations:</b><br/>"
                f"• English: {unit.get('translation_en')}<br/>"
                f"• Hindi: {unit.get('translation_hi')}<br/>"
                f"• Marathi: {unit.get('translation_mr')}",
                body_style,
            ))

            story.append(Paragraph(
                f"<b>Four-Fold Commentary:</b><br/>"
                f"• Nirukta: {unit.get('nirukta')}<br/>"
                f"• Vyavahara-Dharma: {unit.get('vyavahara_dharma')}<br/>"
                f"• Lokasangraha: {unit.get('lokasangraha')}<br/>"
                f"• Modern Synthesis: {unit.get('modern_leadership_synthesis')}",
                body_style,
            ))

            story.append(Paragraph(
                f"<i>Validation Status: {unit.get('validation_status', 'PASS')} | "
                f"Approval Status: {unit.get('approval_status', 'APPROVED')} ({unit.get('approved_by', author)})</i>",
                body_style,
            ))
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC"), spaceAfter=10))

        doc.build(story, canvasmaker=NumberedCanvas)
        return writable
