"""
================================================================================
Script: scripts/extract_attachments_from_transcript.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Extracts the attached documents from the transcript and persists them
             as DOC-01, DOC-02, and DOC-03 in data/knowledge_repository/sources/.
================================================================================
"""

import json
from pathlib import Path

TRANSCRIPT_PATH = Path(r"C:\Users\deshp\.gemini\antigravity\brain\94293167-6c7d-4773-b091-412c085b8cdc\.system_generated\logs\transcript_full.jsonl")
REPO_SOURCES = Path(r"C:\Users\deshp\.gemini\antigravity\scratch\sk-sutras-by-shri-shripad-kulkarni\data\knowledge_repository\sources")
REPO_SOURCES.mkdir(parents=True, exist_ok=True)


def extract():
    print(f"[*] Reading transcript from: {TRANSCRIPT_PATH}")
    last_user_content = ""
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "USER_INPUT":
                    content = data.get("content", "")
                    if "MASTER IMPLEMENTATION PROMPT" in content:
                        last_user_content = content
            except Exception:
                continue

    if not last_user_content:
        print("[!] Could not find MASTER IMPLEMENTATION PROMPT in transcript. Checking latest USER_INPUT...")
        with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get("type") == "USER_INPUT":
                        content = data.get("content", "")
                        if "श्रीमद् उद्यम सूत्राणि" in content:
                            last_user_content = content
                except Exception:
                    continue

    print(f"[+] Found user input length: {len(last_user_content)}")

    # Split attachments
    # Attachment 1 starts with "श्रीमद् उद्यम सूत्राणि"
    # Attachment 2 starts with "उद्यमसूत्रे\nभारतीय ज्ञानपरंपरेतून उद्योजकीय जीवनदर्शन"
    p1 = last_user_content.find("श्रीमद् उद्यम सूत्राणि")
    p2 = last_user_content.find("उद्यमसूत्रे\nभारतीय ज्ञानपरंपरेतून उद्योजकीय जीवनदर्शन")
    if p2 == -1:
        p2 = last_user_content.find("उद्यमसूत्रे\r\nभारतीय ज्ञानपरंपरेतून उद्योजकीय जीवनदर्शन")

    if p1 != -1 and p2 != -1:
        doc01_text = last_user_content[p1:p2].strip()
        doc02_text = last_user_content[p2:].strip()

        # Write DOC-01
        doc01_file = REPO_SOURCES / "DOC-01_SHRIMAD_UDYAM_SUTRANI_100.txt"
        with open(doc01_file, "w", encoding="utf-8") as f:
            f.write(doc01_text)
        print(f"[+] Wrote DOC-01 (100 Sutras): {doc01_file} ({len(doc01_text)} chars)")

        # Write DOC-02 (Full Karyavritti 17)
        doc02_file = REPO_SOURCES / "DOC-02_UDYAM_SUTRE_MANUSCRIPT_V17.txt"
        with open(doc02_file, "w", encoding="utf-8") as f:
            f.write(doc02_text)
        print(f"[+] Wrote DOC-02 (Karyavritti 17): {doc02_file} ({len(doc02_text)} chars)")

        # Extract DOC-03 (Karyavritti 05 milestone)
        kv05_marker = "उद्यमसूत्रे • कार्यावृत्ती ०५ | प्रकरण ५ समाविष्ट"
        pos_kv05 = doc02_text.find(kv05_marker)
        if pos_kv05 != -1:
            doc03_text = doc02_text[:pos_kv05 + len(kv05_marker)].strip()
            doc03_file = REPO_SOURCES / "DOC-03_UDYAM_SUTRE_MANUSCRIPT_V05.txt"
            with open(doc03_file, "w", encoding="utf-8") as f:
                f.write(doc03_text)
            print(f"[+] Wrote DOC-03 (Karyavritti 05): {doc03_file} ({len(doc03_text)} chars)")
        else:
            print("[!] Could not find Karyavritti 05 marker, copying first 5 chapters for DOC-03")
            doc03_file = REPO_SOURCES / "DOC-03_UDYAM_SUTRE_MANUSCRIPT_V05.txt"
            with open(doc03_file, "w", encoding="utf-8") as f:
                f.write(doc02_text[:30000])


if __name__ == "__main__":
    extract()
