"""
================================================================================
Module: src.vectorstore.chroma_store
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Embedded persistent ChromaDB vector store manager. Encapsulates
             semantic aphorism indexing and multilingual cross-text retrieval
             between Narada Bhakti Sutra and Shandilya Bhakti Sutra using BAAI/bge-m3.
================================================================================
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config import CHROMA_DIR


class SutraVectorStore:
    """
    ----------------------------------------------------------------------------
    Class: SutraVectorStore
    ----------------------------------------------------------------------------
    Purpose:
        Manages the local embedded ChromaDB vector collection. Facilitates
        semantic vector indexing of Sanskrit sutras and their analytical
        expositions (English/Hindi/Marathi), allowing multi-agent graph nodes
        to discover thematic pairings between Narada and Shandilya texts.

    Attributes:
        persist_dir (Path): Local filesystem directory for ChromaDB persistence.
        client (Any): ChromaDB client instance.
        collection (Any): Vector collection for sutra aphorisms.
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        persist_directory: Optional[Path] = None,
        collection_name: str = "bhakti_sutras_comparative",
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the ChromaDB persistent client and retrieves or creates
            the comparative aphorism collection.

        Parameters:
            persist_directory (Optional[Path]): Directory where ChromaDB files are stored.
            collection_name (str): Unique name of the vector collection.

        Returns:
            None

        Errors:
            Exception: If ChromaDB client fails to initialize.

        Manual Debugging Notes:
            - When running offline tests where heavy embedding models cannot be
              downloaded, ChromaDB uses its default cosine space with metadata filters.
        ------------------------------------------------------------------------
        """
        self.persist_dir: Path = persist_directory or CHROMA_DIR
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        self.client = self._init_client()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Multilingual Bhakti Sutras Vector Index"},
        )

    def _init_client(self) -> Any:
        """
        ------------------------------------------------------------------------
        Method: _init_client
        ------------------------------------------------------------------------
        Purpose:
            Safely initializes and returns an embedded persistent ChromaDB client.

        Parameters:
            None

        Returns:
            chromadb.PersistentClient: Embedded persistent ChromaDB client instance.

        Errors:
            ImportError: If chromadb package is not installed.
        ------------------------------------------------------------------------
        """
        try:
            import chromadb
            from chromadb.config import Settings
            return chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=Settings(anonymized_telemetry=False, is_persistent=True),
            )
        except ImportError:
            raise ImportError(
                "chromadb is not installed. Please install it via pip: pip install chromadb"
            )

    def index_sutra(
        self,
        source: str,
        sutra_no: str,
        sanskrit: str,
        theme: str,
        english_meaning: str,
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        ------------------------------------------------------------------------
        Method: index_sutra
        ------------------------------------------------------------------------
        Purpose:
            Indexes an individual Sanskrit sutra along with its semantic theme
            and English translation into the vector store.

        Parameters:
            source (str): Source identifier ('narada' or 'shandilya').
            sutra_no (str): Canonical numbering string.
            sanskrit (str): Sanskrit verse in Devanagari.
            theme (str): Philosophical theme.
            english_meaning (str): English translation/exposition.
            extra_metadata (Optional[Dict[str, Any]]): Additional metadata attributes.

        Returns:
            str: The unique document ID created for the vector index.

        Errors:
            ValueError: If required fields are blank.
        ------------------------------------------------------------------------
        """
        doc_id = f"{source}_{sutra_no}"
        # Combine Devanagari and English semantic text for rich multilingual matching
        document_text = f"Source: {source} Sutra {sutra_no}\nTheme: {theme}\nSanskrit: {sanskrit}\nMeaning: {english_meaning}"

        metadata = {
            "source": source,
            "sutra_no": sutra_no,
            "theme": theme,
            "sanskrit": sanskrit,
            "english_meaning": english_meaning,
        }
        if extra_metadata:
            metadata.update(extra_metadata)

        self.collection.upsert(
            ids=[doc_id],
            documents=[document_text],
            metadatas=[metadata],
        )
        return doc_id

    def query_similar_sutras(
        self,
        query_text: str,
        target_source: Optional[str] = None,
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: query_similar_sutras
        ------------------------------------------------------------------------
        Purpose:
            Performs semantic similarity search against the vector index to identify
            philosophically aligned aphorisms. Can filter by target text source.

        Parameters:
            query_text (str): Query string (theme, meaning, or concept).
            target_source (Optional[str]): Target source to filter (e.g. 'shandilya').
            top_k (int): Number of top semantic matches to retrieve.

        Returns:
            List[Dict[str, Any]]: List of matching results with metadata and distances.

        Errors:
            Exception: If query execution fails within ChromaDB.
        ------------------------------------------------------------------------
        """
        where_filter: Optional[Dict[str, Any]] = None
        if target_source:
            where_filter = {"source": target_source}

        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k,
            where=where_filter,
        )

        formatted_matches: List[Dict[str, Any]] = []
        if results and results.get("ids") and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                doc_id = results["ids"][0][i]
                metadata = results["metadatas"][0][i] if results.get("metadatas") else {}
                distance = results["distances"][0][i] if results.get("distances") else 0.0
                formatted_matches.append({
                    "id": doc_id,
                    "metadata": metadata,
                    "distance": distance,
                })
        return formatted_matches

    def count(self) -> int:
        """
        ------------------------------------------------------------------------
        Method: count
        ------------------------------------------------------------------------
        Purpose:
            Returns the total number of indexed sutras currently in the collection.

        Parameters:
            None

        Returns:
            int: Number of indexed records.
        ------------------------------------------------------------------------
        """
        return self.collection.count()
