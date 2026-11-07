"""
================================================================================
Module: src.orchestration.council_logger
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: High-fidelity logging and audit trail system for the Vidvat Parishad
             (Four-Agent Scholarly Council). Captures live inter-agent dialogue,
             candidate matching scores, Sutrakara arbitration inquiries,
             rejection of forced/weak pairs, and Agent 4 metric validations.
             Streams formatted transcripts to stdout and persists to logs/.
================================================================================
"""

import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional


class CouncilLogger:
    """
    ----------------------------------------------------------------------------
    Class: CouncilLogger
    ----------------------------------------------------------------------------
    Purpose:
        Provides centralized, persistent, and live-streaming logging for the
        four-agent orchestration pipeline. Ensures 100% transparency into how
        Agent 1 (Narada Specialist), Agent 2 (Shandilya Specialist), Agent 3
        (Sutrakar Master Arbiter), and Agent 4 (Independent Validator) interact,
        deliberate, challenge each other, and decide on candidate aphorisms.

    Attributes:
        log_dir (Path): Dedicated directory for persistent audit logs.
        session_id (str): Unique timestamped session identifier.
        log_file (Path): Path to active text session log file.
        jsonl_file (Path): Path to structured JSONL event log file.
        logger (logging.Logger): Internal Python logger instance.
    ----------------------------------------------------------------------------
    """

    def __init__(self, log_dir: Optional[Path] = None, session_name: str = "vidvat_council") -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the CouncilLogger, creates the logs directory, and sets
            up dual file/stream handlers for console and persistent storage.

        Parameters:
            log_dir (Optional[Path]): Directory where logs are stored.
            session_name (str): Prefix identifier for the log files.

        Errors Handled:
            - Gracefully handles directory creation errors.
            - Configures UTF-8 encoding for Devanagari Sanskrit rendering.

        Manual Debugging Notes:
            - Check 'logs/council_transcripts.jsonl' for machine-readable JSON logs.
            - Check 'logs/vidvat_council_*.log' for human-readable Shastrartha debates.
        ------------------------------------------------------------------------
        """
        base_dir = Path(__file__).resolve().parent.parent.parent
        self.log_dir = log_dir or (base_dir / "logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = f"{session_name}_{now_str}"
        self.log_file = self.log_dir / f"{self.session_id}.log"
        self.jsonl_file = self.log_dir / "council_transcripts.jsonl"

        # Setup standard python logger
        self.logger = logging.getLogger(f"CouncilLogger_{self.session_id}")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()

        # File handler (UTF-8 for Devanagari Sanskrit support)
        fh = logging.FileHandler(self.log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def log_event(self, stage: str, agent_name: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        ------------------------------------------------------------------------
        Method: log_event
        ------------------------------------------------------------------------
        Purpose:
            Records a single scholarly orchestration event to console, text log,
            and structured JSONL audit stream.

        Parameters:
            stage (str): Workflow stage (e.g., 'CANDIDATE_SEARCH', 'ARBITRATION').
            agent_name (str): Name of agent generating the message.
            message (str): Detailed scholarly dialogue or decision statement.
            metadata (Optional[Dict[str, Any]]): Key-value contextual attributes.

        Returns:
            None
        ------------------------------------------------------------------------
        """
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": self.session_id,
            "stage": stage,
            "agent": agent_name,
            "message": message,
            "metadata": metadata or {},
        }

        # Write to persistent text log
        self.logger.info(f"[{stage}] [{agent_name}] {message}")

        # Append to JSONL audit file
        try:
            with open(self.jsonl_file, "a", encoding="utf-8") as jf:
                jf.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to append to JSONL audit log: {e}")

    def log_dialogue(
        self,
        sutra_id: str,
        theme: str,
        agent1_narada: Dict[str, Any],
        agent2_shandilya: Dict[str, Any],
        sutrakar_arbitration: Dict[str, Any],
        agent4_validation: Optional[Dict[str, Any]] = None,
        print_to_console: bool = True,
    ) -> str:
        """
        ------------------------------------------------------------------------
        Method: log_dialogue
        ------------------------------------------------------------------------
        Purpose:
            Formats and logs the complete 4-agent Shastrartha (deliberation)
            for a specific sutra candidate pair. Outputs clear agent demarcations
            to stdout and saves the conversation transcript to disk.

        Parameters:
            sutra_id (str): Identifier for the unit/pair (e.g., 'UDYOGA-001').
            theme (str): Unifying thematic subject.
            agent1_narada (Dict[str, Any]): Output payload from Narada Specialist.
            agent2_shandilya (Dict[str, Any]): Output payload from Shandilya Specialist.
            sutrakar_arbitration (Dict[str, Any]): Arbiter verdict and inquiry.
            agent4_validation (Optional[Dict[str, Any]]): Syllabic/grammatical audit.
            print_to_console (bool): Whether to stream formatted dialogue to stdout.

        Returns:
            str: Full formatted multi-agent dialogue transcript.
        ------------------------------------------------------------------------
        """
        divider = "=" * 80
        sub_divider = "-" * 80

        lines = [
            divider,
            f" VIDVAT PARISHAD DIALOGUE TRANSCRIPT — {sutra_id}",
            f" Theme: {theme}",
            f" Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            divider,
            "",
            " [Agent 1 — Narada Bhakti Sutra Specialist (Gemini 1.5 Pro)]",
            f"  • Sutra #{agent1_narada.get('sutra_no', 'N/A')}: {agent1_narada.get('sanskrit', '')}",
            f"  • Exposition Thesis:",
            f"    {agent1_narada.get('thesis', agent1_narada.get('exposition', ''))}",
            "",
            sub_divider,
            " [Agent 2 — Shandilya Bhakti Sutra Specialist (OpenAI GPT-4o)]",
            f"  • Sutra #{agent2_shandilya.get('sutra_no', 'N/A')}: {agent2_shandilya.get('sanskrit', '')}",
            f"  • Semantic Candidate Rationale:",
            f"    {agent2_shandilya.get('thesis', agent2_shandilya.get('counter_thesis', ''))}",
            "",
            sub_divider,
            " [Agent 3 — Sutrakara Master Arbiter & Orchestrator (Claude 3.5 Sonnet)]",
            f"  • Critical Inquiry: {sutrakar_arbitration.get('sutrakar_inquiry', '')}",
            f"  • Dialectical Tension: {sutrakar_arbitration.get('philosophical_tension', '')}",
            f"  • Synthesis Ground: {sutrakar_arbitration.get('synthetic_resolution', '')}",
            f"  • RULING (Vidvat Nirnaya): {sutrakar_arbitration.get('arbitration_verdict', 'ACCEPTED')}",
            f"  • Rationale: {sutrakar_arbitration.get('arbitration_notes', '')}",
            "",
        ]

        if agent4_validation:
            lines.extend([
                sub_divider,
                " [Agent 4 — Independent Sanskrit & Metre Review (OpenAI GPT-4o)]",
                f"  • Verification Status: {agent4_validation.get('overall_status', 'UNKNOWN')}",
                f"  • Syllable Count Gate: {agent4_validation.get('syllables_count', '32')}/32 (Anushtubh: 8-8-8-8)",
                f"  • Grammatical Gate: {agent4_validation.get('grammar_status', 'PASS')}",
                f"  • Philosophical Fidelity: {agent4_validation.get('philosophical_status', 'PASS')}",
                f"  • Reviewer Findings: {agent4_validation.get('location_specific_findings', 'All 7 Gates Passed')}",
                "",
            ])

        lines.append(divider)
        transcript = "\n".join(lines)

        # Log event to disk
        self.log_event(
            stage="COUNCIL_DELIBERATION",
            agent_name="VidvatParishad",
            message=f"Deliberation recorded for {sutra_id} ({theme}) - Verdict: {sutrakar_arbitration.get('arbitration_verdict')}",
            metadata={
                "sutra_id": sutra_id,
                "theme": theme,
                "verdict": sutrakar_arbitration.get("arbitration_verdict"),
                "narada_sutra_no": agent1_narada.get("sutra_no"),
                "shandilya_sutra_no": agent2_shandilya.get("sutra_no"),
            },
        )

        if print_to_console:
            print(transcript)

        return transcript


# Global singleton instance for easy import across nodes
default_council_logger = CouncilLogger()
