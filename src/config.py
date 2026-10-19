"""
================================================================================
Module: src.config
Author: Hiranyam AI Labs
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Dynamic configuration management and flexible LLM abstraction engine.
             Provides runtime switching between proprietary APIs (OpenAI, Anthropic,
             Gemini) and local open-source inference (Ollama) using LangChain's
             `init_chat_model`.
================================================================================
"""

import os
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv

# Load environment configuration from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Root directory paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = BASE_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
OUTPUT_DIR: Path = DATA_DIR / "output" / "manuscripts"
CHROMA_DIR: Path = Path(os.getenv("CHROMA_PERSIST_DIRECTORY", str(DATA_DIR / "chroma_db")))
SQLITE_DB_PATH: Path = Path(os.getenv("SQLITE_DB_PATH", str(DATA_DIR / "manuscript.db")))

# Ensure necessary data directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# Dynamic LLM Provider Factory Function
# ==============================================================================

def get_chat_model(
    model: Optional[str] = None,
    model_provider: Optional[str] = None,
    temperature: float = 0.2,
    **kwargs: Any,
) -> Any:
    """
    ----------------------------------------------------------------------------
    Function: get_chat_model
    ----------------------------------------------------------------------------
    Purpose:
        Dynamically initializes and returns a flexible LangChain chat model
        instance using `langchain.chat_models.init_chat_model`. This enables
        seamless zero-code toggling between commercial proprietary APIs (OpenAI,
        Anthropic, Google Gemini) and local open-source models (Ollama).

    Parameters:
        model (Optional[str]):
            The specific model name/identifier (e.g. 'gpt-4o', 'claude-3-5-sonnet',
            'gemini-1.5-pro', or 'qwen2.5:latest'). Defaults to the LLM_MODEL env var.
        model_provider (Optional[str]):
            The provider name ('openai', 'anthropic', 'google_vertexai', 'ollama').
            Defaults to the LLM_PROVIDER env var.
        temperature (float):
            Sampling temperature for synthesis generation. Defaults to 0.2.
        **kwargs (Any):
            Additional provider-specific keyword arguments (e.g., base_url for Ollama).

    Returns:
        Any: An initialized LangChain BaseChatModel compatible instance.

    Exceptions / Errors:
        ValueError:
            Raised if neither parameters nor environment variables supply a valid
            model identifier or supported provider.
        ImportError:
            Raised if the underlying integration package for the requested provider
            is missing.

    Manual Debugging Notes:
        - When running offline with Ollama, verify that Ollama is listening at
          `http://localhost:11434` and that `LLM_PROVIDER=ollama` is set.
        - To test in isolation via python interactive shell:
          >>> from src.config import get_chat_model
          >>> llm = get_chat_model()
          >>> print(llm.invoke("Namaste").content)
    ----------------------------------------------------------------------------
    """
    resolved_provider: str = model_provider or os.getenv("LLM_PROVIDER", "openai").lower()
    resolved_model: str = model or os.getenv("LLM_MODEL", "gpt-4o")

    # Pass base_url for local Ollama instances if configured
    if resolved_provider == "ollama":
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        kwargs.setdefault("base_url", ollama_base_url)

    try:
        from langchain.chat_models import init_chat_model
        return init_chat_model(
            model=resolved_model,
            model_provider=resolved_provider,
            temperature=temperature,
            **kwargs,
        )
    except Exception as exc:
        # Fallback or detailed diagnostic error message
        raise RuntimeError(
            f"[Hiranyam AI LLM Factory Error] Failed to initialize chat model "
            f"'{resolved_model}' with provider '{resolved_provider}'. "
            f"Underlying error: {str(exc)}. Please verify your API keys and dependencies."
        ) from exc
