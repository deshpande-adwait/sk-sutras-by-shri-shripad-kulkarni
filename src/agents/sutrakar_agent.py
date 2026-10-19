"""
================================================================================
Module: src.agents.sutrakar_agent
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: The Sutrakar Agent (Master Coordinator & Compiler). Coordinates
             dialogue between the Narada Agent and Shandilya Agent, performs
             philosophical comparative synthesis (Udyoga Bhashya), validates
             against the canonical schema, persists records to SQLite, and
             compiles the print-ready Udyoga Sutra publication PDF.
================================================================================
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config import get_chat_model
from src.database.repository import ManuscriptRepository
from src.models.schema import MultilingualText, SutraItem, SutraPairManuscript
from src.pdf.generator import ManuscriptPDFGenerator


class SutrakarAgent:
    """
    ----------------------------------------------------------------------------
    Class: SutrakarAgent
    ----------------------------------------------------------------------------
    Purpose:
        The central presiding compiler agent that synthesizes the distinct
        philosophical perspectives of Narada Bhakti Sutra and Shandilya Bhakti
        Sutra. Harmonizes experiential love and analytical inquiry into the
        definitive 'Udyoga Bhashya', manages accumulator state in SQLite, and
        produces the final typeset PDF for human review.

    Attributes:
        repository (ManuscriptRepository): Relational persistence manager.
        pdf_generator (ManuscriptPDFGenerator): WeasyPrint publication generator.
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        repository: Optional[ManuscriptRepository] = None,
        pdf_generator: Optional[ManuscriptPDFGenerator] = None,
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the SutrakarAgent with its database repository and PDF
            generator instances.

        Parameters:
            repository (Optional[ManuscriptRepository]): SQLite repository.
            pdf_generator (Optional[ManuscriptPDFGenerator]): Typesetting engine.

        Returns:
            None
        ------------------------------------------------------------------------
        """
        self.repository = repository or ManuscriptRepository()
        self.pdf_generator = pdf_generator or ManuscriptPDFGenerator()

    def synthesize_and_compile(
        self,
        pair_id: str,
        theme: str,
        narada_sutra: SutraItem,
        shandilya_sutra: SutraItem,
        narada_statement: str,
        shandilya_statement: str,
    ) -> SutraPairManuscript:
        """
        ------------------------------------------------------------------------
        Method: synthesize_and_compile
        ------------------------------------------------------------------------
        Purpose:
            Synthesizes the paired dialogue of Narada Agent and Shandilya Agent
            into the Udyoga Bhashya across English, Hindi, and Marathi. Validates
            the resulting SutraPairManuscript model and persists it to SQLite.

        Parameters:
            pair_id (str): Unique identifier for this comparative pair.
            theme (str): Central philosophical theme.
            narada_sutra (SutraItem): Extracted Narada aphorism model.
            shandilya_sutra (SutraItem): Matched Shandilya aphorism model.
            narada_statement (str): Philosophical message from Narada Agent.
            shandilya_statement (str): Scholarly reply from Shandilya Agent.

        Returns:
            SutraPairManuscript: The fully compiled, validated manuscript pair.

        Errors:
            Exception: Caught gracefully with structured fallback synthesis.
        ------------------------------------------------------------------------
        """
        prompt = f"""You are the 'Sutrakar Agent', the master synthesizer and compiler of the 'Udyoga Sutra' comparative manuscript.

Theme: {theme}

Dialogic Input from Narada Agent:
- Verse: Narada Sutra #{narada_sutra.sutra_no} ({narada_sutra.sanskrit})
- Narada Analysis: {narada_sutra.vishleshan.en}
- Narada Thesis: "{narada_statement}"

Dialogic Input from Shandilya Agent:
- Verse: Shandilya Sutra #{shandilya_sutra.sutra_no} ({shandilya_sutra.sanskrit})
- Shandilya Analysis: {shandilya_sutra.vishleshan.en}
- Shandilya Thesis: "{shandilya_statement}"

Your Task as Sutrakar:
Synthesize both viewpoints into an authoritative 'Udyoga Bhashya' commentary. Reconcile the apparent tension between Narada's ecstatic emotional surrender (prema) and Shandilya's epistemological inquiry (jijnasa / anurakti). Show how they complete each other in the universal philosophy of Devotion.
Provide the synthesis in English, Hindi, and Marathi.

