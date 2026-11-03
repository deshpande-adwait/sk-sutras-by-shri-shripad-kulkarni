-- =============================================================================
-- Production Database Schema: PostgreSQL
-- Author: Hiranyam AI Labs (https://hiranyamai.com/)
-- Project: SK Sutras - by Shri Shripad Kulkarni
-- Description: Comprehensive relational PostgreSQL schema for scholarly Sanskrit
--              sutra research, four-agent authoring, validation audit trails,
--              manuscript versioning, central token metering, and author governance.
-- Standards: Strict Hiranyam AI Guidelines, ACID transactions, data persistence.
-- Note: DEVELOPMENT ONLY - Schema definition; DO NOT apply to live production.
-- =============================================================================

-- Enable UUID extension for globally unique IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------------------------------
-- 1. Security & Role-Based Access Control (RBAC)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'viewer', -- 'author', 'scholar', 'admin', 'viewer'
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    senior_citizen_mode BOOLEAN NOT NULL DEFAULT TRUE, -- Default 65+ Mode
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    role VARCHAR(50) NOT NULL,
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'read', 'write', 'approve', 'admin'
    UNIQUE(role, resource, action)
);

-- -----------------------------------------------------------------------------
-- 2. Authenticated Source Texts (Narada 84 & Shandilya 100 Sutras)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS source_texts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tradition VARCHAR(50) NOT NULL, -- 'narada', 'shandilya'
    sutra_no VARCHAR(20) NOT NULL,  -- '1', '2', ..., '84' or '100'
    sanskrit_text TEXT NOT NULL,
    transliteration TEXT,
    edition_provenance TEXT NOT NULL,
    publisher_source TEXT,
    translation_en TEXT NOT NULL,
    translation_hi TEXT,
    translation_mr TEXT,
    traditional_commentary TEXT,
    verification_status VARCHAR(50) NOT NULL DEFAULT 'authenticated',
    ingestion_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tradition, sutra_no)
);

-- -----------------------------------------------------------------------------
-- 3. Candidate Relationships & Arbitration
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS candidate_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_code VARCHAR(100) UNIQUE NOT NULL,
    narada_sutra_id UUID NOT NULL REFERENCES source_texts(id) ON DELETE RESTRICT,
    shandilya_sutra_id UUID NOT NULL REFERENCES source_texts(id) ON DELETE RESTRICT,
    semantic_similarity NUMERIC(6, 4),
    agent1_rationale TEXT,
    agent2_critique TEXT,
    arbitration_verdict VARCHAR(50) NOT NULL, -- 'strong_defensible', 'complementary', 'qualified', 'weak_forced', 'rejected'
    rejection_rationale TEXT,
    is_accepted BOOLEAN NOT NULL DEFAULT FALSE,
    arbitrated_by VARCHAR(100) NOT NULL DEFAULT 'Agent 3 Sutrakar',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 4. Manuscript Units (Sections A through F) with Full Versioning
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS manuscript_units (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unit_id VARCHAR(100) NOT NULL, -- e.g., 'UDYOGA-SUTRA-001'
    version_number INTEGER NOT NULL DEFAULT 1,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    parent_version_id UUID REFERENCES manuscript_units(id),
    candidate_relationship_id UUID REFERENCES candidate_relationships(id),
    
    -- Chapter & Metadata
    chapter_number INTEGER NOT NULL DEFAULT 1,
    sutra_number VARCHAR(20) NOT NULL,
    theme VARCHAR(255) NOT NULL,
    central_principle TEXT NOT NULL,
    composition_label VARCHAR(100) NOT NULL DEFAULT 'Original contemporary composition',
    
    -- Section A: Source Foundation
    narada_sutra_ref VARCHAR(100) NOT NULL,
    narada_sanskrit TEXT NOT NULL,
    shandilya_sutra_ref VARCHAR(100) NOT NULL,
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
    chandas_name VARCHAR(100) NOT NULL DEFAULT 'Anushtubh',
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
    validation_status VARCHAR(50) NOT NULL DEFAULT 'PENDING_VALIDATION', -- 'PASS', 'FAIL', 'NEEDS_REVISION', 'HUMAN_REVIEW_REQUIRED'
    approval_status VARCHAR(50) NOT NULL DEFAULT 'PENDING_REVIEW', -- 'PENDING_REVIEW', 'APPROVED', 'REJECTED', 'REVISION_REQUESTED', 'SCHOLAR_REVIEW', 'ON_HOLD'
    approved_by VARCHAR(255),
    approved_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(unit_id, version_number)
);

