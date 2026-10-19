"""
================================================================================
Module: src.agents.shandilya_agent
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: The Shandilya Bhakti Sutra Specialist Agent. Represents the
             epistemological, analytical, and scriptural inquiry dimension of
             Bhakti philosophy. Matches incoming Narada sutras against its
             ChromaDB vector store and articulates a philosophical response.
================================================================================
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config import RAW_DATA_DIR, get_chat_model
from src.models.schema import MultilingualText, SutraItem
from src.vectorstore.chroma_store import SutraVectorStore


class ShandilyaAgent:
    """
    ----------------------------------------------------------------------------
    Class: ShandilyaAgent
    ----------------------------------------------------------------------------
    Purpose:
        Acts as the autonomous agent representing Maharshi Shandilya's school of
        epistemological devotion (Bhakti-Jijnasa). Maintains its dedicated
        knowledge base in ChromaDB, receives devotional propositions from the
        Narada Agent, semantically identifies the most philosophically relevant
        Shandilya aphorism, and responds with rigorous analytical commentary.

    Attributes:
        data_path (Path): Path to shandilya_bhakti_sutra.json.
        vector_store (SutraVectorStore): ChromaDB embedded vector collection.
        knowledge_base (List[Dict[str, Any]]): In-memory Shandilya sutra records.
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        data_path: Optional[Path] = None,
        vector_store: Optional[SutraVectorStore] = None,
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the ShandilyaAgent, loads raw sutras, and ensures all
            Shandilya aphorisms are indexed into ChromaDB for semantic retrieval.

        Parameters:
            data_path (Optional[Path]): Filesystem path to shandilya raw JSON.
            vector_store (Optional[SutraVectorStore]): Injected vector store instance.

        Returns:
            None
        ------------------------------------------------------------------------
        """
        self.data_path = data_path or (RAW_DATA_DIR / "shandilya_bhakti_sutra.json")
        self.vector_store = vector_store or SutraVectorStore()
        self.knowledge_base = self._load_and_index_knowledge_base()

    def _load_and_index_knowledge_base(self) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: _load_and_index_knowledge_base
        ------------------------------------------------------------------------
        Purpose:
            Reads Shandilya sutras and indexes them into the ChromaDB collection
            if not already present.

        Parameters:
            None

        Returns:
            List[Dict[str, Any]]: List of loaded Shandilya sutras.
        ------------------------------------------------------------------------
        """
        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding="utf-8") as f:
            items: List[Dict[str, Any]] = json.load(f)

        # Index each Shandilya sutra into the vector store
        for item in items:
            s_no = str(item.get("sutra_no"))
            sanskrit = item.get("sanskrit", "")
            theme = item.get("theme", "")
            en_meaning = item.get("initial_meaning", {}).get("en", "")

            self.vector_store.index_sutra(
                source="shandilya",
                sutra_no=s_no,
                sanskrit=sanskrit,
                theme=theme,
                english_meaning=en_meaning,
            )
        return items

    def match_and_respond(
        self,
        narada_sutra: SutraItem,
        theme: str,
        narada_message: str,
    ) -> Dict[str, Any]:
        """
        ------------------------------------------------------------------------
        Method: match_and_respond
        ------------------------------------------------------------------------
        Purpose:
            Receives Narada's aphorism and message, executes semantic vector
            search against the Shandilya collection to identify the best paired
            sutra, expounds it into multilingual vishleshan, and articulates an
            analytical response addressed to both Narada and the Sutrakar Agent.

        Parameters:
            narada_sutra (SutraItem): The incoming Narada sutra model.
            theme (str): Central philosophical theme.
            narada_message (str): Inter-agent communication from NaradaAgent.

        Returns:
            Dict[str, Any]: Dictionary containing:
                - 'shandilya_sutra': Validated SutraItem for Shandilya.
                - 'agent_message_to_sutrakar': Scholarly response message.
        ----------------------------------------------------------------------------
        """
        # Query vector store for the closest Shandilya sutra
        query_text = f"Theme: {theme}. Verse: {narada_sutra.sanskrit}. Meaning: {narada_sutra.vishleshan.en}"
        matches = self.vector_store.query_similar_sutras(
            query_text=query_text,
            target_source="shandilya",
            top_k=1,
        )

        matched_data: Optional[Dict[str, Any]] = None
        if matches:
            meta = matches[0].get("metadata", {})
            matched_s_no = meta.get("sutra_no")
            for item in self.knowledge_base:
                if str(item.get("sutra_no")) == str(matched_s_no):
                    matched_data = item
                    break

        if not matched_data and self.knowledge_base:
            # Fallback to corresponding index or first entry
            matched_data = self.knowledge_base[0]

        s_no = str(matched_data.get("sutra_no", "1"))
        sanskrit = matched_data.get("sanskrit", "अथातो भक्तिजिज्ञासा॥")
        init_en = matched_data.get("initial_meaning", {}).get("en", "")

        prompt = f"""You are the 'Shandilya Bhakti Sutra Specialist Agent' representing Maharshi Shandilya's school of rigorous, epistemological devotion.

You received this proposition from the Narada Agent:
"{narada_message}"

Narada Verse: {narada_sutra.sanskrit}
Narada Analysis: {narada_sutra.vishleshan.en}

Your Selected Matching Shandilya Sutra #{s_no}:
Sanskrit: {sanskrit}
Initial English Context: {init_en}

Your Tasks:
1. Provide an analytical, epistemological vishleshan of Shandilya Sutra #{s_no} across three languages (English, Hindi, Marathi).
2. Articulate a scholarly response message addressed to both Narada Agent and the 'Sutrakar Agent' (Compiler). Explain how Shandilya's view of 'anurakti' (attachment founded on knowledge of God's majesty) or 'jijnasa' (spiritual inquiry) correlates with or grounds Narada's ecstatic love.

Provide output strictly in this valid JSON format:
{{
  "vishleshan": {{
    "en": "Detailed English epistemological analysis...",
    "hi": "हिंदी में दार्शनिक एवं ज्ञानात्मक विश्लेषण...",
    "mr": "मराठीतील तात्विक आणि ज्ञानमूलक विश्लेषण..."
  }},
  "message_to_sutrakar": "Pranams Narada Agent and Sutrakar. In response to Narada Sutra #{narada_sutra.sutra_no}, Shandilya Sutra #{s_no} establishes that..."
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
            msg = parsed.get("message_to_sutrakar", "")
        except Exception:
            vishleshan_data = {
                "en": (
                    f"Shandilya Bhakti Sutra #{s_no} ({sanskrit}) approaches devotion through epistemological inquiry ('jijñāsā') "
                    f"and supreme attachment ('parānurakti') directed toward Ishvara. Unlike mere sentimental impulse, Shandilya "
                    f"grounds devotion as a legitimate, sovereign means of direct spiritual knowledge (Pramāna) and eternal liberation."
                ),
                "hi": (
                    f"शांडिल्य भक्ति सूत्र #{s_no} ({sanskrit}) भक्ति को ज्ञाननिष्ठ जिज्ञासा और ईश्वर के प्रति 'परानुरक्ति' के रूप में "
                    f"प्रतिपादित करता है। यह भक्ति को केवल भावुकता नहीं, बल्कि मुक्ति का सर्वोच्च दार्शनिक आधार सिद्ध करता है।"
                ),
                "mr": (
                    f"शांडिल्य भक्ति सूत्र #{s_no} ({sanskrit}) भक्तीला तात्त्विक जिज्ञासा आणि ईश्वराप्रती 'परानुरक्ती' म्हणून प्रस्थापित करतो. "
                    f"भक्ती ही केवळ भावनिक नसून अंतिम मोक्ष देणारे सर्वोच्च ज्ञानसाधन आहे हे या सूत्राचे वैशिष्ट्य आहे."
                ),
            }
            msg = (
                f"Respected Narada Agent and Sutrakar Compiler. In response to your exposition of Narada Sutra "
                f"#{narada_sutra.sutra_no}, Shandilya Sutra #{s_no} ('{sanskrit}') establishes that devotion "
                f"attains perfection when accompanied by discerning inquiry and steadfast adherence to Ishvara."
            )

        shandilya_item = SutraItem(
            sutra_no=s_no,
            sanskrit=sanskrit,
            vishleshan=MultilingualText(
                en=vishleshan_data.get("en", init_en),
                hi=vishleshan_data.get("hi"),
                mr=vishleshan_data.get("mr"),
            ),
        )

        return {
            "shandilya_sutra": shandilya_item,
            "agent_message_to_sutrakar": msg,
        }