Output format must be strictly valid JSON:
{{
  "en": "Masterful English synthesis harmonizing both traditions...",
  "hi": "हिंदी में दोनों परंपराओं का दार्शनिक समन्वय...",
  "mr": "मराठीतील दोन्ही परंपरांचा तात्त्विक व अनुभवाधिष्ठित समन्वय..."
}}
Return ONLY raw JSON with no markdown formatting and no extra preamble.
"""
        try:
            llm = get_chat_model()
            res = llm.invoke(prompt)
            content = res.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            synthesis_data = json.loads(content.strip())
        except Exception:
            synthesis_data = {
                "en": (
                    f"The Udyoga Sutra synthesizes Narada Sutra #{narada_sutra.sutra_no} ({narada_sutra.sanskrit}) "
                    f"and Shandilya Sutra #{shandilya_sutra.sutra_no} ({shandilya_sutra.sanskrit}) under the theme '{theme}'. "
                    f"Narada provides the direct, ecstatic realization of love as the supreme goal, while Shandilya provides "
                    f"the epistemological foundation demonstrating that this devotion is the pinnacle of all spiritual inquiry. "
                    f"Thus, emotion and intellect culminate in an indivisible union with the Divine."
                ),
                "hi": (
                    f"उद्योग भाष्य ('{theme}'): नारद सूत्र #{narada_sutra.sutra_no} और शांडिल्य सूत्र #{shandilya_sutra.sutra_no} "
                    f"का समन्वय यह सिद्ध करता है कि प्रेम और ज्ञान एक-दूसरे के पूरक हैं। नारद का परम प्रेम और शांडिल्य की "
                    f"परानुरक्ति वस्तुतः भक्ति रूपी एक ही नदी के दो तट हैं।"
                ),
                "mr": (
                    f"उद्योग भाष्य ('{theme}'): नारद सूत्र #{narada_sutra.sutra_no} आणि शांडिल्य सूत्र #{shandilya_sutra.sutra_no} "
                    f"यांचा तात्त्विक समन्वय दाखवून देतो की भक्ती ही केवळ भावनिक नसून ज्ञानाधिष्ठित आहे. नारदांचे उत्कट प्रेम "
                    f"आणि शांडिल्यांची अखंड अनुरक्ती मिळून साधकाला परिपूर्ण मुक्तीचा अनुभव देतात."
                ),
            }

        manuscript_pair = SutraPairManuscript(
            pair_id=pair_id,
            theme=theme,
            narada_sutra=narada_sutra,
            shandilya_sutra=shandilya_sutra,
            udyoga_bhashya_synthesis=MultilingualText(
                en=synthesis_data.get("en", ""),
                hi=synthesis_data.get("hi"),
                mr=synthesis_data.get("mr"),
            ),
        )

        # Persist in SQLite
        self.repository.save_pair(manuscript_pair, status="pending_review")

        # Record audit entry
        self.repository.record_review(
            pair_id=pair_id,
            reviewer_name="Sutrakar Coordinating Agent",
            action="pending_human_review",
            notes=f"Synthesized by Sutrakar Agent from Narada Sutra #{narada_sutra.sutra_no} & Shandilya Sutra #{shandilya_sutra.sutra_no}.",
        )

        return manuscript_pair

    def compile_treatise_pdf(
        self, output_filename: str = "udyoga_sutra_compiled.pdf"
    ) -> Path:
        """
        ------------------------------------------------------------------------
        Method: compile_treatise_pdf
        ------------------------------------------------------------------------
        Purpose:
            Compiles all persisted comparative pairs from the SQLite database
            into a unified, publication-grade PDF manuscript using WeasyPrint.

        Parameters:
            output_filename (str): Target PDF filename.

        Returns:
            Path: Filesystem path to the compiled PDF document.
        ------------------------------------------------------------------------
        """
        all_pairs = self.repository.get_all_pairs()
        return self.pdf_generator.generate_pdf(
            pairs=all_pairs,
            output_filename=output_filename,
            title="SK Sutras: Udyoga Sutra",
        )
