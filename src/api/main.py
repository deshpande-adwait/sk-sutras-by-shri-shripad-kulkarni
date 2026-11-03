"""
================================================================================
Module: src.api.main
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: Main FastAPI REST Application Entry Point for the Four-Agent
             Authoring and Review Platform. Exposes manuscript review, central
             cost metering, administrative model reallocation, and accessibility.
================================================================================
"""

from typing import Any, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import admin, cost, manuscript

app = FastAPI(
    title="SK Sutras by Shri Shripad Kulkarni: Four-Agent Platform API",
    description=(
        "Scholarly API backend supporting the comparative study of Narada Bhakti Sutras "
        "(84 Aphorisms) and Shandilya Bhakti Sutras (100 Aphorisms), and the composition "
        "of the original contemporary Sanskrit Udyoga Sutras with Four-Agent AI assistance."
    ),
    version="1.0.0",
)

# CORS middleware for secure Author Portal web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular API routers
app.include_router(manuscript.router)
app.include_router(cost.router)
app.include_router(admin.router)


@app.get("/", summary="Platform Health & Provenance")
def root_status() -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: root_status
    ----------------------------------------------------------------------------
    Purpose:
        Returns platform health, versioning, author attribution, and Hiranyam AI
        attribution with official hyperlink.
    ----------------------------------------------------------------------------
    """
    return {
        "platform": "SK Sutras Four-Agent Authoring Platform",
        "author": "Shri Shripad Kulkarni",
        "technology_partner": "Hiranyam AI Labs",
        "website": "https://hiranyamai.com/",
        "status": "operational",
        "environment": "development_offline_verified",
        "agents": {
            "agent_1": "Narada Specialist (Google Gemini)",
            "agent_2": "Shandilya Specialist (OpenAI GPT-4o)",
            "agent_3": "Sutrakar Master Author (Anthropic Claude 3.5 Sonnet)",
            "agent_4": "Independent Validator (OpenAI GPT-4o)",
        },
    }
