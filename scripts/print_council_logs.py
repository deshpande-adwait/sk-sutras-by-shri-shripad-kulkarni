"""
================================================================================
Script: scripts/print_council_logs.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Interactive diagnostic script that prints the complete history of
             inter-agent discussions, or executes a live multi-agent dialogue
             cycle with full verbose streaming of Agent 1, Agent 2, Agent 3,
             and Agent 4 logs.
================================================================================
"""

import argparse
import json
import sys
from pathlib import Path

# Configure UTF-8 encoding on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.orchestration.council_logger import default_council_logger
from src.orchestration.graph import build_four_agent_scholarly_graph


def show_historical_logs(limit: int = 10) -> None:
    """
    ----------------------------------------------------------------------------
    Function: show_historical_logs
    ----------------------------------------------------------------------------
    Purpose:
        Reads and displays existing logs from logs/council_transcripts.jsonl
        and the latest text session log file.

    Parameters:
        limit (int): Number of most recent event entries to show.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    log_dir = BASE_DIR / "logs"
    jsonl_file = log_dir / "council_transcripts.jsonl"

    print("=" * 80)
    print(" VIDVAT PARISHAD: HISTORICAL INTER-AGENT LOG AUDIT")
    print(f" Log Directory: {log_dir}")
    print("=" * 80)

    if not jsonl_file.exists():
        print(f"[!] No existing council transcript log found at {jsonl_file}.")
        print("[*] Run a live orchestration cycle using --live to generate new logs.")
        return

    with open(jsonl_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"[*] Total recorded events in audit trail: {len(lines)}")
    print(f"[*] Displaying last {min(limit, len(lines))} events:\n")

    for line in lines[-limit:]:
        try:
            entry = json.loads(line)
            ts = entry.get("timestamp", "")[:19]
            stage = entry.get("stage", "")
            agent = entry.get("agent", "")
            msg = entry.get("message", "")
            print(f"[{ts}] [{stage:<22}] [{agent:<18}] {msg}")
        except Exception:
            print(line.strip())
    print("\n" + "=" * 80)


def run_live_council_cycle(narada_sutra_no: str = "1", candidate_shandilya_no: str = None) -> None:
    """
    ----------------------------------------------------------------------------
    Function: run_live_council_cycle
    ----------------------------------------------------------------------------
    Purpose:
        Executes an end-to-end live 4-agent orchestration cycle and streams all
        logs of Agent 1, Agent 2, Agent 3, and Agent 4 in real time.

    Parameters:
        narada_sutra_no (str): The Narada aphorism number to analyze.
        candidate_shandilya_no (str): Optional explicit Shandilya sutra number.

    Returns:
        None
    ----------------------------------------------------------------------------
    """
    print("=" * 80)
    print(f" STARTING LIVE 4-AGENT VIDVAT PARISHAD DIALOGUE FOR SUTRA #{narada_sutra_no}")
    print(" Powered by Hiranyam AI Labs (https://hiranyamai.com/)")
    print("=" * 80 + "\n")

    graph = build_four_agent_scholarly_graph()

    candidate_info = {"sutra_no": str(narada_sutra_no)}
    if candidate_shandilya_no:
        candidate_info["shandilya_sutra_no"] = str(candidate_shandilya_no)

    initial_state = {
        "batch_queue": [candidate_info],
        "current_index": 0,
        "current_pair": {
            "candidate_info": candidate_info,
            "pair_id": f"UDYOGA-{str(narada_sutra_no).zfill(3)}",
            "sutra_no": str(narada_sutra_no),
        },
    }

    config = {"configurable": {"thread_id": f"council_live_sutra_{narada_sutra_no}"}}

    try:
        # Run graph up to the review interruption
        res = graph.invoke(initial_state, config=config)
        print("\n" + "=" * 80)
        print(" [ORCHESTRATION CYCLE COMPLETE]")
        print(f" Verdict: {res.get('arbitration_verdict')}")
        print(f" Notes: {res.get('arbitration_notes')}")
        if "agent4_validation_report" in res:
            v_rep = res["agent4_validation_report"]
            print(f" Agent 4 Validation: {v_rep.get('overall_status')}")
        print(f" Full persistent log saved to: {default_council_logger.log_file}")
        print("=" * 80)
    except Exception as e:
        print(f"[!] Error executing multi-agent graph: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print and inspect 4-Agent Vidvat Parishad dialogue logs.")
    parser.add_argument("--history", action="store_true", help="Display historical audit logs from disk.")
    parser.add_argument("--live", action="store_true", help="Run a live 4-agent cycle with full streaming dialogue.")
    parser.add_argument("--sutra", type=str, default="1", help="Narada Sutra number for live cycle.")
    parser.add_argument("--shandilya", type=str, default=None, help="Explicit Shandilya Sutra number (optional).")
    args = parser.parse_args()

    if args.live:
        run_live_council_cycle(narada_sutra_no=args.sutra, candidate_shandilya_no=args.shandilya)
    else:
        show_historical_logs(limit=20)
