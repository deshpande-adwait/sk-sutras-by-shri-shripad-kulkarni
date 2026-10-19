"""
================================================================================
Module: src.pdf.generator
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Typesetting and publication engine utilizing WeasyPrint and Noto
             Serif Devanagari for rendering comparative manuscripts into
             print-ready PDF documents.
================================================================================
"""

from pathlib import Path
from typing import List, Optional

from src.config import OUTPUT_DIR
from src.models.schema import SutraPairManuscript


class ManuscriptPDFGenerator:
    """
    ----------------------------------------------------------------------------
    Class: ManuscriptPDFGenerator
    ----------------------------------------------------------------------------
    Purpose:
        Produces publication-grade, typeset manuscripts for the Udyoga Sutra
        comparative treatise. Formats Devanagari Sanskrit verses alongside
        their English, Hindi, and Marathi expositions using Noto Serif Devanagari.

    Attributes:
        output_dir (Path): Output directory where rendered PDFs are saved.
    ----------------------------------------------------------------------------
    """

    def __init__(self, output_dir: Optional[Path] = None) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the PDF compilation generator with the specified output path.

        Parameters:
            output_dir (Optional[Path]): Directory path for saving PDF files.

        Returns:
            None
        ------------------------------------------------------------------------
        """
        self.output_dir = output_dir or OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render_html(
        self,
        pairs: List[SutraPairManuscript],
        title: str = "SK Sutras: Udyoga Sutra",
        author: str = "Shri Shripad Kulkarni",
    ) -> str:
        """
        ------------------------------------------------------------------------
        Method: render_html
        ------------------------------------------------------------------------
        Purpose:
            Generates the print-ready HTML5 document with embedded CSS typography
            specifically optimized for senior citizen readability (65+ Mode):
            - Large Devanagari typography (19-21pt) with generous line heights (1.8)
            - Prominent scholarly Marathi titles and Marathi-first exposition
            - Spelled-out HINDI and MARATHI language labels
            - High-contrast, gentle warm reading palette
            - Refined header: 'Authored by: Shri Shripad Kulkarni' and
              'Technologically supported by: Hiranyam AI Labs'
        ------------------------------------------------------------------------
        """
        items_html = ""
        for p in pairs:
            # Pre-render language sections to prevent f-string backslash syntax errors in Python 3.11
            narada_mr_html = (
                f'<div class="lang-note marathi-note"><strong>MARATHI:</strong> {p.narada_sutra.vishleshan.mr}</div>'
                if p.narada_sutra.vishleshan.mr
                else ""
            )
            narada_hi_html = (
                f'<div class="lang-note hindi-note"><strong>HINDI:</strong> {p.narada_sutra.vishleshan.hi}</div>'
                if p.narada_sutra.vishleshan.hi
                else ""
            )
            shandilya_mr_html = (
                f'<div class="lang-note marathi-note"><strong>MARATHI:</strong> {p.shandilya_sutra.vishleshan.mr}</div>'
                if p.shandilya_sutra.vishleshan.mr
                else ""
            )
            shandilya_hi_html = (
                f'<div class="lang-note hindi-note"><strong>HINDI:</strong> {p.shandilya_sutra.vishleshan.hi}</div>'
                if p.shandilya_sutra.vishleshan.hi
                else ""
            )
            bhashya_mr_html = (
                f'<div class="bhashya-block marathi-bhashya"><strong>MARATHI:</strong><br/>{p.udyoga_bhashya_synthesis.mr}</div>'
                if p.udyoga_bhashya_synthesis.mr
                else ""
            )
            bhashya_hi_html = (
                f'<div class="bhashya-block hindi-bhashya"><strong>HINDI:</strong><br/>{p.udyoga_bhashya_synthesis.hi}</div>'
                if p.udyoga_bhashya_synthesis.hi
                else ""
            )
            bhashya_en_html = (
                f'<div class="bhashya-block english-bhashya"><strong>Analysis (EN):</strong><br/>{p.udyoga_bhashya_synthesis.en}</div>'
                if p.udyoga_bhashya_synthesis.en
                else ""
            )

            items_html += f"""
            <div class="sutra-pair-container">
                <div class="pair-header">
                    <span class="pair-badge">{p.pair_id}</span>
                    <h2 class="theme-title">{p.theme}</h2>
                </div>

                <div class="comparison-grid">
                    <!-- Narada Sutra Column -->
                    <div class="sutra-card narada-card">
                        <div class="card-tag">नारद भक्ति सूत्र #{p.narada_sutra.sutra_no}</div>
                        <div class="sanskrit-verse">{p.narada_sutra.sanskrit}</div>
                        {narada_mr_html}
                        {narada_hi_html}
                        <div class="vishleshan-section">
                            <strong>Analysis (EN):</strong> {p.narada_sutra.vishleshan.en}
                        </div>
                    </div>

                    <!-- Shandilya Sutra Column -->
                    <div class="sutra-card shandilya-card">
                        <div class="card-tag">शांडिल्य भक्ति सूत्र #{p.shandilya_sutra.sutra_no}</div>
                        <div class="sanskrit-verse">{p.shandilya_sutra.sanskrit}</div>
                        {shandilya_mr_html}
                        {shandilya_hi_html}
                        <div class="vishleshan-section">
                            <strong>Analysis (EN):</strong> {p.shandilya_sutra.vishleshan.en}
                        </div>
                    </div>
                </div>

                <!-- Unified Udyoga Bhashya Synthesis -->
                <div class="synthesis-card">
                    <h3 class="synthesis-heading">उद्योग भाष्य (तुलनात्मक तात्त्विक समन्वय व जीवन-साधना)</h3>
                    <div class="synthesis-body">
                        {bhashya_mr_html}
                        {bhashya_hi_html}
                        {bhashya_en_html}
                    </div>
                </div>
            </div>
            """

        html_template = f"""<!DOCTYPE html>
