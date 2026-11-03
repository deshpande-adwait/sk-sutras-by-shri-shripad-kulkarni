"""
================================================================================
Test Module: tests.test_api
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: QA unit tests verifying the FastAPI backend endpoints offline without
             launching any live web server.
================================================================================
"""

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_api_root_endpoint():
    """Verifies that the root endpoint returns platform provenance and Hiranyam AI branding."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "SK Sutras Four-Agent Authoring Platform"
    assert data["author"] == "Shri Shripad Kulkarni"
    assert data["technology_partner"] == "Hiranyam AI Labs"
    assert data["website"] == "https://hiranyamai.com/"
    assert "agents" in data
    assert len(data["agents"]) == 4


def test_manuscript_dashboard_endpoint():
    """Verifies the dashboard returns canonical sutra counts (84 Narada, 100 Shandilya)."""
    response = client.get("/api/manuscript/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["canonical_narada_sutras_count"] == 84
    assert data["canonical_shandilya_sutras_count"] == 100
    assert "approved_for_publication_count" in data


def test_cost_summary_endpoint():
    """Verifies the four-agent cost telemetry endpoint."""
    response = client.get("/api/cost/summary")
    assert response.status_code == 200
    data = response.json()
    assert "by_agent" in data
    assert data["currency"] == "INR"


def test_admin_config_endpoint():
    """Verifies that admin config lists all four agent role allocations."""
    response = client.get("/api/admin/config")
    assert response.status_code == 200
    data = response.json()
    allocations = data["allocations"]
    assert "narada_specialist" in allocations
    assert "shandilya_specialist" in allocations
    assert "sutrakar_master" in allocations
    assert "independent_validator" in allocations


def test_admin_accessibility_settings_endpoint():
    """Verifies updating Senior Citizen 65+ Mode settings."""
    payload = {
        "senior_mode_enabled": True,
        "default_font_scale": "extra_large",
        "high_contrast_theme": True,
    }
    response = client.post("/api/admin/settings", json=payload)
    assert response.status_code == 200

    get_resp = client.get("/api/admin/settings")
    assert get_resp.status_code == 200
    settings = get_resp.json()
    assert settings["senior_mode_enabled"] is True
    assert settings["default_font_scale"] == "extra_large"
