"""
================================================================================
Test Module: tests.test_providers
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: QA unit tests verifying the unified provider adapter framework,
             offline execution safety, token estimation, and dynamic model switching.
================================================================================
"""

import pytest
from src.providers.anthropic_adapter import AnthropicAdapter
from src.providers.base import ProviderAuthenticationError
from src.providers.gemini_adapter import GeminiAdapter
from src.providers.openai_adapter import OpenAIAdapter
from src.providers.registry import ProviderRegistry, get_provider_registry


def test_gemini_adapter_offline_mode() -> None:
    """Verifies that GeminiAdapter in offline mode emits simulated scholarly output without network calls."""
    adapter = GeminiAdapter(offline_mode=True)
    assert adapter.provider_name == "google"
    assert adapter.supports_prompt_caching is True

    response = adapter.generate(prompt="Explain Narada Sutra 1", system_prompt="You are Narada specialist.")
    assert response.content is not None
    assert "Narada Specialist Exposition" in response.content
    assert response.usage.input_tokens > 0
    assert response.usage.output_tokens > 0


def test_openai_adapter_offline_mode() -> None:
    """Verifies that OpenAIAdapter in offline mode emits simulated analytical output without network calls."""
    adapter = OpenAIAdapter(offline_mode=True)
    assert adapter.provider_name == "openai"
    assert adapter.supports_prompt_caching is True

    response = adapter.generate(prompt="Analyze Shandilya Sutra 1")
    assert response.content is not None
    assert "Scholarly Analysis" in response.content
    assert response.usage.input_tokens > 0


def test_anthropic_adapter_offline_mode() -> None:
    """Verifies that AnthropicAdapter in offline mode emits simulated composition output without network calls."""
    adapter = AnthropicAdapter(offline_mode=True)
    assert adapter.provider_name == "anthropic"
    assert adapter.supports_prompt_caching is True

    response = adapter.generate(prompt="Compose Udyoga Sutra 1")
    assert response.content is not None
    assert "Sutrakar Master Author" in response.content
    assert response.usage.input_tokens > 0


def test_provider_authentication_error_when_online_without_key() -> None:
    """Verifies that attempting live execution without an API key raises ProviderAuthenticationError."""
    adapter = OpenAIAdapter(api_key=None, offline_mode=False)
    with pytest.raises(ProviderAuthenticationError):
        adapter.generate(prompt="Test live prompt")


def test_provider_registry_four_agent_allocations() -> None:
    """Verifies that the registry allocates all four distinct agents correctly."""
    registry = ProviderRegistry(offline_mode=True)

    agent1 = registry.get_adapter(ProviderRegistry.ROLE_NARADA)
    assert agent1.provider_name == "google"

    agent2 = registry.get_adapter(ProviderRegistry.ROLE_SHANDILYA)
    assert agent2.provider_name == "openai"

    agent3 = registry.get_adapter(ProviderRegistry.ROLE_SUTRAKAR)
    assert agent3.provider_name == "anthropic"

    agent4 = registry.get_adapter(ProviderRegistry.ROLE_VALIDATOR)
    assert agent4.provider_name == "openai"


def test_provider_registry_dynamic_model_switch() -> None:
    """Verifies that an agent's underlying provider/model can be switched dynamically."""
    registry = ProviderRegistry(offline_mode=True)
    # Switch Agent 1 to Anthropic
    registry.switch_model(ProviderRegistry.ROLE_NARADA, provider="anthropic", model_id="claude-3-5-sonnet-20241022")
    new_agent1 = registry.get_adapter(ProviderRegistry.ROLE_NARADA)
    assert new_agent1.provider_name == "anthropic"
    assert new_agent1.model_id == "claude-3-5-sonnet-20241022"
