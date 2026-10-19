"""
================================================================================
Script: scripts/run_batch_synthesis.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Executes the full automated batch multi-agent orchestration across
             all 84 Narada Bhakti Sutras mapped against Shandilya Bhakti Sutras.
             1. NaradaAgent presents devotional exposition.
             2. ShandilyaAgent searches vector store & provides epistemological thesis.
             3. SutrakarAgent harmonizes both into Udyoga Bhashya across en, hi, mr.
             4. Commits all 84 records to SQLite relational repository.
             5. Compiles the publication-ready Devanagari treatise (PDF & HTML).
================================================================================
"""

import sys
import time
from pathlib import Path

# Configure Windows UTF-8 stdout
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.agents.narada_agent import NaradaAgent
from src.agents.shandilya_agent import ShandilyaAgent
from src.agents.sutrakar_agent import SutrakarAgent
from src.database.repository import ManuscriptRepository


def run_full_84_sutras_batch():
    print("=" * 80)
    print(" HIRANYAM AI LABS: SK SUTRAS ORCHESTRATION PIPELINE")
    print(" BATCH SYNTHESIS OF ALL 84 NARADA & SHANDILYA SUTRAS")
    print(" Compiling Treatise: 'Udyoga Sutra' - by Shri Shripad Kulkarni")
    print("=" * 80)
    print()

    narada_agent = NaradaAgent()
    shandilya_agent = ShandilyaAgent()
    repo = ManuscriptRepository()
    sutrakar_agent = SutrakarAgent(repository=repo)

    total_sutras = len(narada_agent.knowledge_base)
    print(f"[*] Total Narada Bhakti Sutras to process: {total_sutras}")
    print("[*] Storage Engine: SQLite (data/manuscript.db)")
    print("[*] Vector Engine: ChromaDB (data/chroma_db)")
    print("[*] Typography: Noto Serif Devanagari")
    print("-" * 80)

    start_time = time.time()

    for idx, sutra_raw in enumerate(narada_agent.knowledge_base, start=1):
        s_no = str(sutra_raw.get("sutra_no", idx))
        pair_id = f"PAIR-{s_no.zfill(3)}"
        theme = sutra_raw.get("theme", "Devotional Philosophy")

        # 1. Narada Agent
        narada_out = narada_agent.expound_sutra(sutra_raw)
        narada_item = narada_out["sutra_item"]

        # 2. Shandilya Agent
        shandilya_out = shandilya_agent.match_and_respond(
            narada_sutra=narada_item,
            theme=theme,
            narada_message=narada_out["agent_message_to_shandilya"],
        )
        shandilya_item = shandilya_out["shandilya_sutra"]

        # 3. Sutrakar Agent (Synthesis & DB Persistence)
        compiled_pair = sutrakar_agent.synthesize_and_compile(
            pair_id=pair_id,
            theme=theme,
            narada_sutra=narada_item,
            shandilya_sutra=shandilya_item,
            narada_statement=narada_out["agent_message_to_shandilya"],
            shandilya_statement=shandilya_out["agent_message_to_sutrakar"],
        )

        progress = (idx / total_sutras) * 100
        print(
            f"[{idx:02d}/{total_sutras}] {pair_id} | Theme: {theme[:30]:<30} | "
            f"Narada #{narada_item.sutra_no} <-> Shandilya #{shandilya_item.sutra_no} | "
            f"Progress: {progress:5.1f}% [SAVED]"
        )

    elapsed = time.time() - start_time
    print("-" * 80)
    print(f"[+] All {total_sutras} comparative sutra pairs successfully synthesized & stored in {elapsed:.1f}s.")
    print()

    # 4. Generate Final Publication Treatise (HTML / PDF)
    print("[*] Compiling Complete 84-Aphorism Publication Treatise with WeasyPrint...")
    pdf_path = sutrakar_agent.compile_treatise_pdf(
        output_filename="udyoga_sutra_final_treatise.pdf"
    )
    print(f"[+] Publication Deliverable ready at:\n    {pdf_path.resolve()}\n")

    print("=" * 80)
    print(" UDYOGA SUTRA FINAL TREATISE COMPILATION COMPLETE!")
    print(" All 84 pairs are available in the Review Portal for Shri Shripad Kulkarni:")
    print("   Run:  run_portal.bat   (or: streamlit run src/ui/app.py)")
    print("=" * 80)


if __name__ == "__main__":
    run_full_84_sutras_batch()
