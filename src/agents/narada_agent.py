"""
================================================================================
Module: src.agents.narada_agent
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: The Narada Bhakti Sutra Specialist Agent. Represents the devotional,
             experiential, and ecstatic dimension of Bhakti philosophy. Analyzes
             Narada aphorisms and articulates an inter-agent philosophical prompt
             for the Shandilya Agent.
================================================================================
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config import RAW_DATA_DIR, get_chat_model
from src.models.schema import MultilingualText, SutraItem


class NaradaAgent:
    """
    ----------------------------------------------------------------------------
    Class: NaradaAgent
    ----------------------------------------------------------------------------
    Purpose:
        Acts as the primary autonomous agent representing Devarshi Narada's
        philosophical perspective. Manages the Narada Bhakti Sutra knowledge
        repository, expounds individual verses into multilingual vishleshan
        (English, Hindi, Marathi), and presents devotional theses to the
        Shandilya Agent for comparative discourse.

    Attributes:
        knowledge_base (List[Dict[str, Any]]): Loaded repository of Narada sutras.
        llm (Any): Dynamic LangChain chat model instance.
    ----------------------------------------------------------------------------
    """

    def __init__(self, data_path: Optional[Path] = None) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the NaradaAgent by loading the canonical Narada Bhakti
            Sutra knowledge base and initializing the dynamic language model.

        Parameters:
            data_path (Optional[Path]): Filesystem path to narada_bhakti_sutra.json.
                                        Defaults to RAW_DATA_DIR / narada_bhakti_sutra.json.

        Returns:
            None

        Errors:
            FileNotFoundError: If the source JSON file is absent.

        Manual Debugging Notes:
            - When testing without API keys, fallback analytical generation is
              automatically invoked to maintain pipeline integrity.
        ------------------------------------------------------------------------
        """
        self.data_path = data_path or (RAW_DATA_DIR / "narada_bhakti_sutra.json")
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: _load_knowledge_base
        ------------------------------------------------------------------------
        Purpose:
            Reads and parses the raw Narada Bhakti Sutra JSON file into memory.

        Parameters:
            None

        Returns:
            List[Dict[str, Any]]: List of sutra dictionaries.
        ------------------------------------------------------------------------
        """
        if not self.data_path.exists():
            return []
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_sutra_by_number(self, sutra_no: str) -> Optional[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_sutra_by_number
        ------------------------------------------------------------------------
        Purpose:
            Searches the internal knowledge base for a specific aphorism by number.

        Parameters:
            sutra_no (str): The sutra identifier (e.g. '1', '2').

        Returns:
            Optional[Dict[str, Any]]: Sutra data if found, otherwise None.
        ------------------------------------------------------------------------
        """
        for item in self.knowledge_base:
            if str(item.get("sutra_no")) == str(sutra_no):
                return item
        return None

    def expound_sutra(
        self, sutra_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        ------------------------------------------------------------------------
        Method: expound_sutra
        ------------------------------------------------------------------------
        Purpose:
            Analyzes a Narada Bhakti Sutra verse from an experiential devotional
            viewpoint, generating comprehensive multilingual vishleshan (English,
            Hindi, Marathi) and formulating a structured philosophical message
            addressed to the Shandilya Agent.

        Parameters:
            sutra_data (Dict[str, Any]): Dictionary containing sutra_no, sanskrit,
                                         and theme.

        Returns:
            Dict[str, Any]: Dictionary containing:
                - 'sutra_item': Validated SutraItem object.
                - 'theme': Core philosophical theme.
                - 'agent_message_to_shandilya': Formal inter-agent inquiry prompt.

        Errors:
            Exception: Caught gracefully with structured fallback commentary.

        Manual Debugging Notes:
            - Prompt guides the model to adopt Devarshi Narada's persona:
              unconditional love, experiential surrender, and nectarine bliss.
        ------------------------------------------------------------------------
        """
        sutra_no = str(sutra_data.get("sutra_no", "1"))
        sanskrit = sutra_data.get("sanskrit", "")
        theme = sutra_data.get("theme", "Nature of Divine Love")
        init_en = sutra_data.get("initial_meaning", {}).get("en", "")

        prompt = f"""You are the 'Narada Bhakti Sutra Specialist Agent' representing Devarshi Narada's school of pure, experiential, nectarine Devotion (Bhakti).

Examine Narada Bhakti Sutra #{sutra_no}:
Sanskrit: {sanskrit}
Theme: {theme}
Initial English Context: {init_en}

Your Tasks:
1. Provide an in-depth devotional and experiential analysis (vishleshan) across three languages: English, Hindi, and Marathi.
2. Formulate a direct, courteous, scholarly message addressed to the 'Shandilya Bhakti Sutra Specialist Agent'. In this message, articulate your devotional thesis and invite the Shandilya Agent to present the epistemological/rational counterpart from the Shandilya Bhakti Sutras.

Provide output strictly in this valid JSON format:
{{
  "vishleshan": {{
    "en": "Detailed English devotional exposition...",
    "hi": "हिंदी में विस्तृत भक्तिपरक विश्लेषण...",
    "mr": "मराठीतील सविस्तर भक्तीपरक विश्लेषण..."
  }},
  "message_to_shandilya": "Respected Shandilya Agent, I present Narada Sutra #{sutra_no} on '{theme}'. Our thesis is that Bhakti is... How does the Shandilya tradition epistemologically substantiate this?"
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
            vishleshan_data = parsed.get("vishleshan", {})
            msg = parsed.get("message_to_shandilya", "")
        except Exception:
            # Deterministic, scholarly fallback
            vishleshan_data = {
                "en": (
                    f"Narada Bhakti Sutra #{sutra_no} ({sanskrit}) expounds Bhakti from the stance of pure "
                    f"experiential ecstasy and supreme divine love ('parama-prema'). Here, devotion is neither a mere "
                    f"ritual nor dry ratiocination, but the ultimate direct realization of the soul's eternal relationship with God."
                ),
                "hi": (
                    f"नारद भक्ति सूत्र #{sutra_no} ({sanskrit}) भक्ति को साक्षात् परम प्रेमरूपा और अमृतस्वरूपा घोषित करता है। "
                    f"यह साधक को बौद्धिक वाद-विवाद से परे ले जाकर ईश्वर के प्रति पूर्ण आत्मसमर्पण का मार्ग दिखाता है।"
                ),
                "mr": (
                    f"नारद भक्ति सूत्र #{sutra_no} ({sanskrit}) भक्तीला साक्षात परम प्रेमरूप व अमृतस्वरूप मानतो. "
                    f"केवळ शुष्क बुद्धीवादापेक्षा ईश्वराप्रती असलेले उत्कट समर्पण आणि निष्काम प्रेम हेच या सूत्राचे सार आहे."
                ),
            }
            msg = (
                f"Pranams Shandilya Agent. I present Narada Bhakti Sutra #{sutra_no}: '{sanskrit}', highlighting "
                f"the theme of '{theme}'. We maintain that divine love is direct, experiential, and self-fulfilling. "
                f"Kindly search your Shandilya knowledge base and present the aphorism that addresses this inquiry."
            )

        sutra_item = SutraItem(
            sutra_no=sutra_no,
            sanskrit=sanskrit,
            vishleshan=MultilingualText(
                en=vishleshan_data.get("en", init_en),
                hi=vishleshan_data.get("hi"),
                mr=vishleshan_data.get("mr"),
            ),
        )

        return {
            "sutra_item": sutra_item,
            "theme": theme,
            "agent_message_to_shandilya": msg,
        }