-- -----------------------------------------------------------------------------
-- 5. Validation Reports & Issue Tracking (Agent 4 Independent Validator)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS validation_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    manuscript_unit_id UUID NOT NULL REFERENCES manuscript_units(id) ON DELETE CASCADE,
    execution_id VARCHAR(100) NOT NULL,
    validator_model_id VARCHAR(100) NOT NULL,
    overall_status VARCHAR(50) NOT NULL, -- 'PASS', 'FAIL', 'NEEDS_REVISION', 'HUMAN_REVIEW_REQUIRED'
    revision_cycle INTEGER NOT NULL DEFAULT 0,
    
    -- Distinct Scholarly Gates
    source_authenticity_check VARCHAR(50) NOT NULL,
    philosophical_integrity_check VARCHAR(50) NOT NULL,
    sanskrit_grammar_check VARCHAR(50) NOT NULL,
    chandas_metre_check VARCHAR(50) NOT NULL,
    translations_check VARCHAR(50) NOT NULL,
    commentary_check VARCHAR(50) NOT NULL,
    originality_repetition_check VARCHAR(50) NOT NULL,
    
    -- Specific Findings & Revision Directives
    findings_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    critical_issues_count INTEGER NOT NULL DEFAULT 0,
    major_issues_count INTEGER NOT NULL DEFAULT 0,
    minor_issues_count INTEGER NOT NULL DEFAULT 0,
    required_corrections TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 6. Author Editorial Reviews & Human-in-the-Loop Decisions
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS author_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    manuscript_unit_id UUID NOT NULL REFERENCES manuscript_units(id) ON DELETE CASCADE,
    reviewer_name VARCHAR(255) NOT NULL DEFAULT 'Shri Shripad Kulkarni',
    action VARCHAR(50) NOT NULL, -- 'APPROVE', 'REJECT', 'REQUEST_REVISION', 'SCHOLAR_REFERRAL', 'HOLD'
    editorial_comments TEXT,
    scholar_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 7. Agent Executions & Prompt Configurations
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS provider_model_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider VARCHAR(50) NOT NULL, -- 'google', 'openai', 'anthropic'
    model_id VARCHAR(100) NOT NULL,
    agent_role VARCHAR(100) NOT NULL, -- 'narada_specialist', 'shandilya_specialist', 'sutrakar_master', 'independent_validator'
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    temperature NUMERIC(3, 2) NOT NULL DEFAULT 0.20,
    max_tokens INTEGER NOT NULL DEFAULT 4096,
    supports_caching BOOLEAN NOT NULL DEFAULT FALSE,
    supports_batch BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prompt_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_role VARCHAR(100) NOT NULL,
    version_tag VARCHAR(50) NOT NULL,
    system_prompt TEXT NOT NULL,
    user_prompt_template TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_id VARCHAR(100) UNIQUE NOT NULL,
    workflow_id VARCHAR(100) NOT NULL,
    agent_role VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    prompt_version_tag VARCHAR(50),
    manuscript_unit_id UUID REFERENCES manuscript_units(id),
    status VARCHAR(50) NOT NULL, -- 'success', 'failed', 'retrying', 'budget_blocked'
    duration_ms INTEGER,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 8. Central Four-Model Token Metering & Cost Accounting
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS price_catalog (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider VARCHAR(50) NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    input_price_per_m NUMERIC(10, 4) NOT NULL,      -- in USD
    output_price_per_m NUMERIC(10, 4) NOT NULL,     -- in USD
    cache_read_price_per_m NUMERIC(10, 4),          -- in USD
    cache_write_price_per_m NUMERIC(10, 4),         -- in USD
    batch_input_price_per_m NUMERIC(10, 4),         -- in USD
    batch_output_price_per_m NUMERIC(10, 4),        -- in USD
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    official_source_url TEXT NOT NULL,
    effective_date DATE NOT NULL,
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, model_id)
);

