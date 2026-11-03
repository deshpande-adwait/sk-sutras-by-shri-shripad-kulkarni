"""
================================================================================
Module: src.cost.reporting
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Comprehensive Cost Reporting and Visibility Engine. Aggregates
             token consumption, initial vs revision costs, provider-level vs
             agent-level breakdowns, and generates CSV/JSON export artifacts.
================================================================================
"""

import csv
import io
import json
from typing import Any, Dict, List, Optional

from src.database.repository import ManuscriptRepository


class CostReporter:
    """
    ----------------------------------------------------------------------------
    Class: CostReporter
    ----------------------------------------------------------------------------
    Purpose:
        Produces detailed cost breakdowns across all four scholarly agents.
        Distinguishes Agent 2 (Shandilya) and Agent 4 (Validator) spend even when
        sharing the same OpenAI provider account.
    ----------------------------------------------------------------------------
    """

    def __init__(self, repository: Optional[ManuscriptRepository] = None) -> None:
        self.repository = repository or ManuscriptRepository()

    def get_four_agent_breakdown(self) -> Dict[str, Any]:
        """
        ------------------------------------------------------------------------
        Method: get_four_agent_breakdown
        ------------------------------------------------------------------------
        Purpose:
            Generates individual metrics for:
            - Agent 1: Narada Specialist (Google Gemini)
            - Agent 2: Shandilya Specialist (OpenAI GPT)
            - Agent 3: Sutrakar Master Author (Anthropic Claude)
            - Agent 4: Independent Validator (OpenAI GPT)
        ------------------------------------------------------------------------
        """
        agent_summaries = self.repository.get_token_usage_summary(group_by="agent_role")
        provider_summaries = self.repository.get_token_usage_summary(group_by="provider")

        return {
            "by_agent": agent_summaries,
            "by_provider": provider_summaries,
            "currency": "INR",
        }

    def export_csv(self) -> str:
        """
        Generates CSV string of all individual token usage transactions.
        """
        records = self.repository.get_token_usage_records(limit=1000)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "id", "idempotency_key", "provider", "model_id", "agent_role",
            "workflow_id", "manuscript_unit_id", "input_tokens", "output_tokens",
            "cached_input_tokens", "total_tokens", "cost_usd", "cost_inr", "call_status", "created_at"
        ])

        for r in records:
            writer.writerow([
                r.get("id"),
                r.get("idempotency_key"),
                r.get("provider"),
                r.get("model_id"),
                r.get("agent_role"),
                r.get("workflow_id"),
                r.get("manuscript_unit_id"),
                r.get("input_tokens"),
                r.get("output_tokens"),
                r.get("cached_input_tokens"),
                r.get("total_tokens"),
                r.get("estimated_cost_usd"),
                r.get("cost_inr"),
                r.get("call_status"),
                r.get("created_at"),
            ])
        return output.getvalue()
