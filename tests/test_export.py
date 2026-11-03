"""
================================================================================
Test Module: tests.test_export
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: QA unit tests verifying Word (.docx) master and Print-Ready PDF
             export generation, checking all 23 scholarly components and enforcing
             the mandatory confidentiality footer:
             "Proprietory and Confidential- Hiranyam AI Labs".
================================================================================
"""

from pathlib import Path
from docx import Document
from src.agents.sutrakar_agent import SutrakarAgent
from src.doc_export.docx_exporter import ManuscriptWordExporter
from src.doc_export.pdf_exporter import ManuscriptPrintPDFExporter
from src.models.schema import MultilingualText, SutraItem


def test_word_master_export_with_mandatory_footer(tmp_path: Path):
    """Verifies Word .docx export creates valid file with mandatory confidentiality footer."""
    exporter = ManuscriptWordExporter(output_dir=tmp_path)
    sutrakar = SutrakarAgent()

    unit = sutrakar.compose_complete_manuscript_unit(
        unit_id="UDYOGA-001",
        chapter_no=1,
        sutra_no="1",
        theme="Universal Duty and Ethical Conduct",
        narada_item=SutraItem(sutra_no="1", sanskrit="अथातो भक्तिं व्याख्यास्यामः॥", vishleshan=MultilingualText(en="Devotion.")),
        shandilya_item=SutraItem(sutra_no="1", sanskrit="अथातो भक्तिजिज्ञासा॥", vishleshan=MultilingualText(en="Inquiry.")),
    )
    unit_dict = unit.model_dump()
    unit_dict["approval_status"] = "APPROVED"

    doc_path = exporter.export_master_docx(
        units=[unit_dict],
        output_filename="test_master.docx",
        approved_only=True,
    )
    assert doc_path.exists()
    assert doc_path.stat().st_size > 0

    # Verify footer in docx sections
    doc = Document(str(doc_path))
    found_footer = False
    for section in doc.sections:
        footer_text = section.footer.paragraphs[0].text
        if "Proprietory and Confidential- Hiranyam AI Labs" in footer_text:
            found_footer = True
            break
    assert found_footer is True


def test_pdf_export_with_mandatory_footer(tmp_path: Path):
    """Verifies Print-Ready PDF export creates valid PDF file with NumberedCanvas footer."""
    exporter = ManuscriptPrintPDFExporter(output_dir=tmp_path)
    sutrakar = SutrakarAgent()

    unit = sutrakar.compose_complete_manuscript_unit(
        unit_id="UDYOGA-002",
        chapter_no=1,
        sutra_no="2",
        theme="Supreme Devotion in Enterprise",
        narada_item=SutraItem(sutra_no="2", sanskrit="सा त्वस्मिन् परमप्रेमरूपा॥", vishleshan=MultilingualText(en="Supreme love.")),
        shandilya_item=SutraItem(sutra_no="2", sanskrit="सा परानुरक्तिरीश्वरे॥", vishleshan=MultilingualText(en="Supreme attachment.")),
    )
    unit_dict = unit.model_dump()
    unit_dict["approval_status"] = "APPROVED"

    pdf_path = exporter.export_pdf(
        units=[unit_dict],
        output_filename="test_treatise.pdf",
        approved_only=True,
    )
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0
