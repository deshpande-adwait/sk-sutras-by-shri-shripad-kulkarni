# SK Sutras - by Shri Shripad Kulkarni

[![Powered by Hiranyam AI Labs](https://img.shields.io/badge/Powered%20by-Hiranyam%20AI%20Labs-blue.svg)](https://hiranyamai.com/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT/OpenSource](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise NLP and computational Sanskrit comparative synthesis platform developed by **[Hiranyam AI Labs](https://hiranyamai.com/)**.

---

## 1. Project Overview

**SK Sutras - by Shri Shripad Kulkarni** employs an advanced multi-agent LangGraph orchestration pipeline to semantically map, compare, and synthesize two monumental texts of Indian philosophy:
1. **Narada Bhakti Sutra** (84 sutras)
2. **Shandilya Bhakti Sutra** (100 sutras)

The platform compiles an authoritative, multilingual comparative treatise titled **Udyoga Sutra**, providing Devanagari Sanskrit verses, verse-by-verse analyses (*vishleshan* in English, Hindi, and Marathi), and comprehensive philosophical syntheses (*Udyoga Bhashya*).

---

## 2. Core Architecture & Infrastructure

* **100% Free & Open-Source Core**:
  * **Database**: SQLite (ACID compliant local relational storage for review checkpoints and metadata)
  * **Vector Engine**: ChromaDB (Embedded local persistent vector store)
  * **Embeddings**: `BAAI/bge-m3` via FastEmbed / Hugging Face (Multilingual Devanagari & English)
  * **Review Portal**: Streamlit (Apache 2.0)
  * **Publication Engine**: WeasyPrint with Noto Serif Devanagari
* **Flexible LLM Provider Engine**:
  * Employs LangChain's `init_chat_model` to allow zero-code-change runtime switching across:
    * `openai:gpt-4o`
    * `anthropic:claude-3-5-sonnet`
    * `google_vertexai:gemini-1.5-pro`
    * `ollama:qwen2.5` (Offline local inference)

---

## 3. Human-Centric UI/UX & Senior Citizen (65+ Mode) Accessibility

The review portal is engineered to be completely device-agnostic (desktop, tablet, mobile) and incorporates a dedicated **Senior Citizen (65+ Mode)** accessibility preset:
* **Generous Touch Targets**: Minimum $48 \times 48\,\text{px}$ touch and click zones to accommodate varying motor precision.
* **Dynamic Font Scaling**: Instant enlargement to 18–24pt Devanagari and high-legibility English typography.
* **Fatigue-Free Contrast**: Soothing, high-contrast palette minimizing visual strain during prolonged review sessions.
* **Zero Technical Jargon**: Clean, dignified business language (*Live Manuscript Overview*, *Comparative Sutra Review*, *Approve Synthesis*).

---

## 4. Repository Layout

```
sk-sutras-by-shri-shripad-kulkarni/
├── CLIENT_CHANGELOG.md       # Client-facing release & validation history
├── README.md                 # System overview and deployment guide
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Build & package configuration
├── .env.example              # Environment variable template
├── data/
│   ├── raw/                  # Canonical Sanskrit source texts
│   └── output/manuscripts/   # Compiled JSON & PDF deliverables
├── src/
│   ├── config.py             # Provider configuration via init_chat_model
│   ├── database/             # SQLite repository & relational schema
│   ├── models/               # Pydantic schemas & LangGraph state definitions
│   ├── vectorstore/          # ChromaDB & multilingual embedding handlers
│   ├── orchestration/        # LangGraph DAG state machine with HitL interrupt
│   ├── pdf/                  # WeasyPrint Devanagari PDF generator
│   └── ui/                   # Streamlit Review Portal & Accessibility Engine
└── tests/                    # Comprehensive unit, integration & QA test suites
```

---

## 5. Quick Start & Setup

### Prerequisites
* Python 3.11 or higher
* Git

### Installation
```bash
# Clone the repository
git clone https://github.com/deshpande-adwait/sk-sutras-by-shri-shripad-kulkarni.git
cd sk-sutras-by-shri-shripad-kulkarni

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration
Copy `.env.example` to `.env` and configure your preferred provider:
```bash
cp .env.example .env
```

```ini
# Choose provider: openai, anthropic, google_vertexai, or ollama
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=your_key_here

# Or for local offline inference:
# LLM_PROVIDER=ollama
# LLM_MODEL=qwen2.5:latest
# OLLAMA_BASE_URL=http://localhost:11434
```

### Launch Review Portal
```bash
streamlit run src/ui/app.py
```

### Run Quality Assurance Test Suite
```bash
pytest tests/ -v
```

---

## 6. Governance & Attribution
Developed and maintained in accordance with the **Hiranyam AI Governance Standards**.  
Powered by **[Hiranyam AI Labs](https://hiranyamai.com/)**.
