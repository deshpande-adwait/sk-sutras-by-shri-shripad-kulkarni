# Security & Data Integrity Notes — SK Sutras Audit Remediation

**Document Identifier**: `REM-SEC-20261110-V1`  
**Project**: SK Sutras — by Shri Shripad Kulkarni  
**Organization**: Hiranyam AI Labs ([https://hiranyamai.com/](https://hiranyamai.com/))  
**Date**: November 10, 2026  
**Auditor & Remediation Lead**: Principal Software Architect & Senior Lead QA Engineer  

---

## 1. Zero Data Mutation Protocol

In strict adherence to the project's **Mandatory Data Preservation Protocol**:
- Under no circumstances was any production data modified, overwritten, or reset during remediation.
- The live SQLite database (`data/manuscript.db`) remained strictly in read-only inspection mode. All synchronization logic was tested exclusively on temporary mock databases initialized in pytest fixtures (`tmp_path`).
- Pre-flight dry-run inspection was executed with `--dry-run`, confirming 0 disk writes.

---

## 2. Credential Security & Governance

- **Zero Hardcoded Secrets**: All commercial AI provider keys (Google Gemini, OpenAI, Anthropic Claude) are sourced exclusively through environment variables and dedicated credential helper routines (`src/credentials.py`).
- **Windows Credential Manager Integration**: Project credentials and dedicated tokens are securely held in the Windows Credential Manager without plaintext persistence in git-tracked files.
- **Provider Authentication Safety**: Offline execution modes are enforced by default across tests, preventing accidental network egress or unintended credit consumption.

---

## 3. Cryptographic Source Integrity

To ensure that the classical foundations (Narada Bhakti Sutras, Shandilya Bhakti Sutras, and corporate manuscripts) cannot be silently tampered with or corrupted:
- `data/knowledge_repository/registry/source_register.json` was updated to replace placeholder strings with cryptographically verified SHA-256 hashes:
  - `DOC-01`: `3744e80343ed10bad6e873bf2082a2c94727a6429af9e0592556fedeb4d77523`
  - `DOC-02`: `c43eec51256d15436d74b860a90b7506ad63bf01502b2d77c89cfc75b6201a8d`
  - `DOC-03`: `9fc34f8206da810887039278b63397f99e2105abd9bf648785bb7ffccc5f79a7`
  - `DOC-04`: `46e0efea4647c0479c0afefb76693911a50981ed98f0e50416bab3e8126fbc77`
- Automated test `test_source_register_sha256_cryptographic_integrity` runs in the regression suite to continuously verify byte-level file integrity.

---

## 4. Audit Trail Preservation & Collision Prevention

In earlier iterations, the primary key of `live_api_execution_logs` was generated as a simple sequential counter (`LIVE_CALL_001`). When diagnostic or test runs were executed, they collided with and silently overwrote production records.
- **Remediation**: Call IDs are now explicitly scoped to the execution run:
  ```python
  call_id = f"{self.execution_id}_{self.call_counter:03d}"
  ```
- **Result**: Complete, tamper-evident audit history is preserved across all historical, diagnostic, and production runs without risk of primary key collisions.

---

## 5. Fail-Closed Architectural Policy

The remediation program identified and systematically purged all "fail-open" anti-patterns:
1. **Auto-Approve Purged**: Agent 5's validation fallback that previously returned `return True, 97` upon JSON parse failure was replaced with an affirmative rejection (`return False, 0, verdict="REJECTED"`).
2. **Duplicate Fallback Purged**: Agent 4's fallback dictionary returning `॥ उद्यमेन कार्यसिद्धिः ॥ {sutra_idx} ॥` was completely removed; parse errors now raise an explicit `RuntimeError`.
3. **Multi-Layer Duplicate Gate Enforced**: Gate 13 in `ValidatorAgent` runs algorithmic normalization and Levenshtein similarity analysis against all previously approved sutras, rejecting any candidate with similarity $\ge 0.85$.

---

## 6. Client Privacy & Presentation Standards

- **Zero Technical Jargon**: All technical schema references, AI evaluation scores, internal token counters, and prompt templates have been strictly removed from client-facing deliverables.
- **Mandatory Confidentiality Footer**: All client manuscript pages include the standardized footer:
  `"Proprietory and Confidential- Hiranyam AI Labs"`
- **Hyperlink Attribution**: Brand attribution text links directly to the official Hiranyam AI website: `https://hiranyamai.com/`.
