"""
================================================================================
Module: src.orchestration.five_agent_council
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: The Five-Agent Orchestration Engine for SK Sutras.
             Coordinates:
             - Agent 1: Narada Bhakti Sutra Specialist
             - Agent 2: Shandilya Bhakti Sutra Specialist
             - Agent 3: Bharatiya Jnana Specialist (IKS & Source Documents)
             - Agent 4: Sutrakar (Discussion Lead & Primary Author)
             - Agent 5: Independent Verification Specialist (13 Criteria Auditor)
             Enforces independent document consultation, genuine Shastrartha
             debates, Agent 4 challenging Agent 3, and Agent 5 rejection workflows.
================================================================================
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.agents.bharatiya_jnana_agent import BharatiyaJnanaAgent
from src.agents.narada_agent import NaradaAgent
from src.agents.shandilya_agent import ShandilyaAgent
from src.agents.sutrakar_agent import SutrakarAgent
from src.agents.validator_agent import SanskritMetreValidator, ValidatorAgent
from src.config import BASE_DIR


class FiveAgentCouncil:
    """
    ----------------------------------------------------------------------------
    Class: FiveAgentCouncil
    ----------------------------------------------------------------------------
    Purpose:
        Executes the full Five-Agent research, deliberation, composition, and
        verification pipeline for the 10 original Udyam Sutras.
    ----------------------------------------------------------------------------
    """

    def __init__(self) -> None:
        self.repo_dir = BASE_DIR / "data" / "knowledge_repository"
        self.ledger_file = self.repo_dir / "consultation" / "consultation_ledger.jsonl"
        self.sources_dir = self.repo_dir / "sources"
        self.registry_file = self.repo_dir / "registry" / "source_register.json"

        # Initialize the 5 Specialized Agents
        self.agent1_narada = NaradaAgent()
        self.agent2_shandilya = ShandilyaAgent(force_reindex=False)
        self.agent3_bharatiya = BharatiyaJnanaAgent(repo_dir=self.repo_dir)
        self.agent4_sutrakar = SutrakarAgent(shandilya_agent=self.agent2_shandilya)
        self.agent5_validator = ValidatorAgent()

        # Load Document Register
        self.register_data = self._load_register()

    def _load_register(self) -> Dict[str, Any]:
        if self.registry_file.exists():
            with open(self.registry_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"documents": []}

    def log_agent4_consultation(
        self,
        sutra_no: int,
        doc_id: str,
        section: str,
        finding: str,
        influence: str
    ) -> None:
        """
        Records Agent 4's independent source consultation in the ledger.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "sutra_no": sutra_no,
            "agent_name": "Agent 4 — Sutrakar (Discussion Lead)",
            "document_id": doc_id,
            "section_or_passage": section,
            "independent_consultation": True,
            "finding": finding,
            "influence_on_sutra": influence
        }
        with open(self.ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def run_pre_execution_audit(self) -> Dict[str, Any]:
        """
        Executes Stage 1 Pre-Execution Audit:
        Verifies registered source files, accessibility for Agents 3 and 4,
        and ensures fresh generation context while preserving permanent knowledge.
        """
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "status": "PASS",
            "registered_documents_count": len(self.register_data.get("documents", [])),
            "source_files_verified": [],
            "access_checks": {},
            "notes": []
        }

        required_docs = ["DOC-01", "DOC-02", "DOC-03", "DOC-04"]
        for doc in self.register_data.get("documents", []):
            d_id = doc.get("document_id")
            path = BASE_DIR / doc.get("source_location")
            exists = path.exists() and path.stat().st_size > 0
            audit_results["source_files_verified"].append({
                "doc_id": d_id,
                "path": str(path),
                "exists": exists,
                "size_bytes": path.stat().st_size if exists else 0,
                "is_authoritative": doc.get("is_authoritative")
            })
            if not exists and d_id in required_docs:
                audit_results["status"] = "FAIL"
                audit_results["notes"].append(f"Missing mandatory document: {d_id}")

        # Verify Agent 3 access to DOC-01 and DOC-04
        a3_access = (
            len(self.agent3_bharatiya.source_documents.get("DOC-01", "")) > 1000
            and len(self.agent3_bharatiya.source_documents.get("DOC-04", "")) > 1000
        )
        audit_results["access_checks"]["agent3_source_access"] = "VERIFIED" if a3_access else "FAILED"

        # Verify Agent 4 access
        doc01_file = self.sources_dir / "DOC-01_SHRIMAD_UDYAM_SUTRANI_100.txt"
        a4_access = doc01_file.exists() and doc01_file.stat().st_size > 1000
        audit_results["access_checks"]["agent4_source_access"] = "VERIFIED" if a4_access else "FAILED"

        # Verify Agent 3 access to ChromaDB 20+ Canonical IKS Collection
        iks_coll_accessible = (
            hasattr(self.agent3_bharatiya, "iks_collection")
            and self.agent3_bharatiya.iks_collection is not None
            and self.agent3_bharatiya.iks_collection.count() >= 20
        )
        audit_results["access_checks"]["chromadb_iks_collection_access"] = (
            "VERIFIED" if iks_coll_accessible else "FAILED"
        )
        if not iks_coll_accessible:
            audit_results["status"] = "FAIL"
            audit_results["notes"].append("ChromaDB iks_canonical_library collection missing or unindexed (< 20 entries).")

        return audit_results

    # ==========================================================================
    # CANONICAL ENTERPRISE TOPIC DOMAINS (DOMAINS A THROUGH Q)
    # Decouples forced 1:1 pairing and introduces topic-driven IKS derivation
    # ==========================================================================
    ENTERPRISE_DOMAINS: List[Dict[str, Any]] = [
        {
            "domain_id": "A",
            "theme": "Enterprise Vision, Sankalpa & Inception",
            "concept": "Passionate entrepreneurial inception, commitment, and single-pointed vision",
            "narada_target": "1",
            "iks_focus": "Kautilya Arthashastra (Utthana) & Taittiriya Upanishad",
        },
        {
            "domain_id": "B",
            "theme": "Rational Due Diligence, Feasibility & Logic (Tarka)",
            "concept": "Empirical scrutiny, market validation, and disciplined capital allocation",
            "narada_target": "2",
            "iks_focus": "Gautama Nyaya Sutras & Brihaspati Niti Shastra",
        },
        {
            "domain_id": "C",
            "theme": "Svadharma, Craftsmanship & Operational Precision",
            "concept": "Zero-defect engineering, pride in production, and sacred dedication to duty",
            "narada_target": "3",
            "iks_focus": "Bhagavad Gita 18.45 & Sant Dnyaneshwar Dnyaneshwari",
        },
        {
            "domain_id": "D",
            "theme": "Ethical Governance & Incorruptible Integrity (Satya-Vyavahara)",
            "concept": "Uncompromising moral rectitude, transparency, and multi-generational trust",
            "narada_target": "4",
            "iks_focus": "Bhartrihari Niti Shataka 68 & Chanakya Niti",
        },
        {
            "domain_id": "E",
            "theme": "Sustainable Capital Stewardship & Non-Greed (Trusteeship)",
            "concept": "Non-extractive commerce, circulation of wealth, and fair stakeholder sharing",
            "narada_target": "5",
            "iks_focus": "Isha Upanishad Mantra 1 & Sant Tukaram Maharaj Abhanga 1",
        },
        {
            "domain_id": "F",
            "theme": "Founder Mental Health & Psychological Resilience (Patanjali)",
            "concept": "Overcoming anxiety, depression, burnout, and acute market volatility through inner mastery",
            "narada_target": "6",
            "iks_focus": "Patanjali Yoga Sutras 1.12-14 (Abhyasa-Vairagya)",
        },
        {
            "domain_id": "G",
            "theme": "Team Alignment, Shared Purpose & Sangha Power",
            "concept": "Cohesive organizational culture, psychological safety, and collective intelligence",
            "narada_target": "7",
            "iks_focus": "Rigveda Samhita 10.191 (Sangacchadhvam) & Vidura Niti",
        },
        {
            "domain_id": "H",
            "theme": "Executive Strategic Vigilance & Enterprise Risk Management",
            "concept": "Zero complacency, cash runway awareness, and robust corporate defense",
            "narada_target": "8",
            "iks_focus": "Kautilya Arthashastra 1.15 & Vidura Niti 33.16",
        },
        {
            "domain_id": "I",
            "theme": "Leadership by Example & Tone-at-the-Top (Shreshtha Achara)",
            "concept": "Embodied ethical leadership, moral stature, and culture creation by demonstration",
            "narada_target": "9",
            "iks_focus": "Bhagavad Gita 3.21 & Samarth Ramdas Dasbodh",
        },
        {
            "domain_id": "J",
            "theme": "Crisis Equanimity, Patience & Agility in Volatility",
            "concept": "Inner poise amid economic storms, anti-fragile adaptability, and unhurried strategy",
            "narada_target": "10",
            "iks_focus": "Bhagavad Gita 2.48 & Sant Eknath Maharaj",
        },
    ]

    def get_enterprise_domain(self, domain_id: str) -> Optional[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_enterprise_domain
        ------------------------------------------------------------------------
        Purpose:
            Looks up an enterprise thematic domain by ID (e.g. 'A', 'B') to guide
            decoupled Shastrartha topic routing.
        ------------------------------------------------------------------------
        """
        for d in self.ENTERPRISE_DOMAINS:
            if d["domain_id"].upper() == domain_id.upper():
                return d
        return None
