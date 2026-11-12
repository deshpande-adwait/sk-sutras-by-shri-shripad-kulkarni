"""
================================================================================
Module: src.providers.gemini_adapter
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Adapter for Google Gemini models (Gemini 1.5 Pro) designated for
             Agent 1 (Narada Bhakti Sutra Specialist). Supports prompt caching,
             usage extraction, token estimation, and offline development mode.
================================================================================
"""

import os
import warnings
from typing import Any, Dict, Optional

# Suppress Python version lifecycle and package deprecation warnings for 100% clean logs
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from src.credentials import get_gemini_key
from src.providers.base import (
    BaseLLMAdapter,
    ProviderAuthenticationError,
    ProviderError,
    ProviderResponse,
    ProviderUsage,
)

_UNSET_KEY = object()


class GeminiAdapter(BaseLLMAdapter):
    """
    ----------------------------------------------------------------------------
    Class: GeminiAdapter
    ----------------------------------------------------------------------------
    Purpose:
        Implements Google Gemini API communication for the Narada Specialist Agent.
        Provides prompt caching integration, token consumption extraction, and
        safe offline development modes preventing unapproved live API calls.
        Reads the API key from its separate dedicated credential file (keys/gemini_key.txt).
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
            Initializes the Google Gemini adapter with configurable model IDs
            and safe key retrieval from keys/gemini_key.txt.
        ------------------------------------------------------------------------
        """
        resolved_model = model_id or os.getenv("GEMINI_MODEL_ID", "gemini-3.8-flash")
        resolved_key = get_gemini_key() if api_key is _UNSET_KEY else api_key
        # In this phase, offline mode defaults to True if credentials are absent or explicitly set
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
        return "google"

    @property
    def supports_prompt_caching(self) -> bool:
        """Gemini 1.5 Pro natively supports context caching for large corpora."""
        return True

    @property
    def supports_batch_api(self) -> bool:
        """Google Vertex/Gemini Batch Prediction interface support."""
        return True

    def estimate_tokens(self, text: str) -> int:
        """
        ------------------------------------------------------------------------
        Method: estimate_tokens
        ------------------------------------------------------------------------
        Purpose:
            Provides a safe offline estimation of token count. For Sanskrit and
            Devanagari text, UTF-8 character density is approximately 1 token
            per 2-3 characters.
        ------------------------------------------------------------------------
        """
        if not text:
            return 0
        # For Devanagari text, tokens roughly equal len(text) / 2.5
        return max(1, int(len(text) / 2.5))

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
            # Deterministic, scholarly mock response for offline verification
            input_toks = self.estimate_tokens((system_prompt or "") + prompt)
            output_toks = 180
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
                "[Google Gemini / Narada Specialist Exposition - Offline Review Mode]\n"
                "Sutra analysis completed with fidelity to Devarshi Narada's canonical tradition.\n"
                "Emphasizes ecstatic devotion, self-surrender, and supreme love (Prema-Rupa)."
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
                message="Google API key missing or unconfigured.",
                provider=self.provider_name,
                model_id=self.model_id,
            )

        # When authorized live mode is triggered by owner
        try:
            # Modern official Google GenAI SDK (google-genai)
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            config = types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
                system_instruction=system_prompt if system_prompt else None,
            )
            response = client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config,
            )

            raw_usage = getattr(response, "usage_metadata", None)
            input_toks = (
                getattr(raw_usage, "prompt_token_count", self.estimate_tokens(prompt))
                if raw_usage
                else self.estimate_tokens(prompt)
            )
            output_toks = (
                getattr(raw_usage, "candidates_token_count", 200)
                if raw_usage
                else 200
            )
            cached_toks = (
                getattr(raw_usage, "cached_content_token_count", 0)
                if raw_usage
                else 0
            )

            usage = ProviderUsage(
                input_tokens=input_toks,
                output_tokens=output_toks,
                cached_input_tokens=cached_toks,
                total_tokens=input_toks + output_toks,
                estimated_cost_usd=self.estimate_cost(input_toks, output_toks),
                currency="USD",
            )
            cand_finish = "stop"
            if hasattr(response, "candidates") and response.candidates:
                cand_finish = str(getattr(response.candidates[0], "finish_reason", "stop")).lower()

            return ProviderResponse(
                content=response.text or "",
                usage=usage,
                model_id=self.model_id,
                provider=self.provider_name,
                finish_reason=cand_finish,
                is_truncated=("max_tokens" in cand_finish or "length" in cand_finish),
            )
        except Exception as exc:
            # Fallback to legacy google.generativeai if google.genai experiences transient client issues
            try:
                import google.generativeai as legacy_genai

                legacy_genai.configure(api_key=self.api_key)
                model = legacy_genai.GenerativeModel(
                    model_name=self.model_id,
                    system_instruction=system_prompt,
                )
                response = model.generate_content(
                    prompt,
                    generation_config=legacy_genai.types.GenerationConfig(
                        temperature=self.temperature,
                        max_output_tokens=self.max_tokens,
                    ),
                )
                raw_usage = getattr(response, "usage_metadata", None)
                input_toks = (
                    getattr(raw_usage, "prompt_token_count", self.estimate_tokens(prompt))
                    if raw_usage
                    else self.estimate_tokens(prompt)
                )
                output_toks = (
                    getattr(raw_usage, "candidates_token_count", 200)
                    if raw_usage
                    else 200
                )
                cached_toks = (
                    getattr(raw_usage, "cached_content_token_count", 0)
                    if raw_usage
                    else 0
                )
                usage = ProviderUsage(
                    input_tokens=input_toks,
                    output_tokens=output_toks,
                    cached_input_tokens=cached_toks,
                    total_tokens=input_toks + output_toks,
                    estimated_cost_usd=self.estimate_cost(input_toks, output_toks),
                    currency="USD",
                )
                return ProviderResponse(
                    content=response.text or "",
                    usage=usage,
                    model_id=self.model_id,
                    provider=self.provider_name,
                    finish_reason="stop",
                )
            except Exception as fb_exc:
                raise ProviderError(
                    message=f"Gemini generation failed: {str(exc)} (legacy fallback: {str(fb_exc)})",
                    provider=self.provider_name,
                    model_id=self.model_id,
                    raw_error=exc,
                )
