# Safe Rollback Guide — SK Sutras Audit Remediation

**Document Identifier**: `REM-ROL-20261110-V1`  
**Project**: SK Sutras — by Shri Shripad Kulkarni  
**Organization**: Hiranyam AI Labs ([https://hiranyamai.com/](https://hiranyamai.com/))  
**Date**: November 10, 2026  
**Auditor & Remediation Lead**: Principal Software Architect & Senior Lead QA Engineer  

---

## 1. Overview

This document provides explicit, step-by-step procedures to revert any or all modifications introduced during the technical audit remediation program. Because all changes were executed under the **Zero-Mutation Protocol**, rolling back can be accomplished cleanly without risk of data loss.

---

## 2. Git Version Control Rollback

### Baseline State
- **Baseline Git Commit**: `f575126` (`fix(v0.7.4): remove all technical jargon from manuscript and resolve duplicate sutras 3, 4, 7`)
- **Current Branch**: `main`

### Complete Code Rollback to Baseline
To discard all uncommitted working directory modifications and return exactly to commit `f575126`:

```bash
cd "C:\Users\deshp\.gemini\antigravity\scratch\sk-sutras-by-shri-shripad-kulkarni"

# 1. Discard modified tracked files
git restore .

# 2. Clean newly created untracked test and script files (if desired)
git clean -fd
```

---

## 3. Targeted Component-by-Component Rollback

If only specific components need to be reverted:

### A. Revert Provider Adapter & Registry Changes
To revert `AnthropicAdapter`, `GeminiAdapter`, `OpenAIAdapter`, `ProviderRegistry`, and `base.py`:
```bash
git restore src/providers/
```

### B. Revert Validator Agent & Duplicate Detection
To revert `ValidatorAgent` to baseline:
```bash
git restore src/agents/validator_agent.py
```

### C. Revert Live Council Runner
To revert `scripts/run_dynamic_live_council.py`:
```bash
git restore scripts/run_dynamic_live_council.py
```

### D. Revert Source Registry Hashes
To revert `source_register.json` to its prior state:
```bash
git restore data/knowledge_repository/registry/source_register.json
```

### E. Revert Environment Variables (`.env`)
To revert `.env`:
```bash
git restore .env
```

---

## 4. Database Rollback Procedures

### Current Database State
- The live production database (`data/manuscript.db`) was **NEVER mutated** during this remediation session. It remains in its exact baseline state.
- Therefore, **no database rollback is required** for the current session.

### Post-Apply Database Rollback (If `--apply` is Executed in the Future)
Prior to running `scripts/sync_database_canonical_canon.py --apply`, an automated backup snapshot must always be taken:
```bash
# Automated Pre-Sync Snapshot Command
cp data/manuscript.db "data/backups/manuscript_pre_sync_$(date +%Y%m%d_%H%M%S).db"
```
To restore the database if needed:
```bash
cp "data/backups/manuscript_pre_sync_<TIMESTAMP>.db" data/manuscript.db
```

---

## 5. Verification Following Rollback

After performing any rollback, verify system state by running the standard unit test suite:
```bash
.venv\Scripts\pytest.exe tests/test_providers.py
```
Assert that all baseline tests pass.
