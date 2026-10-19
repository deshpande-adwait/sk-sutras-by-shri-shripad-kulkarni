"""
================================================================================
Test Module: tests.test_vectorstore
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Senior Lead QA test suite verifying ChromaDB embedded vector store
             indexing, metadata integrity, and semantic retrieval operations.
================================================================================
"""

from pathlib import Path
import pytest
from src.vectorstore.chroma_store import SutraVectorStore


@pytest.fixture
def temp_vector_store(tmp_path: Path) -> SutraVectorStore:
    """
    ----------------------------------------------------------------------------
    Fixture: temp_vector_store
    ----------------------------------------------------------------------------
    Purpose:
        Initializes an isolated SutraVectorStore instance targeting a pytest
        temporary directory.

    Parameters:
        tmp_path (Path): Pytest temporary path fixture.

    Returns:
        SutraVectorStore: Clean, isolated vector store instance.
    ----------------------------------------------------------------------------
    """
    chroma_dir = tmp_path / "test_chroma"
    return SutraVectorStore(persist_directory=chroma_dir, collection_name="test_sutras")


def test_index_and_count_sutras(temp_vector_store: SutraVectorStore) -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_index_and_count_sutras
    ----------------------------------------------------------------------------
    Purpose:
        Verifies that aphorisms can be indexed and that the collection count
        increments accurately.

    Parameters:
        temp_vector_store (SutraVectorStore): Isolated test vector store.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    initial_count = temp_vector_store.count()
    assert initial_count == 0

    doc_id = temp_vector_store.index_sutra(
        source="narada",
        sutra_no="1",
        sanskrit="अथातो भक्तिं व्याख्यास्यामः॥",
        theme="Definition of Bhakti",
        english_meaning="Now, therefore, we shall expound Devotion.",
    )

    assert doc_id == "narada_1"
    assert temp_vector_store.count() == 1


def test_query_similar_sutras(temp_vector_store: SutraVectorStore) -> None:
    """
    ----------------------------------------------------------------------------
    Function: test_query_similar_sutras
    ----------------------------------------------------------------------------
    Purpose:
        Verifies semantic search retrieval and metadata filtering.

    Parameters:
        temp_vector_store (SutraVectorStore): Isolated test vector store.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    temp_vector_store.index_sutra(
        source="narada",
        sutra_no="2",
        sanskrit="सा त्वस्मिन् परमप्रेमरूपा॥",
        theme="Supreme Love",
        english_meaning="Devotion is supreme love.",
    )
    temp_vector_store.index_sutra(
        source="shandilya",
        sutra_no="2",
        sanskrit="सा परानुरक्तिरीश्वरे॥",
        theme="Supreme Love",
        english_meaning="Devotion is supreme attachment to the Lord.",
    )

    results = temp_vector_store.query_similar_sutras(
        query_text="love and devotion to God",
        target_source="shandilya",
        top_k=1,
    )

    assert len(results) > 0
    match = results[0]
    assert match["metadata"]["source"] == "shandilya"
    assert match["metadata"]["sutra_no"] == "2"
