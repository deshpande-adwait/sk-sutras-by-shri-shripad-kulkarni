"""
================================================================================
Module: src.database.repository
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Relational SQLite repository managing ACID-compliant persistence for
             comparative sutra pairs, human review audit trails, full manuscript
             units (Sections A-F), Agent 4 validation reports, token metering,
             budgets, and accessibility system settings.
================================================================================
"""

import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config import SQLITE_DB_PATH
from src.models.schema import MultilingualText, SutraItem, SutraPairManuscript


class ManuscriptRepository:
    """
    ----------------------------------------------------------------------------
    Class: ManuscriptRepository
    ----------------------------------------------------------------------------
    Purpose:
        Encapsulates all database interactions for persisting manuscript records,
        retrieving pending reviews for Human-in-the-Loop workflows, logging
        editorial decisions, storing validation reports, tracking token costs,
        and managing accessibility presets.

    Attributes:
        db_path (Path): Filesystem path to the SQLite database file.
    ----------------------------------------------------------------------------
    """

    def __init__(self, db_path: Optional[Path] = None) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the repository with the specified database path and
            triggers automated schema creation if the database is uninitialized.

        Parameters:
            db_path (Optional[Path]): Target SQLite database path. Defaults to
                                      SQLITE_DB_PATH configured in src.config.

        Returns:
            None

        Errors:
            sqlite3.Error: Raised if the database connection or schema initialization fails.

        Manual Debugging Notes:
            - When running unit tests, pass an in-memory database or temporary file:
              `repo = ManuscriptRepository(Path(":memory:"))` or temporary file.
        ------------------------------------------------------------------------
        """
        self.db_path: Path = db_path or SQLITE_DB_PATH
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """
        ------------------------------------------------------------------------
        Method: _get_connection
        ------------------------------------------------------------------------
        Purpose:
            Creates and returns an active SQLite database connection with row
            factory configured for dictionary-style attribute access.

        Parameters:
            None

        Returns:
            sqlite3.Connection: Active database connection.

        Errors:
            sqlite3.OperationalError: If directory cannot be written or file is locked.
        ------------------------------------------------------------------------
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        """
        ------------------------------------------------------------------------
        Method: _init_db
        ------------------------------------------------------------------------
        Purpose:
            Applies schema.sql to the database to ensure all tables, indexes, and
            default settings are present.

        Parameters:
            None

        Returns:
            None

        Errors:
            FileNotFoundError: If schema.sql is missing.
            sqlite3.Error: If SQL execution encounters syntax or integrity issues.
        ------------------------------------------------------------------------
        """
        schema_file = Path(__file__).parent / "schema.sql"
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found at {schema_file}")

        with open(schema_file, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        with self._get_connection() as conn:
            conn.executescript(schema_sql)
            conn.commit()

    # ==========================================================================
    # Legacy / Simple Sutra Pairs Methods (Maintained for Backward Compatibility)
    # ==========================================================================

    def save_pair(
        self,
        pair: SutraPairManuscript,
        status: str = "pending_review",
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: save_pair
        ------------------------------------------------------------------------
        Purpose:
            Persists or updates a SutraPairManuscript record in the relational store.

        Parameters:
            pair (SutraPairManuscript): The validated manuscript record to store.
            status (str): Workflow review status (default: 'pending_review').

        Returns:
            None

        Errors:
            sqlite3.IntegrityError: If foreign keys or constraint violations occur.

        Manual Debugging Notes:
            - Performs an UPSERT on conflict with `pair_id`.
        ------------------------------------------------------------------------
        """
        sql = """
        INSERT INTO sutra_pairs (
            pair_id, theme,
            narada_sutra_no, narada_sanskrit, narada_vishleshan_en,
            narada_vishleshan_hi, narada_vishleshan_mr,
            shandilya_sutra_no, shandilya_sanskrit, shandilya_vishleshan_en,
            shandilya_vishleshan_hi, shandilya_vishleshan_mr,
            udyoga_bhashya_en, udyoga_bhashya_hi, udyoga_bhashya_mr,
            review_status, updated_at
        ) VALUES (
            ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?,
            ?, CURRENT_TIMESTAMP
        )
        ON CONFLICT(pair_id) DO UPDATE SET
            theme = excluded.theme,
            narada_sutra_no = excluded.narada_sutra_no,
            narada_sanskrit = excluded.narada_sanskrit,
            narada_vishleshan_en = excluded.narada_vishleshan_en,
            narada_vishleshan_hi = excluded.narada_vishleshan_hi,
            narada_vishleshan_mr = excluded.narada_vishleshan_mr,
            shandilya_sutra_no = excluded.shandilya_sutra_no,
            shandilya_sanskrit = excluded.shandilya_sanskrit,
            shandilya_vishleshan_en = excluded.shandilya_vishleshan_en,
            shandilya_vishleshan_hi = excluded.shandilya_vishleshan_hi,
            shandilya_vishleshan_mr = excluded.shandilya_vishleshan_mr,
            udyoga_bhashya_en = excluded.udyoga_bhashya_en,
            udyoga_bhashya_hi = excluded.udyoga_bhashya_hi,
            udyoga_bhashya_mr = excluded.udyoga_bhashya_mr,
            review_status = excluded.review_status,
            updated_at = CURRENT_TIMESTAMP;
        """
        params = (
            pair.pair_id,
            pair.theme,
            pair.narada_sutra.sutra_no,
            pair.narada_sutra.sanskrit,
            pair.narada_sutra.vishleshan.en,
            pair.narada_sutra.vishleshan.hi,
            pair.narada_sutra.vishleshan.mr,
            pair.shandilya_sutra.sutra_no,
            pair.shandilya_sutra.sanskrit,
            pair.shandilya_sutra.vishleshan.en,
            pair.shandilya_sutra.vishleshan.hi,
            pair.shandilya_sutra.vishleshan.mr,
            pair.udyoga_bhashya_synthesis.en,
            pair.udyoga_bhashya_synthesis.hi,
            pair.udyoga_bhashya_synthesis.mr,
            status,
        )

        with self._get_connection() as conn:
            conn.execute(sql, params)
            conn.commit()

    def get_pair(self, pair_id: str) -> Optional[SutraPairManuscript]:
        """
        ------------------------------------------------------------------------
        Method: get_pair
        ------------------------------------------------------------------------
        Purpose:
            Retrieves a single SutraPairManuscript record by its unique pair_id.

        Parameters:
            pair_id (str): The identifier of the sutra pair.

        Returns:
            Optional[SutraPairManuscript]: Hydrated Pydantic model if found, else None.

        Errors:
            sqlite3.Error: If query execution fails.
        ------------------------------------------------------------------------
        """
        sql = "SELECT * FROM sutra_pairs WHERE pair_id = ?;"
        with self._get_connection() as conn:
            row = conn.execute(sql, (pair_id,)).fetchone()
            if not row:
                return None
            return self._row_to_model(row)

    def get_all_pairs(
        self, status: Optional[str] = None
    ) -> List[SutraPairManuscript]:
        """
        ------------------------------------------------------------------------
        Method: get_all_pairs
        ------------------------------------------------------------------------
        Purpose:
            Retrieves all manuscript pairs, optionally filtered by review status.

        Parameters:
            status (Optional[str]): Workflow filter (e.g. 'approved', 'pending_review').

        Returns:
            List[SutraPairManuscript]: Collection of matching manuscript models.

        Errors:
            sqlite3.Error: If database read fails.
        ------------------------------------------------------------------------
        """
        if status:
            sql = "SELECT * FROM sutra_pairs WHERE review_status = ? ORDER BY pair_id ASC;"
            params = (status,)
        else:
            sql = "SELECT * FROM sutra_pairs ORDER BY pair_id ASC;"
            params = ()

        with self._get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_model(r) for r in rows]

    def record_review(
        self,
        pair_id: str,
        reviewer_name: str,
        action: str,
        notes: Optional[str] = None,
        updated_bhashya_en: Optional[str] = None,
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: record_review
        ------------------------------------------------------------------------
        Purpose:
            Records a human editorial review action, updates the pair status,
            and logs the decision into the audit trail table atomically.

        Parameters:
            pair_id (str): The target sutra pair ID.
            reviewer_name (str): Name of the human reviewer (e.g. 'Shri Shripad Kulkarni').
            action (str): Review decision ('approved', 'revised', 'rejected').
            notes (Optional[str]): Reviewer observations or corrections.
            updated_bhashya_en (Optional[str]): Optional modified synthesis text.

        Returns:
            None

        Errors:
            ValueError: If pair_id does not exist.
            sqlite3.Error: If transaction fails.
        ------------------------------------------------------------------------
        """
        with self._get_connection() as conn:
            cur = conn.cursor()
            # Fetch existing synthesis for audit trail
            row = cur.execute(
                "SELECT udyoga_bhashya_en FROM sutra_pairs WHERE pair_id = ?;",
                (pair_id,),
            ).fetchone()
            if not row:
                raise ValueError(f"Sutra pair with ID '{pair_id}' does not exist.")

            previous_bhashya = row["udyoga_bhashya_en"]

            # 1. Insert audit log
            cur.execute(
                """
                INSERT INTO review_history (pair_id, reviewer_name, action, notes, previous_bhashya_en)
                VALUES (?, ?, ?, ?, ?);
                """,
                (pair_id, reviewer_name, action, notes, previous_bhashya),
            )

            # 2. Update pair status and synthesis if modified
            if updated_bhashya_en:
                cur.execute(
                    """
                    UPDATE sutra_pairs
                    SET review_status = ?, udyoga_bhashya_en = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE pair_id = ?;
                    """,
                    (action, updated_bhashya_en, pair_id),
                )
            else:
                cur.execute(
                    """
                    UPDATE sutra_pairs
                    SET review_status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE pair_id = ?;
                    """,
                    (action, pair_id),
                )

            conn.commit()

    def get_setting(self, key: str, default: str = "") -> str:
        """
        ------------------------------------------------------------------------
        Method: get_setting
        ------------------------------------------------------------------------
        Purpose:
            Retrieves a persistent system/accessibility setting from system_settings.

        Parameters:
            key (str): Setting identifier.
            default (str): Fallback value if key is not found.

        Returns:
            str: Setting value.
        ------------------------------------------------------------------------
        """
        sql = "SELECT setting_value FROM system_settings WHERE setting_key = ?;"
        with self._get_connection() as conn:
            row = conn.execute(sql, (key,)).fetchone()
            return row["setting_value"] if row else default

    def set_setting(self, key: str, value: str, description: Optional[str] = None) -> None:
        """
        ------------------------------------------------------------------------
        Method: set_setting
        ------------------------------------------------------------------------
        Purpose:
            Persists or updates a system/accessibility setting in the database.

        Parameters:
            key (str): Setting identifier.
            value (str): Setting value to persist.
            description (Optional[str]): Explanatory context for the setting.

        Returns:
            None
        ------------------------------------------------------------------------
        """
        sql = """
        INSERT INTO system_settings (setting_key, setting_value, description, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(setting_key) DO UPDATE SET
            setting_value = excluded.setting_value,
            description = COALESCE(excluded.description, system_settings.description),
            updated_at = CURRENT_TIMESTAMP;
        """
        with self._get_connection() as conn:
            conn.execute(sql, (key, value, description))
            conn.commit()

    def _row_to_model(self, row: sqlite3.Row) -> SutraPairManuscript:
        """
        ------------------------------------------------------------------------
        Method: _row_to_model
        ------------------------------------------------------------------------
        Purpose:
            Converts an SQLite row object into a fully validated SutraPairManuscript
            Pydantic model.

        Parameters:
            row (sqlite3.Row): Database row containing sutra pair attributes.

        Returns:
            SutraPairManuscript: Hydrated model.
        ------------------------------------------------------------------------
        """
        return SutraPairManuscript(
            pair_id=row["pair_id"],
            theme=row["theme"],
            narada_sutra=SutraItem(
                sutra_no=row["narada_sutra_no"],
                sanskrit=row["narada_sanskrit"],
                vishleshan=MultilingualText(
                    en=row["narada_vishleshan_en"],
                    hi=row["narada_vishleshan_hi"],
                    mr=row["narada_vishleshan_mr"],
                ),
            ),
            shandilya_sutra=SutraItem(
                sutra_no=row["shandilya_sutra_no"],
                sanskrit=row["shandilya_sanskrit"],
                vishleshan=MultilingualText(
                    en=row["shandilya_vishleshan_en"],
                    hi=row["shandilya_vishleshan_hi"],
                    mr=row["shandilya_vishleshan_mr"],
                ),
            ),
            udyoga_bhashya_synthesis=MultilingualText(
                en=row["udyoga_bhashya_en"],
                hi=row["udyoga_bhashya_hi"],
                mr=row["udyoga_bhashya_mr"],
            ),
        )

    # ==========================================================================
    # Full Manuscript Units (Sections A through F) with Versioning
    # ==========================================================================

    def save_manuscript_unit(self, unit: Dict[str, Any]) -> str:
        """
        ------------------------------------------------------------------------
        Method: save_manuscript_unit
        ------------------------------------------------------------------------
        Purpose:
            Persists a complete manuscript unit (Sections A through F) adhering
            strictly to the versioning mandate: approved content is never overwritten,
            and revisions produce new version numbers.

        Parameters:
            unit (Dict[str, Any]): Dictionary containing full manuscript unit attributes.

        Returns:
            str: The primary key ID of the persisted record.
        ------------------------------------------------------------------------
        """
        record_id = unit.get("id") or str(uuid.uuid4())
        unit_id = unit.get("unit_id", "UDYOGA-SUTRA-001")
        version_number = int(unit.get("version_number", 1))

        # Check if this unit_id already exists and what the highest version is
        with self._get_connection() as conn:
            cursor = conn.cursor()
            existing = cursor.execute(
                "SELECT id, version_number, approval_status FROM manuscript_units WHERE unit_id = ? ORDER BY version_number DESC LIMIT 1;",
                (unit_id,),
            ).fetchone()

            if existing:
                if existing["approval_status"] == "APPROVED":
                    # Cannot overwrite approved content; increment version
                    version_number = existing["version_number"] + 1
                    unit["parent_version_id"] = existing["id"]
                    cursor.execute("UPDATE manuscript_units SET is_current = 0 WHERE unit_id = ?;", (unit_id,))
                else:
                    # Update existing unapproved draft or create next version
                    cursor.execute("UPDATE manuscript_units SET is_current = 0 WHERE unit_id = ?;", (unit_id,))

            # Check if this exact unit_id and version_number already exists
            exact_row = cursor.execute(
                "SELECT id FROM manuscript_units WHERE unit_id = ? AND version_number = ?;",
                (unit_id, version_number),
            ).fetchone()
            if exact_row:
                record_id = exact_row["id"]

            sql = """
            INSERT INTO manuscript_units (
                id, unit_id, version_number, is_current, parent_version_id,
                chapter_number, sutra_number, theme, central_principle, composition_label,
                narada_sutra_ref, narada_sanskrit, shandilya_sutra_ref, shandilya_sanskrit,
                philosophical_relationship, selection_justification,
                original_sanskrit_verse, intended_meaning,
                padaccheda, anvaya, word_meanings, grammatical_explanation,
                sandhi_analysis, dhatu_derivation, chandas_name, chandas_analysis,
                translation_en, translation_hi, translation_mr,
                nirukta, vyavahara_dharma, lokasangraha, modern_leadership_synthesis,
                philosophical_significance, contemporary_examples, limitations_notes, cross_references,
                validation_status, approval_status, approved_by, approved_at,
                created_at, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?,
                ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?,
                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
            )
            ON CONFLICT(unit_id, version_number) DO UPDATE SET
                theme = excluded.theme,
                central_principle = excluded.central_principle,
                original_sanskrit_verse = excluded.original_sanskrit_verse,
                intended_meaning = excluded.intended_meaning,
                padaccheda = excluded.padaccheda,
                anvaya = excluded.anvaya,
                word_meanings = excluded.word_meanings,
                grammatical_explanation = excluded.grammatical_explanation,
                sandhi_analysis = excluded.sandhi_analysis,
                dhatu_derivation = excluded.dhatu_derivation,
                chandas_analysis = excluded.chandas_analysis,
                translation_en = excluded.translation_en,
                translation_hi = excluded.translation_hi,
                translation_mr = excluded.translation_mr,
                nirukta = excluded.nirukta,
                vyavahara_dharma = excluded.vyavahara_dharma,
                lokasangraha = excluded.lokasangraha,
                modern_leadership_synthesis = excluded.modern_leadership_synthesis,
                validation_status = excluded.validation_status,
                approval_status = excluded.approval_status,
                updated_at = CURRENT_TIMESTAMP;
            """
            cursor.execute(
                sql,
                (
                    record_id,
                    unit_id,
                    version_number,
                    1,
                    unit.get("parent_version_id"),
                    unit.get("chapter_number", 1),
                    unit.get("sutra_number", "1"),
                    unit.get("theme", "Universal Conduct"),
                    unit.get("central_principle", ""),
                    unit.get("composition_label", "Original contemporary composition"),
                    unit.get("narada_sutra_ref", "NBS-1"),
                    unit.get("narada_sanskrit", ""),
                    unit.get("shandilya_sutra_ref", "SBS-1"),
                    unit.get("shandilya_sanskrit", ""),
                    unit.get("philosophical_relationship", ""),
                    unit.get("selection_justification", ""),
                    unit.get("original_sanskrit_verse", ""),
                    unit.get("intended_meaning", ""),
                    unit.get("padaccheda", ""),
                    unit.get("anvaya", ""),
                    unit.get("word_meanings", ""),
                    unit.get("grammatical_explanation", ""),
                    unit.get("sandhi_analysis", ""),
                    unit.get("dhatu_derivation", ""),
                    unit.get("chandas_name", "Anushtubh"),
                    unit.get("chandas_analysis", ""),
                    unit.get("translation_en", ""),
                    unit.get("translation_hi", ""),
                    unit.get("translation_mr", ""),
                    unit.get("nirukta", ""),
                    unit.get("vyavahara_dharma", ""),
                    unit.get("lokasangraha", ""),
                    unit.get("modern_leadership_synthesis", ""),
                    unit.get("philosophical_significance", ""),
                    unit.get("contemporary_examples", ""),
                    unit.get("limitations_notes", ""),
                    unit.get("cross_references", ""),
                    unit.get("validation_status", "PENDING_VALIDATION"),
                    unit.get("approval_status", "PENDING_REVIEW"),
                    unit.get("approved_by"),
                    unit.get("approved_at"),
                ),
            )
            conn.commit()
            return record_id

    def get_manuscript_unit(
        self, unit_id: str, version_number: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_manuscript_unit
        ------------------------------------------------------------------------
        Purpose:
            Retrieves a manuscript unit by unit_id and optional version number.
            Defaults to the current active version if version is omitted.
        ------------------------------------------------------------------------
        """
        with self._get_connection() as conn:
            if version_number is not None:
                sql = "SELECT * FROM manuscript_units WHERE unit_id = ? AND version_number = ?;"
                row = conn.execute(sql, (unit_id, version_number)).fetchone()
            else:
                sql = "SELECT * FROM manuscript_units WHERE unit_id = ? AND is_current = 1;"
                row = conn.execute(sql, (unit_id,)).fetchone()
            return dict(row) if row else None

    def get_all_manuscript_units(
        self, approval_status: Optional[str] = None, current_only: bool = True
    ) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_all_manuscript_units
        ------------------------------------------------------------------------
        Purpose:
            Retrieves all manuscript units, optionally filtered by approval status.
        ------------------------------------------------------------------------
        """
        conditions = []
        params = []
        if current_only:
            conditions.append("is_current = 1")
        if approval_status:
            conditions.append("approval_status = ?")
            params.append(approval_status)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT * FROM manuscript_units {where_clause} ORDER BY chapter_number ASC, CAST(sutra_number AS INTEGER) ASC;"

        with self._get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]

    def update_manuscript_approval(
        self,
        unit_id: str,
        status: str,
        approved_by: str = "Shri Shripad Kulkarni",
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: update_manuscript_approval
        ------------------------------------------------------------------------
        Purpose:
            Updates the author approval status of a manuscript unit.
        ------------------------------------------------------------------------
        """
        sql = """
        UPDATE manuscript_units
        SET approval_status = ?, approved_by = ?, approved_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
        WHERE unit_id = ? AND is_current = 1;
        """
        with self._get_connection() as conn:
            conn.execute(sql, (status, approved_by, unit_id))
            conn.commit()

    # ==========================================================================
    # Agent 4 Validation Reports Persistence
    # ==========================================================================

    def save_validation_report(self, report: Dict[str, Any]) -> str:
        """
        ------------------------------------------------------------------------
        Method: save_validation_report
        ------------------------------------------------------------------------
        Purpose:
            Persists an Agent 4 Validation Report with all sub-check results,
            severity counts, and required corrections.
        ------------------------------------------------------------------------
        """
        report_id = report.get("id") or str(uuid.uuid4())
        findings_json = json.dumps(report.get("findings", []))

        sql = """
        INSERT OR REPLACE INTO validation_reports (
            id, manuscript_unit_id, execution_id, validator_model_id,
            overall_status, revision_cycle,
            source_authenticity_check, philosophical_integrity_check,
            sanskrit_grammar_check, chandas_metre_check,
            translations_check, commentary_check, originality_repetition_check,
            findings_json, critical_issues_count, major_issues_count,
            minor_issues_count, required_corrections, created_at
        ) VALUES (
            ?, ?, ?, ?,
            ?, ?,
            ?, ?,
            ?, ?,
            ?, ?, ?,
            ?, ?, ?,
            ?, ?, CURRENT_TIMESTAMP
        );
        """
        params = (
            report_id,
            report.get("manuscript_unit_id", ""),
            report.get("execution_id", ""),
            report.get("validator_model_id", "gpt-4o"),
            report.get("overall_status", "NEEDS_REVISION"),
            report.get("revision_cycle", 0),
            report.get("source_authenticity_check", "PASS"),
            report.get("philosophical_integrity_check", "PASS"),
            report.get("sanskrit_grammar_check", "PASS"),
            report.get("chandas_metre_check", "PASS"),
            report.get("translations_check", "PASS"),
            report.get("commentary_check", "PASS"),
            report.get("originality_repetition_check", "PASS"),
            findings_json,
            report.get("critical_issues_count", 0),
            report.get("major_issues_count", 0),
            report.get("minor_issues_count", 0),
            report.get("required_corrections", ""),
        )

        with self._get_connection() as conn:
            conn.execute(sql, params)
            # Update validation status on the manuscript unit
            conn.execute(
                "UPDATE manuscript_units SET validation_status = ? WHERE id = ?;",
                (report.get("overall_status", "NEEDS_REVISION"), report.get("manuscript_unit_id", "")),
            )
            conn.commit()
            return report_id

    def get_validation_reports_for_unit(self, manuscript_unit_id: str) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_validation_reports_for_unit
        ------------------------------------------------------------------------
        Purpose:
            Retrieves all validation reports recorded for a given manuscript unit.
        ------------------------------------------------------------------------
        """
        sql = "SELECT * FROM validation_reports WHERE manuscript_unit_id = ? ORDER BY revision_cycle ASC;"
        with self._get_connection() as conn:
            rows = conn.execute(sql, (manuscript_unit_id,)).fetchall()
            results = []
            for r in rows:
                item = dict(r)
                item["findings"] = json.loads(item.get("findings_json", "[]"))
                results.append(item)
            return results

    # ==========================================================================
    # Token Usage & Budget Accounting Persistence
    # ==========================================================================

    def record_token_usage(self, usage: Dict[str, Any]) -> None:
        """
        ------------------------------------------------------------------------
        Method: record_token_usage
        ------------------------------------------------------------------------
        Purpose:
            Records token consumption and cost for any of the four agents,
            enforcing idempotency to prevent duplicate billing records.
        ------------------------------------------------------------------------
        """
        record_id = usage.get("id") or str(uuid.uuid4())
        idempotency_key = usage.get("idempotency_key") or f"{usage.get('execution_id')}_{usage.get('attempt_number', 1)}"

        sql = """
        INSERT INTO token_usage_records (
            id, idempotency_key, provider, model_id, agent_role, workflow_id,
            manuscript_unit_id, execution_id, attempt_number, is_revision,
            input_tokens, output_tokens, cached_input_tokens, cache_write_tokens,
            total_tokens, billing_currency, estimated_cost_usd, actual_cost_usd,
            exchange_rate_inr, cost_inr, call_status, created_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, CURRENT_TIMESTAMP
        )
        ON CONFLICT(idempotency_key) DO NOTHING;
        """
        params = (
            record_id,
            idempotency_key,
            usage.get("provider", "unknown"),
            usage.get("model_id", "unknown"),
            usage.get("agent_role", "unknown"),
            usage.get("workflow_id", "unknown"),
            usage.get("manuscript_unit_id"),
            usage.get("execution_id", str(uuid.uuid4())),
            usage.get("attempt_number", 1),
            1 if usage.get("is_revision") else 0,
            usage.get("input_tokens", 0),
            usage.get("output_tokens", 0),
            usage.get("cached_input_tokens", 0),
            usage.get("cache_write_tokens", 0),
            usage.get("total_tokens", usage.get("input_tokens", 0) + usage.get("output_tokens", 0)),
            usage.get("billing_currency", "USD"),
            usage.get("estimated_cost_usd", 0.0),
            usage.get("actual_cost_usd"),
            usage.get("exchange_rate_inr", 83.50),
            usage.get("cost_inr", 0.0),
            usage.get("call_status", "success"),
        )
        with self._get_connection() as conn:
            conn.execute(sql, params)
            conn.commit()

    def get_token_usage_summary(self, group_by: str = "agent_role") -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_token_usage_summary
        ------------------------------------------------------------------------
        Purpose:
            Aggregates token and cost metrics grouped by agent_role, provider, or model.
        ------------------------------------------------------------------------
        """
        valid_groups = {"agent_role", "provider", "model_id", "workflow_id"}
        group_col = group_by if group_by in valid_groups else "agent_role"

        sql = f"""
        SELECT 
            {group_col} AS category,
            COUNT(*) AS call_count,
            SUM(input_tokens) AS total_input_tokens,
            SUM(output_tokens) AS total_output_tokens,
            SUM(cached_input_tokens) AS total_cached_tokens,
            SUM(total_tokens) AS grand_total_tokens,
            SUM(cost_inr) AS total_cost_inr
        FROM token_usage_records
        GROUP BY {group_col}
        ORDER BY total_cost_inr DESC;
        """
        with self._get_connection() as conn:
            rows = conn.execute(sql).fetchall()
            return [dict(r) for r in rows]

    def get_token_usage_records(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_token_usage_records
        ------------------------------------------------------------------------
        Purpose:
            Retrieves recent token usage entries ordered chronologically.
        ------------------------------------------------------------------------
        """
        sql = "SELECT * FROM token_usage_records ORDER BY created_at DESC LIMIT ?;"
        with self._get_connection() as conn:
            rows = conn.execute(sql, (limit,)).fetchall()
            return [dict(r) for r in rows]

    def upsert_budget(self, scope_type: str, scope_name: str, monthly_limit_inr: float) -> None:
        """
        ------------------------------------------------------------------------
        Method: upsert_budget
        ------------------------------------------------------------------------
        Purpose:
            Configures or updates an admin budget in INR for a given scope.
        ------------------------------------------------------------------------
        """
        budget_id = str(uuid.uuid4())
        sql = """
        INSERT INTO budget_configurations (
            id, scope_type, scope_name, monthly_limit_inr, current_spent_inr,
            alert_50_fired, alert_75_fired, alert_90_fired, hard_stop_active,
            updated_at
        ) VALUES (
            ?, ?, ?, ?, 0.0,
            0, 0, 0, 0,
            CURRENT_TIMESTAMP
        )
        ON CONFLICT(scope_type, scope_name) DO UPDATE SET
            monthly_limit_inr = excluded.monthly_limit_inr,
            updated_at = CURRENT_TIMESTAMP;
        """
        with self._get_connection() as conn:
            conn.execute(sql, (budget_id, scope_type, scope_name, monthly_limit_inr))
            conn.commit()

    def get_budget(self, scope_type: str, scope_name: str) -> Optional[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_budget
        ------------------------------------------------------------------------
        Purpose:
            Retrieves current budget status and limits for a specific scope.
        ------------------------------------------------------------------------
        """
        sql = "SELECT * FROM budget_configurations WHERE scope_type = ? AND scope_name = ?;"
        with self._get_connection() as conn:
            row = conn.execute(sql, (scope_type, scope_name)).fetchone()
            return dict(row) if row else None

    def update_budget_spent(
        self, scope_type: str, scope_name: str, additional_spent_inr: float
    ) -> Dict[str, Any]:
        """
        ------------------------------------------------------------------------
        Method: update_budget_spent
        ------------------------------------------------------------------------
        Purpose:
            Atomically increments spent INR and returns alert triggers (50%, 75%, 90%, 100%).
        ------------------------------------------------------------------------
        """
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM budget_configurations WHERE scope_type = ? AND scope_name = ?;",
                (scope_type, scope_name),
            ).fetchone()
            if not row:
                # Create default budget if not explicitly configured
                self.upsert_budget(scope_type, scope_name, 50000.0)
                row = conn.execute(
                    "SELECT * FROM budget_configurations WHERE scope_type = ? AND scope_name = ?;",
                    (scope_type, scope_name),
                ).fetchone()

            current_spent = row["current_spent_inr"] + additional_spent_inr
            limit = row["monthly_limit_inr"]
            ratio = (current_spent / limit) if limit > 0 else 0.0

            alert_50 = 1 if (ratio >= 0.50 or row["alert_50_fired"]) else 0
            alert_75 = 1 if (ratio >= 0.75 or row["alert_75_fired"]) else 0
            alert_90 = 1 if (ratio >= 0.90 or row["alert_90_fired"]) else 0
            hard_stop = 1 if ratio >= 1.0 else 0

            conn.execute(
                """
                UPDATE budget_configurations
                SET current_spent_inr = ?,
                    alert_50_fired = ?,
                    alert_75_fired = ?,
                    alert_90_fired = ?,
                    hard_stop_active = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?;
                """,
                (current_spent, alert_50, alert_75, alert_90, hard_stop, row["id"]),
            )
            conn.commit()

            return {
                "scope_type": scope_type,
                "scope_name": scope_name,
                "limit_inr": limit,
                "spent_inr": current_spent,
                "percentage_used": round(ratio * 100, 2),
                "alert_50": bool(alert_50 and not row["alert_50_fired"]),
                "alert_75": bool(alert_75 and not row["alert_75_fired"]),
                "alert_90": bool(alert_90 and not row["alert_90_fired"]),
                "hard_stop_active": bool(hard_stop),
            }

    # ==========================================================================
    # Immutable Audit Trail
    # ==========================================================================

    def record_audit_log(
        self,
        user_email: str,
        action: str,
        entity_type: str,
        entity_id: str,
        change_summary: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: record_audit_log
        ------------------------------------------------------------------------
        Purpose:
            Persists an immutable system audit record.
        ------------------------------------------------------------------------
        """
        log_id = str(uuid.uuid4())
        metadata_str = json.dumps(metadata) if metadata else None
        sql = """
        INSERT INTO audit_logs (id, user_email, action, entity_type, entity_id, change_summary, metadata_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
        """
        with self._get_connection() as conn:
            conn.execute(sql, (log_id, user_email, action, entity_type, entity_id, change_summary, metadata_str))
            conn.commit()

    def get_audit_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        ------------------------------------------------------------------------
        Method: get_audit_logs
        ------------------------------------------------------------------------
        Purpose:
            Retrieves recent audit log entries.
        ------------------------------------------------------------------------
        """
        sql = "SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT ?;"
        with self._get_connection() as conn:
            rows = conn.execute(sql, (limit,)).fetchall()
            return [dict(r) for r in rows]
