-- =============================================================================
-- Database Schema: SK Sutras - by Shri Shripad Kulkarni
-- Author: Hiranyam AI Labs
-- Description: Robust relational schema for manuscript pair persistence,
--              Human-in-the-Loop review tracking, and accessibility configurations.
-- =============================================================================

-- 1. System Settings & Accessibility Preferences Table
CREATE TABLE IF NOT EXISTS system_settings (
    setting_key TEXT PRIMARY KEY,
    setting_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Comparative Sutra Pairs Manuscript Table
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

-- 3. Review History & Audit Trail Table
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

-- Optimize queries with indexes
CREATE INDEX IF NOT EXISTS idx_sutra_pairs_theme ON sutra_pairs(theme);
CREATE INDEX IF NOT EXISTS idx_sutra_pairs_status ON sutra_pairs(review_status);
CREATE INDEX IF NOT EXISTS idx_review_history_pair ON review_history(pair_id);

-- Initialize default system settings (Senior Citizen 65+ Mode enabled by default)
INSERT OR IGNORE INTO system_settings (setting_key, setting_value, description)
VALUES 
    ('senior_mode_enabled', 'true', 'Enable Senior Citizen (65+ Mode) accessibility features across portals'),
    ('default_font_scale', 'large', 'Default typography scaling: standard, large, extra_large'),
    ('high_contrast_theme', 'true', 'Default high-contrast, fatigue-free reading theme');
