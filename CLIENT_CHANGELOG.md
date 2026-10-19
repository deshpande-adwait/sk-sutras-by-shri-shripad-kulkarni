# Client Change-Log: SK Sutras - by Shri Shripad Kulkarni

All notable changes, architectural updates, and releases for **SK Sutras - by Shri Shripad Kulkarni** are documented in this client-facing log.

---

## [v0.1.0-alpha] - 2026-10-19

### Executive Summary of Changes
Initial enterprise scaffolding and core architecture establishment for **SK Sutras - by Shri Shripad Kulkarni**, developed by Hiranyam AI Labs. This release sets up the multi-agent LangGraph orchestration pipeline, dynamic LLM provider abstraction, embedded ChromaDB vector store, SQLite relational persistence layer, WeasyPrint Devanagari typesetting engine, and a device-agnostic Streamlit manuscript review portal featuring an admin-configurable Senior Citizen (65+ Mode) accessibility engine.

### Direct Client/User Benefits & Features Added
* **Three Autonomous Specialist Agents Implemented**:
  * **NaradaAgent (`src/agents/narada_agent.py`)**: Represents Devarshi Narada's school of experiential, ecstatic Bhakti. Expounds verses into English, Hindi, and Marathi, and dispatches philosophical inquiries.
  * **ShandilyaAgent (`src/agents/shandilya_agent.py`)**: Represents Maharshi Shandilya's school of epistemological devotion. Interrogates its embedded ChromaDB vector store to discover semantically matching aphorisms and articulates analytical responses.
  * **SutrakarAgent (`src/agents/sutrakar_agent.py`)**: The master presiding coordinator that receives inputs from both agents, resolves the dialectic into the comparative *Udyoga Bhashya*, validates strict JSON schemas, persists to SQLite, and compiles the publication PDF.
* **Interactive Live Pipeline Demonstration (`run_pipeline.py`)**: End-to-end execution script showing the agents communicating step-by-step in the terminal.
* **Dynamic Multi-LLM Runtime Switching**: Full flexibility to toggle seamlessly between commercial LLM APIs (OpenAI `gpt-4o`, Anthropic `claude-3-5-sonnet`, Google `gemini-1.5-pro`) and local offline inference via Ollama (`qwen2.5`) through standardized environment configurations.
* **Device-Agnostic Manuscript Review Portal**: Responsive Streamlit portal designed for desktop, tablet, and mobile browsers with zero technical jargon.
* **Configurable Senior Citizen (65+ Mode) Accessibility Preset**: Enabled by default to provide large high-legibility typography, gentle high contrast, touch targets $\ge 48\times 48\,\text{px}$, and simplified card-based comparative review of Narada Bhakti Sutras and Shandilya Bhakti Sutras.
* **Relational & Vector Data Persistence**: Dual-tier storage ensuring zero data loss:
  * SQLite relational database for tracking manuscript pairs, review statuses, editorial bhashya, and reviewer annotations.
  * ChromaDB vector store for multilingual semantic mapping using `BAAI/bge-m3`.
* **High-Fidelity Devanagari PDF Typesetting**: Integrated WeasyPrint typesetting engine with embedded *Noto Serif Devanagari* font for print-ready manuscript publication.
* **Bi-Directional Human-in-the-Loop (HitL) Interrupt**: LangGraph DAG state machine pausing at human review checkpoints for scholar approval before synthesizing the final comparative *Udyoga Sutra*.

### Issues/Defects Resolved
* Fresh initialization: Addressed architectural requirement for 100% open-source local infrastructure while retaining enterprise LLM flexibility.
* Prevention of accessibility barriers for senior scholars through dedicated large-touch and high-contrast UI modes.
* Resolved Windows Devanagari terminal encoding by enforcing UTF-8 console output.

### Data/Knowledge Base Updates
* Initialized canonical raw schema for Narada Bhakti Sutra (84 sutras) and Shandilya Bhakti Sutra (100 sutras).
* Structured multilingual schema supporting English (`en`), Hindi (`hi`), and Marathi (`mr`).

### Validation & Test Results
* **Test Suite**: Automated `pytest` suite covering 16 test cases across schema, database, vector store, LangGraph DAG, accessibility, and 3-agent multi-agent communication.
* **Quality Gate**: Passed with 100% pass rate (16/16 tests passing).

### Deployment Details
* **Environment**: Local Staging / Test Environment (Workstation Instance).
* **Target Workstation Directory**: `C:\Users\deshp\.gemini\antigravity\scratch\sk-sutras-by-shri-shripad-kulkarni`
* **Release Status**: Initial Scaffolding Complete & Ready for Model Ingestion.
