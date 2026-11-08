"""
Diagnostic script to inspect Gemini models and Anthropic workspace requirements.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import httpx

from src.credentials import get_claude_key, get_gemini_key


def probe_gemini():
    key = get_gemini_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(url)
            print("Gemini ListModels status:", resp.status_code)
            if resp.status_code == 200:
                models = [m.get("name") for m in resp.json().get("models", [])]
                print("Available Gemini models (first 10):", models[:10])
            else:
                print("Gemini ListModels error:", resp.text[:300])
                
                # Also test v1 endpoint
                url_v1 = f"https://generativelanguage.googleapis.com/v1/models?key={key}"
                resp_v1 = client.get(url_v1)
                print("Gemini v1 ListModels status:", resp_v1.status_code)
                if resp_v1.status_code == 200:
                    models_v1 = [m.get("name") for m in resp_v1.json().get("models", [])]
                    print("Available Gemini v1 models:", models_v1[:10])
                else:
                    print("Gemini v1 ListModels error:", resp_v1.text[:300])
    except Exception as e:
        print("Gemini probe exception:", e)


def probe_anthropic():
    key = get_claude_key()
    # Try calling /v1/organizations or /v1/workspaces to see workspace IDs
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(
                "https://api.anthropic.com/v1/organizations",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01"}
            )
            print("Anthropic /v1/organizations status:", resp.status_code, resp.text[:300])
    except Exception as e:
        print("Anthropic probe exception:", e)


if __name__ == "__main__":
    print("PROBING GEMINI...")
    probe_gemini()
    print("\nPROBING ANTHROPIC...")
    probe_anthropic()
