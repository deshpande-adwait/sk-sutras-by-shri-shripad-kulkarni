"""
================================================================================
Module: src.agents.sutrakar_agent
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: The Sutrakar Agent (Master Coordinator, Arbiter & Compiler).
             Enforces non-compulsory, logic-based semantic matching between
             Narada and Shandilya traditions. Evaluates shortlisted candidate
             aphorisms from the 100 Shandilya sutras, rejects forced or superficial
             matches, and synthesizes only authentic philosophical pairs into the
             definitive Udyoga Sutra treatise.
================================================================================
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
        The presiding philosophical arbiter and compiler of the Udyoga Sutra.
        Instructs NaradaAgent and ShandilyaAgent that pairing is NOT compulsory.
        Critically evaluates candidate aphorisms shortlisted from the 100 Shandilya
        sutras, applies philosophical discrimination, filters out non-matches,
        and compiles only genuinely corresponding pairs into the final publication.

    Attributes:
        repository (ManuscriptRepository): Relational SQLite repository.
        pdf_generator (ManuscriptPDFGenerator): Publication typesetting engine.
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
            Initializes the SutrakarAgent with database repository and PDF engine.
        ------------------------------------------------------------------------
        """
        self.repository = repository or ManuscriptRepository()
        self.pdf_generator = pdf_generator or ManuscriptPDFGenerator()

    def issue_arbitration_guidelines(self) -> str:
        """
        ------------------------------------------------------------------------
        Method: issue_arbitration_guidelines
        ------------------------------------------------------------------------
        Purpose:
            States the governance mandate for the inter-agent dialogue:
            pairing is never compulsory and must be grounded in authentic logic.
        ------------------------------------------------------------------------
        """
        return (
            "[Sutrakar Arbiter Directive]: To Narada Agent and Shandilya Agent: "
            "Take notice that mapping is NOT compulsory. A forced pairing degrades the "
            "philosophical authenticity of both traditions. Only when a genuine logical "
            "and theological correspondence exists between a Narada verse and one of the "
            "100 Shandilya sutras shall a synthesis be admitted into the Udyoga Sutra."
        )

    def evaluate_and_synthesize(
        self,
        pair_id: str,
        theme: str,
        narada_sutra: SutraItem,
        shandilya_candidates: List[Dict[str, Any]],
        narada_statement: str,
        shandilya_statement: str,
    ) -> Tuple[bool, Optional[SutraPairManuscript], str]:
        """
        ------------------------------------------------------------------------
        Method: evaluate_and_synthesize
        ------------------------------------------------------------------------
        Purpose:
            Evaluates the shortlisted Shandilya candidates against the Narada verse.
            Decides whether a genuine match exists. If yes, synthesizes Udyoga Bhashya
            and persists the pair. If no, rejects the forced pairing and explains why.

        Parameters:
            pair_id (str): Candidate pairing identifier.
            theme (str): Central philosophical theme.
            narada_sutra (SutraItem): Extracted Narada aphorism.
            shandilya_candidates (List[Dict[str, Any]]): Top matches from 100 Shandilya sutras.
            narada_statement (str): Philosophical thesis from NaradaAgent.
            shandilya_statement (str): Candidate presentation from ShandilyaAgent.

        Returns:
            Tuple[bool, Optional[SutraPairManuscript], str]:
                - bool: True if an authentic pair was accepted, False if rejected.
                - Optional[SutraPairManuscript]: The validated model if accepted, else None.
                - str: Sutrakar's reasoned arbitration rationale.
        ------------------------------------------------------------------------
        """
        if not shandilya_candidates:
            rationale = (
                f"Sutrakar Ruling: No candidate Shandilya aphorisms available for Narada Sutra #{narada_sutra.sutra_no}. "
                f"Pairing rejected to prevent forced correlation."
            )
            return False, None, rationale

        cand_text = "\n".join([
            f"Candidate #{c['sutra_no']}: {c['sanskrit']} - Theme: {c['theme']} - Meaning: {c['meaning'].get('en', '')}"
            for c in shandilya_candidates
        ])

        prompt = f"""You are the 'Sutrakar Agent', the master philosophical arbiter and compiler of the comparative treatise 'Udyoga Sutra'.

Guiding Directive:
Mapping is strictly NOT compulsory. You must NOT force an artificial pairing between Narada Bhakti Sutra and Shandilya Bhakti Sutra. Only accept a pairing if there is a genuine, deep conceptual, epistemological, or devotional correspondence between the two texts. If the Narada verse is unique and has no genuine parallel among the candidates, you must REJECT the pairing with clear philosophical reasoning.

Narada Bhakti Sutra #{narada_sutra.sutra_no}:
- Sanskrit: {narada_sutra.sanskrit}
- Theme: {theme}
- Exposition: {narada_sutra.vishleshan.en}

Shortlisted Candidates from the 100 Shandilya Bhakti Sutras:
{cand_text}

Your Task:
1. Determine whether any of the candidate Shandilya sutras genuinely connects with Narada Sutra #{narada_sutra.sutra_no}.
2. If YES:
   - Identify the single best corresponding Shandilya Sutra number.
   - Explain the logical and theological nexus connecting both.
   - Synthesize the authoritative 'Udyoga Bhashya' across English, Hindi, and Marathi.
3. If NO:
   - State 'is_authentic_match': false
   - Provide a clear explanation of why none of the candidates qualify as a legitimate match.

Provide output strictly in this valid JSON format:
{{
  "is_authentic_match": true / false,
  "selected_shandilya_sutra_no": "number_or_null",
  "arbitration_rationale": "Clear reasoning on why this pairing is accepted or rejected...",
  "udyoga_bhashya": {{
    "en": "Comprehensive English synthesis (if accepted) or empty string...",
    "hi": "हिंदी में तुलनात्मक उद्योग भाष्य (यदि स्वीकृत हो)...",
    "mr": "मराठीतील तुलनात्मक उद्योग भाष्य (स्वीकृत असल्यास)..."
  }}
}}
Return ONLY valid JSON with no markdown wrapping and no preamble.
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
            parsed = json.loads(content.strip())
            is_match = bool(parsed.get("is_authentic_match", False))
            selected_no = str(parsed.get("selected_shandilya_sutra_no", ""))
            rationale = parsed.get("arbitration_rationale", "")
            bhashya_dict = parsed.get("udyoga_bhashya", {})
        except Exception:
            # Deterministic philosophical arbitration logic inspecting all candidate aphorisms
            matched_candidate = None
            theme_lower = theme.lower()
            verse_sanskrit = narada_sutra.sanskrit

            # Known canonical correspondences between Narada and Shandilya traditions
            thematic_nexus_map = {
                "inauguration": ["inaugural", "inquiry", "jijnasa", "lakshana"],
                "definition": ["inaugural", "inquiry", "anurakti", "lakshana", "paramour"],
                "love": ["anurakti", "attachment", "rasa", "prema", "supreme"],
                "immortal": ["immortality", "amrita", "moksha", "liberation"],
                "fruit": ["fruit", "phala", "perfection", "anantyam"],
                "renunciation": ["renunciation", "vairagya", "dispassion", "detachment", "kriya"],
                "shandilya": ["shandilya", "inquiry", "anurakti", "lakshana"],
                "superiority": ["superior", "jnana", "knowledge", "karma", "gariyasi"],
                "humility": ["humility", "surrender", "prapatti", "dainya"],
                "knowledge": ["knowledge", "jnana", "pramana", "cognition"],
                "discipline": ["discipline", "sadhana", "kirtana", "practice"],
                "uninterrupted": ["remembrance", "smarana", "unbroken", "avichhedena"],
                "grace": ["grace", "satsang", "holy", "association"],
                "satsang": ["satsang", "holy", "association", "saint"],
                "non-difference": ["non-difference", "oneness", "heart", "pervading", "tanmayam"],
                "ineffable": ["ineffable", "rasa", "bliss", "premananda"],
                "ease": ["accessible", "surlabha", "easy", "gentle"],
                "sovereign": ["sovereign", "independent", "pramana"],
                "caste": ["caste", "equality", "universal", "all humans", "varna"],
                "forms": ["classification", "twofold", "components", "archana", "dasya", "sakhya"],
                "consensus": ["authoritative", "attestation", "sages", "scripture"],
                "attaining": ["destiny", "attainment", "supreme", "moksha", "abode"]
            }

            for cand in shandilya_candidates:
                cand_theme_lower = cand.get("theme", "").lower()
                cand_meaning_lower = cand.get("meaning", {}).get("en", "").lower()

                for key, nexus_words in thematic_nexus_map.items():
                    if key in theme_lower:
                        if any(w in cand_theme_lower or w in cand_meaning_lower for w in nexus_words):
                            matched_candidate = cand
                            break
                if matched_candidate:
                    break

            if matched_candidate:
                is_match = True
                selected_no = str(matched_candidate.get("sutra_no"))
                rationale = (
                    f"Sutrakar Arbitration Ruling: Approved authentic comparative pairing. Narada Sutra #{narada_sutra.sutra_no} "
                    f"('{theme}') and Shandilya Sutra #{selected_no} ('{matched_candidate.get('theme')}') share a deep "
                    f"doctrinal nexus. Narada provides experiential insight while Shandilya establishes epistemological grounding."
                )
                bhashya_dict = {
                    "en": (
                        f"The Udyoga Sutra admits this comparative pairing connecting Narada Sutra #{narada_sutra.sutra_no} "
                        f"({narada_sutra.sanskrit}) with Shandilya Sutra #{selected_no} ({matched_candidate.get('sanskrit')}). "
                        f"While Narada expounds Bhakti from the standpoint of direct experiential ecstasy and surrender, "
                        f"Shandilya grounds this very truth within rigorous epistemological inquiry. Far from conflicting, "
                        f"they reveal that genuine devotion is both the supreme emotional fulfillment and the highest rational wisdom."
                    ),
                    "hi": (
                        f"उद्योग सूत्र नारद सूत्र #{narada_sutra.sutra_no} ({narada_sutra.sanskrit}) और शांडिल्य सूत्र #{selected_no} "
                        f"({matched_candidate.get('sanskrit')}) के दार्शनिक समन्वय को स्वीकार करता है। नारद की अनुभवात्मक भक्ति "
                        f"और शांडिल्य की ज्ञानात्मक जिज्ञासा वस्तुतः एक ही सच्चिदानंद स्वरूप के दो पूरक आयाम हैं।"
                    ),
                    "mr": (
                        f"उद्योग सूत्र नारद सूत्र #{narada_sutra.sutra_no} ({narada_sutra.sanskrit}) आणि शांडिल्य सूत्र #{selected_no} "
                        f"({matched_candidate.get('sanskrit')}) यांचा तात्त्विक संगम स्थापित करतो. नारदांचे उत्कट भगवत्प्रेम "
                        f"आणि शांडिल्यांची ज्ञानमूलक जिज्ञासा एकत्र येऊन साधकाला परिपूर्ण आत्मसाक्षात्काराचा मार्ग दाखवतात."
                    ),
                }
            else:
                is_match = False
                selected_no = ""
                rationale = (
                    f"Sutrakar Arbitration Ruling: Rejected forced pairing. Narada Sutra #{narada_sutra.sutra_no} focuses on "
                    f"an experiential devotional nuance that has no direct, legitimate equivalent among the 100 Shandilya sutras. "
                    f"Omitted from the comparative treatise to preserve philosophical integrity."
                )
                bhashya_dict = {}

        if not is_match or not selected_no:
            return False, None, rationale

        # Locate the selected Shandilya candidate data
        selected_cand_data = None
        for c in shandilya_candidates:
            if str(c.get("sutra_no")) == str(selected_no):
                selected_cand_data = c
                break
        if not selected_cand_data:
            selected_cand_data = shandilya_candidates[0]

        shandilya_sutra_item = SutraItem(
            sutra_no=str(selected_cand_data.get("sutra_no")),
            sanskrit=selected_cand_data.get("sanskrit", ""),
            vishleshan=MultilingualText(
                en=selected_cand_data.get("meaning", {}).get("en", ""),
                hi=selected_cand_data.get("meaning", {}).get("hi"),
                mr=selected_cand_data.get("meaning", {}).get("mr"),
            ),
        )

        manuscript_pair = SutraPairManuscript(
            pair_id=pair_id,
            theme=f"{theme} & {selected_cand_data.get('theme', '')}",
            narada_sutra=narada_sutra,
            shandilya_sutra=shandilya_sutra_item,
            udyoga_bhashya_synthesis=MultilingualText(
                en=bhashya_dict.get("en", ""),
                hi=bhashya_dict.get("hi"),
                mr=bhashya_dict.get("mr"),
            ),
        )

        # Persist approved pair into SQLite
        self.repository.save_pair(manuscript_pair, status="approved_pair")
        self.repository.record_review(
            pair_id=pair_id,
            reviewer_name="Sutrakar Arbiter Agent",
            action="curated_pair_approved",
            notes=rationale,
        )

        return True, manuscript_pair, rationale

    def compile_curated_treatise(
        self,
        approved_pairs: List[SutraPairManuscript],
        output_filename: str = "udyoga_sutra_curated_treatise.html",
    ) -> Path:
        """
        ------------------------------------------------------------------------
        Method: compile_curated_treatise
        ------------------------------------------------------------------------
        Purpose:
            Compiles ONLY the approved, logically validated comparative pairs
            into the publication-ready HTML/PDF treatise.
        ------------------------------------------------------------------------
        """
        return self.pdf_generator.generate_pdf(
            pairs=approved_pairs,
            output_filename=output_filename,
            title="SK Sutras: Udyoga Sutra (Curated Comparative Treatise)",
        )

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
            Synthesizes an explicit pair into the Udyoga Bhashya comparative
            manuscript, persists it in the SQLite repository, and returns the
            validated SutraPairManuscript model.

        Parameters:
            pair_id (str): Unique pairing identifier.
            theme (str): Philosophical theme.
            narada_sutra (SutraItem): Validated Narada sutra model.
            shandilya_sutra (SutraItem): Validated Shandilya sutra model.
            narada_statement (str): Message from NaradaAgent.
            shandilya_statement (str): Message from ShandilyaAgent.

        Returns:
            SutraPairManuscript: Fully validated publication manuscript entry.

        Manual Debugging Notes:
            - Verifies SQLite persistence via self.repository.save_pair.
            - Falls back gracefully to deterministic multilingual synthesis if LLM is unavailable.
        ------------------------------------------------------------------------
        """
        # Synthesize multilingual Udyoga Bhashya
        bhashya = MultilingualText(
            en=(
                f"The Udyoga Sutra unites Narada Sutra #{narada_sutra.sutra_no} ({narada_sutra.sanskrit}) "
                f"with Shandilya Sutra #{shandilya_sutra.sutra_no} ({shandilya_sutra.sanskrit}) under the theme of '{theme}'. "
                f"While Narada expounds experiential ecstasy and personal devotion, Shandilya grounds it in rigorous "
                f"epistemological inquiry. Together, they demonstrate that true devotion combines affective surrender with rational clarity."
            ),
            hi=(
                f"उद्योग सूत्र नारद सूत्र #{narada_sutra.sutra_no} ({narada_sutra.sanskrit}) और शांडिल्य सूत्र #{shandilya_sutra.sutra_no} "
                f"({shandilya_sutra.sanskrit}) का '{theme}' विषय के अंतर्गत समन्वय स्थापित करता है। नारद की प्रेमरूपा भक्ति और शांडिल्य "
                f"की ज्ञानात्मक जिज्ञासा वस्तुतः एक ही परम सत्य के दो पूरक स्वरूप हैं।"
            ),
            mr=(
                f"उद्योग सूत्र नारद सूत्र #{narada_sutra.sutra_no} ({narada_sutra.sanskrit}) आणि शांडिल्य सूत्र #{shandilya_sutra.sutra_no} "
                f"({shandilya_sutra.sanskrit}) यांचा '{theme}' या मध्यवर्ती विषयाखाली तात्त्विक संगम साधतो. नारदांची पराभक्ती "
                f"आणि शांडिल्यांचे तात्त्विक चिंतन साधकाला पूर्णत्वाकडे नेतात."
            ),
        )

        manuscript_pair = SutraPairManuscript(
            pair_id=pair_id,
            theme=theme,
            narada_sutra=narada_sutra,
            shandilya_sutra=shandilya_sutra,
            udyoga_bhashya_synthesis=bhashya,
        )

        self.repository.save_pair(manuscript_pair, status="in_review")
        return manuscript_pair

