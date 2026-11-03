"""
================================================================================
Module: src.providers.registry
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Centralized Provider Registry managing LLM adapter allocations for
             all four scholarly agents. Enables dynamic switching of providers
             and model IDs without altering core agent business logic.
================================================================================
"""

import os
from typing import Dict, Optional

from src.providers.anthropic_adapter import AnthropicAdapter
from src.providers.base import BaseLLMAdapter
from src.providers.gemini_adapter import GeminiAdapter
from src.providers.openai_adapter import OpenAIAdapter


class ProviderRegistry:
    """
    ----------------------------------------------------------------------------
    Class: ProviderRegistry
    ----------------------------------------------------------------------------
    Purpose:
        Maintains the mapping of scholarly agent roles to their designated LLM
        provider adapters. Guarantees that model assignments remain centrally
        configurable and replaceable.
    ----------------------------------------------------------------------------
    """

    ROLE_NARADA = "narada_specialist"
    ROLE_SHANDILYA = "shandilya_specialist"
    ROLE_SUTRAKAR = "sutrakar_master"
    ROLE_VALIDATOR = "independent_validator"

    def __init__(self, offline_mode: Optional[bool] = None) -> None:
        """
        ------------------------------------------------------------------------
        Method: __init__
        ------------------------------------------------------------------------
        Purpose:
            Initializes the registry with the default 4-agent provider allocations.
        ------------------------------------------------------------------------
        """
        self._offline_mode = offline_mode
        self._adapters: Dict[str, BaseLLMAdapter] = {}
        self._initialize_default_adapters()

    def _initialize_default_adapters(self) -> None:
        """
        ------------------------------------------------------------------------
        Method: _initialize_default_adapters
        ------------------------------------------------------------------------
        Purpose:
            Instantiates the standard role allocations defined in Part 3 of
            the Master Specification:
            - Agent 1 (Narada): Google Gemini 1.5 Pro
            - Agent 2 (Shandilya): OpenAI GPT-4o
            - Agent 3 (Sutrakar): Anthropic Claude 3.5 Sonnet
            - Agent 4 (Validator): OpenAI GPT-4o (independent configuration)
        ------------------------------------------------------------------------
        """
        # Agent 1: Narada Specialist -> Google Gemini
        narada_model = os.getenv("AGENT1_MODEL_ID", os.getenv("GEMINI_MODEL_ID", "gemini-1.5-pro"))
        self._adapters[self.ROLE_NARADA] = GeminiAdapter(
            model_id=narada_model,
            offline_mode=self._offline_mode,
        )

        # Agent 2: Shandilya Specialist -> OpenAI GPT
        shandilya_model = os.getenv("AGENT2_MODEL_ID", os.getenv("OPENAI_MODEL_ID", "gpt-4o"))
        self._adapters[self.ROLE_SHANDILYA] = OpenAIAdapter(
            model_id=shandilya_model,
            offline_mode=self._offline_mode,
        )

        # Agent 3: Sutrakar Master Author -> Anthropic Claude
        sutrakar_model = os.getenv("AGENT3_MODEL_ID", os.getenv("ANTHROPIC_MODEL_ID", "claude-3-5-sonnet-20241022"))
        self._adapters[self.ROLE_SUTRAKAR] = AnthropicAdapter(
            model_id=sutrakar_model,
            offline_mode=self._offline_mode,
        )

        # Agent 4: Independent Validator -> Separately configurable OpenAI model
        validator_model = os.getenv("AGENT4_MODEL_ID", os.getenv("OPENAI_VALIDATOR_MODEL_ID", "gpt-4o"))
        self._adapters[self.ROLE_VALIDATOR] = OpenAIAdapter(
            model_id=validator_model,
            offline_mode=self._offline_mode,
        )

    def get_adapter(self, agent_role: str) -> BaseLLMAdapter:
        """
        ------------------------------------------------------------------------
        Method: get_adapter
        ------------------------------------------------------------------------
        Purpose:
            Retrieves the active LLM adapter assigned to a specific agent role.
        ------------------------------------------------------------------------
        """
        if agent_role not in self._adapters:
            # Fallback to Agent 2 OpenAI adapter if unknown role
            return self._adapters[self.ROLE_SHANDILYA]
        return self._adapters[agent_role]

    def set_adapter(self, agent_role: str, adapter: BaseLLMAdapter) -> None:
        """
        ------------------------------------------------------------------------
        Method: set_adapter
        ------------------------------------------------------------------------
        Purpose:
            Overrides or assigns a custom provider adapter to an agent role.
        ------------------------------------------------------------------------
        """
        self._adapters[agent_role] = adapter

    def switch_model(self, agent_role: str, provider: str, model_id: str, **kwargs) -> None:
        """
        ------------------------------------------------------------------------
        Method: switch_model
        ------------------------------------------------------------------------
        Purpose:
            Dynamically switches the provider and model for an agent role.
        ------------------------------------------------------------------------
        """
        provider_lower = provider.lower()
        if provider_lower == "google":
            self._adapters[agent_role] = GeminiAdapter(model_id=model_id, offline_mode=self._offline_mode, **kwargs)
        elif provider_lower == "openai":
            self._adapters[agent_role] = OpenAIAdapter(model_id=model_id, offline_mode=self._offline_mode, **kwargs)
        elif provider_lower == "anthropic":
            self._adapters[agent_role] = AnthropicAdapter(model_id=model_id, offline_mode=self._offline_mode, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")


# Global Singleton Registry Instance
_GLOBAL_REGISTRY: Optional[ProviderRegistry] = None


def get_provider_registry(offline_mode: Optional[bool] = None) -> ProviderRegistry:
    """
    ----------------------------------------------------------------------------
    Function: get_provider_registry
    ----------------------------------------------------------------------------
    Purpose:
        Returns the application-wide singleton ProviderRegistry instance.
    ----------------------------------------------------------------------------
    """
    global _GLOBAL_REGISTRY
    if _GLOBAL_REGISTRY is None:
        _GLOBAL_REGISTRY = ProviderRegistry(offline_mode=offline_mode)
    return _GLOBAL_REGISTRY
