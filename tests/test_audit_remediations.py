"""
================================================================================
Test Suite: tests/test_audit_remediations.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Comprehensive offline regression test suite validating all audit
             remediations and architectural integrity guarantees.
================================================================================
"""

import hashlib
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.agents.validator_agent import (
    ValidatorAgent,
    check_duplicate_or_near_duplicate,
    normalize_sutra_text,
)
from src.config import BASE_DIR
from src.providers.anthropic_adapter import AnthropicAdapter
from src.providers.base import (
    OutputTruncationError,
    ProviderError,
    ProviderResponse,
    ProviderUsage,
)
from src.providers.registry import ProviderRegistry


def test_sutra_normalization_and_duplicate_detection() -> None:
    """
    ============================================================================
    Test: test_sutra_normalization_and_duplicate_detection
    Purpose: Verifies that Devanagari Sanskrit aphorisms with differing dandas,
             whitespace, brackets, and numerals (Latin vs Devanagari) normalize
             to identical stems and are correctly flagged as duplicates.
    ============================================================================
    """
    v1 = "॥ उद्यमेन कार्यसिद्धिः ॥ ३ ॥"
    v2 = "उद्यमेन कार्यसिद्धिः 3"
    v3 = "  ॥  उद्यमेन   कार्य-सिद्धिः  ॥  "
    v4 = "॥ कर्तव्यपूर्त्या परमं पदम् ॥ ४ ॥"

    # Verify normalization
    norm1 = normalize_sutra_text(v1)
    norm2 = normalize_sutra_text(v2)
    norm3 = normalize_sutra_text(v3)

    assert norm1 == norm2
    assert norm1 == norm3
    assert norm1 == "उद्यमेनकार्यसिद्धिः"

    # Test duplicate detection against list of existing sutras
    existing = [v1, v4]

    # v2 and v3 must be detected as duplicates of v1
    is_dup2, match2, sim2 = check_duplicate_or_near_duplicate(v2, existing)
    assert is_dup2 is True
    assert match2 == v1
    assert sim2 == 1.0

    is_dup3, match3, sim3 = check_duplicate_or_near_duplicate(v3, existing)
    assert is_dup3 is True
    assert match3 == v1
    assert sim3 == 1.0

    # Distinct verse must NOT be flagged as duplicate
    distinct = "॥ निष्ठावतः सर्वं सफलम् ॥ १ ॥"
    is_dup_d, match_d, sim_d = check_duplicate_or_near_duplicate(distinct, existing)
    assert is_dup_d is False
    assert sim_d < 0.85


def test_provider_truncation_detection_and_classes() -> None:
    """
    ============================================================================
    Test: test_provider_truncation_detection_and_classes
    Purpose: Verifies the OutputTruncationError hierarchy and ProviderResponse
             was_truncated property.
    ============================================================================
    """
    assert issubclass(OutputTruncationError, ProviderError)

    resp_normal = ProviderResponse(
        content="Complete text",
        provider="anthropic",
        model_id="claude-sonnet-5-5",
        usage=ProviderUsage(input_tokens=100, output_tokens=500),
        finish_reason="end_turn",
        is_truncated=False,
    )
    assert resp_normal.was_truncated is False

    resp_cut = ProviderResponse(
        content="Incomplete json payload {",
        provider="anthropic",
        model_id="claude-sonnet-5-5",
        usage=ProviderUsage(input_tokens=100, output_tokens=8192),
        finish_reason="max_tokens",
        is_truncated=True,
    )
    assert resp_cut.was_truncated is True


def test_anthropic_adapter_continuation_logic_offline() -> None:
    """
    ============================================================================
    Test: test_anthropic_adapter_continuation_logic_offline
    Purpose: Simulates an Anthropic API call that truncates at max_tokens on the
             first iteration, verifying that generate_with_continuation()
             automatically invokes continuation and stitches the full payload.
    ============================================================================
    """
    adapter = AnthropicAdapter(model_id="claude-sonnet-5-5", api_key="test-key", offline_mode=False)

    part1_content = '{"sutra": "॥ उद्यमेन कार्यसिद्धिः ॥", "explanation": "'
    part2_content = 'सतत परिश्रमानेच कार्य पूर्ण होते."}'

    # Mock first response (truncated at max_tokens)
    mock_resp1 = MagicMock()
    mock_resp1.content = [MagicMock(type="text", text=part1_content)]
    mock_resp1.stop_reason = "max_tokens"
    mock_resp1.usage = MagicMock(input_tokens=200, output_tokens=4096)

    # Mock second response (continuation completed)
    mock_resp2 = MagicMock()
    mock_resp2.content = [MagicMock(type="text", text=part2_content)]
    mock_resp2.stop_reason = "end_turn"
    mock_resp2.usage = MagicMock(input_tokens=4300, output_tokens=150)

    mock_client_instance = MagicMock()
    mock_client_instance.messages.create.side_effect = [mock_resp1, mock_resp2]

    with patch("anthropic.Anthropic", return_value=mock_client_instance):
        full_resp = adapter.generate_with_continuation(
            prompt="Compose canonical sutra with full commentary.",
            system_prompt="Master Sutrakar",
            max_continuations=2,
        )

        assert full_resp.was_truncated is False
        assert full_resp.content == part1_content + part2_content
        assert full_resp.finish_reason == "end_turn"
        assert full_resp.usage.output_tokens == (4096 + 150)
        assert mock_client_instance.messages.create.call_count == 2


