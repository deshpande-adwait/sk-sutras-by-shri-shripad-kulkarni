"""
================================================================================
Module: src.cost.estimator
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Pre-call Token and Cost Estimator. Performs conservative upfront
             token calculation and pre-call budget checks prior to LLM dispatch.
================================================================================
"""

import os
import uuid
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from src.cost.budget import BudgetManager, get_budget_manager
from src.cost.catalog import PriceCatalog, get_default_price_catalog
from src.providers.base import BaseLLMAdapter


class CostEstimate(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: CostEstimate
    ----------------------------------------------------------------------------
    Purpose:
        Container holding pre-dispatch token and cost projections.
    ----------------------------------------------------------------------------
    """
    estimated_input_tokens: int = Field(..., description="Projected prompt tokens")
    estimated_output_tokens: int = Field(..., description="Maximum expected completion tokens")
    estimated_cost_usd: float = Field(..., description="Conservative USD cost")
    estimated_cost_inr: float = Field(..., description="Conservative INR cost")
    is_budget_permissible: bool = Field(default=True, description="Budget check status")
    reservation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class PreCallEstimator:
    """
    ----------------------------------------------------------------------------
    Class: PreCallEstimator
    ----------------------------------------------------------------------------
    Purpose:
        Calculates conservative token and expense estimates before dispatching
        external or offline calls. Enforces budget reservations.
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        catalog: Optional[PriceCatalog] = None,
        budget_manager: Optional[BudgetManager] = None,
        exchange_rate_inr: Optional[float] = None,
    ) -> None:
        self.catalog = catalog or get_default_price_catalog()
        self.budget_manager = budget_manager or get_budget_manager()
        self.exchange_rate_inr = (
            exchange_rate_inr
            if exchange_rate_inr is not None
            else float(os.getenv("USD_TO_INR_EXCHANGE_RATE", "83.50"))
        )

    def estimate(
        self,
        adapter: BaseLLMAdapter,
        prompt: str,
        system_prompt: Optional[str] = None,
        cached_context: Optional[str] = None,
        max_output_tokens: Optional[int] = None,
        agent_role: str = "general",
    ) -> CostEstimate:
        """
        ------------------------------------------------------------------------
        Method: estimate
        ------------------------------------------------------------------------
        Purpose:
            Performs conservative pre-call token and cost projection, and reserves
            funds against the agent and monthly budget.
        ------------------------------------------------------------------------
        """
        full_text = (system_prompt or "") + prompt
        inp_tokens = adapter.estimate_tokens(full_text)
        cached_tokens = adapter.estimate_tokens(cached_context or "") if cached_context else 0
        out_tokens = max_output_tokens or adapter.max_tokens

        cost_usd = self.catalog.calculate_cost_usd(
            provider=adapter.provider_name,
            model_id=adapter.model_id,
            input_tokens=inp_tokens,
            output_tokens=out_tokens,
            cached_input_tokens=cached_tokens,
        )
        cost_inr = round(cost_usd * self.exchange_rate_inr, 4)

        reservation_id = str(uuid.uuid4())
        # Check against project monthly budget
        permissible = True
        try:
            self.budget_manager.check_and_reserve(
                scope_type="project_monthly",
                scope_name="sk_sutras_total",
                estimated_cost_inr=cost_inr,
                reservation_id=reservation_id,
            )
        except Exception:
            permissible = False

        return CostEstimate(
            estimated_input_tokens=inp_tokens,
            estimated_output_tokens=out_tokens,
            estimated_cost_usd=cost_usd,
            estimated_cost_inr=cost_inr,
            is_budget_permissible=permissible,
            reservation_id=reservation_id,
        )
