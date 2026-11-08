"""
================================================================================
Script: scripts/diagnostic_api_test.py
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - Phase 1 Safe Diagnostic API Connectivity Test
Description: Performs small, isolated diagnostic REST API connectivity checks
             for Anthropic Claude, OpenAI, and Google Gemini using the keys
             present in keys/*.
             Does NOT expose full keys. Does NOT execute any research or generation.
================================================================================
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import httpx

from src.credentials import get_claude_key, get_gemini_key, get_openai_key


def mask_key(k: str) -> str:
    if not k:
        return "NONE"
    if len(k) <= 12:
        return k[:3] + "..." + k[-3:]
    return k[:6] + "..." + k[-4:]


def test_openai() -> dict:
    key = get_openai_key()
    if not key:
        return {"status": "FAIL", "reason": "OpenAI API key missing in keys/openai_key.txt"}
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5
    }
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"].strip()
                return {
                    "status": "PASS",
                    "status_code": 200,
                    "model": data.get("model", "gpt-4o"),
                    "response": content,
                    "usage": data.get("usage", {}),
                    "key_masked": mask_key(key)
                }
            else:
                return {
                    "status": "FAIL",
                    "status_code": resp.status_code,
                    "error": resp.text[:300],
                    "key_masked": mask_key(key)
                }
    except Exception as e:
        return {"status": "ERROR", "error": str(e), "key_masked": mask_key(key)}


def test_claude() -> dict:
    key = get_claude_key()
    if not key:
        return {"status": "FAIL", "reason": "Claude API key missing in keys/claude_key.txt"}
    
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5
    }
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                content = data["content"][0]["text"].strip()
                return {
                    "status": "PASS",
                    "status_code": 200,
                    "model": data.get("model", "claude-3-5-sonnet-20241022"),
                    "response": content,
                    "usage": data.get("usage", {}),
                    "key_masked": mask_key(key)
                }
            else:
                return {
                    "status": "FAIL",
                    "status_code": resp.status_code,
                    "error": resp.text[:300],
                    "key_masked": mask_key(key)
                }
    except Exception as e:
        return {"status": "ERROR", "error": str(e), "key_masked": mask_key(key)}


def test_gemini() -> dict:
    key = get_gemini_key()
    if not key:
        return {"status": "FAIL", "reason": "Gemini API key missing in keys/gemini_key.txt"}

    # Attempt 1: Standard Google AI Studio API key via query parameter
    url_query = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": "ping"}]}],
        "generationConfig": {"maxOutputTokens": 5}
    }
    
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url_query, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                text = candidates[0]["content"]["parts"][0]["text"].strip() if candidates else ""
                return {
                    "status": "PASS",
                    "auth_method": "query_param_key",
                    "status_code": 200,
                    "response": text,
                    "usage": data.get("usageMetadata", {}),
                    "key_masked": mask_key(key)
                }
            else:
                err_text = resp.text
                
                # Attempt 2: If query param fails, attempt Bearer token header
                resp_bearer = client.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent",
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json=payload
                )
                if resp_bearer.status_code == 200:
                    data = resp_bearer.json()
                    candidates = data.get("candidates", [])
                    text = candidates[0]["content"]["parts"][0]["text"].strip() if candidates else ""
                    return {
                        "status": "PASS",
                        "auth_method": "bearer_header",
                        "status_code": 200,
                        "response": text,
                        "usage": data.get("usageMetadata", {}),
                        "key_masked": mask_key(key)
                    }
                
                return {
                    "status": "FAIL",
                    "query_status_code": resp.status_code,
                    "query_error": err_text[:300],
                    "bearer_status_code": resp_bearer.status_code,
                    "bearer_error": resp_bearer.text[:300],
                    "key_masked": mask_key(key)
                }
    except Exception as e:
        return {"status": "ERROR", "error": str(e), "key_masked": mask_key(key)}


if __name__ == "__main__":
    print("--- TESTING OPENAI ---")
    o_res = test_openai()
    print(json.dumps(o_res, indent=2))

    print("\n--- TESTING ANTHROPIC CLAUDE ---")
    c_res = test_claude()
    print(json.dumps(c_res, indent=2))

    print("\n--- TESTING GOOGLE GEMINI ---")
    g_res = test_gemini()
    print(json.dumps(g_res, indent=2))