<html lang="mr">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+Devanagari:wght@400;600;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400&display=swap');

        @page {{
            size: A4;
            margin: 20mm 15mm 20mm 15mm;
            @bottom-right {{
                content: counter(page);
                font-family: 'Noto Serif', serif;
                font-size: 10pt;
            }}
            @bottom-left {{
                content: "SK Sutras: Udyoga Sutra";
                font-family: 'Noto Serif', serif;
                font-size: 9pt;
                color: #555;
            }}
        }}

        body {{
            font-family: 'Noto Serif', 'Noto Serif Devanagari', serif;
            color: #1a1a1a;
            line-height: 1.85;
            font-size: 16pt;
            background-color: #faf7f2;
            margin: 0;
            padding: 0;
        }}

        .cover-header {{
            text-align: center;
            border-bottom: 3px solid #800000;
            padding-bottom: 24px;
            margin-bottom: 38px;
        }}

        .main-title {{
            font-size: 32pt;
            color: #800000;
            margin: 0 0 12px 0;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}

        .subtitle {{
            font-size: 21pt;
            color: #443322;
            margin: 8px 0 16px 0;
            font-weight: 600;
            font-family: 'Noto Serif Devanagari', serif;
        }}

        .author-line {{
            font-size: 17pt;
            color: #222222;
            margin: 6px 0;
            font-weight: 600;
        }}

        .support-line {{
            font-size: 15pt;
            color: #444444;
            margin: 5px 0;
        }}

        .support-line a {{
            color: #0b5394;
            text-decoration: none;
            font-weight: bold;
        }}

        .sutra-pair-container {{
            page-break-inside: avoid;
            margin-bottom: 40px;
            border: 2px solid #d4c5b9;
            border-radius: 8px;
            padding: 24px;
            background-color: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}

        .pair-header {{
            display: flex;
            align-items: center;
            margin-bottom: 16px;
            border-bottom: 2px dashed #c0b0a0;
            padding-bottom: 10px;
        }}

        .pair-badge {{
            background-color: #8b0000;
            color: #ffffff;
            font-size: 14pt;
            font-weight: bold;
            padding: 6px 16px;
            border-radius: 6px;
            margin-right: 14px;
        }}

        .theme-title {{
            font-size: 24pt;
            color: #7a1818;
            margin: 0;
            font-weight: 700;
            font-family: 'Noto Serif Devanagari', serif;
            display: inline-block;
        }}

        .comparison-grid {{
            display: table;
            width: 100%;
            margin-bottom: 18px;
        }}

        .sutra-card {{
            display: table-cell;
            width: 48%;
            vertical-align: top;
            background: #fdfcf9;
            padding: 20px;
            border-radius: 6px;
            border: 1.5px solid #dfd5c8;
        }}

        .narada-card {{
            margin-right: 4%;
        }}

        .card-tag {{
            font-size: 17pt;
            font-weight: 700;
            color: #7a3a0e;
            margin-bottom: 12px;
            font-family: 'Noto Serif Devanagari', serif;
        }}

        .sanskrit-verse {{
            font-family: 'Noto Serif Devanagari', serif;
            font-size: 21pt;
            font-weight: 700;
            color: #6b1414;
            background: #fdfaf6;
            padding: 14px 18px;
            border-left: 6px solid #8b0000;
            margin-bottom: 16px;
            line-height: 1.65;
        }}

        .marathi-note {{
            font-family: 'Noto Serif Devanagari', serif;
            font-size: 16.5pt;
            line-height: 1.85;
            color: #1f2937;
            margin-bottom: 14px;
            background: #fbf7ee;
            padding: 14px 16px;
            border-radius: 4px;
            border-left: 4px solid #b85d19;
        }}

        .hindi-note {{
            font-family: 'Noto Serif Devanagari', serif;
            font-size: 15.5pt;
            line-height: 1.8;
            color: #374151;
            margin-bottom: 14px;
            padding: 8px 6px;
        }}

        .vishleshan-section {{
            font-size: 15pt;
            line-height: 1.75;
            color: #4b5563;
            border-top: 1px dashed #e2d6c5;
            padding-top: 12px;
            margin-top: 12px;
        }}

        .synthesis-card {{
            background: #fbf7f0;
            border-left: 6px solid #8b0000;
            border: 1.5px solid #e2d5c3;
            border-left-width: 6px;
            padding: 24px;
            border-radius: 6px;
            margin-top: 20px;
        }}

        .synthesis-heading {{
            margin: 0 0 18px 0;
            font-size: 21pt;
            color: #7a1818;
            font-weight: bold;
            font-family: 'Noto Serif Devanagari', serif;
            border-bottom: 2px solid #e8dec8;
            padding-bottom: 12px;
        }}

        .bhashya-block {{
            margin-bottom: 18px;
            white-space: pre-line;
        }}

        .marathi-bhashya {{
            font-family: 'Noto Serif Devanagari', serif;
            font-size: 16.5pt;
            line-height: 1.9;
            color: #111827;
            background: #fffcf7;
            padding: 18px;
            border-radius: 6px;
            border: 1.5px solid #ede3d4;
        }}

        .hindi-bhashya {{
            font-family: 'Noto Serif Devanagari', serif;
            font-size: 15.5pt;
            line-height: 1.8;
            color: #1f2937;
            padding: 12px 16px;
            border-top: 1px dashed #dfd5c6;
        }}

        .english-bhashya {{
            font-size: 15pt;
            line-height: 1.75;
            color: #374151;
            border-top: 1px dashed #dfd5c6;
            padding-top: 16px;
        }}

        .footer-branding {{
            margin-top: 50px;
            text-align: center;
            font-size: 12pt;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 16px;
        }}

        .footer-branding a {{
            color: #0b5394;
            text-decoration: none;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="cover-header">
        <h1 class="main-title">{title}</h1>
        <div class="subtitle">नारद भक्ति सूत्र आणि शांडिल्य भक्ति सूत्र यांचा तात्त्विक समन्वय</div>
        <div class="author-line">Authored by: {author}</div>
        <div class="support-line">Technologically supported by: <a href="https://hiranyamai.com/" target="_blank" rel="noopener noreferrer">Hiranyam AI Labs</a></div>
    </div>

    {items_html}

    <div class="footer-branding">
        Powered by <a href="https://hiranyamai.com/" target="_blank" rel="noopener noreferrer">Hiranyam AI Labs</a>
    </div>
</body>
</html>"""
        return html_template

    def generate_pdf(
        self,
        pairs: List[SutraPairManuscript],
        output_filename: str = "udyoga_sutra_manuscript.pdf",
        title: str = "SK Sutras: Udyoga Sutra",
        author: str = "Shri Shripad Kulkarni",
    ) -> Path:
        """
        ------------------------------------------------------------------------
        Method: generate_pdf
        ------------------------------------------------------------------------
        Purpose:
            Compiles the provided manuscript pairs into a styled PDF file using
            WeasyPrint, saving the artifact to the configured output directory.

        Parameters:
            pairs (List[SutraPairManuscript]): Validated sutra pairs to compile.
            output_filename (str): Name of the generated PDF file.
            title (str): Publication title.
            author (str): Publication author attribution.

        Returns:
            Path: Absolute filesystem path to the compiled PDF document.

        Errors:
            ImportError: If weasyprint is not installed.
            Exception: If PDF compilation encounters rendering failures.

        Manual Debugging Notes:
            - If weasyprint native dependencies (Pango, Cairo) are not installed on
              the host, the raw HTML is safely saved alongside the PDF path.
        ------------------------------------------------------------------------
        """
        html_content = self.render_html(pairs=pairs, title=title, author=author)
        html_path = self.output_dir / output_filename.replace(".pdf", ".html")
        pdf_path = self.output_dir / output_filename

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(str(pdf_path))
            return pdf_path
        except Exception as exc:
            # Provide diagnostic warning and return the generated HTML representation
            print(
                f"[Hiranyam AI Typesetting Warning] WeasyPrint rendering encountered: {str(exc)}. "
                f"Generated HTML manuscript preserved at: {html_path}"
            )
            return html_path
