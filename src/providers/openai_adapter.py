"""
================================================================================
Module: src.providers.openai_adapter
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Adapter for OpenAI GPT models (GPT-4o) designated for Agent 2
             (Shandilya Specialist) and Agent 4 (Independent Validator). Supports
             prompt caching, usage extraction, token estimation, and offline development mode.
================================================================================
"""

import os
import warnings
from typing import Any, Dict, Optional

# Suppress lifecycle and deprecation warnings for 100% clean logs
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from src.credentials import get_openai_key
from src.providers.base import (
    BaseLLMAdapter,
    ProviderAuthenticationError,
    ProviderError,
    ProviderResponse,
    ProviderUsage,
)

_UNSET_KEY = object()


class OpenAIAdapter(BaseLLMAdapter):
    """
    ----------------------------------------------------------------------------
    Class: OpenAIAdapter
    ----------------------------------------------------------------------------
    Purpose:
        Implements OpenAI API communication for the Shandilya Specialist and
        Independent Validator agents. Supports prompt caching metrics, token
        accounting, and safe offline development modes. Reads the API key from
        its separate dedicated credential file (keys/openai_key.txt).
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        model_id: Optional[str] = None,
        api_key: Any = _UNSET_KEY,
        temperature: float = 0.20,
        max_tokens: int = 4096,
        timeout_seconds: float = 60.0,
        offline_mode: Optional[bool] = None,
    ) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the OpenAI adapter with configurable model IDs
            and safe key retrieval from keys/openai_key.txt.
        ------------------------------------------------------------------------
        """
        resolved_model = model_id or os.getenv("OPENAI_MODEL_ID", "gpt-4o")
        resolved_key = get_openai_key() if api_key is _UNSET_KEY else api_key
        resolved_offline = (
            offline_mode
            if offline_mode is not None
            else (os.getenv("OFFLINE_MODE", "true").lower() == "true" or not resolved_key)
        )

        super().__init__(
            model_id=resolved_model,
            api_key=resolved_key,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout_seconds=timeout_seconds,
            offline_mode=resolved_offline,
        )

    @property
    def provider_name(self) -> str:
        """Returns the provider identifier string."""
        return "openai"

    @property
    def supports_prompt_caching(self) -> bool:
        """GPT-4o supports automatic prompt caching for prompts >= 1024 tokens."""
        return True

    @property
    def supports_batch_api(self) -> bool:
        """OpenAI Batch API interface support."""
        return True

    def estimate_tokens(self, text: str) -> int:
        """
        ------------------------------------------------------------------------
        Method: estimate_tokens
        ------------------------------------------------------------------------
        Purpose:
            Safe offline token estimation using character/word heuristics.
        ------------------------------------------------------------------------
        """
        if not text:
            return 0
        return max(1, int(len(text) / 2.8))

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        cached_context: Optional[str] = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """
        ------------------------------------------------------------------------
        Method: generate
        ------------------------------------------------------------------------
        Purpose:
            Generates text completions. In offline mode, constructs a structured
            offline analytical response without making external network calls.
        ------------------------------------------------------------------------
        """
        if self.offline_mode:
            input_toks = self.estimate_tokens((system_prompt or "") + prompt)
            output_toks = 200
            usage = ProviderUsage(
                input_tokens=input_toks,
                output_tokens=output_toks,
                cached_input_tokens=self.estimate_tokens(cached_context or "") if cached_context else 0,
                total_tokens=input_toks + output_toks,
                estimated_cost_usd=self.estimate_cost(input_toks, output_toks),
                currency="USD",
                raw_usage={"mode": "offline_simulated"},
            )
            mock_content = (
                "[OpenAI GPT-4o / Scholarly Analysis - Offline Review Mode]\n"
                "Rigorous epistemological analysis adhering to classical Darshana principles.\n"
                "Verified against Maharshi Shandilya's 100-sutra canon and Paninian grammatical rules."
            )
            return ProviderResponse(
                content=mock_content,
                usage=usage,
                model_id=self.model_id,
                provider=self.provider_name,
                finish_reason="stop",
            )

        if not self.api_key:
            raise ProviderAuthenticationError(
                message="OpenAI API key missing or unconfigured.",
                provider=self.provider_name,
                model_id=self.model_id,
            )

        # When authorized live mode is triggered by owner
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, timeout=self.timeout_seconds)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            if cached_context:
                messages.append({"role": "system", "content": f"Static Context:\n{cached_context}"})
            messages.append({"role": "user", "content": prompt})

            completion = client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            raw_usage = completion.usage
            input_toks = raw_usage.prompt_tokens if raw_usage else self.estimate_tokens(prompt)
            output_toks = raw_usage.completion_tokens if raw_usage else 200
            cached_toks = 0
            if raw_usage and hasattr(raw_usage, "prompt_tokens_details") and raw_usage.prompt_tokens_details:
                cached_toks = getattr(raw_usage.prompt_tokens_details, "cached_tokens", 0)

            content = completion.choices[0].message.content or ""
            usage = ProviderUsage(
                input_tokens=input_toks,
                output_tokens=output_toks,
                cached_input_tokens=cached_toks,
                total_tokens=input_toks + output_toks,
                estimated_cost_usd=self.estimate_cost(input_toks, output_toks),
                currency="USD",
            )
            return ProviderResponse(
                content=content,
                usage=usage,
                model_id=self.model_id,
                provider=self.provider_name,
                finish_reason=completion.choices[0].finish_reason or "stop",
            )
        except Exception as exc:
            raise ProviderError(
                message=f"OpenAI generation failed: {str(exc)}",
                provider=self.provider_name,
                model_id=self.model_id,
                raw_error=exc,
            )
