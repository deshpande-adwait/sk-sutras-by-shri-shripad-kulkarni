"""
================================================================================
Script: run_pipeline.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Interactive execution demonstration running the 3-agent orchestration
             pipeline live:
             1. NaradaAgent expounds Narada Sutra #1 and presents devotional thesis.
             2. ShandilyaAgent receives thesis, queries ChromaDB knowledge base,
                and selects matching Shandilya Sutra #1 with analytical reply.
             3. SutrakarAgent coordinates synthesis into Udyoga Bhashya, validates
                data schema, persists to SQLite, and compiles publication PDF.
================================================================================
"""

import sys
from pathlib import Path

# Configure UTF-8 encoding on Windows to support Devanagari Sanskrit printing
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.agents.narada_agent import NaradaAgent
from src.agents.shandilya_agent import ShandilyaAgent
from src.agents.sutrakar_agent import SutrakarAgent
from src.models.schema import SutraPairManuscript


def print_banner() -> None:
    print("=" * 80)
    print(" SK SUTRAS - BY SHRI SHRIPAD KULKARNI")
    print(" Multi-Agent LangGraph Comparative Synthesis: Udyoga Sutra")
    print(" Powered by Hiranyam AI Labs (https://hiranyamai.com/) ")
    print("=" * 80)
    print()


def run_multi_agent_cycle(sutra_number: str = "1") -> None:
    print_banner()

    print(f"[*] Initializing Multi-Agent System for Sutra #{sutra_number}...\n")

    # Step 1: Narada Agent
    print("-" * 80)
    print(" >>> STEP 1: NARADA BHAKTI SUTRA SPECIALIST AGENT")
    print("-" * 80)
    narada_agent = NaradaAgent()
    narada_raw = narada_agent.get_sutra_by_number(sutra_number)
    if not narada_raw:
        print(f"[!] Sutra #{sutra_number} not found. Using default inaugural sutra.")
        narada_raw = {
            "sutra_no": "1",
            "sanskrit": "अथातो भक्तिं व्याख्यास्यामः॥",
            "theme": "Inaugural Definition of Bhakti",
            "initial_meaning": {"en": "Now, therefore, we shall expound Devotion (Bhakti)."},
        }

    print(f"[Narada Agent] Reading Verse: {narada_raw['sanskrit']} (Sutra #{narada_raw['sutra_no']})")
    print(f"[Narada Agent] Theme: {narada_raw.get('theme', 'Bhakti')}")
    print("[Narada Agent] Generating devotional vishleshan across English, Hindi, and Marathi...")

    narada_output = narada_agent.expound_sutra(narada_raw)
    narada_item = narada_output["sutra_item"]

    print("\n[Narada Agent Exposition (English)]:")
    print(f"  {narada_item.vishleshan.en}")
    if narada_item.vishleshan.hi:
        print(f"\n[Narada Agent Exposition (Hindi)]:\n  {narada_item.vishleshan.hi}")
    if narada_item.vishleshan.mr:
        print(f"\n[Narada Agent Exposition (Marathi)]:\n  {narada_item.vishleshan.mr}")

    print("\n[Narada Agent Dispatch to Shandilya Agent]:")
    print(f"  \"{narada_output['agent_message_to_shandilya']}\"")
    print()

    # Step 2: Shandilya Agent
    print("-" * 80)
    print(" >>> STEP 2: SHANDILYA BHAKTI SUTRA SPECIALIST AGENT")
    print("-" * 80)
    print("[Shandilya Agent] Received devotional proposition from Narada Agent.")
    print("[Shandilya Agent] Querying local ChromaDB vector store for matching aphorisms...")

    shandilya_agent = ShandilyaAgent()
    shandilya_output = shandilya_agent.match_and_respond(
        narada_sutra=narada_item,
        theme=narada_output["theme"],
        narada_message=narada_output["agent_message_to_shandilya"],
    )
    shandilya_item = shandilya_output["shandilya_sutra"]

    print(f"[Shandilya Agent] Identified Best Match: Sutra #{shandilya_item.sutra_no}")
    print(f"[Shandilya Agent] Sanskrit Verse: {shandilya_item.sanskrit}")
    print("\n[Shandilya Agent Analysis (English)]:")
    print(f"  {shandilya_item.vishleshan.en}")
    if shandilya_item.vishleshan.hi:
        print(f"\n[Shandilya Agent Analysis (Hindi)]:\n  {shandilya_item.vishleshan.hi}")
    if shandilya_item.vishleshan.mr:
        print(f"\n[Shandilya Agent Analysis (Marathi)]:\n  {shandilya_item.vishleshan.mr}")

    print("\n[Shandilya Agent Reply to Narada & Sutrakar]:")
    print(f"  \"{shandilya_output['agent_message_to_sutrakar']}\"")
    print()

    # Step 3: Sutrakar Agent (Coordinator & Synthesizer)
    print("-" * 80)
    print(" >>> STEP 3: SUTRAKAR AGENT (MASTER COMPILER & SYNTHESIZER)")
    print("-" * 80)
    print("[Sutrakar Agent] Harmonizing devotional love with epistemological inquiry...")

    sutrakar_agent = SutrakarAgent()
    manuscript_pair: SutraPairManuscript = sutrakar_agent.synthesize_and_compile(
        pair_id=f"PAIR-{str(sutra_number).zfill(3)}",
        theme=narada_output["theme"],
        narada_sutra=narada_item,
        shandilya_sutra=shandilya_item,
        narada_statement=narada_output["agent_message_to_shandilya"],
        shandilya_statement=shandilya_output["agent_message_to_sutrakar"],
    )

    print("\n[Synthesized Udyoga Bhashya (English)]:")
    print(f"  {manuscript_pair.udyoga_bhashya_synthesis.en}")
    if manuscript_pair.udyoga_bhashya_synthesis.hi:
        print(f"\n[Synthesized Udyoga Bhashya (Hindi)]:\n  {manuscript_pair.udyoga_bhashya_synthesis.hi}")
    if manuscript_pair.udyoga_bhashya_synthesis.mr:
        print(f"\n[Synthesized Udyoga Bhashya (Marathi)]:\n  {manuscript_pair.udyoga_bhashya_synthesis.mr}")

    print("\n[Sutrakar Agent] Validated strict JSON data schema: PASSED [OK]")
    print("[Sutrakar Agent] Persisted record to SQLite database: PASSED [OK]")

    # Step 4: Typeset PDF Compilation
    print("\n[*] Compiling Print-Ready PDF with Noto Serif Devanagari...")
    pdf_path = sutrakar_agent.compile_treatise_pdf()
    print(f"[+] Publication document compiled at:\n    {pdf_path.resolve()}\n")

    print("=" * 80)
    print(" MULTI-AGENT SYNTHESIS CYCLE COMPLETE!")
    print(" To view the Human-in-the-Loop review portal with Senior Citizen (65+ Mode):")
    print("   Run:  run_portal.bat   (or: streamlit run src/ui/app.py)")
    print("=" * 80)


if __name__ == "__main__":
    sutra_arg = sys.argv[1] if len(sys.argv) > 1 else "1"
    run_multi_agent_cycle(sutra_arg)