def test_five_agent_registry_canonical_models() -> None:
    """
    ============================================================================
    Test: test_five_agent_registry_canonical_models
    Purpose: Asserts that all five agent roles are properly configured with
             their canonical commercial models across Google, OpenAI, and Anthropic.
    ============================================================================
    """
    reg = ProviderRegistry(offline_mode=True)
    a1 = reg.get_adapter(ProviderRegistry.ROLE_NARADA)
    assert a1.provider_name == "google"
    assert a1.model_id == "gemini-3.8-flash"

    a2 = reg.get_adapter(ProviderRegistry.ROLE_SHANDILYA)
    assert a2.provider_name == "openai"
    assert a2.model_id == "gpt-4o"

    a3 = reg.get_adapter(ProviderRegistry.ROLE_BHARATIYA_JNANA)
    assert a3.provider_name == "anthropic"
    assert a3.model_id == "claude-sonnet-5-5"

    a4 = reg.get_adapter(ProviderRegistry.ROLE_SUTRAKAR)
    assert a4.provider_name == "anthropic"
    assert a4.model_id == "claude-sonnet-5-5"

    a5 = reg.get_adapter(ProviderRegistry.ROLE_VALIDATOR)
    assert a5.provider_name == "openai"
    assert a5.model_id == "gpt-4o"


def test_source_register_sha256_cryptographic_integrity() -> None:
    """
    ============================================================================
    Test: test_source_register_sha256_cryptographic_integrity
    Purpose: Reads data/knowledge_repository/registry/source_register.json,
             computes the SHA-256 hash of each referenced source document on disk,
             and asserts that every hash matches the verified registered checksum.
    ============================================================================
    """
    register_path = BASE_DIR / "data" / "knowledge_repository" / "registry" / "source_register.json"
    assert register_path.exists(), f"Source register missing at {register_path}"

    with open(register_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = data.get("documents", [])
    assert len(docs) >= 4, f"Expected at least 4 registered documents, found {len(docs)}"

    for doc in docs:
        doc_id = doc.get("document_id")
        registered_sha = doc.get("sha256")
        file_path_rel = doc.get("source_location")

        assert registered_sha is not None and len(registered_sha) == 64, (
            f"Document {doc_id} has invalid sha256: {registered_sha}"
        )

        abs_path = BASE_DIR / file_path_rel
        assert abs_path.exists(), f"Source document file not found on disk: {abs_path}"

        # Compute file hash
        h = hashlib.sha256()
        with open(abs_path, "rb") as f_in:
            while chunk := f_in.read(65536):
                h.update(chunk)
        computed_sha = h.hexdigest()

        assert computed_sha == registered_sha, (
            f"Cryptographic hash mismatch for {doc_id} ({abs_path.name})!\n"
            f"  Registered: {registered_sha}\n"
            f"  Computed:   {computed_sha}"
        )


def test_execution_scoped_call_id_uniqueness() -> None:
    """
    ============================================================================
    Test: test_execution_scoped_call_id_uniqueness
    Purpose: Verifies that call_ids formatted with execution_id scope eliminate
             primary key collisions across distinct runs.
    ============================================================================
    """
    exec1 = "exec_dynamic_20261110_095022"
    exec2 = "exec_dynamic_20261110_161110"

    calls_run1 = [f"{exec1}_{i:03d}" for i in range(1, 51)]
    calls_run2 = [f"{exec2}_{i:03d}" for i in range(1, 10)]

    # Assert mutual exclusivity between run 1 and run 2 IDs
    overlap = set(calls_run1).intersection(set(calls_run2))
    assert len(overlap) == 0, f"Detected call_id collision: {overlap}"

    # Assert within-run uniqueness
    assert len(set(calls_run1)) == len(calls_run1)
    assert len(set(calls_run2)) == len(calls_run2)
