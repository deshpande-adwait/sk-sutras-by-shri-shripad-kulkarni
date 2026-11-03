-- =============================================================================
-- Database Schema: SQLite (Development, Testing & Offline Operations)
-- Author: Hiranyam AI Labs (https://hiranyamai.com/)
-- Project: SK Sutras - by Shri Shripad Kulkarni
-- Description: Comprehensive relational SQLite schema supporting 4-agent
--              manuscript units, Agent 4 validation reports, central token
--              metering, budget enforcement, and author governance.
-- =============================================================================

-- 1. System Settings & Accessibility Preferences Table
CREATE TABLE IF NOT EXISTS system_settings (
    setting_key TEXT PRIMARY KEY,
    setting_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Legacy/Simple Comparative Sutra Pairs Manuscript Table (Maintained for backward compatibility)
CREATE TABLE IF NOT EXISTS sutra_pairs (
    pair_id TEXT PRIMARY KEY,
    theme TEXT NOT NULL,
    
    -- Narada Bhakti Sutra Component
    narada_sutra_no TEXT NOT NULL,
    narada_sanskrit TEXT NOT NULL,
    narada_vishleshan_en TEXT NOT NULL,
    narada_vishleshan_hi TEXT,
    narada_vishleshan_mr TEXT,
    
    -- Shandilya Bhakti Sutra Component
    shandilya_sutra_no TEXT NOT NULL,
    shandilya_sanskrit TEXT NOT NULL,
    shandilya_vishleshan_en TEXT NOT NULL,
    shandilya_vishleshan_hi TEXT,
    shandilya_vishleshan_mr TEXT,
    
    -- Synthesized Udyoga Bhashya Component
    udyoga_bhashya_en TEXT NOT NULL,
    udyoga_bhashya_hi TEXT,
    udyoga_bhashya_mr TEXT,
    
    -- Human Review & Workflow Status
    review_status TEXT NOT NULL DEFAULT 'pending_review',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Review History & Audit Trail Table (Maintained for backward compatibility)
CREATE TABLE IF NOT EXISTS review_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pair_id TEXT NOT NULL,
    reviewer_name TEXT NOT NULL,
    action TEXT NOT NULL,
    notes TEXT,
    previous_bhashya_en TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pair_id) REFERENCES sutra_pairs(pair_id) ON DELETE CASCADE
);

-- 4. Complete Manuscript Units Table (Sections A through F with Versioning)
CREATE TABLE IF NOT EXISTS manuscript_units (
    id TEXT PRIMARY KEY,
    unit_id TEXT NOT NULL,
    version_number INTEGER NOT NULL DEFAULT 1,
    is_current INTEGER NOT NULL DEFAULT 1,
    parent_version_id TEXT,
    
    -- Chapter & Identification
    chapter_number INTEGER NOT NULL DEFAULT 1,
    sutra_number TEXT NOT NULL,
    theme TEXT NOT NULL,
    central_principle TEXT NOT NULL,
    composition_label TEXT NOT NULL DEFAULT 'Original contemporary composition',
    
    -- Section A: Source Foundation
    narada_sutra_ref TEXT NOT NULL,
    narada_sanskrit TEXT NOT NULL,
    shandilya_sutra_ref TEXT NOT NULL,
    shandilya_sanskrit TEXT NOT NULL,
    philosophical_relationship TEXT NOT NULL,
    selection_justification TEXT NOT NULL,
    
    -- Section B: New Udyoga Sutra
    original_sanskrit_verse TEXT NOT NULL,
    intended_meaning TEXT NOT NULL,
    
    -- Section C: Sanskrit Scholarly Analysis
    padaccheda TEXT NOT NULL,
    anvaya TEXT NOT NULL,
    word_meanings TEXT NOT NULL,
    grammatical_explanation TEXT NOT NULL,
    sandhi_analysis TEXT,
    dhatu_derivation TEXT,
    chandas_name TEXT NOT NULL DEFAULT 'Anushtubh',
    chandas_analysis TEXT NOT NULL,
    
    -- Section D: Multilingual Translations
    translation_en TEXT NOT NULL,
    translation_hi TEXT NOT NULL,
    translation_mr TEXT NOT NULL,
    
    -- Section E: Four-Fold Commentary
    nirukta TEXT NOT NULL,
    vyavahara_dharma TEXT NOT NULL,
    lokasangraha TEXT NOT NULL,
    modern_leadership_synthesis TEXT NOT NULL,
    
    -- Section F: Additional Info & Governance
    philosophical_significance TEXT,
    contemporary_examples TEXT,
    limitations_notes TEXT,
    cross_references TEXT,
    
    -- Governance Statuses
    validation_status TEXT NOT NULL DEFAULT 'PENDING_VALIDATION',
    approval_status TEXT NOT NULL DEFAULT 'PENDING_REVIEW',
    approved_by TEXT,
    approved_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(unit_id, version_number)
);

-- 5. Agent 4 Validation Reports
CREATE TABLE IF NOT EXISTS validation_reports (
    id TEXT PRIMARY KEY,
    manuscript_unit_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    validator_model_id TEXT NOT NULL,
    overall_status TEXT NOT NULL, -- 'PASS', 'FAIL', 'NEEDS_REVISION', 'HUMAN_REVIEW_REQUIRED'
    revision_cycle INTEGER NOT NULL DEFAULT 0,
    
    source_authenticity_check TEXT NOT NULL,
    philosophical_integrity_check TEXT NOT NULL,
    sanskrit_grammar_check TEXT NOT NULL,
    chandas_metre_check TEXT NOT NULL,
    translations_check TEXT NOT NULL,
    commentary_check TEXT NOT NULL,
    originality_repetition_check TEXT NOT NULL,
    
    findings_json TEXT NOT NULL DEFAULT '[]',
    critical_issues_count INTEGER NOT NULL DEFAULT 0,
    major_issues_count INTEGER NOT NULL DEFAULT 0,
    minor_issues_count INTEGER NOT NULL DEFAULT 0,
    required_corrections TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manuscript_unit_id) REFERENCES manuscript_units(id) ON DELETE CASCADE
);

