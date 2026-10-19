"""
================================================================================
Script: scripts/run_batch_synthesis.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Executes the non-compulsory, logic-based multi-agent orchestration
             across all 84 Narada Bhakti Sutras evaluated against the complete
             100 Shandilya Bhakti Sutras:
             1. NaradaAgent presents devotional proposition.
             2. ShandilyaAgent searches all 100 Shandilya Sutras in ChromaDB & shortlists top 3.
             3. SutrakarAgent arbitrates, rejects forced matches, and synthesizes Udyoga Bhashya
                only for authentic, logically corresponding pairs.
             4. Compiles the publication-ready Udyoga Sutra curated treatise.
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
from src.models.schema import SutraPairManuscript


def run_curated_batch_synthesis():
    print("=" * 80)
    print(" HIRANYAM AI LABS: SK SUTRAS LOGIC-BASED MULTI-AGENT ARBITRATION")
    print(" Comparing Narada Sutras against all 100 Shandilya Sutras")
    print(" Non-Compulsory Semantic Mapping & Curated Udyoga Sutra Compilation")
    print("=" * 80)
    print()

    # Clear previous database table to ensure clean curated persistence
    repo = ManuscriptRepository()
    with repo._get_connection() as conn:
        conn.execute("DELETE FROM sutra_pairs;")
        conn.execute("DELETE FROM review_history;")
        conn.commit()

    narada_agent = NaradaAgent()
    # Force reindex all 100 Shandilya sutras into ChromaDB
    shandilya_agent = ShandilyaAgent(force_reindex=True)
    sutrakar_agent = SutrakarAgent(repository=repo)

    print(sutrakar_agent.issue_arbitration_guidelines())
    print()
    print(f"[*] Narada Canon: {len(narada_agent.knowledge_base)} Sutras")
    print(f"[*] Shandilya Canon in ChromaDB: {len(shandilya_agent.knowledge_base)} Sutras")
    print("-" * 80)

    accepted_pairs = []
    rejected_count = 0
    start_time = time.time()

    for idx, sutra_raw in enumerate(narada_agent.knowledge_base, start=1):
        s_no = str(sutra_raw.get("sutra_no", idx))
        theme = sutra_raw.get("theme", "Devotion")

        # 1. Narada Agent Proposition
        narada_out = narada_agent.expound_sutra(sutra_raw)
        narada_item = narada_out["sutra_item"]

        # 2. Shandilya Agent: Search all 100 Shandilya Sutras for top 3 candidates
        candidates = shandilya_agent.search_candidates(
            narada_sutra=narada_item,
            theme=theme,
            top_k=3,
        )
        shandilya_out = shandilya_agent.formulate_candidate_response(
            narada_sutra=narada_item,
            theme=theme,
            narada_message=narada_out["agent_message_to_shandilya"],
            candidates=candidates,
        )

        # 3. Sutrakar Agent: Logic-Based Arbitration & Non-Compulsory Synthesis
        pair_id = f"PAIR-{str(len(accepted_pairs) + 1).zfill(3)}"
        is_accepted, pair_model, rationale = sutrakar_agent.evaluate_and_synthesize(
            pair_id=pair_id,
            theme=theme,
            narada_sutra=narada_item,
            shandilya_candidates=candidates,
            narada_statement=narada_out["agent_message_to_shandilya"],
            shandilya_statement=shandilya_out["agent_message_to_sutrakar"],
        )

        if is_accepted and pair_model:
            accepted_pairs.append(pair_model)
            print(
                f"[ACCEPTED {len(accepted_pairs):02d}] Narada #{narada_item.sutra_no} <==> "
                f"Shandilya #{pair_model.shandilya_sutra.sutra_no} | Theme: {theme[:30]}"
            )
            print(f"   Nexus: {rationale[:100]}...")
        else:
            rejected_count += 1
            print(
                f"[SKIPPED   ] Narada #{narada_item.sutra_no} (No authentic conceptual counterpart in 100 Shandilya sutras)"
            )

    elapsed = time.time() - start_time
    print("-" * 80)
    print(f"[+] Total Narada Sutras Analyzed: {len(narada_agent.knowledge_base)}")
    print(f"[+] Curated Authentic Pairs Accepted: {len(accepted_pairs)}")
    print(f"[+] Forced Mappings Rejected / Skipped: {rejected_count}")
    print(f"[+] Total Evaluation Time: {elapsed:.1f}s")
    print()

    # 4. Compile the Final Curated Publication Treatise (HTML / PDF)
    print("[*] Compiling Curated Udyoga Sutra Publication Treatise with Devanagari Typography...")
    treatise_path = sutrakar_agent.compile_curated_treatise(
        approved_pairs=accepted_pairs,
        output_filename="udyoga_sutra_final_treatise.html",
    )
    print(f"[+] Curated Treatise ready for Human Review at:\n    {treatise_path.resolve()}\n")

    print("=" * 80)
    print(" CURATED UDYOGA SUTRA COMPILATION COMPLETE!")
    print(f" {len(accepted_pairs)} verified comparative pairs loaded into SQLite (data/manuscript.db)")
    print(" Launch Review Portal for Shri Shripad Kulkarni:")
    print("   Run:  run_portal.bat   (or: streamlit run src/ui/app.py)")
    print("=" * 80)


if __name__ == "__main__":
    run_curated_batch_synthesis()
