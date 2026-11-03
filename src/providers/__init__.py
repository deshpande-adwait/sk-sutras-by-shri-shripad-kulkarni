"""
================================================================================
Package: src.providers
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Unified multi-provider adapter framework supporting Google Gemini,
             OpenAI GPT, and Anthropic Claude models with token metering,
             caching interfaces, and offline development capabilities.
================================================================================
"""

from src.providers.base import (
    BaseLLMAdapter,
    ProviderAuthenticationError,
    ProviderBudgetExceededError,
    ProviderError,
    ProviderRateLimitError,
    ProviderResponse,
    ProviderTimeoutError,
    ProviderUsage,
)
from src.providers.gemini_adapter import GeminiAdapter
from src.providers.openai_adapter import OpenAIAdapter
from src.providers.anthropic_adapter import AnthropicAdapter
from src.providers.registry import ProviderRegistry, get_provider_registry

__all__ = [
    "BaseLLMAdapter",
    "ProviderError",
    "ProviderAuthenticationError",
    "ProviderRateLimitError",
    "ProviderTimeoutError",
    "ProviderBudgetExceededError",
    "ProviderUsage",
    "ProviderResponse",
    "GeminiAdapter",
    "OpenAIAdapter",
    "AnthropicAdapter",
    "ProviderRegistry",
    "get_provider_registry",
]
