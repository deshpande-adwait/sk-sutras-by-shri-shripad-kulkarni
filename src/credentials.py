"""
================================================================================
Module: src.credentials
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Dedicated secure credential loader for individual LLM API keys.
             Reads API keys from separate, dedicated repository files:
             - Claude Key: keys/claude_key.txt
             - Gemini Key: keys/gemini_key.txt
             - OpenAI Key: keys/openai_key.txt
             Strictly enforces zero hardcoded keys across the codebase and
             provides environment synchronization and status verification.
================================================================================
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

# Root directory of the repository
BASE_DIR: Path = Path(__file__).resolve().parent.parent
KEYS_DIR: Path = BASE_DIR / "keys"

# Canonical file locations for separate keys
CLAUDE_KEY_PATHS: List[Path] = [
    KEYS_DIR / "claude_key.txt",
    KEYS_DIR / "claude.key",
    BASE_DIR / "CLAUDE_KEY.txt",
    BASE_DIR / "claude_key.txt",
]

CLAUDE_WORKSPACE_ID_PATHS: List[Path] = [
    KEYS_DIR / "claude_workspace_id.txt",
    KEYS_DIR / "anthropic_workspace_id.txt",
    BASE_DIR / "claude_workspace_id.txt",
    BASE_DIR / "anthropic_workspace_id.txt",
]

GEMINI_KEY_PATHS: List[Path] = [
    KEYS_DIR / "gemini_key.txt",
    KEYS_DIR / "gemini.key",
    BASE_DIR / "GEMINI_KEY.txt",
    BASE_DIR / "gemini_key.txt",
]

OPENAI_KEY_PATHS: List[Path] = [
    KEYS_DIR / "openai_key.txt",
    KEYS_DIR / "openai.key",
    BASE_DIR / "OPENAI_KEY.txt",
    BASE_DIR / "openai_key.txt",
]


def _read_key_from_file_paths(paths: List[Path]) -> Optional[str]:
    """
    ----------------------------------------------------------------------------
    Function: _read_key_from_file_paths
    ----------------------------------------------------------------------------
    Purpose:
        Iterates through candidate file paths, opens the first existing file,
        reads the key, strips whitespace/newlines/quotes, and returns the
        sanitized credential string.

    Parameters:
        paths (List[Path]): Ordered candidate file paths to search.

    Returns:
        Optional[str]: Sanitized key string if found and non-empty, else None.

    Errors Handled:
        - Catches FileNotFoundError, PermissionError, and general OSError safely
          without raising uncaught exceptions.

    Manual Debugging Notes:
        - Check that the target file does not contain accidental leading/trailing spaces.
        - Never log or print the returned key string in logs or console output.
    ----------------------------------------------------------------------------
    """
    for path in paths:
        try:
            if path.is_file():
                content = path.read_text(encoding="utf-8").strip()
                # Remove surrounding single or double quotes if present
                if (content.startswith('"') and content.endswith('"')) or (
                    content.startswith("'") and content.endswith("'")
                ):
                    content = content[1:-1].strip()
                if content:
                    return content
        except OSError:
            continue
    return None


def get_claude_key() -> Optional[str]:
    """
    ----------------------------------------------------------------------------
    Function: get_claude_key
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves the Anthropic Claude API key from its separate dedicated file
        (e.g., keys/claude_key.txt). If the file is not present, falls back to the
        ANTHROPIC_API_KEY environment variable.

    Parameters:
        None

    Returns:
        Optional[str]: Claude API key string, or None if not configured.

    Manual Debugging Notes:
        - Expected file: keys/claude_key.txt
        - Used by Agent 3 (Sutrakar Master Author) via AnthropicAdapter.
    ----------------------------------------------------------------------------
    """
    file_key = _read_key_from_file_paths(CLAUDE_KEY_PATHS)
    if file_key:
        return file_key
    return os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")


def get_claude_workspace_id() -> Optional[str]:
    """
    ----------------------------------------------------------------------------
    Function: get_claude_workspace_id
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves the Anthropic Workspace ID required when using Anthropic
        user-scoped API keys (sk-ant-usr-...). Searches dedicated files
        (e.g., keys/claude_workspace_id.txt) or ANTHROPIC_WORKSPACE_ID env var.

    Parameters:
        None

    Returns:
        Optional[str]: Workspace ID string (e.g. 'wrkspc_...'), or None.

    Manual Debugging Notes:
        - Anthropic enforces 'anthropic-workspace-id' header for User keys.
        - Place the ID in keys/claude_workspace_id.txt or export ANTHROPIC_WORKSPACE_ID.
    ----------------------------------------------------------------------------
    """
    file_ws = _read_key_from_file_paths(CLAUDE_WORKSPACE_ID_PATHS)
    if file_ws:
        return file_ws
    return os.getenv("ANTHROPIC_WORKSPACE_ID") or os.getenv("CLAUDE_WORKSPACE_ID")


def get_gemini_key() -> Optional[str]:
    """
    ----------------------------------------------------------------------------
    Function: get_gemini_key
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves the Google Gemini Pro API key from its separate dedicated file
        (e.g., keys/gemini_key.txt). If the file is not present, falls back to the
        GOOGLE_API_KEY or GEMINI_API_KEY environment variable.

    Parameters:
        None

    Returns:
        Optional[str]: Gemini API key string, or None if not configured.

    Manual Debugging Notes:
        - Expected file: keys/gemini_key.txt
        - Used by Agent 1 (Narada Specialist) via GeminiAdapter.
    ----------------------------------------------------------------------------
    """
    file_key = _read_key_from_file_paths(GEMINI_KEY_PATHS)
    if file_key:
        return file_key
    return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def get_openai_key() -> Optional[str]:
    """
    ----------------------------------------------------------------------------
    Function: get_openai_key
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves the OpenAI API key from its separate dedicated file
        (e.g., keys/openai_key.txt). If the file is not present, falls back to the
        OPENAI_API_KEY environment variable.

    Parameters:
        None

    Returns:
        Optional[str]: OpenAI API key string, or None if not configured.

    Manual Debugging Notes:
        - Expected file: keys/openai_key.txt
        - Used by Agent 2 (Shandilya Specialist) and Agent 4 (Validator).
    ----------------------------------------------------------------------------
    """
    file_key = _read_key_from_file_paths(OPENAI_KEY_PATHS)
    if file_key:
        return file_key
    return os.getenv("OPENAI_API_KEY")


def get_api_key_for_provider(provider: str) -> Optional[str]:
    """
    ----------------------------------------------------------------------------
    Function: get_api_key_for_provider
    ----------------------------------------------------------------------------
    Purpose:
        Generic provider dispatch function returning the appropriate API key
        read from its dedicated separate file.

    Parameters:
        provider (str): Provider identifier ('anthropic', 'claude', 'google',
                        'gemini', 'openai').

    Returns:
        Optional[str]: Resolved API key string.
    ----------------------------------------------------------------------------
    """
    norm = (provider or "").strip().lower()
    if norm in ("anthropic", "claude"):
        return get_claude_key()
    elif norm in ("google", "gemini", "google_vertexai"):
        return get_gemini_key()
    elif norm in ("openai", "chatgpt"):
        return get_openai_key()
    return None


def sync_keys_to_environment(override: bool = False) -> Dict[str, bool]:
    """
    ----------------------------------------------------------------------------
    Function: sync_keys_to_environment
    ----------------------------------------------------------------------------
    Purpose:
        Reads all keys from their separate dedicated files and injects them into
        os.environ (ANTHROPIC_API_KEY, GOOGLE_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY)
        so that underlying client SDKs (LangChain, official provider SDKs) can
        discover them without manual configuration.

    Parameters:
        override (bool): If True, overwrites existing non-empty env variables.
                         Defaults to False.

    Returns:
        Dict[str, bool]: Dictionary indicating which provider keys were synced.
    ----------------------------------------------------------------------------
    """
    results: Dict[str, bool] = {"claude": False, "gemini": False, "openai": False}

    c_key = get_claude_key()
    if c_key and (override or not os.getenv("ANTHROPIC_API_KEY")):
        os.environ["ANTHROPIC_API_KEY"] = c_key
        results["claude"] = True

    c_ws = get_claude_workspace_id()
    if c_ws and (override or not os.getenv("ANTHROPIC_WORKSPACE_ID")):
        os.environ["ANTHROPIC_WORKSPACE_ID"] = c_ws

    g_key = get_gemini_key()
    if g_key and (override or not os.getenv("GOOGLE_API_KEY")):
        os.environ["GOOGLE_API_KEY"] = g_key
        os.environ["GEMINI_API_KEY"] = g_key
        results["gemini"] = True

    o_key = get_openai_key()
    if o_key and (override or not os.getenv("OPENAI_API_KEY")):
        os.environ["OPENAI_API_KEY"] = o_key
        results["openai"] = True

    return results


def verify_keys_present() -> Dict[str, bool]:
    """
    ----------------------------------------------------------------------------
    Function: verify_keys_present
    ----------------------------------------------------------------------------
    Purpose:
        Inspects the separate key files on disk and returns a boolean status
        map indicating whether each file exists and contains a non-empty key,
        strictly without leaking or printing secret key contents.

    Parameters:
        None

    Returns:
        Dict[str, bool]: Status mapping {'claude': bool, 'gemini': bool, 'openai': bool}.
    ----------------------------------------------------------------------------
    """
    return {
        "claude": bool(get_claude_key()),
        "gemini": bool(get_gemini_key()),
        "openai": bool(get_openai_key()),
    }
