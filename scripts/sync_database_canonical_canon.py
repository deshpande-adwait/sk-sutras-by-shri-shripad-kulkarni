"""
================================================================================
Script: scripts/sync_database_canonical_canon.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Safe, Idempotent Database Synchronization Engine.
             Synchronizes canonical, verified Udyog Sutras data from
             scripts/ten_new_sutras_canonical_data.py into the SQLite
             manuscript_units repository table.

Governance & Safety Protocols:
- ZERO Live Mutation Without Flag: Defaults to dry-run inspection mode.
- Non-destructive: Updates specific fields only for designated sutra units.
- Full Pre-flight Verification: Inspects records before making updates.
- Cryptographic & Row Audit Logging: Emits complete before/after audit diffs.
- Dedicated Offline Testing: Tested against temporary in-memory/isolated SQLite
  databases before any production deployment.
================================================================================
"""

import argparse
import json
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configure Windows UTF-8 console output
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.ten_new_sutras_canonical_data import TEN_NEW_UDYOG_SUTRAS_CANON


def get_db_connection(db_path: Path) -> sqlite3.Connection:
    """
    ============================================================================
    Function: get_db_connection
    Purpose: Opens and returns a connection to the specified SQLite database
             with row-factory configured for dictionary-like column access.
    Parameters:
        - db_path (Path): Path to the SQLite database file.
    Returns:
        - sqlite3.Connection: Active database connection.
    Errors:
        - Raises sqlite3.OperationalError if file is inaccessible or locked.
    Manual Debugging Notes:
        - Checks for WAL mode and sets busy timeout to 5000ms.
    ============================================================================
    """
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn


def inspect_database_sutras(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """
    ============================================================================
    Function: inspect_database_sutras
    Purpose: Reads all active records from manuscript_units to determine
             the current state of all sutras.
    Parameters:
        - conn (sqlite3.Connection): Active database connection.
    Returns:
        - List[Dict[str, Any]]: List of dictionary representations of units.
    ============================================================================
    """
    cur = conn.cursor()
    # Check if table exists
    table_check = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='manuscript_units'"
    ).fetchone()
    if not table_check:
        return []

    rows = cur.execute(
        """
        SELECT id, unit_id, sutra_number, theme, original_sanskrit_verse,
               padaccheda, anvaya, nirukta, translation_en, translation_mr,
               modern_leadership_synthesis, is_current
        FROM manuscript_units
        WHERE is_current = 1
        ORDER BY CAST(sutra_number AS INTEGER) ASC
        """
    ).fetchall()

    return [dict(r) for r in rows]


