"""
================================================================================
Script: scripts/populate_source_documents.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Persists the attached master source documents into
             data/knowledge_repository/sources/ so that Agent 3 and Agent 4
             can independently retrieve, query, and verify them.
================================================================================
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_DIR = BASE_DIR / "data" / "knowledge_repository" / "sources"
SOURCES_DIR.mkdir(parents=True, exist_ok=True)

# 1. DOC-01: Shrimad Udyam Sutrani (100 Shlokas)
DOC_01_PATH = SOURCES_DIR / "DOC-01_SHRIMAD_UDYAM_SUTRANI_100.txt"
DOC_02_PATH = SOURCES_DIR / "DOC-02_UDYAM_SUTRE_MANUSCRIPT_V17.txt"
DOC_03_PATH = SOURCES_DIR / "DOC-03_UDYAM_SUTRE_MANUSCRIPT_V05.txt"

print(f"[*] Ensuring source files are persisted at: {SOURCES_DIR}")