-- 6. Token Usage & Cost Metering Table
CREATE TABLE IF NOT EXISTS token_usage_records (
    id TEXT PRIMARY KEY,
    idempotency_key TEXT UNIQUE NOT NULL,
    provider TEXT NOT NULL,
    model_id TEXT NOT NULL,
    agent_role TEXT NOT NULL,
    workflow_id TEXT NOT NULL,
    manuscript_unit_id TEXT,
    execution_id TEXT NOT NULL,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    is_revision INTEGER NOT NULL DEFAULT 0,
    
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    cached_input_tokens INTEGER NOT NULL DEFAULT 0,
    cache_write_tokens INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    
    billing_currency TEXT NOT NULL DEFAULT 'USD',
    estimated_cost_usd REAL NOT NULL DEFAULT 0.0,
    actual_cost_usd REAL,
    exchange_rate_inr REAL NOT NULL DEFAULT 83.50,
    cost_inr REAL NOT NULL DEFAULT 0.0,
    
    call_status TEXT NOT NULL DEFAULT 'success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Budget Configurations & Limits Table
CREATE TABLE IF NOT EXISTS budget_configurations (
    id TEXT PRIMARY KEY,
    scope_type TEXT NOT NULL, -- 'project_monthly', 'provider', 'model', 'agent'
    scope_name TEXT NOT NULL,
    monthly_limit_inr REAL NOT NULL,
    current_spent_inr REAL NOT NULL DEFAULT 0.0,
    reserved_inr REAL NOT NULL DEFAULT 0.0,
    alert_50_fired INTEGER NOT NULL DEFAULT 0,
    alert_75_fired INTEGER NOT NULL DEFAULT 0,
    alert_90_fired INTEGER NOT NULL DEFAULT 0,
    hard_stop_active INTEGER NOT NULL DEFAULT 0,
    reset_day_of_month INTEGER NOT NULL DEFAULT 1,
    timezone TEXT NOT NULL DEFAULT 'Asia/Kolkata',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scope_type, scope_name)
);

-- 8. Budget Alert Audit Logs
CREATE TABLE IF NOT EXISTS budget_alert_logs (
    id TEXT PRIMARY KEY,
    budget_id TEXT NOT NULL,
    threshold_percent INTEGER NOT NULL,
    alert_message TEXT NOT NULL,
    spent_at_trigger REAL NOT NULL,
    recipient_email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (budget_id) REFERENCES budget_configurations(id) ON DELETE CASCADE
);

-- 9. System Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL DEFAULT 'system',
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    change_summary TEXT NOT NULL,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_sutra_pairs_theme ON sutra_pairs(theme);
CREATE INDEX IF NOT EXISTS idx_sutra_pairs_status ON sutra_pairs(review_status);
CREATE INDEX IF NOT EXISTS idx_review_history_pair ON review_history(pair_id);
CREATE INDEX IF NOT EXISTS idx_manuscript_units_uid ON manuscript_units(unit_id);
CREATE INDEX IF NOT EXISTS idx_manuscript_units_appr ON manuscript_units(approval_status);
CREATE INDEX IF NOT EXISTS idx_token_usage_agent ON token_usage_records(agent_role);
CREATE INDEX IF NOT EXISTS idx_token_usage_provider ON token_usage_records(provider);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);

-- Default system settings (Senior Citizen 65+ Mode enabled by default)
INSERT OR IGNORE INTO system_settings (setting_key, setting_value, description)
VALUES 
    ('senior_mode_enabled', 'true', 'Enable Senior Citizen (65+ Mode) accessibility features across portals'),
    ('default_font_scale', 'large', 'Default typography scaling: standard, large, extra_large'),
    ('high_contrast_theme', 'true', 'Default high-contrast, fatigue-free reading theme');
