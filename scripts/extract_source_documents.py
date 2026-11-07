"""
================================================================================
Script: scripts/extract_source_documents.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Extracts DOC-01, DOC-02, and DOC-03 from transcript_full.jsonl
             and writes them cleanly to data/knowledge_repository/sources/.
================================================================================
"""

import sys
from pathlib import Path

# Configure Windows UTF-8 console output
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TRANSCRIPT_PATH = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc\.system_generated\logs\transcript_full.jsonl")
REPO_SOURCES = Path(r"C:\Users\deshp\.gemini\antigravity\scratch\sk-sutras-by-shri-shripad-kulkarni\data\knowledge_repository\sources")
REPO_SOURCES.mkdir(parents=True, exist_ok=True)


import json
import re
import sys
from pathlib import Path

# Configure Windows UTF-8 console output
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TRANSCRIPT_PATH = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc\.system_generated\logs\transcript_full.jsonl")
REPO_SOURCES = Path(r"C:\Users\deshp\.gemini\antigravity\scratch\sk-sutras-by-shri-shripad-kulkarni\data\knowledge_repository\sources")
REPO_SOURCES.mkdir(parents=True, exist_ok=True)


def clean_json_str(s: str) -> str:
    return s.replace("\\r\\n", "\n").replace("\\n", "\n").replace('\\"', '"').replace("\\t", "\t")


def run_extraction():
    print(f"[*] Reading transcript from: {TRANSCRIPT_PATH}")
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8", errors="ignore") as f:
        full_text = f.read()

    # Find matches for 100 sutras doc
    matches_start = [m.start() for m in re.finditer(r"श्रीमद् उद्यम सूत्राणि", full_text)]
    matches_end = [m.start() for m in re.finditer(r"संपूर्ण १०० सूत्रांचा महाग्रंथ अंतिम निष्कर्ष", full_text)]
    
    print(f"Found {len(matches_start)} start matches and {len(matches_end)} end matches for DOC-01.")
    
    if matches_start and matches_end:
        # Take the match where distance to end is reasonable (around 40,000 - 80,000 chars)
        best_s = None
        best_e = None
        for s in matches_start:
            for e in matches_end:
                if 20000 < (e - s) < 100000:
                    best_s = s
                    best_e = e + 2000  # include conclusion
                    break
            if best_s:
                break
        
        if not best_s:
            best_s = matches_start[-2] if len(matches_start) >= 2 else matches_start[0]
            best_e = matches_end[-1] + 2000

        doc01_raw = full_text[best_s:best_e]
        doc01_clean = doc01_raw.replace("\\r\\n", "\n").replace("\\n", "\n").replace('\\"', '"').replace("\\t", "\t")
        
        doc01_path = REPO_SOURCES / "DOC-01_SHRIMAD_UDYAM_SUTRANI_100.txt"
        with open(doc01_path, "w", encoding="utf-8") as f:
            f.write(doc01_clean)
        print(f"[+] Successfully wrote DOC-01: {doc01_path} ({len(doc01_clean)} chars)")

    # Use exact coordinates found for DOC-02
    s_ms = 6292302
    e_ms = 6344840 + 500
    doc02_raw = full_text[s_ms:e_ms]
    doc02_clean = clean_json_str(doc02_raw)

    doc02_path = REPO_SOURCES / "DOC-02_UDYAM_SUTRE_MANUSCRIPT_V17.txt"
    with open(doc02_path, "w", encoding="utf-8") as f:
        f.write(doc02_clean)
    print(f"[+] Successfully wrote DOC-02: {doc02_path} ({len(doc02_clean)} chars)")

    # DOC-03 (Karyavritti 05)
    kv05_marker = "कार्यावृत्ती ०५ | प्रकरण ५ समाविष्ट"
    pos_kv05 = doc02_clean.find(kv05_marker)
    if pos_kv05 != -1:
        doc03_clean = doc02_clean[:pos_kv05 + len(kv05_marker)].strip()
    else:
        pos_ch6 = doc02_clean.find("६. भक्तिसूत्रांपासून उद्यमसूत्रांपर्यंत")
        doc03_clean = doc02_clean[:pos_ch6].strip() if pos_ch6 != -1 else doc02_clean[:25000]

    doc03_path = REPO_SOURCES / "DOC-03_UDYAM_SUTRE_MANUSCRIPT_V05.txt"
    with open(doc03_path, "w", encoding="utf-8") as f:
        f.write(doc03_clean)
    print(f"[+] Successfully wrote DOC-03: {doc03_path} ({len(doc03_clean)} chars)")


if __name__ == "__main__":
    run_extraction()
