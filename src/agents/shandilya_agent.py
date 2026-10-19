"""
================================================================================
Module: src.agents.shandilya_agent
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: The Shandilya Bhakti Sutra Specialist Agent. Maintains the complete
             100-sutra canonical repository in ChromaDB. Receives propositions from
             NaradaAgent, searches across all 100 Shandilya aphorisms, shortlists
             top candidate matches based on semantic distance, and submits them
             to SutrakarAgent for logical evaluation.
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
        Represents Maharshi Shandilya's school of epistemological devotion
        (Bhakti-Jijnasa). Maintains the full 100-sutra corpus in ChromaDB,
        evaluates incoming Narada propositions against the entire canon, and
        provides shortlisted candidate aphorisms with similarity metrics
        to the Sutrakar Agent.

    Attributes:
        data_path (Path): Path to shandilya_bhakti_sutra.json (100 sutras).
        vector_store (SutraVectorStore): ChromaDB embedded vector store.
        knowledge_base (List[Dict[str, Any]]): 100 Shandilya sutras in memory.
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        data_path: Optional[Path] = None,
        vector_store: Optional[SutraVectorStore] = None,
        force_reindex: bool = False,
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes ShandilyaAgent, loads all 100 canonical sutras, and
            ensures all 100 are indexed in ChromaDB.
        ------------------------------------------------------------------------
        """
        self.data_path = data_path or (RAW_DATA_DIR / "shandilya_bhakti_sutra.json")
        self.vector_store = vector_store or SutraVectorStore(collection_name="shandilya_100_sutras")
        self.knowledge_base = self._load_and_index_knowledge_base(force_reindex=force_reindex)

    def _load_and_index_knowledge_base(self, force_reindex: bool = False) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: _load_and_index_knowledge_base
        ------------------------------------------------------------------------
        Purpose:
            Loads all 100 Shandilya sutras from JSON and indexes them into ChromaDB.
        ------------------------------------------------------------------------
        """
        if not self.data_path.exists():
            return []

        with open(self.data_path, "r", encoding="utf-8") as f:
            items: List[Dict[str, Any]] = json.load(f)

        # Index all 100 sutras into ChromaDB if not already indexed
        current_count = self.vector_store.count()
        if force_reindex or current_count < len(items):
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

    def get_sutra_by_number(self, sutra_no: str) -> Optional[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_sutra_by_number
        ------------------------------------------------------------------------
        Purpose:
            Retrieves a Shandilya aphorism by its number (1 to 100).
        ------------------------------------------------------------------------
        """
        for item in self.knowledge_base:
            if str(item.get("sutra_no")) == str(sutra_no):
                return item
        return None

    def search_candidates(
        self,
        narada_sutra: SutraItem,
        theme: str,
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: search_candidates
        ------------------------------------------------------------------------
        Purpose:
            Executes semantic similarity search against all 100 Shandilya sutras
            using Narada's verse, theme, and English meaning. Returns top candidates
            with distance metrics.

        Parameters:
            narada_sutra (SutraItem): The incoming Narada aphorism model.
            theme (str): Unifying philosophical theme.
            top_k (int): Number of candidate matches to return.

        Returns:
            List[Dict[str, Any]]: Shortlisted candidate matches with full metadata.
        ------------------------------------------------------------------------
        """
        query_text = (
            f"Philosophical Theme: {theme}\n"
            f"Devanagari Sanskrit: {narada_sutra.sanskrit}\n"
            f"Meaning: {narada_sutra.vishleshan.en}"
        )

        matches = self.vector_store.query_similar_sutras(
            query_text=query_text,
            target_source="shandilya",
            top_k=top_k,
        )

        candidates: List[Dict[str, Any]] = []
        for m in matches:
            meta = m.get("metadata", {})
            s_no = str(meta.get("sutra_no"))
            raw = self.get_sutra_by_number(s_no)
            if raw:
                candidates.append({
                    "sutra_no": s_no,
                    "sanskrit": raw.get("sanskrit", ""),
                    "theme": raw.get("theme", ""),
                    "meaning": raw.get("initial_meaning", {}),
                    "distance": m.get("distance", 1.0),
                })
        return candidates

    def formulate_candidate_response(
        self,
        narada_sutra: SutraItem,
        theme: str,
        narada_message: str,
        candidates: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        ------------------------------------------------------------------------
        Method: formulate_candidate_response
        ------------------------------------------------------------------------
        Purpose:
            Examines the top candidates from the 100 Shandilya sutras and articulates
            a scholarly message to NaradaAgent and SutrakarAgent presenting the
            shortlisted aphorisms with their theological relevance.
        ------------------------------------------------------------------------
        """
        candidate_summaries = []
        for c in candidates:
            candidate_summaries.append(
                f"- Shandilya Sutra #{c['sutra_no']} ({c['sanskrit']}) [Theme: {c['theme']}]: {c['meaning'].get('en', '')}"
            )
        cand_str = "\n".join(candidate_summaries)

        message = (
            f"Respected Narada Agent and Sutrakar Compiler: In response to Narada Sutra #{narada_sutra.sutra_no} "
            f"('{narada_sutra.sanskrit}' on '{theme}'), I have queried the entire 100-sutra Shandilya canon. "
            f"Here are the top candidate aphorisms identified by semantic relevance:\n{cand_str}\n"
            f"I submit these candidates to the Sutrakar Agent to determine whether a genuine, non-forced "
            f"logical correspondence exists."
        )

        return {
            "candidates": candidates,
            "agent_message_to_sutrakar": message,
        }

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
            Provides direct semantic matching and conversational response for a
            given Narada sutra candidate. Searches across the full 100 Shandilya
            corpus in ChromaDB, retrieves the top candidates, formats the
            inter-agent message addressed to SutrakarAgent, and packages the top
            Shandilya sutra as a validated SutraItem.

        Parameters:
            narada_sutra (SutraItem): The input Narada aphorism model.
            theme (str): Unifying philosophical theme.
            narada_message (str): Explanatory message from NaradaAgent.

        Returns:
            Dict[str, Any]: Dictionary containing:
                - 'shandilya_sutra': SutraItem instance for the top candidate.
                - 'agent_message_to_sutrakar': Scholarly message addressed to SutrakarAgent.
                - 'candidates': Full list of shortlisted candidate dictionaries.

        Manual Debugging Notes:
            - If ChromaDB returns no matches, falls back to sutra #1.
            - Ensures SutraItem schema validation succeeds for multilingual fields.
        ------------------------------------------------------------------------
        """
        candidates = self.search_candidates(narada_sutra=narada_sutra, theme=theme, top_k=3)
        formatted = self.formulate_candidate_response(
            narada_sutra=narada_sutra,
            theme=theme,
            narada_message=narada_message,
            candidates=candidates,
        )

        top_cand = candidates[0] if candidates else None
        if not top_cand:
            raw = self.get_sutra_by_number("1") or {}
            top_cand = {
                "sutra_no": "1",
                "sanskrit": raw.get("sanskrit", "अथातो भक्तिजिज्ञासा॥"),
                "theme": raw.get("theme", "Definition of Bhakti"),
                "meaning": raw.get("initial_meaning", {"en": "Now, therefore, the inquiry into Devotion."}),
            }

        shandilya_sutra_item = SutraItem(
            sutra_no=str(top_cand.get("sutra_no", "1")),
            sanskrit=top_cand.get("sanskrit", ""),
            vishleshan=MultilingualText(
                en=top_cand.get("meaning", {}).get("en", "Analytical exposition"),
                hi=top_cand.get("meaning", {}).get("hi"),
                mr=top_cand.get("meaning", {}).get("mr"),
            ),
        )

        return {
            "shandilya_sutra": shandilya_sutra_item,
            "agent_message_to_sutrakar": formatted["agent_message_to_sutrakar"],
            "candidates": candidates,
        }

