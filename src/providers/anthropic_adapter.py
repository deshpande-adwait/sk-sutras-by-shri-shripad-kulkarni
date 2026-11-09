"""
================================================================================
Module: src.providers.anthropic_adapter
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Adapter for Anthropic Claude models (Claude 3.5 Sonnet) designated
             for Agent 3 (Sutrakar / Master Author). Supports prompt caching,
             ephemeral cache breakpoints, usage extraction, and offline mode.
================================================================================
"""

import os
import warnings
from typing import Any, Dict, Optional

# Suppress lifecycle and deprecation warnings for 100% clean logs
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from src.credentials import get_claude_key, get_claude_workspace_id
from src.providers.base import (
    BaseLLMAdapter,
    ProviderAuthenticationError,
    ProviderError,
    ProviderResponse,
    ProviderUsage,
)

_UNSET_KEY = object()


class AnthropicAdapter(BaseLLMAdapter):
    """
    ----------------------------------------------------------------------------
    Class: AnthropicAdapter
    ----------------------------------------------------------------------------
    Purpose:
        Implements Anthropic API communication for the Sutrakar Master Author.
        Supports Claude prompt caching headers, token accounting, and safe
        offline development modes. Reads the API key from its separate dedicated
        credential file (keys/claude_key.txt).
    ----------------------------------------------------------------------------
    """

    def __init__(
        self,
        model_id: Optional[str] = None,
        api_key: Any = _UNSET_KEY,
        workspace_id: Optional[str] = None,
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
            Initializes the Anthropic Claude adapter with configurable model IDs,
            safe key retrieval from keys/claude_key.txt, and optional workspace ID.
        ------------------------------------------------------------------------
        """
        resolved_model = model_id or os.getenv("ANTHROPIC_MODEL_ID", "claude-sonnet-5-5")
        resolved_key = get_claude_key() if api_key is _UNSET_KEY else api_key
        resolved_ws = (
            workspace_id
            if workspace_id is not None
            else get_claude_workspace_id()
        )
        self.workspace_id: Optional[str] = resolved_ws
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
        return "anthropic"

    @property
    def supports_prompt_caching(self) -> bool:
        """Claude 3.5 Sonnet supports prompt caching with ephemeral breakpoints."""
        return True

    @property
    def supports_batch_api(self) -> bool:
        """Anthropic Message Batches API support."""
        return True

    def estimate_tokens(self, text: str) -> int:
        """
        ------------------------------------------------------------------------
        Method: estimate_tokens
        ------------------------------------------------------------------------
        Purpose:
            Safe offline token estimation for Anthropic models.
        ------------------------------------------------------------------------
        """
        if not text:
            return 0
        return max(1, int(len(text) / 2.7))

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
            output_toks = 220
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
                "[Anthropic Claude 3.5 Sonnet / Sutrakar Master Author - Offline Mode]\n"
                "Original Udyoga Sutra synthesized with complete Sections A through F.\n"
                "Composed in Anushtubh metre with Padaccheda, Anvaya, and Nirukta analysis."
            )
            return ProviderResponse(
                content=mock_content,
                usage=usage,
                model_id=self.model_id,
                provider=self.provider_name,
                finish_reason="end_turn",
            )

        if not self.api_key:
            raise ProviderAuthenticationError(
                message="Anthropic API key missing or unconfigured.",
                provider=self.provider_name,
                model_id=self.model_id,
            )

        # Dedicated Anthropic Claude direct live execution
        # (Silent OpenAI bypass removed as requested; direct live Anthropic client used)
        try:
            import anthropic

            extra_headers = {}
            if self.workspace_id:
                extra_headers["anthropic-workspace-id"] = self.workspace_id

            client = anthropic.Anthropic(
                api_key=self.api_key,
                timeout=self.timeout_seconds,
                default_headers=extra_headers if extra_headers else None,
            )

            system_blocks = []
            if system_prompt:
                system_blocks.append({
                    "type": "text",
                    "text": system_prompt,
                })
            if cached_context:
                system_blocks.append({
                    "type": "text",
                    "text": cached_context,
                    "cache_control": {"type": "ephemeral"},
                })

            create_kwargs = {
                "model": self.model_id,
                "max_tokens": self.max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }
            if self.workspace_id:
                create_kwargs["workspace_id"] = self.workspace_id
            if system_blocks:
                create_kwargs["system"] = system_blocks

            message = client.messages.create(**create_kwargs)

            raw_usage = message.usage
            input_toks = getattr(raw_usage, "input_tokens", self.estimate_tokens(prompt))
            output_toks = getattr(raw_usage, "output_tokens", 220)
            cached_read_toks = getattr(raw_usage, "cache_read_input_tokens", 0)
            cache_write_toks = getattr(raw_usage, "cache_creation_input_tokens", 0)

            content = ""
            for block in message.content:
                if block.type == "text":
                    content += block.text

            usage = ProviderUsage(
                input_tokens=input_toks,
                output_tokens=output_toks,
                cached_input_tokens=cached_read_toks,
                cache_write_tokens=cache_write_toks,
                total_tokens=input_toks + output_toks,
                estimated_cost_usd=self.estimate_cost(input_toks, output_toks),
                currency="USD",
            )
            return ProviderResponse(
                content=content,
                usage=usage,
                model_id=self.model_id,
                provider=self.provider_name,
                finish_reason=message.stop_reason or "end_turn",
            )
        except Exception as exc:
            # Direct transparent error propagation: zero silent fallback to OpenAI
            raise ProviderError(
                message=f"Anthropic generation failed: {str(exc)}",
                provider=self.provider_name,
                model_id=self.model_id,
                raw_error=exc,
            )
