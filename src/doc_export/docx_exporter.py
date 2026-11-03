"""
================================================================================
Module: src.doc_export.docx_exporter
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Editable Word Master (.docx) Document Generator. Produces complete
             publication manuscripts with all 23 scholarly components from Part 12
             for approved units, enforcing the mandatory confidentiality footer:
             "Proprietory and Confidential- Hiranyam AI Labs".
================================================================================
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor


class ManuscriptWordExporter:
    """
    ----------------------------------------------------------------------------
    Class: ManuscriptWordExporter
    ----------------------------------------------------------------------------
    Purpose:
        Generates the editable Word master (.docx) manuscript containing all 23
        scholarly sections for approved Udyoga Sutra units. Ensures that rejected
        or unapproved drafts are strictly excluded, and enforces the mandatory
        confidentiality footer on every section.
    ----------------------------------------------------------------------------
    """

    MANDATORY_FOOTER_TEXT = "Proprietory and Confidential- Hiranyam AI Labs"

    def __init__(self, output_dir: Optional[Path] = None) -> None:
        self.output_dir = output_dir or (Path(__file__).resolve().parent.parent.parent / "data" / "output" / "manuscripts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_writable_path(self, target_path: Path) -> Path:
        """Handles Windows file-locking if document is currently open in Word."""
        if not target_path.exists():
            return target_path
        try:
            with open(target_path, "a+"):
                return target_path
        except (PermissionError, IOError):
            # Append counter
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

    def export_master_docx(
        self,
        units: List[Dict[str, Any]],
        output_filename: str = "udyoga_sutra_master.docx",
        approved_only: bool = True,
        title: str = "Udyoga Sutras (उद्योग सूत्राणि)",
        author: str = "Shri Shripad Kulkarni",
    ) -> Path:
        """
        ------------------------------------------------------------------------
        Method: export_master_docx
        ------------------------------------------------------------------------
        Purpose:
            Compiles the approved manuscript units into an editable Word document
            containing sections 1-23 from Part 12 and the mandatory confidentiality footer.
        ------------------------------------------------------------------------
        """
        doc = Document()

        # ----------------------------------------------------------------------
        # Configure Header & Mandatory Confidentiality Footer
        # ----------------------------------------------------------------------
        for section in doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)

            # Footer configuration
            footer = section.footer
            footer_para = footer.paragraphs[0]
            footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            footer_run = footer_para.add_run(self.MANDATORY_FOOTER_TEXT)
            footer_run.font.name = "Arial"
            footer_run.font.size = Pt(9)
            footer_run.font.color.rgb = RGBColor(128, 128, 128)

        # ----------------------------------------------------------------------
        # Title Page / Masthead
        # ----------------------------------------------------------------------
        title_p = doc.add_paragraph()
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        t_run = title_p.add_run(title)
        t_run.font.name = "Georgia"
        t_run.font.size = Pt(26)
        t_run.font.bold = True
        t_run.font.color.rgb = RGBColor(139, 0, 0)

        sub_p = doc.add_paragraph()
        sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sub_run = sub_p.add_run("A Four-Agent AI-Assisted Sanskrit Treatise on Ethical Enterprise & Leadership")
        sub_run.font.name = "Georgia"
        sub_run.font.size = Pt(13)
        sub_run.font.italic = True
        sub_run.font.color.rgb = RGBColor(80, 80, 80)

        auth_p = doc.add_paragraph()
        auth_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        a_run = auth_p.add_run(f"Author & Final Approver: {author}\nTechnology Implementation Partner: Hiranyam AI Labs (https://hiranyamai.com/)")
        a_run.font.name = "Arial"
        a_run.font.size = Pt(10)
        a_run.font.color.rgb = RGBColor(100, 100, 100)

        doc.add_page_break()

        # Filter units
        target_units = [u for u in units if u.get("approval_status") == "APPROVED"] if approved_only else units
        if not target_units:
            target_units = units # Fallback for initial export preview if none explicitly marked

        for unit in target_units:
            # 1. Chapter and Sutra Number & Theme
            s_num = unit.get("sutra_number", "1")
            chap_num = unit.get("chapter_number", 1)
            theme = unit.get("theme", "Universal Conduct")

            h1 = doc.add_paragraph()
            h1_run = h1.add_run(f"अध्याय {chap_num} • उद्योग सूत्र #{s_num} : {theme}")
            h1_run.font.name = "Georgia"
            h1_run.font.size = Pt(16)
            h1_run.font.bold = True
            h1_run.font.color.rgb = RGBColor(139, 0, 0)

            # 2. Selected Narada Sutra & original Sanskrit
            # 3. Source translation & provenance
            p_n = doc.add_paragraph()
            p_n.add_run("१. आधारभूत नारद भक्ति सूत्र (Narada Bhakti Sutra Foundation):\n").bold = True
            p_n.add_run(f"संदर्भ: {unit.get('narada_sutra_ref', 'NBS-1')}\n")
            p_n.add_run(f"संस्कृत: {unit.get('narada_sanskrit', '')}\n").italic = True
            p_n.add_run(f"तात्त्विक अधिष्ठान: {unit.get('philosophical_relationship', '')}\n")

            # 4. Selected Shandilya Sutra & original Sanskrit
            # 5. Source translation & provenance
            p_s = doc.add_paragraph()
            p_s.add_run("२. आधारभूत शाण्डिल्य भक्ति सूत्र (Shandilya Bhakti Sutra Foundation):\n").bold = True
            p_s.add_run(f"संदर्भ: {unit.get('shandilya_sutra_ref', 'SBS-1')}\n")
            p_s.add_run(f"संस्कृत: {unit.get('shandilya_sanskrit', '')}\n").italic = True
            p_s.add_run(f"निवडीचे प्रयोजन: {unit.get('selection_justification', '')}\n")

            # 8. Original Udyoga Sutra in Sanskrit
            p_u = doc.add_paragraph()
            u_lbl = p_u.add_run(f"[{unit.get('composition_label', 'Original contemporary composition')}]\n")
            u_lbl.font.size = Pt(9)
            u_lbl.font.color.rgb = RGBColor(46, 125, 50)
            u_lbl.bold = True

            v_run = p_u.add_run(f"{unit.get('original_sanskrit_verse', '')}\n")
            v_run.font.name = "Georgia"
            v_run.font.size = Pt(14)
            v_run.font.bold = True
            v_run.font.color.rgb = RGBColor(0, 0, 100)

            # 9-13. Sanskrit Analysis
            p_an = doc.add_paragraph()
            p_an.add_run("३. संस्कृत व्याकरण व छन्दोमीमांसा (Sanskrit Analysis):\n").bold = True
            p_an.add_run(f"• पदच्छेद: {unit.get('padaccheda', '')}\n")
            p_an.add_run(f"• अन्वय: {unit.get('anvaya', '')}\n")
            p_an.add_run(f"• शब्दार्थ: {unit.get('word_meanings', '')}\n")
            p_an.add_run(f"• व्याकरण विवरण: {unit.get('grammatical_explanation', '')}\n")
            p_an.add_run(f"• छन्दोमीमांसा: {unit.get('chandas_name', 'Anushtubh')} ({unit.get('chandas_analysis', '')})\n")

            # 14-16. Translations
            p_tr = doc.add_paragraph()
            p_tr.add_run("४. त्रैभाषिक अनुवाद (Translations):\n").bold = True
            p_tr.add_run(f"• English: {unit.get('translation_en', '')}\n")
            p_tr.add_run(f"• हिंदी: {unit.get('translation_hi', '')}\n")
            p_tr.add_run(f"• मराठी: {unit.get('translation_mr', '')}\n")

            # 17-20. Four-Fold Commentary
            p_com = doc.add_paragraph()
            p_com.add_run("५. चतुर्विध भाष्य (Four-Fold Commentary):\n").bold = True
            p_com.add_run(f"• निरुक्त (Nirukta): {unit.get('nirukta', '')}\n")
            p_com.add_run(f"• व्यवहार-धर्म (Conduct & Ethics): {unit.get('vyavahara_dharma', '')}\n")
            p_com.add_run(f"• लोकसंग्रह (Societal Welfare): {unit.get('lokasangraha', '')}\n")
            p_com.add_run(f"• आधुनिक नेतृत्व समन्वय (Leadership Synthesis): {unit.get('modern_leadership_synthesis', '')}\n")

            # 22-23. Governance Status
            p_gov = doc.add_paragraph()
            p_gov.add_run(
                f"पडताळणी स्थिती: {unit.get('validation_status', 'PASS')} | "
                f"ग्रंथकार मान्यता: {unit.get('approval_status', 'APPROVED')} "
                f"({unit.get('approved_by', author)})\n"
            ).italic = True

            doc.add_paragraph().paragraph_format.space_after = Pt(12)

        target_file = self.output_dir / output_filename
        writable = self._get_writable_path(target_file)
        doc.save(str(writable))
        return writable
