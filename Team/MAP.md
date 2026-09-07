# Workstream Map — Control-Room

> **Target:** 600 lines | **Ceiling:** 900 lines
> When approaching ceiling, archive historical dated sections into `Team/MAP_ARCHIVE.md`.

---

## CURRENT STATE (Overview)

| Workstream | Status | Lead / Runner | Target Repo |
|------------|--------|---------------|-------------|
| 1. Control-Room Core & Gates | ACTIVE | Local / AGY Bot / MCP | `mohammadlali0707-stack/Control-Room` |
| 2. Cloud Runner Workflows | OPERATIONAL | GitHub Actions / AGY | `mohammadlali0707-stack/agw-workers` |
| 3. Project Integrations (Tehran City) | ACTIVE | TBD | Account 1997 repo |

---

## 1. Control-Room Core & Governance
- **Scaffolding:** `AGENTS.md`, `Team/`, `Tools/` completed and operational.
- **Verification Gates (100% Green):**
  - `check_changelog.py`: Enforces 100% commit record compliance.
  - `poll_tasks.py`: Validates task format and `falsifiable_by` existence.
  - `verify_claims.py`: Validates file reference integrity in reports.
  - `check_links.py`: Added to suite; mechanically verifies internal document markdown links and paths.
  - `run_gates.py`: Master runner with zero-token silent pass.
- **Bot & Automation:**
  - `control-agy.yml`: AGY bot listening for `@agy` mentions on Issues and Issue comments.
  - All tasks routed and executed through AGY issues.
  - Issues 1 through 17 fully resolved and closed.
  - Bash injection resolved: issue body/title passed safely via environment variables (`e8b9e42`).
  - Sequential execution mode active (`EXECUTION MODE: sequential`), eliminating timeouts and preventing background subagents/tasks (`2408d7a`, Issue #16).
  - MCP Integration: Full operational access to Control-Room repository.
  - Authenticated Git operations enabled via `CONTROL_ROOM_PAT` for direct main delivery.
  - `batch-dispatch.yml`: 99-slot round-robin batch dispatch across 9 accounts ready.
  - Pre-push git hook (`.githooks/pre-push`) for offline gate enforcement.
  - Comprehensive user & agent guide in `Team/START_HERE.md` (Issue #11).
  - Pipeline execution verification & sequential mode stabilization documented in `Team/pipeline_test.md` (Issue #16).

---

## 2. Cloud Runners & Workers
- Integration with `agw-workers` for distributed background task execution.
- 99-slot batch dispatch ready (`.github/workflows/batch-dispatch.yml`).
- Task intake driven directly by AGY Issue bot triggers.

---

## 3. Project Integrations
- Tehran City (Game development project on Account 1997 repo)
