# Workstream Map — Control-Room

> **Target:** 600 lines | **Ceiling:** 900 lines
> When approaching ceiling, archive historical dated sections into `Team/MAP_ARCHIVE.md`.

---

## CURRENT STATE (Overview)

| Workstream | Status | Lead / Runner | Target Repo |
|------------|--------|---------------|-------------|
| 1. Control-Room Core & Gates | ACTIVE | Local / Antigravity | `mohammadlali0707-stack/Control-Room` |
| 2. Cloud Runner Workflows | READY | GitHub Actions | `mohammadlali0707-stack/agw-workers` |
| 3. Project Portfolios (AirboxVIP) | PENDING INTEGRATION | TBD | Account 07 Repos |

---

## 1. Control-Room Core & Governance
- **Scaffolding:** `AGENTS.md`, `Team/`, `Tools/` completed.
- **Verification Gates:**
  - `check_changelog.py`: Enforces 100% commit record compliance.
  - `poll_tasks.py`: Validates task format and `falsifiable_by` existence.
  - `verify_claims.py`: Validates file reference integrity in reports.
  - `run_gates.py`: Master runner with zero-token silent pass.

---

## 2. Cloud Runners & Workers
- Integration with `agw-workers` for distributed background task execution.
- Task dispatching mechanism: tasks committed to `Team/tasks/pending/` trigger worker evaluation.

---

## 3. Project Integrations
- AirboxVIP_Coffeenet: Telegram bot service management and content generation jobs.

