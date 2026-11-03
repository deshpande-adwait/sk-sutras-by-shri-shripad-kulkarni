-- =============================================================================
-- Migration: 001_initial_schema.sql
-- Description: Baseline schema migration for SK Sutras Four-Agent Platform
-- Author: Hiranyam AI Labs (https://hiranyamai.com/)
-- Target Database: PostgreSQL 14+
-- Safety: Enforces transactional DDL and idempotent creation.
-- =============================================================================

BEGIN;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Apply base entities
\ir ../postgres_schema.sql

-- Record initial migration metadata
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(50) PRIMARY KEY,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL
);

INSERT INTO schema_migrations (version, description)
VALUES ('001_initial_schema', 'Initial 4-agent scholarly schema, token metering, and author review tables')
ON CONFLICT (version) DO NOTHING;

COMMIT;
