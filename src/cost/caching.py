"""
================================================================================
Module: src.cost.caching
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Prompt Caching Management abstraction. Manages cache keys, TTL,
             ephemeral cache breakpoints, hit/miss telemetry, and prompt-change
             invalidation across supported providers (Gemini, Claude, GPT-4o).
================================================================================
"""

import hashlib
import time
from typing import Any, Dict, Optional


class PromptCacheManager:
    """
    ----------------------------------------------------------------------------
    Class: PromptCacheManager
    ----------------------------------------------------------------------------
    Purpose:
        Maintains cache entry tracking and generates provider-appropriate cache
        keys for static scholarly instructions, minimizing token re-transmission.
    ----------------------------------------------------------------------------
    """

    def __init__(self, default_ttl_seconds: int = 3600) -> None:
        self.default_ttl = default_ttl_seconds
        self._cache_registry: Dict[str, Dict[str, Any]] = {}

    def compute_cache_key(self, provider: str, model_id: str, content: str) -> str:
        """Computes a deterministic SHA256 hash key for cacheable prompt content."""
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return f"{provider}:{model_id}:{content_hash[:16]}"

    def register_cache_entry(
        self,
        provider: str,
        model_id: str,
        content: str,
        tokens_cached: int,
        ttl_seconds: Optional[int] = None,
    ) -> str:
        """Registers a newly cached prompt block."""
        cache_key = self.compute_cache_key(provider, model_id, content)
        ttl = ttl_seconds or self.default_ttl
        now = time.time()
        self._cache_registry[cache_key] = {
            "provider": provider,
            "model_id": model_id,
            "tokens_cached": tokens_cached,
            "created_at": now,
            "expires_at": now + ttl,
            "hit_count": 0,
        }
        return cache_key

    def check_cache_hit(self, cache_key: str) -> bool:
        """Verifies if a cache key is active and unexpired."""
        entry = self._cache_registry.get(cache_key)
        if not entry:
            return False
        if time.time() > entry["expires_at"]:
            self._cache_registry.pop(cache_key, None)
            return False
        entry["hit_count"] += 1
        return True

    def invalidate_stale_cache(self) -> int:
        """Purges expired cache entries and returns count of removed keys."""
        now = time.time()
        expired_keys = [k for k, v in self._cache_registry.items() if now > v["expires_at"]]
        for k in expired_keys:
            self._cache_registry.pop(k, None)
        return len(expired_keys)
