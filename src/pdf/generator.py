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
        author: str = "Shri Shripad Kulkarni & Hiranyam AI Labs",
    ) -> str:
        """
        ------------------------------------------------------------------------
        Method: render_html
        ------------------------------------------------------------------------
        Purpose:
            Generates the semantic, print-ready HTML5 document with embedded
            CSS typography tailored for WeasyPrint and Devanagari scripts.

        Parameters:
            pairs (List[SutraPairManuscript]): Sequence of validated sutra pairs.
            title (str): Title of the publication.
            author (str): Author attribution.

        Returns:
            str: Standalone HTML markup string.
        ------------------------------------------------------------------------
        """
        items_html = ""
        for p in pairs:
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
                        <div class="vishleshan-section">
                            <strong>Analysis (EN):</strong> {p.narada_sutra.vishleshan.en}
                        </div>
                        {f'<div class="lang-note"><strong>(HI):</strong> {p.narada_sutra.vishleshan.hi}</div>' if p.narada_sutra.vishleshan.hi else ''}
                        {f'<div class="lang-note"><strong>(MR):</strong> {p.narada_sutra.vishleshan.mr}</div>' if p.narada_sutra.vishleshan.mr else ''}
                    </div>

                    <!-- Shandilya Sutra Column -->
                    <div class="sutra-card shandilya-card">
                        <div class="card-tag">शाण्डिल्य भक्ति सूत्र #{p.shandilya_sutra.sutra_no}</div>
                        <div class="sanskrit-verse">{p.shandilya_sutra.sanskrit}</div>
                        <div class="vishleshan-section">
                            <strong>Analysis (EN):</strong> {p.shandilya_sutra.vishleshan.en}
                        </div>
                        {f'<div class="lang-note"><strong>(HI):</strong> {p.shandilya_sutra.vishleshan.hi}</div>' if p.shandilya_sutra.vishleshan.hi else ''}
                        {f'<div class="lang-note"><strong>(MR):</strong> {p.shandilya_sutra.vishleshan.mr}</div>' if p.shandilya_sutra.vishleshan.mr else ''}
                    </div>
                </div>

                <!-- Unified Udyoga Bhashya Synthesis -->
                <div class="synthesis-card">
                    <h3 class="synthesis-heading">उद्योग भाष्य (Udyoga Bhashya Synthesis)</h3>
                    <div class="synthesis-body">
                        <p class="bhashya-text-en">{p.udyoga_bhashya_synthesis.en}</p>
                        {f'<p class="bhashya-text-indic"><strong>हिंदी:</strong> {p.udyoga_bhashya_synthesis.hi}</p>' if p.udyoga_bhashya_synthesis.hi else ''}
                        {f'<p class="bhashya-text-indic"><strong>मराठी:</strong> {p.udyoga_bhashya_synthesis.mr}</p>' if p.udyoga_bhashya_synthesis.mr else ''}
                    </div>
                </div>
            </div>
            """

        html_template = f"""<!DOCTYPE html>
<html lang="sa">
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
                font-size: 9pt;
            }}
            @bottom-left {{
                content: "SK Sutras: Udyoga Sutra";
                font-family: 'Noto Serif', serif;
                font-size: 8pt;
                color: #555;
            }}
        }}

        body {{
            font-family: 'Noto Serif', 'Noto Serif Devanagari', serif;
            color: #1a1a1a;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}

        .cover-header {{
            text-align: center;
            border-bottom: 2px solid #8b0000;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}

        .main-title {{
            font-size: 24pt;
            color: #8b0000;
            margin: 0;
            font-weight: 700;
        }}

        .subtitle {{
            font-size: 13pt;
            color: #444;
            margin: 8px 0;
            font-style: italic;
        }}

        .author-line {{
            font-size: 10pt;
            color: #666;
            margin: 5px 0;
        }}

        .sutra-pair-container {{
            page-break-inside: avoid;
            margin-bottom: 30px;
            border: 1px solid #d4c5b9;
            border-radius: 6px;
            padding: 16px;
            background-color: #faf8f5;
        }}

        .pair-header {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            border-bottom: 1px dashed #c0b0a0;
            padding-bottom: 6px;
        }}

        .pair-badge {{
            background-color: #8b0000;
            color: #ffffff;
            font-size: 9pt;
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 4px;
            margin-right: 12px;
        }}

        .theme-title {{
            font-size: 14pt;
            color: #2c2c2c;
            margin: 0;
            display: inline-block;
        }}

        .comparison-grid {{
            display: table;
            width: 100%;
            margin-bottom: 14px;
        }}

        .sutra-card {{
            display: table-cell;
            width: 48%;
            vertical-align: top;
            background: #ffffff;
            padding: 12px;
            border-radius: 4px;
            border: 1px solid #e0d8cf;
        }}

        .narada-card {{
            margin-right: 4%;
        }}

        .card-tag {{
            font-size: 9pt;
            font-weight: 700;
            color: #8b4513;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}

        .sanskrit-verse {{
            font-family: 'Noto Serif Devanagari', serif;
            font-size: 13pt;
            font-weight: 600;
            color: #6b1414;
            background: #fdfaf6;
            padding: 8px;
            border-left: 3px solid #8b0000;
            margin-bottom: 8px;
        }}

        .vishleshan-section {{
            font-size: 9.5pt;
            color: #2b2b2b;
            margin-bottom: 4px;
        }}

        .lang-note {{
            font-size: 9pt;
            color: #555;
            margin-top: 4px;
        }}

        .synthesis-card {{
            background: #f4eee6;
            border-left: 4px solid #b85d19;
            padding: 12px;
            border-radius: 4px;
            margin-top: 10px;
        }}

        .synthesis-heading {{
            margin: 0 0 8px 0;
            font-size: 11pt;
            color: #7a3a0e;
            font-weight: bold;
        }}

        .bhashya-text-en {{
            font-size: 10pt;
            line-height: 1.6;
            color: #1a1a1a;
            margin: 0 0 10px 0;
            white-space: pre-line;
        }}

        .bhashya-text-indic {{
            font-family: 'Noto Serif Devanagari', serif;
            font-size: 9.5pt;
            line-height: 1.6;
            color: #2b2b2b;
            margin: 8px 0;
            white-space: pre-line;
            border-top: 1px dashed #e2d6c5;
            padding-top: 8px;
        }}

        .footer-branding {{
            margin-top: 40px;
            text-align: center;
            font-size: 8.5pt;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 10px;
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
        <div class="subtitle">A Comparative Synthesis of Narada Bhakti Sutra & Shandilya Bhakti Sutra</div>
        <div class="author-line">Authored by: {author}</div>
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
        html_content = self.render_html(pairs=pairs, title=title)
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
