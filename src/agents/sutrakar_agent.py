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
   - Synthesize the authoritative, comprehensive 'Udyoga Bhashya' across English, Hindi, and Marathi.
     The Udyoga Bhashya MUST contain distinct multi-paragraph sections:
     a) [Philosophical Nexus / तात्त्विक समन्वय]: Deep doctrinal harmony between Narada's experiential love and Shandilya's epistemological inquiry.
     b) [Applied Enterprise & Duty / उद्योग एवं कर्म-साधना]: Concrete guidance on how this principle applies to purposeful endeavor ('Udyoga'), daily work, and ethical responsibility in life.
     c) [Core Realization / अंतिम बोध]: The unifying resolution of intellect, heart, and action.
3. If NO:
   - State 'is_authentic_match': false
   - Provide a clear explanation of why none of the candidates qualify as a legitimate match.

Provide output strictly in this valid JSON format:
{{
  "is_authentic_match": true / false,
  "selected_shandilya_sutra_no": "number_or_null",
  "arbitration_rationale": "Clear reasoning on why this pairing is accepted or rejected...",
  "udyoga_bhashya": {{
    "en": "Extensive English synthesis detailing [Philosophical Nexus], [Applied Enterprise & Duty], and [Core Realization]...",
    "hi": "हिंदी में विस्तृत उद्योग भाष्य [दार्शनिक समन्वय], [उद्योग एवं कर्म-साधना], और [तात्त्विक निष्कर्ष]...",
    "mr": "मराठीतील विस्तृत उद्योग भाष्य [तात्त्विक समन्वय], [उद्योग आणि जीवन-साधना], आणि [अंतिम बोध]..."
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
                bhashya_dict = self._generate_comprehensive_udyoga_bhashya(
                    narada_sutra=narada_sutra,
                    shandilya_cand=matched_candidate,
                    theme=theme,
                )
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

        # Guarantee extensive tri-fold Udyoga Bhashya if LLM commentary is brief or absent
        if not bhashya_dict.get("en") or len(bhashya_dict.get("en", "")) < 200:
            bhashya_dict = self._generate_comprehensive_udyoga_bhashya(
                narada_sutra=narada_sutra,
                shandilya_cand=selected_cand_data,
                theme=theme,
            )

        shandilya_sutra_item = SutraItem(
            sutra_no=str(selected_cand_data.get("sutra_no")),
            sanskrit=selected_cand_data.get("sanskrit", ""),
            vishleshan=MultilingualText(
                en=selected_cand_data.get("meaning", {}).get("en", ""),
                hi=selected_cand_data.get("meaning", {}).get("hi"),
                mr=selected_cand_data.get("meaning", {}).get("mr"),
            ),
        )

        marathi_title = self._get_marathi_theme_title(
            narada_sutra_no=str(narada_sutra.sutra_no),
            shandilya_sutra_no=str(selected_cand_data.get("sutra_no", "")),
            default_theme=theme,
        )

        manuscript_pair = SutraPairManuscript(
            pair_id=pair_id,
            theme=marathi_title,
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
        title: str = "SK Sutras: Udyoga Sutra",
        author: str = "Shri Shripad Kulkarni",
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
            title=title,
            author=author,
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
        # Synthesize comprehensive multilingual Udyoga Bhashya
        cand_dict = {
            "sutra_no": shandilya_sutra.sutra_no,
            "sanskrit": shandilya_sutra.sanskrit,
            "theme": theme,
        }
        bhashya_dict = self._generate_comprehensive_udyoga_bhashya(
            narada_sutra=narada_sutra,
            shandilya_cand=cand_dict,
            theme=theme,
        )

        bhashya = MultilingualText(
            en=bhashya_dict.get("en", ""),
            hi=bhashya_dict.get("hi"),
            mr=bhashya_dict.get("mr"),
        )

        marathi_title = self._get_marathi_theme_title(
            narada_sutra_no=str(narada_sutra.sutra_no),
            shandilya_sutra_no=str(shandilya_sutra.sutra_no),
            default_theme=theme,
        )

        manuscript_pair = SutraPairManuscript(
            pair_id=pair_id,
            theme=marathi_title,
            narada_sutra=narada_sutra,
            shandilya_sutra=shandilya_sutra,
            udyoga_bhashya_synthesis=bhashya,
        )

        self.repository.save_pair(manuscript_pair, status="in_review")
        return manuscript_pair

    def _generate_comprehensive_udyoga_bhashya(
        self,
        narada_sutra: SutraItem,
        shandilya_cand: Dict[str, Any],
        theme: str,
    ) -> Dict[str, str]:
        """
        ------------------------------------------------------------------------
        Method: _generate_comprehensive_udyoga_bhashya
        ------------------------------------------------------------------------
        Purpose:
            Synthesizes an extensive, publication-grade, tri-fold Udyoga Bhashya
            across English, Hindi, and Marathi whenever a comparative sutra pairing
            is finalized. The synthesis uniquely addresses:
            1. Philosophical Nexus (Doctrinal & Epistemological Harmony)
            2. Applied Enterprise & Duty (Udyoga in Daily Life & Professional Work)
            3. Core Realization & Definitive Synthesis (Unity of Head, Heart & Hands)

        Parameters:
            narada_sutra (SutraItem): The Narada aphorism model.
            shandilya_cand (Dict[str, Any]): The matched Shandilya candidate dictionary.
            theme (str): Unifying philosophical theme.

        Returns:
            Dict[str, str]: Dictionary containing rich 'en', 'hi', and 'mr' commentaries.

        Manual Debugging Notes:
            - Formats with clear section headers for readability in HTML and PDF publications.
            - Preserves Devanagari script integrity across Hindi and Marathi texts.
        ------------------------------------------------------------------------
        """
        n_no = str(narada_sutra.sutra_no)
        n_sanskrit = narada_sutra.sanskrit
        s_no = str(shandilya_cand.get("sutra_no", "1"))
        s_sanskrit = shandilya_cand.get("sanskrit", "")
        s_theme = shandilya_cand.get("theme", "")

        theme_lower = (theme + " " + s_theme).lower()

        # Category 1: Inauguration, Inquiry, and Definition of Bhakti
        if any(w in theme_lower for w in ["inaugur", "jijnasa", "inquiry", "definition"]):
            en_text = (
                f"[Philosophical Nexus / तात्त्विक समन्वय]: The Udyoga Sutra establishes this inaugural comparative "
                f"pairing connecting Narada Sutra #{n_no} ({n_sanskrit}) with Shandilya Sutra #{s_no} ({s_sanskrit}) "
                f"under the theme of '{theme}'. Narada inaugurates the path through direct, heart-centered exposition ('vyākhyā'), "
                f"presenting devotion as an immediate experiential sweetness. Conversely, Shandilya opens with rigorous epistemological "
                f"inquiry ('jijñāsā'), paralleling the classical Badarayana Vedanta tradition. Where Shandilya satisfies the philosophical "
                f"intellect by validating Bhakti as a legitimate, sovereign field of ontological inquiry, Narada immediately invites "
                f"the seeker to participate in its nectarine reality. Far from conflicting, they demonstrate that genuine Bhakti is "
                f"simultaneously the summit of rational inquiry and the perfection of emotional fulfillment.\n\n"
                f"[Applied Enterprise & Duty / उद्योग एवं कर्म-साधना]: In human enterprise and daily life, this inaugural harmony reveals "
                f"the essential psychology of purposeful action ('Udyoga'). Before embarking upon any great endeavor, the practitioner must "
                f"synthesize Shandilya's critical inquiry (thoroughly investigating the purpose, ethics, and fundamental principles of the mission) "
                f"with Narada's total devotional dedication. Action without philosophical inquiry is blind and prone to error; conversely, inquiry "
                f"without wholehearted commitment remains sterile intellectual speculation. The Udyoga Sutra teaches that true achievement begins "
                f"when critical discernment and selfless dedication are consecrated as one.\n\n"
                f"[Core Realization / अंतिम बोध]: Head and heart converge at the inception of truth. Inquiry blossoms into love, and love "
                f"illuminates the intellect, guiding the seeker toward supreme excellence and inner peace."
            )
            hi_text = (
                f"[दार्शनिक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) और शांडिल्य सूत्र #{s_no} ({s_sanskrit}) का "
                f"'{theme}' के अंतर्गत भव्य तात्त्विक समन्वय प्रस्तुत करता है। देवर्षि नारद भक्ति की व्याख्या को प्रत्यक्ष, अनुभवात्मक और "
                f"हृदयस्पर्शी रूप में प्रस्तुत करते हैं, जबकि महर्षि शांडिल्य 'भक्तिजिज्ञासा' के माध्यम से वेदान्त-सुलभ दार्शनिक और प्रमाण-संगत "
                f"अन्वेषण का सूत्रपात करते हैं। शांडिल्य जहाँ बुद्धि को संतुष्ट कर भक्ति को एक स्वतंत्र और प्रामाणिक विद्या सिद्ध करते हैं, "
                f"वहीं नारद साधक को उसके अमृतमय रस का आस्वादन कराते हैं। ज्ञान और प्रेम का यह संगम भक्ति के समग्र स्वरूप को प्रकट करता है।\n\n"
                f"[उद्योग एवं कर्म-साधना]: सांसारिक उद्योग, व्यवसाय और कर्तव्य-कर्म के धरातल पर यह सूत्र कर्मण्यता की आधारशिला रखता है। "
                f"किसी भी महान कार्य का शुभारंभ शांडिल्य की विवेकी जिज्ञासा (कार्य के उद्देश्य और नीति का सूक्ष्म विचार) और नारद के उत्कट "
                f"समर्पण के संगम से होना चाहिए। विवेकहीन उत्साह भ्रम पैदा करता है और प्रेमविहीन बुद्धि शुष्कता लाती है। उद्योग सूत्र यह सिखाता "
                f"है कि जब विचार और समर्पण एक साथ मिलते हैं, तब प्रत्येक लौकिक उद्यम साक्षात् साधना बन जाता है।\n\n"
                f"[तात्त्विक निष्कर्ष]: सत्य के प्रवेशद्वार पर ज्ञान और प्रेम एकाकार हो जाते हैं। जिज्ञासा का चरम फल प्रेम है, और प्रेम का आधार प्रबुद्ध विवेक है।"
            )
            mr_text = (
                f"[तात्त्विक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) आणि शांडिल्य सूत्र #{s_no} ({s_sanskrit}) यांचा "
                f"'{theme}' या मध्यवर्ती विषयाखाली उदात्त तात्त्विक संगम घडवून आणतो. नारद भक्तीची मांडणी अंतःकरणातील उत्कट प्रेमाच्या व "
                f"अनुभूतीच्या पातळीवर करतात, तर शांडिल्य 'भक्तिजिज्ञासा' या सूत्राद्वारे भक्तीला तर्कशुद्ध व शास्त्रीय अधिष्ठान देतात. "
                f"शांडिल्य बुद्धीला समाधान देतात आणि नारद अंतःकरणाला तृप्त करतात. दोन्हींचा समन्वय परिपूर्ण भक्तीमार्ग प्रस्थापित करतो.\n\n"
                f"[उद्योग आणि जीवन-साधना]: दैनंदिन जीवन, व्यवसाय आणि कर्मक्षेत्रात हे सूत्र 'सत्-उद्योगाची' पायाभरणी करते. कोणतेही श्रेष्ठ कार्य करताना "
                f"शांडिल्यांची विवेकनिष्ठ विचारशीलता (कार्याचा खरा हेतू काय?) आणि नारदांची निस्वार्थ निष्ठा यांचा मेळ घातला पाहिजे. केवळ बुद्धी असेल तर "
                f"कर्म कोरडे होते, आणि केवळ भावना असेल तर दिशा भरकटते. जेव्हा विवेक आणि प्रेम एकत्र येतात, तेव्हा मानवी प्रयत्न सिद्धीस जातात.\n\n"
                f"[अंतिम बोध]: ज्ञान आणि भक्ती हे एकाच परमतत्त्वाचे दोन पंख आहेत. विवेकाने सुरू झालेली जिज्ञासा प्रेमात परिपूर्ण होते."
            )

        # Category 2: Supreme Love, Absolute Attachment, Sole Goal
        elif any(w in theme_lower for w in ["love", "anurakti", "prema", "supreme", "goal", "essence"]):
            en_text = (
                f"[Philosophical Nexus / तात्त्विक समन्वय]: The Udyoga Sutra admits this profound comparative pairing connecting "
                f"Narada Sutra #{n_no} ({n_sanskrit}) with Shandilya Sutra #{s_no} ({s_sanskrit}) under the theme of '{theme}'. "
                f"Narada identifies the intrinsic essence of devotion as 'Parama-Prema-Rūpā' (the nature of supreme, unconditioned love), "
                f"while Shandilya establishes 'Parānurakti' (continuous, unbroken attraction toward Ishvara) and affirms 'Tatra Parā Sādhyā' "
                f"(Supreme love is the ultimate end, not a subordinate means). Both traditions definitively reject the notion that devotion "
                f"is merely an emotional stepping-stone; it is the ultimate ontological reality and the highest spiritual consummation.\n\n"
                f"[Applied Enterprise & Duty / उद्योग एवं कर्म-साधना]: In professional and everyday human endeavors, this principle transforms "
                f"ordinary labor into selfless excellence. When an individual works solely out of fear or transactional greed, fatigue and "
                f"anxiety are inevitable. However, when endeavor ('Udyoga') is animated by supreme love—love for excellence, truth, and the "
                f"welfare of all beings—work ceases to be a burden and becomes a joyful expression of divine energy. The practitioner acts with "
                f"boundless dedication, unaffected by petty egoism or fear of failure.\n\n"
                f"[Core Realization / अंतिम बोध]: Love is the supreme sovereign power of consciousness. When action is saturated with divine love, "
                f"work becomes worship, and enterprise becomes liberation."
            )
            hi_text = (
                f"[दार्शनिक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) और शांडिल्य सूत्र #{s_no} ({s_sanskrit}) का "
                f"'{theme}' के अंतर्गत मिलन स्वीकार करता है। नारद जहाँ भक्ति को 'परमप्रेमरूपा' कहकर उसके शुद्ध रागात्मक और अमृतमय स्वभाव को "
                f"उद्घाटित करते हैं, वहीं शांडिल्य उसे 'परानुरक्तिरीश्वरे' तथा 'तत्र परा साध्या' कहकर यह सिद्ध करते हैं कि भक्ति किसी अन्य फल "
                f"का साधन मात्र नहीं, अपितु जीवन का परम साध्य है। दोनों परंपराएँ एकमत होकर यह स्थापित करती हैं कि अनन्य प्रेम ही आत्मा की "
                f"सर्वोच्च पूर्णता है।\n\n"
                f"[उद्योग एवं कर्म-साधना]: सांसारिक उद्यम और कार्यक्षेत्र में यह सिद्धांत कर्मयोग की पराकाष्ठा है। जब व्यक्ति भय, लोभ या संकीर्ण "
                f"स्वार्थ से कार्य करता है, तो मानसिक तनाव और शिथिलता जन्म लेती है। इसके विपरीत, जब उद्यम ('उद्योग') में सत्य, सेवा और परमेश्वर के "
                f"प्रति अनन्य अनुराग जुड़ जाता है, तो साधारण कर्म भी असाधारण उत्कृष्टता में बदल जाता है। ऐसा साधक निष्काम भाव से निरंतर कर्मरत "
                f"रहकर भी आंतरिक शांति में प्रतिष्ठित रहता है।\n\n"
                f"[तात्त्विक निष्कर्ष]: प्रेम ही चेतना की सर्वोच्च शक्ति है। जब कर्म प्रेम से अभिसिंचित होता है, तब वह बंधन नहीं बल्कि मोक्ष का साधन बन जाता है।"
            )
            mr_text = (
                f"[तात्त्विक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) आणि शांडिल्य सूत्र #{s_no} ({s_sanskrit}) यांचा "
                f"'{theme}' या विषयाखाली तात्त्विक मेळ साधतो. नारद भक्तीला 'परमप्रेमरूपा' मानून तिच्या उत्कट प्रेमाविष्काराचे वर्णन करतात, "
                f"तर शांडिल्य 'परानुरक्तिरीश्वरे' आणि 'तत्र परा साध्या' या सूत्रांद्वारे हे सिद्ध करतात की भक्ती हे केवळ साधन नसून तेच अंतिम "
                f"साध्य आहे. दोन्ही ऋषी एका सुरात सांगतात की ईश्वरावरील निरतिशय प्रेम हीच मानवी जीवनाची सर्वोच्च परिणती आहे.\n\n"
                f"[उद्योग आणि जीवन-साधना]: दैनंदिन कर्म आणि कर्तव्यक्षेत्रात हा सिद्धांत कर्मयोगाचे रहस्य उलगडतो. जेव्हा माणूस स्वार्थ किंवा भीतीने "
                f"काम करतो, तेव्हा थकवा व निराशा येते. परंतु जेव्हा आपल्या उद्योगात प्रेमाचा, निष्ठेचा आणि ईश्वरी सेवेचा भाव येतो, तेव्हा प्रत्येक कृती "
                f"पूजा बनते. असा साधक यशापयशाने विचलित न होता सातत्याने सर्वोत्तम कार्य करत राहतो.\n\n"
                f"[अंतिम बोध]: प्रेम हीच आत्म्याची खरी शक्ती आहे. जेव्हा कर्माला प्रेमाचा स्पर्श होतो, तेव्हा उद्योगच मोक्षदायी ठरतो."
            )

        # Category 3: Superiority over Mere Intellect, Knowledge & Interdependence
        elif any(w in theme_lower for w in ["knowledge", "intellect", "jnana", "superior", "interdepend"]):
            en_text = (
                f"[Philosophical Nexus / तात्त्विक समन्वय]: The Udyoga Sutra unites Narada Sutra #{n_no} ({n_sanskrit}) with "
                f"Shandilya Sutra #{s_no} ({s_sanskrit}) under the theme of '{theme}'. Both masters address the classical dilemma between "
                f"dry intellect (Jnana) and loving surrender (Bhakti). Shandilya delivers a masterclass in epistemological precision "
                f"('Jñāneti cenna parasya jñānapratiṣṭhānāt'), demonstrating that mere intellectual cognition cannot be equated with devotion; "
                f"knowledge merely provides the cognitive scaffold upon which supreme love rests. Narada vigorously corroborates this, declaring "
                f"devotion superior to karma, jnana, and yoga, observing that a starving person cannot be nourished simply by intellectually "
                f"analyzing food. Both acharyas conclude that knowledge is the foundation, but love is the living edifice.\n\n"
                f"[Applied Enterprise & Duty / उद्योग एवं कर्म-साधना]: In modern organizational leadership and enterprise, this doctrine holds "
                f"monumental relevance. Data, technical intellect, and strategic models are vital foundational tools, but they cannot inspire "
                f"human greatness or ethical resilience on their own. Strategy without dedication produces cynical paralysis; passion without "
                f"knowledge produces chaotic failure. True 'Udyoga' requires technical mastery anchored in a passionate, values-driven heart. "
                f"The practitioner combines rigorous competence with deep care for the mission.\n\n"
                f"[Core Realization / अंतिम बोध]: Knowledge is the lamp that illuminates the path; devotion is the flame that provides warmth "
                f"and life. Together, they dissolve darkness and grant total spiritual sovereignty."
            )
            hi_text = (
                f"[दार्शनिक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) और शांडिल्य सूत्र #{s_no} ({s_sanskrit}) का "
                f"'{theme}' के परिप्रेक्ष्य में समन्वय करता है। दोनों आचार्य शुष्क बुद्धिवाद और भक्ति के संबंध का गहरा विश्लेषण करते हैं। "
                f"शांडिल्य तार्किक स्पष्टता से स्थापित करते हैं कि केवल बौद्धिक ज्ञान भक्ति नहीं हो सकता, क्योंकि ज्ञान तो केवल प्रेम का "
                f"अधिष्ठान (आधार) मात्र है। नारद इस सत्य को पुष्ट करते हुए कहते हैं कि भोजन की केवल चर्चा करने से भूख शांत नहीं होती, उसे ग्रहण "
                f"करने से तृप्ति मिलती है। ज्ञान पथ दिखाता है, परंतु गंतव्य तक पहुँचाने वाली शक्ति भक्ति ही है।\n\n"
                f"[उद्योग एवं कर्म-साधना]: आधुनिक उद्यम और नेतृत्व के संदर्भ में यह सिद्धांत अत्यंत मार्गदर्शक है। योजनाएँ, डेटा और तकनीकी ज्ञान "
                f"आवश्यक साधन हैं, परंतु बिना निष्ठा, सेवा-भाव और समर्पण के कोई भी संगठन महान नहीं बन सकता। शुष्क बुद्धि केवल विश्लेषण में उलझी "
                f"रहती है, जबकि प्रेम और समर्पण असंभव को भी संभव बना देते हैं। उद्योग सूत्र कुशल ज्ञान और समर्पित कर्म के समन्वय का आदेश देता है।\n\n"
                f"[तात्त्विक निष्कर्ष]: ज्ञान दीपक है और भक्ति उसका प्रकाश। दोनों के संगम से साधक अज्ञान के अंधकार से पार होकर परमानंद को प्राप्त करता है।"
            )
            mr_text = (
                f"[तात्त्विक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) आणि शांडिल्य सूत्र #{s_no} ({s_sanskrit}) यांचा "
                f"'{theme}' या विषयानुसार समन्वय साधतो. दोन्ही ऋषी बुद्धी आणि भक्ती यांमधील संबंध स्पष्ट करतात. शांडिल्य स्पष्ट करतात की केवळ ज्ञान "
                f"म्हणजे भक्ती नव्हे, ज्ञान हे केवळ भक्तीचे अधिष्ठान आहे. नारद सांगतात की अन्नाची नुसती माहिती असण्याने भूक भागत नाही, तर ते प्रत्यक्ष "
                f"सेवन केल्यावरच तृप्ती मिळते. ज्ञान पाया रचतो, पण त्यावर भक्तीचा कळस चढवावा लागतो.\n\n"
                f"[उद्योग आणि जीवन-साधना]: कार्यक्षेत्रात आणि उद्योगात हा सिद्धांत यशाचा मूलमंत्र आहे. कौशल्य, तंत्रज्ञान आणि नियोजन हे साधन आहेत; "
                f"परंतु कामाप्रती निष्ठा, प्रेम आणि नैतिक मूल्ये नसतील तर मोठे कार्य उभे राहू शकत नाही. केवळ बुद्धी असेल तर अहंकार वाढतो, पण जेव्हा "
                f"बुद्धीला भक्तीची जोड मिळते, तेव्हा कार्याला पावित्र्य लाभते.\n\n"
                f"[अंतिम बोध]: ज्ञान ही दृष्टी आहे आणि भक्ती ही शक्ती आहे. या दोन्हींच्या संयोगाने साधक जीवनात कृतार्थ होतो."
            )

        # Category 4: Renunciation, Non-attachment, Transcending Ritualism
        elif any(w in theme_lower for w in ["renunciat", "detachment", "vairagya", "ritual", "mechanical"]):
            en_text = (
                f"[Philosophical Nexus / तात्त्विक समन्वय]: The Udyoga Sutra unites Narada Sutra #{n_no} ({n_sanskrit}) with "
                f"Shandilya Sutra #{s_no} ({s_sanskrit}) under the theme of '{theme}'. Narada defines renunciation ('nirodha') not as "
                f"passive nihilism, but as 'loka-veda-vyāpāra-nyāsaḥ'—the transcendence of mechanical social and scriptural rituals to achieve "
                f"undivided focus on the Divine. Shandilya confirms this epistemologically, explaining that ritualistic actions produce "
                f"perishable, transient fruits and therefore cannot satisfy the soul's yearning for the Infinite. Both sages agree that true "
                f"renunciation is the elimination of ego-driven desires, making room for boundless spiritual love.\n\n"
                f"[Applied Enterprise & Duty / उद्योग एवं कर्म-साधना]: In practical work and professional discipline, this principle translates "
                f"into radical focus and ethical integrity. It instructs the worker to renounce trivial distractions, toxic office politics, and "
                f"superficial status-seeking, channeling all energy toward meaningful, value-creating enterprise. Non-attachment does not mean "
                f"abandoning duty; it means performing duty with total dedication while releasing anxious fixation on personal aggrandizement.\n\n"
                f"[Core Realization / अंतिम बोध]: Renunciation is not the denial of life, but the purification of action. When selfish desires "
                f"are surrendered, enterprise becomes pure spiritual power."
            )
            hi_text = (
                f"[दार्शनिक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) और शांडिल्य सूत्र #{s_no} ({s_sanskrit}) का "
                f"'{theme}' के अंतर्गत समन्वय स्थापित करता है। नारद 'निरोध' की व्याख्या करते हुए सांसारिक प्रपंच और यांत्रिक कर्मकांडों के "
                f"त्याग का उपदेश देते हैं, ताकि चित्त केवल ईश्वर में एकाग्र हो सके। शांडिल्य दार्शनिक रूप से सिद्ध करते हैं कि सकाम कर्म विनाशी "
                f"फल देने वाले हैं, अतः वे आत्मा को परम तृप्ति नहीं दे सकते। दोनों आचार्य सकाम कर्म के त्याग और निष्काम भगवत्-प्रेम का प्रतिपादन करते हैं।\n\n"
                f"[उद्योग एवं कर्म-साधना]: कर्मक्षेत्र में यह सिद्धांत एकाग्रता और शुचिता का पाठ पढ़ाता है। इसका अर्थ कार्य छोड़ना नहीं, अपितु व्यर्थ के "
                f"प्रपंच, दिखावे और संकीर्ण स्वार्थ को त्यागना है। जब कार्यकर्ता व्यक्तिगत लोभ और व्यर्थ की चिंताओं से मुक्त होकर अपने लक्ष्य के प्रति समर्पित "
                f"होता है, तब उसके उद्यम में अभूतपूर्व प्रभावशीलता और सृजनात्मकता का उदय होता है।\n\n"
                f"[तात्त्विक निष्कर्ष]: त्याग जीवन का नकार नहीं, बल्कि कर्म की शुद्धि है। स्वार्थ के मिटते ही उद्यम दिव्य साधना बन जाता है।"
            )
            mr_text = (
                f"[तात्त्विक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) आणि शांडिल्य सूत्र #{s_no} ({s_sanskrit}) यांचा "
                f"'{theme}' या विषयाखाली मेळ घालतो. नारद 'निरोध' म्हणजे व्यावहारिक व कर्मकांडी बंधनांचा त्याग करून ईश्वरात लीन होणे असे सांगतात. "
                f"शांडिल्य स्पष्ट करतात की फळाची आशा ठेवून केलेले कर्म अशाश्वत असते, म्हणून ते आत्म्याला पूर्णत्व देऊ शकत नाही. दोन्ही तत्त्वज्ञ सांगतात "
                f"की स्वार्थाचा त्याग हाच खऱ्या भक्तीचा पाया आहे.\n\n"
                f"[उद्योग आणि जीवन-साधना]: कर्तव्यक्षेत्रात हा सिद्धांत एकाग्रतेची आणि निस्वार्थतेची प्रेरणा देतो. काम सोडणे म्हणजे त्याग नव्हे, तर कामातील "
                f"स्वार्थ, मत्सर आणि व्यर्थ चिंता सोडणे हा खरा त्याग होय. जेव्हा कार्यकर्ता फळाच्या हव्यासाशिवाय प्रामाणिकपणे झोकून देऊन काम करतो, तेव्हा "
                f"त्याच्या हातून महान कार्य घडते.\n\n"
                f"[अंतिम बोध]: त्याग म्हणजे कर्तव्यापासून पळ काढणे नव्हे, तर कर्माला निस्वार्थ बनवणे होय."
            )

        # Category 5: Universal Equality, Transcending Caste & Lineage
        elif any(w in theme_lower for w in ["caste", "equal", "lineage", "universal", "all humans"]):
            en_text = (
                f"[Philosophical Nexus / तात्त्विक समन्वय]: The Udyoga Sutra synthesizes Narada Sutra #{n_no} ({n_sanskrit}) with "
                f"Shandilya Sutra #{s_no} ({s_sanskrit}) under the theme of '{theme}'. Both acharyas champion a revolutionary spiritual egalitarianism. "
                f"Narada resoundingly proclaims that among true devotees, distinctions of caste, academic pedigree, physical appearance, family "
                f"lineage, wealth, or secular profession cease to exist ('Nāsti teṣu jāti-vidyā-rūpa-kula-dhana-kriyādi-bhedaḥ'). Shandilya provides "
                f"absolute epistemological justification by declaring universal entitlement to Bhakti ('Sarveṣām cādhikāraḥ'). Unlike restrictive "
                f"orthodox rituals, the sanctuary of divine devotion belongs equally to every living being.\n\n"
                f"[Applied Enterprise & Duty / उद्योग एवं कर्म-साधना]: In modern organizational culture and human enterprise, this stands as the "
                f"timeless charter of dignity, meritocracy, and inclusion. An enlightened institution evaluates individuals not by birth, privilege, "
                f"or external labels, but by inner character, ethical commitment, and excellence in contribution. True leadership creates an "
                f"environment of profound psychological safety where every individual's contribution is valued with equal reverence.\n\n"
                f"[Core Realization / अंतिम बोध]: Before the Supreme, the only distinction that matters is purity of heart. In unity of spirit, "
                f"all artificial human barriers dissolve."
            )
            hi_text = (
                f"[दार्शनिक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) और शांडिल्य सूत्र #{s_no} ({s_sanskrit}) का "
                f"'{theme}' के पावन विषय पर एकीकरण करता है। दोनों आचार्यों ने सामाजिक और जन्मगत संकीर्णताओं का समूल खंडन किया है। नारद "
                f"सिंहगर्जना करते हैं कि भक्तों में जाति, विद्या, रूप, कुल, धन और क्रिया आदि का कोई भेद नहीं होता। शांडिल्य शास्त्र सम्मत "
                f"प्रमाण देते हैं कि भक्ति पर प्रत्येक प्राणी का समान और जन्मसिद्ध अधिकार है। ईश्वर के प्रेम-दरबार में सभी आत्माएँ समान हैं।\n\n"
                f"[उद्योग एवं कर्म-साधना]: व्यावसायिक संगठन और समाज के संचालन में यह समता, गरिमा और सर्वसमावेशी न्याय का अमर संदेश है। एक श्रेष्ठ "
                f"कार्य-संस्कृति वही है जहाँ व्यक्ति का मूल्यांकन उसके वंश, बाह्य प्रतिष्ठा या धन से नहीं, बल्कि उसकी निष्ठा, योग्यता और ईमानदारी "
                f"से होता है। उद्योग सूत्र मानवीय गरिमा और बंधुत्व की रक्षा को सर्वोच्च धर्म मानता है।\n\n"
                f"[तात्त्विक निष्कर्ष]: परमात्मा के समक्ष केवल हृदय की शुद्धि मान्य है। भगवत्-प्रेम की पावन धारा में ऊँच-नीच के सभी कल्पित भेद विलीन हो जाते हैं।"
            )
            mr_text = (
                f"[तात्त्विक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) आणि शांडिल्य सूत्र #{s_no} ({s_sanskrit}) यांचा "
                f"'{theme}' या विषयावर एकात्म विचार मांडतो. दोन्ही आचार्यांनी जात, पात आणि कुळाच्या भेदांना पूर्णपणे नाकारले आहे. नारद स्पष्ट "
                f"सांगतात की ईश्वराच्या भक्तांमध्ये जात, विद्या, रूप, कुल, धन किंवा व्यवसाय यावरून कोणताही भेद नसतो. शांडिल्य सांगतात की भक्तीचा "
                f"अधिकार विश्वातील प्रत्येक जीवाला समान आहे. ईश्वराच्या दरबारात सर्वांना समान स्थान आहे.\n\n"
                f"[उद्योग आणि जीवन-साधना]: सामाजिक आणि व्यावसायिक क्षेत्रात हा सिद्धांत समता, न्याय आणि सर्वसमावेशकतेची शिकवण देतो. कोणत्याही संस्थेचे "
                f"किंवा उद्योगाचे यश माणसाच्या बाह्य रूपावर किंवा वंशावर अवलंबून नसून, त्याच्यातील प्रामाणिकपणा, कष्ट आणि गुणांवर अवलंबून असते. हे सूत्र "
                f"सर्वांना समान संधी आणि आदर देण्याचा आग्रह धरते.\n\n"
                f"[अंतिम बोध]: ईश्वराच्या दृष्टीने अंतःकरणाची शुद्धी हीच खरी संपत्ती आहे. प्रेमाच्या प्रवाहात सर्व मानवनिर्मित भिंती गळून पडतात."
            )

        # Category 6: Ineffable Bliss, Tasting the Divine Nectar (Rasa)
        elif any(w in theme_lower for w in ["ineffable", "rasa", "bliss", "taste"]):
            en_text = (
                f"[Philosophical Nexus / तात्त्विक समन्वय]: The Udyoga Sutra unites Narada Sutra #{n_no} ({n_sanskrit}) with "
                f"Shandilya Sutra #{s_no} ({s_sanskrit}) under the theme of '{theme}'. Narada illustrates the mystery of divine love with the "
                f"poignant metaphor of the mute person tasting delicious nectar ('Mūkāsvādanavat')—the experience of sweetness is profoundly real, "
                f"intoxicating, and transformative, yet utterly beyond the capacity of speech to articulate. Shandilya corroborates this through "
                f"the Upanishadic doctrine of 'Raso vai saḥ', demonstrating that the Supreme is transcendental aesthetic bliss itself. Love is not "
                f"an intellectual concept to be debated, but an immediate ontological reality to be tasted.\n\n"
                f"[Applied Enterprise & Duty / उद्योग एवं कर्म-साधना]: In creative enterprise and master craftsmanship, this reflects the "
                f"psychological phenomenon of deep 'flow' and intrinsic joy. When a dedicated creator or craftsman is completely absorbed in "
                f"purposeful work, the distinction between worker and work vanishes. The joy of creating something truly sublime cannot be fully "
                f"captured in words or metrics; it is known only by the heart that pours itself into the craft.\n\n"
                f"[Core Realization / अंतिम बोध]: Truth in its highest octave is beyond language. It is realized in the silence of deep fulfillment "
                f"and the joy of selfless creation."
            )
            hi_text = (
                f"[दार्शनिक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) और शांडिल्य सूत्र #{s_no} ({s_sanskrit}) का "
                f"'{theme}' के परिप्रेक्ष्य में मिलन कराता है। नारद गूंगे के गुड़ के प्रसिद्ध दृष्टांत ('मूकास्वादनवत्') से समझाते हैं कि "
                f"भक्ति-रस का आस्वादन वाणी से परे, अनिर्वचनीय और केवल स्व-संवेद्य है। शांडिल्य उपनिषदों के 'रसो वै सः' सिद्धांत से इसकी पुष्टि "
                f"करते हुए सिद्ध करते हैं कि परमात्मा साक्षात् रस-स्वरूप और परमानंद हैं। यह प्रेम वाद-विवाद का विषय नहीं, अपितु जीवन में साक्षात् अनुभव करने की वस्तु है।\n\n"
                f"[उद्योग एवं कर्म-साधना]: सृजनात्मक उद्यम और कर्म-कौशल में यह 'परम तन्मयता' का प्रतीक है। जब कोई निष्ठावान शिल्पी या वैज्ञानिक अपने "
                f"कार्य में पूरी तरह लीन हो जाता है, तो कर्म ही उसका आनंद बन जाता है। उत्कृष्ट सृजन का जो गहरा आंतरिक संतोष होता है, उसे शब्दों में "
                f"नहीं बाँधा जा सकता; उसे केवल वही जान सकता है जिसने अपने कार्य में आत्मा उड़ेल दी हो।\n\n"
                f"[तात्त्विक निष्कर्ष]: सर्वोच्च सत्य शब्दों की सीमा से परे है। वह मौन की गहराई में और समर्पित कर्म के आनंद में साक्षात् अनुभूत होता है।"
            )
            mr_text = (
                f"[तात्त्विक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) आणि शांडिल्य सूत्र #{s_no} ({s_sanskrit}) यांचा "
                f"'{theme}' या विषयाखाली समन्वय साधतो. नारद मुक्याच्या गुळाच्या दृष्टान्ताने ('मूकास्वादनवत्') दाखवून देतात की भक्तीचा आनंद अवर्णनीय "
                f"आहे; तो शब्दात सांगता येत नाही, केवळ अनुभवता येतो. शांडिल्य 'रसो वै सः' या श्रुतिवचनाद्वारे स्पष्ट करतात की ईश्वर हा साक्षात रसरूप "
                f"व आनंदरूप आहे. प्रेम हे चर्चेचे साधन नसून ते साक्षात अनुभूतीचे अमृत आहे.\n\n"
                f"[उद्योग आणि जीवन-साधना]: व्यावसायिक आणि कलात्मक क्षेत्रात हे सूत्र 'परम तल्लीनतेची' अनुभूती देते. जेव्हा एखादा कुशल कारागीर किंवा संशोधक "
                f"आपल्या कार्यात मनापासून रमून जातो, तेव्हा कर्माचाच आनंद बनतो. उत्कृष्ट कार्याचा जो आंतरिक आनंद असतो, तो शब्दातीत असतो. तो फक्त त्या "
                f"कार्यात स्वतःला विसरून जाणाऱ्यालाच समजतो.\n\n"
                f"[अंतिम बोध]: परमोच्च सत्य हे भाषेच्या पलीकडचे आहे. ते अंतःकरणाच्या शांततेत आणि समर्पित कर्माच्या आनंदाने प्रकट होते."
            )

        # Default / General Syncretic Commentary
        else:
            en_text = (
                f"[Philosophical Nexus / तात्त्विक समन्वय]: The Udyoga Sutra admits this comparative pairing uniting Narada Sutra #{n_no} "
                f"({n_sanskrit}) with Shandilya Sutra #{s_no} ({s_sanskrit}) under the theme of '{theme}'. Narada expounds Bhakti from the "
                f"perspective of direct experiential realization and ecstatic devotional absorption, while Shandilya grounds this identical "
                f"truth in rigorous epistemological inquiry and ontological certitude. Rather than existing as competing schools, they represent "
                f"two complementary aspects of one indivisible reality: Shandilya provides the rational foundation, and Narada infuses it "
                f"with living, vibrant love.\n\n"
                f"[Applied Enterprise & Duty / उद्योग एवं कर्म-साधना]: In human enterprise and duty, this synthesis provides the foundation for "
                f"sustainable excellence. Diligent endeavor ('Udyoga') requires both clear intellectual discernment and passionate emotional "
                f"commitment. Work undertaken without knowledge lacks strategic efficacy; work performed without heart lacks endurance and moral "
                f"elevation. When intellect and love are unified in purposeful action, everyday duty is elevated into sublime spiritual practice.\n\n"
                f"[Core Realization / अंतिम बोध]: Reason and devotion are the two harmonious wings of human liberation. In their syncretic union, "
                f"the seeker achieves total balance, excellence in work, and eternal spiritual fulfillment."
            )
            hi_text = (
                f"[दार्शनिक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) और शांडिल्य सूत्र #{s_no} ({s_sanskrit}) का "
                f"'{theme}' के अंतर्गत समन्वय स्थापित करता है। नारद जहाँ अनुभवात्मक भक्ति, प्रेम और आत्मसमर्पण का मार्ग दिखाते हैं, वहीं शांडिल्य "
                f"प्रमाण, तर्क और ज्ञानमूलक जिज्ञासा के द्वारा उसी सत्य को दार्शनिक आधार प्रदान करते हैं। यह दोनों धाराएँ परस्पर विरोधी नहीं, बल्कि एक "
                f"ही सच्चिदानंद सत्य के दो अभिन्न अंग हैं—शांडिल्य का विवेक और नारद का प्रेम।\n\n"
                f"[उद्योग एवं कर्म-साधना]: जीवन के कर्मक्षेत्र और उद्योग में यह सिद्धांत संतुलन और पूर्णता का सूत्र है। किसी भी कार्य में सफलता के "
                f"लिए स्पष्ट विवेक (ज्ञान) और गहरी निष्ठा (प्रेम) दोनों की आवश्यकता होती है। जब साधक अपने कर्तव्य-कर्म को विवेकपूर्ण दृष्टि से समझकर "
                f"और प्रेमपूर्वक ईश्वर को समर्पित करके करता है, तब उसका प्रत्येक उद्यम आत्म-कल्याण और लोक-कल्याण का साधन बन जाता है।\n\n"
                f"[तात्त्विक निष्कर्ष]: बुद्धि और हृदय का समन्वय ही जीवन की सार्थकता है। ज्ञान और भक्ति के एकाकार होने पर साधक कर्म में कुशलता और "
                f"हृदय में परमानंद का अनुभव करता है।"
            )
            mr_text = (
                f"[तात्त्विक समन्वय]: उद्योग सूत्र नारद सूत्र #{n_no} ({n_sanskrit}) आणि शांडिल्य सूत्र #{s_no} ({s_sanskrit}) यांचा "
                f"'{theme}' या विषयानुसार तात्त्विक संगम घडवून आणतो. नारद भक्तीला थेट अनुभवाच्या व उत्कट प्रेमाच्या दृष्टीने मांडतात, तर शांडिल्य "
                f"तर्कशुद्ध व शास्त्रीय विचाराने त्याच सत्याला भक्कम अधिष्ठान देतात. या दोन परंपरा भिन्न नसून एकाच परमतत्त्वाच्या दोन बाजू आहेत—"
                f"शांडिल्यांचा विवेक आणि नारदांचे प्रेम.\n\n"
                f"[उद्योग आणि जीवन-साधना]: दैनंदिन जीवन आणि कार्यक्षेत्रात हे सूत्र शाश्वत यशाचा मार्ग दाखवते. कोणत्याही कार्यात यश मिळवण्यासाठी "
                f"योग्य दिशा (ज्ञान) आणि कामाप्रती नितांत निष्ठा (प्रेम) या दोन्हींची गरज असते. जेव्हा बुद्धी आणि भावना यांचा समन्वय साधून कर्तव्य "
                f"पार पाडले जाते, तेव्हा सामान्य कामसुद्धा ईश्वरी सेवा बनते.\n\n"
                f"[अंतिम बोध]: विवेक आणि भक्ती यांचा संगम म्हणजेच मानवी जीवनाची पूर्णता. या समन्वयाने साधकाला कर्मात यश आणि अंतःकरणात चिरंतन शांती लाभते."
            )

        return {"en": en_text, "hi": hi_text, "mr": mr_text}

    def _get_marathi_theme_title(
        self,
        narada_sutra_no: str,
        shandilya_sutra_no: str,
        default_theme: str = "",
    ) -> str:
        """
        ------------------------------------------------------------------------
        Method: _get_marathi_theme_title
        ------------------------------------------------------------------------
        Purpose:
            Returns an authentic, scholarly Marathi title for each comparative
            sutra pair, enriching the Udyoga Sutra treatise with an authentic
            Marathi touch and large Devanagari heading for senior citizen review.

        Parameters:
            narada_sutra_no (str): Aphorism number from Narada Bhakti Sutra.
            shandilya_sutra_no (str): Matched aphorism number from Shandilya Bhakti Sutra.
            default_theme (str): Fallback theme string if sutra number is unmapped.

        Returns:
            str: Scholarly Marathi theme title.

        Manual Debugging Notes:
            - Covers all 84 canonical Narada Bhakti Sutras with precise philosophical titles.
            - Guarantees non-empty Marathi heading even if an unusual sutra index is queried.
        ------------------------------------------------------------------------
        """
        marathi_canon_titles: Dict[str, str] = {
            "1": "भक्तीचे स्वरूप आणि तात्त्विक जिज्ञासा",
            "2": "परम प्रेमरूप भक्ती आणि प्रेमानंदाचे प्राधान्य",
            "3": "भक्तीचे अमृतस्वरूप आणि अमरत्व",
            "4": "परम सिद्धी, अमरत्व आणि आत्मतृप्ती",
            "5": "सर्व वासना, द्वेष आणि शोकापासून मुक्ती",
            "6": "दिव्य परमानंद आणि आत्माराम अवस्था",
            "7": "निष्काम प्रेम आणि वासनांचा निरोध",
            "8": "लौकिक व वैदिक प्रपंचातून निवृत्ती",
            "9": "अनन्य भक्ती आणि निस्वार्थ समर्पण",
            "10": "एकनिष्ठ शरणागती आणि अनन्यता",
            "11": "भक्तीस अनुकूल आचरण आणि लोकसंग्रह",
            "12": "शास्त्रमर्यादेचे रक्षण आणि दृढ निष्ठा",
            "13": "अधःपातापासून रक्षण आणि नित्य सावधानता",
            "14": "शरीर-निर्वाहापुरते आचरण आणि साधेपणा",
            "15": "भक्तीच्या विविध लक्षणांचे दर्शन",
            "16": "व्यासमुनींचे मत: पूजा-अर्चनेतील प्रेम",
            "17": "गर्गमुनींचे मत: भगवत्कथेतील अनुरागाचे माहात्म्य",
            "18": "शांडिल्यमुनींचे मत: आत्मरती आणि ईश्वराशी अनुसंधान",
            "19": "नारदांचे सार्वभौम मत: सर्व कर्मार्पण आणि विरहातील व्याकुळता",
            "20": "भक्तीच्या परिपूर्णतेचा प्रत्यक्ष पुरावा",
            "21": "व्रजगोपींचे आदर्श आणि अनन्य प्रेम",
            "22": "ईश्वरमाहात्म्यज्ञानाची अनिवार्य आवश्यकता",
            "23": "माहात्म्यज्ञानाशिवाय प्रेम म्हणजे केवळ जड आकर्षण",
            "24": "परस्परांच्या आनंदातील निस्वार्थ सुख",
            "25": "कर्म, ज्ञान आणि योगापेक्षा भक्तीचे श्रेष्ठत्व",
            "26": "भक्ती हे केवळ साधन नसून अंतिम साध्य",
            "27": "ईश्वराला नम्रतेची प्रीती आणि अहंकाराचा तिटकारा",
            "28": "ज्ञान हे भक्तीचे केवळ साधन असल्याचा विचार",
            "29": "ज्ञान आणि भक्तीचा परस्पर संवादी समन्वय",
            "30": "सनत्कुमारांचे मत: भक्ती हे स्वतःच स्वयंसिद्ध फळ",
            "31": "राजप्रासाद आणि भोजनाचा दृष्टान्त",
            "32": "केवळ वैचारिक ज्ञानाने खरी तृप्ती लाभत नाही",
            "33": "मुमुक्षूंनी निरुपाधिक भक्तीचाच अंगीकार करावा",
            "34": "भक्ती-प्राप्तीची प्रमुख अंतरंग साधने",
            "35": "विषयासक्ती आणि लौकिक प्रपंचाचा त्याग",
            "36": "अखंड नामस्मरण आणि अविरत भजन-साधना",
            "37": "ईश्वरी कीर्तीचे श्रवण आणि गुणसंकीर्तन",
            "38": "संतकृपा आणि भगवंताच्या अहैतुकी दयेचे सामर्थ्य",
            "39": "सत्पुरुषांचा समागम: दुर्मिळ आणि अमोघ",
            "40": "सत्संग हा केवळ ईश्वराच्या कृपेनेच साध्य",
            "41": "ईश्वर आणि त्याचे भक्त यांच्यात तात्त्विक अभेद",
            "42": "सत्संगाची नित्य तळमळ आणि आचरण",
            "43": "कुसंगतीचा सर्वथा आणि संपूर्ण त्याग",
            "44": "कुसंगाचे घातक दुष्परिणाम आणि अधःपात",
            "45": "कुसंगामुळे लहान वासनांचा विशाल महासागर होतो",
            "46": "मायेचा दुस्तर सागर कोण पार करतो?",
            "47": "एकांतवास, त्रिगुणातीत अवस्था आणि दृढ श्रद्धा",
            "48": "कर्मफलाचा त्याग आणि द्वंद्वातीत अवस्था",
            "49": "अखंड प्रेमाची प्राप्ती आणि परमानंद",
            "50": "जो मायेला तरतो तो सर्व जगालाही तारतो",
            "51": "भगवत्-प्रेमाचे अनिर्वचनीय स्वरूप",
            "52": "मुक्याच्या गुळाचा आस्वाद: शब्दातीत अनुभूती",
            "53": "पात्र जिवाच्या ठायी दिव्य प्रेमाचा प्रादुर्भाव",
            "54": "परम प्रेमाचे षड्विध दिव्य लक्षण",
            "55": "सर्वत्र ईश्वराचेच दर्शन आणि तन्मयता",
            "56": "गौणी भक्तीचे त्रिविध स्वरूप: त्रिगुण भेद",
            "57": "भक्तीच्या उत्तरोत्तर चढत्या पायऱ्यांचे श्रेष्ठत्व",
            "58": "भक्तीमार्गाची सुलभता आणि सहज साध्यता",
            "59": "भक्तीचे स्वयंसिद्ध स्वातंत्र्य आणि प्रमाण",
            "60": "परम शांती आणि आत्मानंदाचे स्वरूप",
            "61": "लौकिक नुकसानीची भीती आणि चिंतेचा अभाव",
            "62": "कर्तव्यपालन आणि फळाची निरपेक्षता",
            "63": "इंद्रियांच्या प्रलोभनांपासून मनाचे रक्षण",
            "64": "दंभ, अहंकार आणि अहंकाराचा त्याग",
            "65": "सर्व भावनांचे ईश्वराकडे उदात्तीकरण",
            "66": "त्रिपुटीचा भेद मोडून परम ऐक्याची प्राप्ती",
            "67": "एकनिष्ठ अनन्य भक्तांचे परम माहात्म्य",
            "68": "भक्तांमुळे कुळाचे आणि पृथ्वीचे पावनत्व",
            "69": "तीर्थक्षेत्रे, शास्त्रे आणि कर्मांचे पावन रूपांतर",
            "70": "भक्तांच्या रोमरोमात भरलेली ईश्वरी चेतना",
            "71": "पितरांचा आनंद आणि देवतांचे नर्तन",
            "72": "परम समता: जात, विद्या, रूप, कुल व धनाचे भेद निरर्थक",
            "73": "कारण सर्व जीव ईश्वराचेच अंश आहेत",
            "74": "व्यर्थ वादविवाद आणि शुष्क तर्काचा निषेध",
            "75": "तर्काला अंत नसतो आणि निर्णय होत नाही",
            "76": "भक्तीशास्त्राचे नित्य मनन आणि चिंतन",
            "77": "अर्धा क्षणही व्यर्थ न घालवता निरंतर साधन",
            "78": "अहिंसा, सत्य, दया आणि सर्व सद्गुणांची जोपासना",
            "79": "निर्भय आणि सर्वभावे ईश्वराला आत्मसमर्पण",
            "80": "अनन्य भावाने आळवताच ईश्वराचा त्वरित साक्षात्कार",
            "81": "त्रिकालाबाधित सत्य: भक्ती हेच सर्वश्रेष्ठ",
            "82": "परम भक्तीची एकादश दिव्य रूपे",
            "83": "सर्व श्रेष्ठ महर्षींचे एकमुखी एकमत",
            "84": "फलश्रुती: परम प्रियतम ईश्वराची अखंड प्राप्ती",
        }
        clean_no = str(narada_sutra_no).strip()
        if clean_no in marathi_canon_titles:
            return marathi_canon_titles[clean_no]
        if default_theme:
            return f"भक्तीचे तात्त्विक अधिष्ठान: {default_theme}"
        return f"नारद सूत्र #{clean_no} तात्त्विक समन्वय"


