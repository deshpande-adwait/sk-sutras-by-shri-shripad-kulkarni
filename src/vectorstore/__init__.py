"""
================================================================================
Package: src.vectorstore
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Embedded ChromaDB vector store and multilingual embedding manager
             using BAAI/bge-m3 for semantic aphorism cross-matching.
================================================================================
"""

from src.vectorstore.chroma_store import SutraVectorStore

__all__ = ["SutraVectorStore"]
