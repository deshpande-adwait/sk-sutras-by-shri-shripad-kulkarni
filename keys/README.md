# LLM Provider Key Storage

This directory holds the separate, individual API key credential files for the three LLM providers utilized in the **SK Sutras** platform:

1. `claude_key.txt`: Dedicated Anthropic Claude API key for Agent 3 (Sutrakar Master Author).
2. `gemini_key.txt`: Dedicated Google Gemini Pro API key for Agent 1 (Narada Specialist).
3. `openai_key.txt`: Dedicated OpenAI GPT-4o API key for Agent 2 (Shandilya Specialist) and Agent 4 (Independent Validator).

The application reads each key independently from its dedicated file via `src/credentials.py` without hardcoding.