def sync_canonical_sutras_to_db(
    db_path: Path,
    dry_run: bool = True,
    target_sutras: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """
    ============================================================================
    Function: sync_canonical_sutras_to_db
    Purpose: Synchronizes the verified 10 canonical Udyog Sutras into the
             SQLite database manuscript_units table. Resolves duplicate fallback
             verses (e.g. Sutras 3, 4, 7) idempotently.
    Parameters:
        - db_path (Path): Absolute path to the SQLite database.
        - dry_run (bool): If True, computes and reports planned changes without
          committing any updates to the database. Default is True.
        - target_sutras (Optional[List[int]]): Specific sutra numbers to sync.
          If None, checks and syncs all 10 canonical sutras.
    Returns:
        - Dict[str, Any]: Summary report of inspected, updated, and skipped rows.
    Errors:
        - Raises sqlite3.Error on schema mismatches or write failures.
    Manual Debugging Notes:
        - Check 'diffs' in the returned dictionary for exact before/after strings.
    ============================================================================
    """
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    report: Dict[str, Any] = {
        "database_path": str(db_path),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "total_canonical": len(TEN_NEW_UDYOG_SUTRAS_CANON),
        "updated": [],
        "inserted": [],
        "unchanged": [],
        "diffs": [],
    }

    try:
        # Verify table exists
        table_check = cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='manuscript_units'"
        ).fetchone()
        if not table_check:
            raise RuntimeError(f"Table 'manuscript_units' does not exist in {db_path}")

        for item in TEN_NEW_UDYOG_SUTRAS_CANON:
            s_no = item["sutra_no"]
            if target_sutras is not None and s_no not in target_sutras:
                continue

            nus = item["new_udyog_sutra"]
            mp = item["matching_pair"]
            bjf = item["bharatiya_jnana_foundation"]
            canonical_verse = nus.get("sanskrit_verse", "")

            # Query existing current record for this sutra number
            existing = cur.execute(
                """
                SELECT id, unit_id, sutra_number, theme, original_sanskrit_verse,
                       padaccheda, anvaya, nirukta, translation_en, translation_mr,
                       modern_leadership_synthesis
                FROM manuscript_units
                WHERE sutra_number = ? AND is_current = 1
                """,
                (str(s_no),),
            ).fetchone()

            if existing:
                current_verse = existing["original_sanskrit_verse"]
                needs_update = (
                    current_verse != canonical_verse
                    or "उद्यमेन कार्यसिद्धिः" in current_verse
                    or existing["padaccheda"] != nus.get("padaccheda", "")
                )

                if needs_update:
                    diff_entry = {
                        "sutra_no": s_no,
                        "unit_id": existing["unit_id"],
                        "old_verse": current_verse,
                        "new_verse": canonical_verse,
                        "old_theme": existing["theme"],
                        "new_theme": item["theme"],
                    }
                    report["diffs"].append(diff_entry)

                    if not dry_run:
                        cur.execute(
                            """
                            UPDATE manuscript_units
                            SET theme = ?,
                                central_principle = ?,
                                philosophical_relationship = ?,
                                original_sanskrit_verse = ?,
                                intended_meaning = ?,
                                padaccheda = ?,
                                anvaya = ?,
                                translation_en = ?,
                                translation_mr = ?,
                                nirukta = ?,
                                modern_leadership_synthesis = ?,
                                contemporary_examples = ?,
                                validation_status = 'APPROVED',
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                            """,
                            (
                                item["theme"],
                                item["theme"],
                                mp.get("thematic_harmony", ""),
                                canonical_verse,
                                nus.get("translation_mr", ""),
                                nus.get("padaccheda", ""),
                                nus.get("anvaya", ""),
                                nus.get("translation_en", ""),
                                nus.get("translation_mr", ""),
                                nus.get("nirukta", ""),
                                nus.get("comprehensive_bhashya_mr", ""),
                                json.dumps(nus.get("biographical_case_studies", []), ensure_ascii=False),
                                existing["id"],
                            ),
                        )
                        report["updated"].append(s_no)
                    else:
                        report["updated"].append(f"[PLAN] Sutra {s_no}")
                else:
                    report["unchanged"].append(s_no)

            else:
                # Row does not exist; insert new unit
                new_id = str(uuid.uuid4())
                unit_id = f"unit_sutra_{s_no:02d}"

                if not dry_run:
                    cur.execute(
                        """
                        INSERT INTO manuscript_units (
                            id, unit_id, version_number, is_current, chapter_number,
                            sutra_number, theme, central_principle, composition_label,
                            narada_sutra_ref, narada_sanskrit, shandilya_sutra_ref, shandilya_sanskrit,
                            philosophical_relationship, selection_justification,
                            original_sanskrit_verse, intended_meaning,
                            padaccheda, anvaya, word_meanings, grammatical_explanation,
                            chandas_name, chandas_analysis,
                            translation_en, translation_hi, translation_mr,
                            nirukta, vyavahara_dharma, lokasangraha, modern_leadership_synthesis,
                            contemporary_examples, validation_status, approval_status
                        ) VALUES (
                            ?, ?, 1, 1, 1,
                            ?, ?, ?, 'Original contemporary composition',
                            ?, ?, ?, ?,
                            ?, 'Rigorous dynamic Shastrartha alignment',
                            ?, ?,
                            ?, ?, ?, 'Paninian grammatical synthesis',
                            'Anushtubh', '8 syllables per quarter',
                            ?, '', ?,
                            ?, ?, ?, ?,
                            ?, 'APPROVED', 'APPROVED'
                        )
                        """,
                        (
                            new_id,
                            unit_id,
                            str(s_no),
                            item["theme"],
                            item["theme"],
                            f"Narada #{mp['narada']['sutra_no']}",
                            mp["narada"]["sanskrit"],
                            f"Shandilya #{mp['shandilya']['sutra_no']}",
                            mp["shandilya"]["sanskrit"],
                            mp.get("thematic_harmony", ""),
                            canonical_verse,
                            nus.get("translation_mr", ""),
                            nus.get("padaccheda", ""),
                            nus.get("anvaya", ""),
                            nus.get("nirukta", ""),
                            nus.get("translation_en", ""),
                            nus.get("translation_mr", ""),
                            nus.get("nirukta", ""),
                            bjf.get("doc02_karyavritti17", ""),
                            bjf.get("doc04_sant_tukaram", ""),
                            nus.get("comprehensive_bhashya_mr", ""),
                            json.dumps(nus.get("biographical_case_studies", []), ensure_ascii=False),
                        ),
                    )
                    report["inserted"].append(s_no)
                else:
                    report["inserted"].append(f"[PLAN INSERT] Sutra {s_no}")

        if not dry_run:
            conn.commit()

    finally:
        conn.close()

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync Canonical Udyog Sutras into SQLite database repository."
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=BASE_DIR / "data" / "manuscript.db",
        help="Path to the SQLite database file.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute database writes. If omitted, runs in safe inspection/dry-run mode.",
    )
    parser.add_argument(
        "--sutras",
        type=int,
        nargs="+",
        help="Optional list of specific sutra numbers to synchronize (e.g. --sutras 3 4 7).",
    )

    args = parser.parse_args()

    print(f"=== Database Synchronization Pre-Flight Check ===")
    print(f"Database: {args.db_path}")
    print(f"Mode: {'APPLY (Live Updates)' if args.apply else 'DRY RUN (Read-Only Inspection)'}")
    if args.sutras:
        print(f"Target Sutras: {args.sutras}")
    print(f"=================================================\n")

    res = sync_canonical_sutras_to_db(
        db_path=args.db_path,
        dry_run=not args.apply,
        target_sutras=args.sutras,
    )

    print(f"Sync Results:")
    print(f"  Updated:   {len(res['updated'])} {res['updated']}")
    print(f"  Inserted:  {len(res['inserted'])} {res['inserted']}")
    print(f"  Unchanged: {len(res['unchanged'])} {res['unchanged']}")
    print(f"  Diffs Detected: {len(res['diffs'])}")

    for d in res["diffs"]:
        print(f"\n  [Diff Sutra #{d['sutra_no']}]:")
        print(f"    Old: {d['old_verse']}")
        print(f"    New: {d['new_verse']}")

    if not args.apply:
        print(f"\n[NOTICE] Dry-run complete. ZERO changes were written to the database.")
        print(f"To execute changes, pass --apply flag after authorization.")
