"""
================================================================================
Script: scripts/ingest_iks_library.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Dedicated One-Time Ingestion Pipeline for the 20+ Canonical
             Bharatiya Jnana Tradition (IKS) texts into ChromaDB.
             - Reads data/knowledge_repository/sources/iks_canonical_corpus.json
             - Connects to embedded persistent ChromaDB at data/chroma_db
             - Populates the 'iks_canonical_library' collection
             - Indexes full Sanskrit verses, English/Marathi meanings, and
               enterprise principles with rich metadata tags.
================================================================================
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Ensure UTF-8 output encoding across Windows consoles
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import chromadb
from chromadb.config import Settings

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
SOURCES_DIR = BASE_DIR / "data" / "knowledge_repository" / "sources"
CORPUS_FILE = SOURCES_DIR / "iks_canonical_corpus.json"
COLLECTION_NAME = "iks_canonical_library"


def get_chroma_client():
    """Initializes and returns an embedded persistent ChromaDB client."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False, is_persistent=True),
    )


def ingest_iks_canonical_library():
    """Ingests the full canonical IKS corpus into ChromaDB."""
    print("================================================================================")
    print("STARTING ONE-TIME IKS CANONICAL LIBRARY INGESTION INTO CHROMADB")
    print(f"Target Directory : {CHROMA_DIR}")
    print(f"Collection Name  : {COLLECTION_NAME}")
    print(f"Source File      : {CORPUS_FILE}")
    print("================================================================================\n")

    if not CORPUS_FILE.exists():
        raise FileNotFoundError(f"Corpus file not found: {CORPUS_FILE}")

    with open(CORPUS_FILE, "r", encoding="utf-8") as f:
        entries: List[Dict[str, Any]] = json.load(f)

    print(f"[Loaded Entries]: {len(entries)} classical verses and aphorisms.")

    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "20+ Canonical Bharatiya Jnana Tradition Texts for Udyam Sutras"},
    )

    ids = []
    documents = []
    metadatas = []

    for item in entries:
        doc_id = item["id"]
        tradition = item["tradition"]
        section = item["section"]
        verse_no = item["verse_no"]
        sanskrit = item["sanskrit"]
        en_meaning = item["english_meaning"]
        mr_meaning = item["marathi_meaning"]
        principle = item["enterprise_principle"]
        tags = ", ".join(item.get("theme_tags", []))

        # Composite document for rich multilingual and conceptual semantic matching
        doc_text = (
            f"Tradition: {tradition} ({section}, Verse {verse_no})\n"
            f"Sanskrit Verse: {sanskrit}\n"
            f"Enterprise Principle: {principle}\n"
            f"English Meaning: {en_meaning}\n"
            f"Marathi Meaning: {mr_meaning}\n"
            f"Themes: {tags}"
        )

        meta = {
            "id": doc_id,
            "category": item.get("category", "general"),
            "tradition": tradition,
            "section": section,
            "verse_no": verse_no,
            "sanskrit": sanskrit,
            "english_meaning": en_meaning,
            "marathi_meaning": mr_meaning,
            "enterprise_principle": principle,
            "theme_tags": tags,
        }

        ids.append(doc_id)
        documents.append(doc_text)
        metadatas.append(meta)

    # Upsert into ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    total_count = collection.count()
    print(f"\n[Ingestion Successful]: {len(ids)} verses upserted.")
    print(f"[Total Collection Count in '{COLLECTION_NAME}']: {total_count}")

    # Verification Query Test
    print("\n--- Running Verification Semantic Query ---")
    test_query = "truth as sovereign capital, ethical commerce and transparent wealth creation"
    results = collection.query(query_texts=[test_query], n_results=2)
    if results and results.get("ids") and len(results["ids"][0]) > 0:
        for i in range(len(results["ids"][0])):
            m = results["metadatas"][0][i]
            dist = results["distances"][0][i] if results.get("distances") else 0.0
            print(f"  Match {i+1} (Dist: {dist:.3f}): {m['tradition']} [{m['section']}]")
            print(f"    Verse: {m['sanskrit'][:60]}...")
            print(f"    Principle: {m['enterprise_principle']}")

    print("\n[ALL IKS CANONICAL TEXTS PERMANENTLY STORED IN CHROMADB]")


if __name__ == "__main__":
    ingest_iks_canonical_library()
