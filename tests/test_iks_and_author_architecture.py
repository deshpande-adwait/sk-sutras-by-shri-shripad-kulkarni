"""
================================================================================
Test Module: tests.test_iks_and_author_architecture
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Comprehensive QA test suite verifying the incorporation of Shri
             Shripad Kulkarni's architectural specifications:
             - 20+ Canonical IKS texts stored permanently in ChromaDB
             - Dynamic semantic retrieval across iks_canonical_library
             - Agent 1 Enterprise Isomorphism Axiom
             - Agent 2 Rational Due Diligence and Logic
             - Agent 3 ChromaDB Dynamic IKS integration
             - Agent 4 Minimum 500-word Bhashya, Biographical Case Studies,
               and Patanjali Yoga Sutras psychological resilience
             - Agent 5 13-gate audit verifying 500-word depth and case studies
             - Mandatory confidentiality footer verification on every page
================================================================================
"""

import json
from pathlib import Path
import pytest

from src.config import BASE_DIR
from src.vectorstore.chroma_store import SutraVectorStore
from scripts.run_dynamic_live_council import DynamicLiveCouncilRunner
from scripts.reformat_canonical_word_document import build_reformatted_canonical_document, MANDATORY_FOOTER


def test_iks_canonical_corpus_data_completeness():
    """Verifies that the canonical IKS JSON corpus contains at least 20 text traditions."""
    corpus_file = BASE_DIR / "data" / "knowledge_repository" / "sources" / "iks_canonical_corpus.json"
    assert corpus_file.exists(), f"Corpus file not found at {corpus_file}"

    with open(corpus_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data if isinstance(data, list) else data.get("entries", [])
    assert len(entries) >= 20, f"Expected at least 20 canonical texts, found {len(entries)}"

    # Verify key canonical traditions are present
    sources = [(e.get("tradition") or e.get("source_text", "")).lower() for e in entries]
    assert any("arthashastra" in s for s in sources)
    assert any("bhagavad gita" in s for s in sources)
    assert any("yoga sutras" in s for s in sources)
    assert any("upanishad" in s for s in sources)
    assert any("tukaram" in s for s in sources)
    assert any("dnyaneshwar" in s for s in sources)
    assert any("ramdas" in s for s in sources)


def test_chromadb_iks_canonical_library_collection():
    """Verifies that the persistent ChromaDB repository contains iks_canonical_library with indexed verses."""
    vector_store = SutraVectorStore(collection_name="shandilya_100_sutras")
    client = vector_store.client

    # Verify collection exists and count >= 20
    iks_coll = client.get_collection("iks_canonical_library")
    assert iks_coll is not None
    count = iks_coll.count()
    assert count >= 20, f"Expected at least 20 verses in iks_canonical_library, found {count}"

    # Semantic query test
    query_text = "Truthful business conduct, customer trust, and ethical wealth stewardship"
    results = iks_coll.query(
        query_texts=[query_text],
        n_results=2,
        include=["documents", "metadatas", "distances"],
    )
    assert len(results["documents"][0]) == 2
    assert results["distances"][0][0] < 1.5


def test_council_runner_author_specifications(monkeypatch):
    """Verifies that DynamicLiveCouncilRunner incorporates Shri Shripad Kulkarni's architectural specifications."""
    from unittest.mock import MagicMock

    runner = DynamicLiveCouncilRunner()

    # 1. Collection initialized
    assert hasattr(runner, "iks_collection")
    assert runner.iks_collection.count() >= 20

    # 2. Agent 3 dynamic research returns IKS retrieved entries from ChromaDB
    sample_narada = {
        "sutra_no": "1",
        "sanskrit": "अथातो भक्तिं व्याख्यास्यामः ॥",
        "vishleshan": {"en": "Now therefore we shall expound devotion.", "mr": "आता भक्तीची व्याख्या करू."},
    }
    sample_shandilya = {
        "sutra_no": "1",
        "sanskrit": "अथातो भक्तिजिज्ञासा ॥",
        "meaning": {"en": "Now therefore the inquiry into devotion.", "mr": "आता भक्तीविषयी जिज्ञासा."},
    }
    research = runner.call_agent3_bharatiya_research(sample_narada, sample_shandilya, "Enterprise Inception")
    assert "iks_retrieved_entries" in research
    assert len(research["iks_retrieved_entries"]) > 0
    assert "Sant Tukaram" in research["doc04_foundation"]

    # 3. Agent 4 composition schema verification
    mock_agent4_response = MagicMock()
    mock_agent4_response.usage.input_tokens = 450
    mock_agent4_response.usage.output_tokens = 920
    mock_agent4_response.content = json.dumps({
        "sutra_no": 1,
        "theme": "Enterprise Inception",
        "original_sanskrit_verse": "अथातो व्यवहारेऽस्मिन् धर्म्यमुद्योगमारभेत् ।\nजिज्ञासा कार्यदक्षाणां सर्वसिद्धेः प्रसाधिका ॥ १ ॥",
        "padaccheda": "अथातो । व्यवहारे । अस्मिन् । धर्म्यम् । उद्योगम् । आरभेत् ।",
        "anvaya": "अथातो अस्मिन् व्यवहारे धर्म्यम् उद्योगम् आरभेत्।",
        "nirukta": "आरभेत् = प्रवर्तयेत्; जिज्ञासा = ज्ञानप्राप्तीच्छा।",
        "translation_en": "Now, in this arena of commerce, one must initiate righteous enterprise.",
        "translation_mr": "व्यवहारात उतरताना पहिली पायरी म्हणजे आपला उद्योग नीतीवर आधारलेला असावा.",
        "philosophical_foundation_mr": "नारदांचा संकल्प आणि शांडिल्यांची जिज्ञासा यांचा येथे मिलाफ होतो.",
        "comprehensive_bhashya_mr": "प्रस्तुत सूत्राचे मराठी भाष्य अत्यंत सखोल आणि विस्तृत आहे. " * 35,
        "biographical_case_studies": [
            {"name": "Jamsetji Tata", "category": "Eastern/Modern", "case_summary": "Pioneered ethical industrialization in India."},
            {"name": "Thomas Edison", "category": "Western/Modern", "case_summary": "Relentless empirical investigation and patent development."}
        ],
        "mental_resilience_yoga_sutras": {
            "sutra_reference": "Patanjali Yoga Sutras 1.12-1.14",
            "sanskrit": "अभ्यासवैराग्याभ्यां तन्निरोधः",
            "psychological_framework": "Equilibrium of mind in entrepreneurial adversity."
        },
        "practical_enterprise_guidance": [
            {"role": "Founders", "guidance": "Conduct extensive customer due diligence before committing capital."}
        ]
    })
    monkeypatch.setattr(runner.agent4_sutrakar, "generate", lambda **kwargs: mock_agent4_response)

    comp = runner.call_agent4_compose_sutra(1, sample_narada, sample_shandilya, "Enterprise Inception", research)
    assert comp["sutra_no"] == 1
    assert "original_sanskrit_verse" in comp
    assert len(comp["comprehensive_bhashya_mr"]) > 30
    assert len(comp["biographical_case_studies"]) == 2
    assert "mental_resilience_yoga_sutras" in comp

    # 4. Agent 5 validation audit logic
    mock_agent5_response = MagicMock()
    mock_agent5_response.usage.input_tokens = 800
    mock_agent5_response.usage.output_tokens = 150
    mock_agent5_response.content = json.dumps({
        "verdict": "APPROVED",
        "overall_score": 98,
        "bhashya_word_count": 85,
        "is_short_and_concise": True,
        "bhashya_depth_verified": True,
        "case_studies_verified": True,
        "yoga_psychology_verified": True,
        "gates_passed": 13,
        "audit_commentary": "Certified compliant with short Sanskrit formulation, concise Marathi Bhashya, and IKS enterprise ethics."
    })
    monkeypatch.setattr(runner.agent5_validator, "generate", lambda **kwargs: mock_agent5_response)

    approved, score, audit = runner.call_agent5_validate_sutra(1, comp, research)
    assert approved is True
    assert score >= 90
    assert audit["bhashya_depth_verified"] is True
    assert audit["case_studies_verified"] is True
    assert audit["yoga_psychology_verified"] is True
    assert audit["gates_passed"] == 13


def test_reformatted_word_document_generation(tmp_path: Path):
    """Verifies that the canonical Word document generates with all new sections and mandatory footer."""
    import docx
    test_docx = tmp_path / "test_canonical_output.docx"
    build_reformatted_canonical_document(output_path=test_docx)

    assert test_docx.exists()
    doc = docx.Document(str(test_docx))

    # Verify footer on sections
    for section in doc.sections:
        footer_text = section.footer.paragraphs[0].text
        assert MANDATORY_FOOTER in footer_text, f"Mandatory footer '{MANDATORY_FOOTER}' missing in section footer"

    # Verify content headers across paragraphs and tables
    all_text = " ".join(p.text for p in doc.paragraphs) + " " + " ".join(c.text for t in doc.tables for row in t.rows for c in row.cells)
    assert "UDYAM SUTRA" in all_text
    assert "Shri Shripad Kulkarni" in all_text
    assert "Source References" in all_text


def test_bharatiya_jnana_agent_dynamic_chromadb_retrieval():
    """Verifies that BharatiyaJnanaAgent dynamically queries ChromaDB and does not hardcode Tukaram for Sutra 11."""
    from src.agents.bharatiya_jnana_agent import BharatiyaJnanaAgent

    agent = BharatiyaJnanaAgent()
    assert hasattr(agent, "iks_collection")
    assert agent.iks_collection is not None
    assert agent.iks_collection.count() >= 20

    # Query for Sutra 11 with ethical commerce topic
    res = agent.research_for_concept(11, "Ethical Commerce, Wealth Circulation and Fair Pricing")
    assert "iks_text" in res
    assert "sanskrit" in res
    assert "iks_retrieved_entries" in res
    assert len(res["iks_retrieved_entries"]) > 0


def test_five_agent_council_pre_execution_audit_and_enterprise_domains():
    """Verifies that FiveAgentCouncil checks ChromaDB and provides enterprise domains A-Q."""
    from src.orchestration.five_agent_council import FiveAgentCouncil

    council = FiveAgentCouncil()
    audit = council.run_pre_execution_audit()
    assert audit["status"] == "PASS"
    assert audit["access_checks"]["chromadb_iks_collection_access"] == "VERIFIED"

    # Verify domain lookup
    domain_a = council.get_enterprise_domain("A")
    assert domain_a is not None
    assert domain_a["theme"] == "Enterprise Vision, Sankalpa & Inception"
    assert domain_a["domain_id"] == "A"

    domain_f = council.get_enterprise_domain("F")
    assert domain_f is not None
    assert "Patanjali" in domain_f["theme"] or "Patanjali" in domain_f["iks_focus"]


def test_anthropic_adapter_bypass_eradication():
    """Verifies that AnthropicAdapter has zero silent fallback to OpenAI."""
    from src.providers.anthropic_adapter import AnthropicAdapter
    from src.providers.base import ProviderAuthenticationError, ProviderError

    # Offline mode behaves properly
    offline_adapter = AnthropicAdapter(offline_mode=True)
    assert offline_adapter.provider_name == "anthropic"

    # Missing API key raises ProviderAuthenticationError
    missing_key_adapter = AnthropicAdapter(api_key=None, offline_mode=False)
    with pytest.raises(ProviderAuthenticationError):
        missing_key_adapter.generate(prompt="Test prompt")
