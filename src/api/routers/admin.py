"""
================================================================================
Module: src.api.routers.admin
Author: Hiranyam AI Labs (https://hiranyamai.com/)
Project: SK Sutras - by Shri Shripad Kulkarni
Description: FastAPI route handlers for Provider/Model configuration, Accessibility
             Engine settings (Senior Citizen 65+ Mode), and immutable audit logs.
================================================================================
"""

from typing import Any, Dict, List
from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.database.repository import ManuscriptRepository
from src.providers.registry import ProviderRegistry, get_provider_registry

router = APIRouter(prefix="/api/admin", tags=["System Administration & Accessibility"])


class ModelSwitchRequest(BaseModel):
    agent_role: str = Field(..., description="Role: 'narada_specialist', 'shandilya_specialist', 'sutrakar_master', 'independent_validator'")
    provider: str = Field(..., description="Provider: 'google', 'openai', 'anthropic'")
    model_id: str = Field(..., description="Exact model ID string")


class AccessibilitySettingsRequest(BaseModel):
    senior_mode_enabled: bool = Field(default=True, description="Enable Senior Citizen 65+ Mode")
    default_font_scale: str = Field(default="large", description="'standard', 'large', 'extra_large'")
    high_contrast_theme: bool = Field(default=True, description="Enable high contrast reading theme")


@router.get("/config", summary="Active Provider Model Allocations")
def get_provider_allocations() -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: get_provider_allocations
    ----------------------------------------------------------------------------
    Purpose:
        Returns current provider adapter and model assignments across all four agents.
    ----------------------------------------------------------------------------
    """
    registry = get_provider_registry()
    return {
        "allocations": {
            ProviderRegistry.ROLE_NARADA: {
                "provider": registry.get_adapter(ProviderRegistry.ROLE_NARADA).provider_name,
                "model_id": registry.get_adapter(ProviderRegistry.ROLE_NARADA).model_id,
            },
            ProviderRegistry.ROLE_SHANDILYA: {
                "provider": registry.get_adapter(ProviderRegistry.ROLE_SHANDILYA).provider_name,
                "model_id": registry.get_adapter(ProviderRegistry.ROLE_SHANDILYA).model_id,
            },
            ProviderRegistry.ROLE_SUTRAKAR: {
                "provider": registry.get_adapter(ProviderRegistry.ROLE_SUTRAKAR).provider_name,
                "model_id": registry.get_adapter(ProviderRegistry.ROLE_SUTRAKAR).model_id,
            },
            ProviderRegistry.ROLE_VALIDATOR: {
                "provider": registry.get_adapter(ProviderRegistry.ROLE_VALIDATOR).provider_name,
                "model_id": registry.get_adapter(ProviderRegistry.ROLE_VALIDATOR).model_id,
            },
        }
    }


@router.post("/config", summary="Dynamically Reallocate Agent Model")
def switch_agent_model(payload: ModelSwitchRequest) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: switch_agent_model
    ----------------------------------------------------------------------------
    Purpose:
        Reallocates the provider and model for an agent role at runtime without
        code modification.
    ----------------------------------------------------------------------------
    """
    registry = get_provider_registry()
    registry.switch_model(
        agent_role=payload.agent_role,
        provider=payload.provider,
        model_id=payload.model_id,
    )
    repo = ManuscriptRepository()
    repo.record_audit_log(
        user_email="admin",
        action="SWITCH_MODEL",
        entity_type="agent_configuration",
        entity_id=payload.agent_role,
        change_summary=f"Reassigned {payload.agent_role} to {payload.provider}:{payload.model_id}",
    )
    return {
        "status": "success",
        "message": f"Successfully switched {payload.agent_role} to {payload.provider}:{payload.model_id}.",
    }


@router.get("/settings", summary="Get Accessibility Preferences")
def get_accessibility_settings() -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: get_accessibility_settings
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves active Senior Citizen (65+ Mode) typography scaling and contrast presets.
    ----------------------------------------------------------------------------
    """
    repo = ManuscriptRepository()
    return {
        "senior_mode_enabled": repo.get_setting("senior_mode_enabled", "true") == "true",
        "default_font_scale": repo.get_setting("default_font_scale", "large"),
        "high_contrast_theme": repo.get_setting("high_contrast_theme", "true") == "true",
    }


@router.post("/settings", summary="Update Accessibility Preferences")
def update_accessibility_settings(payload: AccessibilitySettingsRequest) -> Dict[str, Any]:
    """
    ----------------------------------------------------------------------------
    Function: update_accessibility_settings
    ----------------------------------------------------------------------------
    Purpose:
        Persists updated Senior Citizen (65+ Mode) settings.
    ----------------------------------------------------------------------------
    """
    repo = ManuscriptRepository()
    repo.set_setting("senior_mode_enabled", "true" if payload.senior_mode_enabled else "false")
    repo.set_setting("default_font_scale", payload.default_font_scale)
    repo.set_setting("high_contrast_theme", "true" if payload.high_contrast_theme else "false")

    return {
        "status": "success",
        "message": "Accessibility preferences successfully updated.",
    }


@router.get("/audit", summary="Get Immutable Audit Logs")
def get_audit_trail() -> List[Dict[str, Any]]:
    """
    ----------------------------------------------------------------------------
    Function: get_audit_trail
    ----------------------------------------------------------------------------
    Purpose:
        Retrieves the immutable audit log recording editorial reviews, model switches,
        and system configuration changes.
    ----------------------------------------------------------------------------
    """
    repo = ManuscriptRepository()
    return repo.get_audit_logs(limit=100)
