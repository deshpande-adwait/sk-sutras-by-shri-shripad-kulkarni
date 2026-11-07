"""
================================================================================
Script: scripts/init_knowledge_repository.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Initializes the Persistent Knowledge Governance and Source Traceability
             Repository for the Five-Agent AI System.
             - Saves DOC-01 (100 Udyam Shlokas)
             - Saves DOC-02 (Udyam Sutre Manuscript Karyavritti 17)
             - Saves DOC-03 (Udyam Sutre Manuscript Karyavritti 05)
             - Populates the Source Document Register (registry/source_register.json)
             - Initializes Consultation Ledger & Research Repositories
================================================================================
"""

import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR / "data" / "knowledge_repository"
SOURCES_DIR = REPO_DIR / "sources"
REGISTRY_DIR = REPO_DIR / "registry"
CONSULT_DIR = REPO_DIR / "consultation"
RESEARCH_DIR = REPO_DIR / "research"

SOURCES_DIR.mkdir(parents=True, exist_ok=True)
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
CONSULT_DIR.mkdir(parents=True, exist_ok=True)
RESEARCH_DIR.mkdir(parents=True, exist_ok=True)


def init_source_register():
    """Builds and persists the comprehensive Source Document Register."""
    register_data = {
        "repository_name": "SK Sutras - Persistent Knowledge Repository",
        "governance_authority": "Hiranyam AI Labs & Shri Shripad Kulkarni",
        "last_updated": datetime.now().isoformat(),
        "documents": [
            {
                "document_id": "DOC-01",
                "filename": "DOC-01_SHRIMAD_UDYAM_SUTRANI_100.txt",
                "title": "श्रीमद् उद्यम सूत्राणि (सूत्र १ ते १००)",
                "document_type": "Primary Reference Anthology & Commentary",
                "date_received": "2026-11-07",
                "version": "1.0-Anthology",
                "last_modified": "2026-11-07",
                "source_location": "data/knowledge_repository/sources/DOC-01_SHRIMAD_UDYAM_SUTRANI_100.txt",
                "status": "Authoritative Reference (Subhashita & Classical Analogy Anthology)",
                "is_authoritative": True,
                "scope": "100 aphorisms covering execution, time, ethics, risk, team, and trusteeship with modern corporate cases.",
                "known_conflicts": "Contains direct verbatim quotations of classical Gita, Arthashastra, and Hitopadesha verses treated as Udyam Sutras. Must not be directly plagiarized or paraphrased as original modern composition."
            },
            {
                "document_id": "DOC-02",
                "filename": "DOC-02_UDYAM_SUTRE_MANUSCRIPT_V17.txt",
                "title": "उद्यमसूत्रे: भारतीय ज्ञानपरंपरेतून उद्योजकीय जीवनदर्शन (कार्यावृत्ती १७)",
                "document_type": "Primary Working Manuscript Draft",
                "date_received": "2026-11-07",
                "version": "कार्यावृत्ती १७ (Revision 17)",
                "last_modified": "2026-11-07",
                "source_location": "data/knowledge_repository/sources/DOC-02_UDYAM_SUTRE_MANUSCRIPT_V17.txt",
                "status": "Latest Master Working Draft (Comprehensive Canon & Appendices)",
                "is_authoritative": True,
                "scope": "Contains Chapters 1 to 6, complete commentary on Narada Bhakti Sutras 1 to 84, Appendices A to G, 6 case studies, 12-week course curriculum, and editorial verification checklist.",
                "known_conflicts": "Explicitly notes that new Sanskrit Udyam Sutras must be recognized as independent modern compositions, never claiming ancient Vedic origin. Narada 84 order is primary; Shandilya is 100 sutras."
            },
            {
                "document_id": "DOC-03",
                "filename": "DOC-03_UDYAM_SUTRE_MANUSCRIPT_V05.txt",
                "title": "उद्यमसूत्रे: भारतीय ज्ञानपरंपरेतून उद्योजकीय जीवनदर्शन (कार्यावृत्ती ०५)",
                "document_type": "Intermediate Milestone Manuscript",
                "date_received": "2026-11-07",
                "version": "कार्यावृत्ती ०५ (Revision 05)",
                "last_modified": "2026-11-07",
                "source_location": "data/knowledge_repository/sources/DOC-03_UDYAM_SUTRE_MANUSCRIPT_V05.txt",
                "status": "Superseded Milestone Draft (Baseline for Karma Yoga & Duty)",
                "is_authoritative": False,
                "scope": "Contains Chapters 1 to 5 concluding with Karma Yoga and Duty (कर्मयोग आणि कर्तव्य).",
                "known_conflicts": "Superseded by Karyavritti 17 which adds Chapter 6, the full 84 Narada sutra commentary, and all 7 Appendices (A-G)."
            }
        ]
    }

    reg_file = REGISTRY_DIR / "source_register.json"
    with open(reg_file, "w", encoding="utf-8") as f:
        json.dump(register_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Successfully wrote Source Document Register: {reg_file}")


def init_consultation_ledger():
    """Initializes the empty consultation ledger file."""
    ledger_file = CONSULT_DIR / "consultation_ledger.jsonl"
    if not ledger_file.exists():
        with open(ledger_file, "w", encoding="utf-8") as f:
            pass
    print(f"[+] Initialized Consultation Ledger: {ledger_file}")


if __name__ == "__main__":
    init_source_register()
    init_consultation_ledger()
