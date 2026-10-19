"""
================================================================================
Module: src.database.repository
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Relational SQLite repository managing ACID-compliant persistence for
             comparative sutra pairs, human review audit trails, and accessibility
             system settings.
================================================================================
"""

import sqlite3
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
        editorial decisions, and managing accessibility presets.

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