CREATE TABLE IF NOT EXISTS token_usage_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idempotency_key VARCHAR(150) UNIQUE NOT NULL,
    provider VARCHAR(50) NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    agent_role VARCHAR(100) NOT NULL,
    workflow_id VARCHAR(100) NOT NULL,
    manuscript_unit_id VARCHAR(100),
    execution_id VARCHAR(100) NOT NULL,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    is_revision BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Token metrics
    input_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    cached_input_tokens INTEGER NOT NULL DEFAULT 0,
    cache_write_tokens INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    
    -- Cost metrics
    billing_currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    estimated_cost_usd NUMERIC(10, 6) NOT NULL DEFAULT 0.0,
    actual_cost_usd NUMERIC(10, 6),
    exchange_rate_inr NUMERIC(10, 4) NOT NULL DEFAULT 83.50,
    cost_inr NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    
    call_status VARCHAR(50) NOT NULL DEFAULT 'success',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS budget_configurations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scope_type VARCHAR(50) NOT NULL, -- 'project_monthly', 'provider', 'model', 'agent'
    scope_name VARCHAR(100) NOT NULL, -- 'sk_sutras_total', 'google', 'openai', 'anthropic', 'Agent 3 Sutrakar'
    monthly_limit_inr NUMERIC(12, 2) NOT NULL,
    current_spent_inr NUMERIC(12, 2) NOT NULL DEFAULT 0.0,
    reserved_inr NUMERIC(12, 2) NOT NULL DEFAULT 0.0,
    alert_50_fired BOOLEAN NOT NULL DEFAULT FALSE,
    alert_75_fired BOOLEAN NOT NULL DEFAULT FALSE,
    alert_90_fired BOOLEAN NOT NULL DEFAULT FALSE,
    hard_stop_active BOOLEAN NOT NULL DEFAULT FALSE,
    reset_day_of_month INTEGER NOT NULL DEFAULT 1,
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Kolkata',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scope_type, scope_name)
);

CREATE TABLE IF NOT EXISTS budget_alert_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    budget_id UUID NOT NULL REFERENCES budget_configurations(id) ON DELETE CASCADE,
    threshold_percent INTEGER NOT NULL, -- 50, 75, 90, 100
    alert_message TEXT NOT NULL,
    spent_at_trigger NUMERIC(12, 2) NOT NULL,
    recipient_email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS budget_overrides (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    budget_id UUID NOT NULL REFERENCES budget_configurations(id),
    authorized_by VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    override_amount_inr NUMERIC(12, 2) NOT NULL,
    valid_until TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 9. Cache Metadata & Batch Job Management
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS prompt_cache_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    provider VARCHAR(50) NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    prompt_hash VARCHAR(64) NOT NULL,
    tokens_cached INTEGER NOT NULL DEFAULT 0,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    hit_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_hit_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS batch_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider_batch_id VARCHAR(255) UNIQUE NOT NULL,
    provider VARCHAR(50) NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'submitted', -- 'submitted', 'validating', 'in_progress', 'completed', 'failed', 'cancelled'
    total_requests INTEGER NOT NULL DEFAULT 0,
    completed_requests INTEGER NOT NULL DEFAULT 0,
    failed_requests INTEGER NOT NULL DEFAULT 0,
    input_file_uri TEXT,
    output_file_uri TEXT,
    cost_inr NUMERIC(10, 4) DEFAULT 0.0,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- -----------------------------------------------------------------------------
-- 10. Immutable Audit Trails
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    user_email VARCHAR(255) NOT NULL DEFAULT 'system',
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(100) NOT NULL,
    change_summary TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance and high-throughput scholarly lookup
CREATE INDEX IF NOT EXISTS idx_source_texts_tradition_no ON source_texts(tradition, sutra_no);
CREATE INDEX IF NOT EXISTS idx_manuscript_units_unit_id ON manuscript_units(unit_id);
CREATE INDEX IF NOT EXISTS idx_manuscript_units_approval ON manuscript_units(approval_status);
CREATE INDEX IF NOT EXISTS idx_manuscript_units_validation ON manuscript_units(validation_status);
CREATE INDEX IF NOT EXISTS idx_token_usage_provider ON token_usage_records(provider);
CREATE INDEX IF NOT EXISTS idx_token_usage_agent ON token_usage_records(agent_role);
CREATE INDEX IF NOT EXISTS idx_token_usage_workflow ON token_usage_records(workflow_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
