"""
================================================================================
Test Suite: tests/test_database_sync.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Unit tests for safe, idempotent database synchronization of
             canonical Udyog Sutras. Tested exclusively on temporary isolated
             databases to guarantee ZERO production mutation.
================================================================================
"""

import sqlite3
import uuid
from pathlib import Path

import pytest

from scripts.sync_database_canonical_canon import (
    get_db_connection,
    sync_canonical_sutras_to_db,
)
from scripts.ten_new_sutras_canonical_data import TEN_NEW_UDYOG_SUTRAS_CANON
from src.agents.validator_agent import check_duplicate_or_near_duplicate
from src.config import BASE_DIR


@pytest.fixture
def isolated_mock_db(tmp_path: Path) -> Path:
    """
    ============================================================================
    Fixture: isolated_mock_db
    Purpose: Creates a temporary, completely isolated SQLite database with the
             full manuscript_units schema and seeded with the historical
             duplicate fallback records for Sutras 3, 4, and 7.
    ============================================================================
    """
    db_file = tmp_path / "mock_manuscript.db"
    conn = sqlite3.connect(str(db_file))

    # Read schema
    schema_path = BASE_DIR / "src" / "database" / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)

    cur = conn.cursor()
    # Seed mock records for all 10 sutras (with duplicates at 3, 4, 7)
    for i in range(1, 11):
        if i in (3, 4, 7):
            verse = f"॥ उद्यमेन कार्यसिद्धिः ॥ {i} ॥"
            theme = "उद्यम आणि सातत्य"
        else:
            verse = f"॥ निष्ठावतः सर्वं सफलम् ॥ {i} ॥" if i == 1 else f"॥ सूत्र {i} ॥ {i} ॥"
            theme = f"थीम {i}"

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
                'Narada #1', 'अथातो भक्तिं व्याख्यास्यामः', 'Shandilya #1', 'अथातो भक्तिजिज्ञासा',
                'Thematic alignment', 'Justification',
                ?, 'Meaning',
                'Padaccheda', 'Anvaya', 'Word meanings', 'Grammar',
                'Anushtubh', '8 syllables per quarter',
                'English translation', 'Hindi translation', 'Marathi translation',
                'Nirukta', 'Dharma', 'Lokasangraha', 'Bhashya',
                '[]', 'APPROVED', 'APPROVED'
            )
            """,
            (
                str(uuid.uuid4()),
                f"unit_{i:02d}",
                str(i),
                theme,
                theme,
                verse,
            ),
        )

    conn.commit()
    conn.close()
    return db_file


def test_dry_run_leaves_database_completely_unmutated(isolated_mock_db: Path) -> None:
    """
    ============================================================================
    Test: test_dry_run_leaves_database_completely_unmutated
    Purpose: Verifies that sync in dry_run=True mode detects discrepancies but
             does NOT write or alter any rows in the database.
    ============================================================================
    """
    conn = get_db_connection(isolated_mock_db)
    before_sutras = {
        row["sutra_number"]: row["original_sanskrit_verse"]
        for row in conn.execute(
            "SELECT sutra_number, original_sanskrit_verse FROM manuscript_units WHERE is_current=1"
        ).fetchall()
    }
    conn.close()

    # Run dry run
    report = sync_canonical_sutras_to_db(isolated_mock_db, dry_run=True)

    assert report["dry_run"] is True
    assert len(report["updated"]) == 10
    assert len(report["diffs"]) > 0

    # Verify database contents are strictly identical before and after
    conn = get_db_connection(isolated_mock_db)
    after_sutras = {
        row["sutra_number"]: row["original_sanskrit_verse"]
        for row in conn.execute(
            "SELECT sutra_number, original_sanskrit_verse FROM manuscript_units WHERE is_current=1"
        ).fetchall()
    }
    conn.close()

    assert before_sutras == after_sutras


def test_live_sync_resolves_all_duplicates_and_updates_canon(isolated_mock_db: Path) -> None:
    """
    ============================================================================
    Test: test_live_sync_resolves_all_duplicates_and_updates_canon
    Purpose: Verifies that applying the synchronization updates the database
             so that all 10 sutras match the verified canonical verses and
             contain zero duplicates.
    ============================================================================
    """
    report = sync_canonical_sutras_to_db(isolated_mock_db, dry_run=False)

    assert report["dry_run"] is False
    assert len(report["updated"]) == 10

    conn = get_db_connection(isolated_mock_db)
    rows = conn.execute(
        """
        SELECT sutra_number, original_sanskrit_verse, theme, padaccheda, anvaya, translation_mr
        FROM manuscript_units
        WHERE is_current=1
        ORDER BY CAST(sutra_number AS INTEGER) ASC
        """
    ).fetchall()
    conn.close()

    assert len(rows) == 10
    verses = [r["original_sanskrit_verse"] for r in rows]

    # Verify Sutras 3, 4, 7 specific resolutions
    sutra3 = rows[2]
    sutra4 = rows[3]
    sutra7 = rows[6]

    assert sutra3["sutra_number"] == "3"
    assert sutra3["original_sanskrit_verse"] == TEN_NEW_UDYOG_SUTRAS_CANON[2]["new_udyog_sutra"]["sanskrit_verse"]

    assert sutra4["sutra_number"] == "4"
    assert sutra4["original_sanskrit_verse"] == TEN_NEW_UDYOG_SUTRAS_CANON[3]["new_udyog_sutra"]["sanskrit_verse"]

    assert sutra7["sutra_number"] == "7"
    assert sutra7["original_sanskrit_verse"] == TEN_NEW_UDYOG_SUTRAS_CANON[6]["new_udyog_sutra"]["sanskrit_verse"]

    # Verify zero occurrences of the fallback formula
    for v in verses:
        assert "उद्यमेन कार्यसिद्धिः" not in v

    # Verify 100% pairwise uniqueness across all 10 sutras
    for idx, v in enumerate(verses):
        other_verses = verses[:idx] + verses[idx + 1 :]
        is_dup, match, sim = check_duplicate_or_near_duplicate(v, other_verses)
        assert not is_dup, f"Sutra '{v}' near-duplicate with '{match}' (sim={sim:.2f})"


def test_sync_idempotency_second_run_produces_zero_diffs(isolated_mock_db: Path) -> None:
    """
    ============================================================================
    Test: test_sync_idempotency_second_run_produces_zero_diffs
    Purpose: Verifies that running sync twice in apply mode is completely
             idempotent: the second run reports 10 unchanged rows and 0 diffs.
    ============================================================================
    """
    # First apply
    sync_canonical_sutras_to_db(isolated_mock_db, dry_run=False)

    # Second apply
    report2 = sync_canonical_sutras_to_db(isolated_mock_db, dry_run=False)

    assert len(report2["diffs"]) == 0
    assert len(report2["unchanged"]) == 10
    assert len(report2["updated"]) == 0
