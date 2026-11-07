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

        required_docs = ["DOC-01", "DOC-02", "DOC-03"]
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

        # Verify Agent 3 access
        a3_access = len(self.agent3_bharatiya.source_documents.get("DOC-01", "")) > 1000
        audit_results["access_checks"]["agent3_source_access"] = "VERIFIED" if a3_access else "FAILED"

        # Verify Agent 4 access
        doc01_file = self.sources_dir / "DOC-01_SHRIMAD_UDYAM_SUTRANI_100.txt"
        a4_access = doc01_file.exists() and doc01_file.stat().st_size > 1000
        audit_results["access_checks"]["agent4_source_access"] = "VERIFIED" if a4_access else "FAILED"

        return audit_results
