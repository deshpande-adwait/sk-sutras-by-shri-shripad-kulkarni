"""
================================================================================
Module: src.cost.metering
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Centralized Usage Metering Service recording token metrics across all
             four scholarly agents and LLM providers. Prevents duplicate billing
             via idempotency keys, converts USD to INR, and logs to database.
================================================================================
"""

import os
from typing import Any, Dict, Optional

from src.cost.catalog import PriceCatalog, get_default_price_catalog
from src.database.repository import ManuscriptRepository


class TokenMeteringService:
    """
    ----------------------------------------------------------------------------
    Class: TokenMeteringService
    ----------------------------------------------------------------------------
    Purpose:
        Captures, prices, and persists token usage records across all four agents.
        Guarantees idempotency and maintains dual USD/INR currency accounting.
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        repository: Optional[ManuscriptRepository] = None,
        catalog: Optional[PriceCatalog] = None,
        exchange_rate_inr: Optional[float] = None,
    ) -> None:
        """
        Initializes the metering service with database repository and pricing catalog.
        """
        self.repository = repository or ManuscriptRepository()
        self.catalog = catalog or get_default_price_catalog()
        self.exchange_rate_inr = (
            exchange_rate_inr
            if exchange_rate_inr is not None
            else float(os.getenv("USD_TO_INR_EXCHANGE_RATE", "83.50"))
        )

    def record_usage(
        self,
        provider: str,
        model_id: str,
        agent_role: str,
        workflow_id: str,
        execution_id: str,
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int = 0,
        cache_write_tokens: int = 0,
        manuscript_unit_id: Optional[str] = None,
        attempt_number: int = 1,
        is_revision: bool = False,
        call_status: str = "success",
        is_batch: bool = False,
    ) -> Dict[str, Any]:
        """
        ------------------------------------------------------------------------
        Method: record_usage
        ------------------------------------------------------------------------
        Purpose:
            Records a single LLM execution's token metrics, calculates cost in USD
            and INR, and persists the record idempotently.
        ------------------------------------------------------------------------
        """
        cost_usd = self.catalog.calculate_cost_usd(
            provider=provider,
            model_id=model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_input_tokens=cached_input_tokens,
            cache_write_tokens=cache_write_tokens,
            is_batch=is_batch,
        )
        cost_inr = round(cost_usd * self.exchange_rate_inr, 4)
        total_tokens = input_tokens + output_tokens

        idempotency_key = f"{execution_id}_{attempt_number}"

        usage_payload = {
            "idempotency_key": idempotency_key,
            "provider": provider,
            "model_id": model_id,
            "agent_role": agent_role,
            "workflow_id": workflow_id,
            "manuscript_unit_id": manuscript_unit_id,
            "execution_id": execution_id,
            "attempt_number": attempt_number,
            "is_revision": is_revision,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cached_input_tokens": cached_input_tokens,
            "cache_write_tokens": cache_write_tokens,
            "total_tokens": total_tokens,
            "billing_currency": "USD",
            "estimated_cost_usd": cost_usd,
            "exchange_rate_inr": self.exchange_rate_inr,
            "cost_inr": cost_inr,
            "call_status": call_status,
        }

        self.repository.record_token_usage(usage_payload)

        # Update budget spent in database for agent and provider
        self.repository.update_budget_spent("agent", agent_role, cost_inr)
        self.repository.update_budget_spent("provider", provider, cost_inr)
        self.repository.update_budget_spent("project_monthly", "sk_sutras_total", cost_inr)

        return usage_payload


_GLOBAL_METERING_SERVICE: Optional[TokenMeteringService] = None


def get_metering_service() -> TokenMeteringService:
    """Returns the singleton metering service instance."""
    global _GLOBAL_METERING_SERVICE
    if _GLOBAL_METERING_SERVICE is None:
        _GLOBAL_METERING_SERVICE = TokenMeteringService()
    return _GLOBAL_METERING_SERVICE
