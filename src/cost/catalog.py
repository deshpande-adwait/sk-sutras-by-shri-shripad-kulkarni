"""
================================================================================
Module: src.cost.catalog
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Configurable Price Catalogue storing exact rates per million tokens,
             cache read/write prices, batch rates, effective dates, official
             source references, and verified vs provisional status tags.
================================================================================
"""

from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ModelPrice(BaseModel):
    """
    ----------------------------------------------------------------------------
    Class: ModelPrice
    ----------------------------------------------------------------------------
    Purpose:
        Represents the official pricing schema for a specific LLM model version.

    Attributes:
        provider (str): Provider name ('google', 'openai', 'anthropic').
        model_id (str): Exact model identifier string.
        input_price_per_m (float): Rate in USD per 1 Million input prompt tokens.
        output_price_per_m (float): Rate in USD per 1 Million generated tokens.
        cache_read_price_per_m (float): Rate in USD per 1 Million cached input tokens.
        cache_write_price_per_m (float): Rate in USD per 1 Million cache-creation tokens.
        batch_input_price_per_m (float): Discounted batch input rate per 1M tokens.
        batch_output_price_per_m (float): Discounted batch output rate per 1M tokens.
        currency (str): Original billing currency (default: 'USD').
        is_verified (bool): True if verified against live provider portal; False if provisional.
        official_source_url (str): Link to official vendor documentation.
        effective_date (str): Date from which this pricing tier applies (YYYY-MM-DD).
        last_verified_at (str): ISO timestamp of last scholarly verification.
    ----------------------------------------------------------------------------
    """
    provider: str = Field(..., description="Provider platform identifier")
    model_id: str = Field(..., description="Exact model ID")
    input_price_per_m: float = Field(..., description="USD per 1M input tokens")
    output_price_per_m: float = Field(..., description="USD per 1M output tokens")
    cache_read_price_per_m: float = Field(default=0.0, description="USD per 1M cache read tokens")
    cache_write_price_per_m: float = Field(default=0.0, description="USD per 1M cache write tokens")
    batch_input_price_per_m: float = Field(default=0.0, description="USD per 1M batch input tokens")
    batch_output_price_per_m: float = Field(default=0.0, description="USD per 1M batch output tokens")
    currency: str = Field(default="USD", description="Billing currency")
    is_verified: bool = Field(default=False, description="Verification flag")
    official_source_url: str = Field(..., description="Vendor pricing documentation URL")
    effective_date: str = Field(default="2026-01-01", description="Effective date")
    last_verified_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Verification timestamp")


class PriceCatalog:
    """
    ----------------------------------------------------------------------------
    Class: PriceCatalog
    ----------------------------------------------------------------------------
    Purpose:
        Registry managing and serving model price records. Distinguishes verified
        commercial rates from provisional estimates.
    ----------------------------------------------------------------------------
    """

    def __init__(self) -> None:
        self._catalog: Dict[str, ModelPrice] = {}
        self._load_default_catalog()

    def _make_key(self, provider: str, model_id: str) -> str:
        return f"{provider.lower()}:{model_id.lower()}"

    def _load_default_catalog(self) -> None:
        """Loads baseline catalog entries with vendor source references."""
        # 1. Google Gemini 1.5 Pro
        self.register_price(
            ModelPrice(
                provider="google",
                model_id="gemini-1.5-pro",
                input_price_per_m=3.50,
                output_price_per_m=10.50,
                cache_read_price_per_m=0.875,
                cache_write_price_per_m=3.50,
                batch_input_price_per_m=1.75,
                batch_output_price_per_m=5.25,
                currency="USD",
                is_verified=False, # Flagged provisional until explicit authorized live check
                official_source_url="https://ai.google.dev/pricing",
                effective_date="2026-01-01",
            )
        )

        # 2. OpenAI GPT-4o
        self.register_price(
            ModelPrice(
                provider="openai",
                model_id="gpt-4o",
                input_price_per_m=2.50,
                output_price_per_m=10.00,
                cache_read_price_per_m=1.25,
                cache_write_price_per_m=2.50,
                batch_input_price_per_m=1.25,
                batch_output_price_per_m=5.00,
                currency="USD",
                is_verified=False,
                official_source_url="https://openai.com/api/pricing/",
                effective_date="2026-01-01",
            )
        )

        # 3. Anthropic Claude 3.5 Sonnet
        self.register_price(
            ModelPrice(
                provider="anthropic",
                model_id="claude-3-5-sonnet-20241022",
                input_price_per_m=3.00,
                output_price_per_m=15.00,
                cache_read_price_per_m=0.30,
                cache_write_price_per_m=3.75,
                batch_input_price_per_m=1.50,
                batch_output_price_per_m=7.50,
                currency="USD",
                is_verified=False,
                official_source_url="https://www.anthropic.com/pricing",
                effective_date="2026-01-01",
            )
        )

    def register_price(self, price: ModelPrice) -> None:
        """Registers or updates a model pricing tier."""
        key = self._make_key(price.provider, price.model_id)
        self._catalog[key] = price

    def get_price(self, provider: str, model_id: str) -> Optional[ModelPrice]:
        """Retrieves pricing for a specific provider and model."""
        key = self._make_key(provider, model_id)
        if key in self._catalog:
            return self._catalog[key]
        # Partial match fallback
        for k, v in self._catalog.items():
            if k.startswith(provider.lower()):
                return v
        return None

    def calculate_cost_usd(
        self,
        provider: str,
        model_id: str,
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int = 0,
        cache_write_tokens: int = 0,
        is_batch: bool = False,
    ) -> float:
        """
        Calculates exact cost in USD using active price tier.
        """
        price = self.get_price(provider, model_id)
        if not price:
            # Fallback conservative rates ($3.00 / M input, $12.00 / M output)
            return (input_tokens * 3.0 / 1_000_000) + (output_tokens * 12.0 / 1_000_000)

        if is_batch:
            inp_rate = price.batch_input_price_per_m or (price.input_price_per_m * 0.5)
            out_rate = price.batch_output_price_per_m or (price.output_price_per_m * 0.5)
            return (input_tokens * inp_rate / 1_000_000) + (output_tokens * out_rate / 1_000_000)

        regular_inputs = max(0, input_tokens - cached_input_tokens)
        cost = (regular_inputs * price.input_price_per_m / 1_000_000)
        cost += (cached_input_tokens * price.cache_read_price_per_m / 1_000_000)
        cost += (cache_write_tokens * price.cache_write_price_per_m / 1_000_000)
        cost += (output_tokens * price.output_price_per_m / 1_000_000)
        return round(cost, 6)


_GLOBAL_PRICE_CATALOG: Optional[PriceCatalog] = None


def get_default_price_catalog() -> PriceCatalog:
    """Returns the singleton price catalog instance."""
    global _GLOBAL_PRICE_CATALOG
    if _GLOBAL_PRICE_CATALOG is None:
        _GLOBAL_PRICE_CATALOG = PriceCatalog()
    return _GLOBAL_PRICE_CATALOG
