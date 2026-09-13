# Workstream Map — Control-Room

> **Target:** 600 lines | **Ceiling:** 900 lines
> When approaching ceiling, archive historical dated sections into `Team/MAP_ARCHIVE.md`.

---

## CURRENT STATE (Overview)

**2026-09-13 -- this repo (`mohammadlali0707-stack/Control-Room`, on `ACC6`)
is now the org's ONE canonical Control-Room, superseding the 2026-09-11
entry below.** Caught as a live discrepancy, not taken on a claim alone:
this repo's own git remote was already `mohammadlali0707-stack/Control-Room`;
`Mohammadlali/control-room` (ACC0) and this repo share an identical HEAD
(`de0143e6`), meaning ACC0 was being kept in sync FROM here, not the other
way around; and `agw-workers`' own `agw-worker.yml` already had no
checkout/push case for `Mohammadlali/Control-Room` at all -- only this
repo's path resolved to a real token. `control-agy.yml`'s dispatch
(`target_repo=`) and report-readback were pointing at the wrong (unreachable)
target and are fixed in the same change. Full evidence and what did/didn't
change: `Team/COMPANY_SCOPE.md`'s "What changed 2026-09-13". Unlike ACC0's
old arrangement, ACC6 is NOT management-only -- it hosts Control-Room and
TEHRAN: BLIND SPOT side by side; the old "management-only account"
invariant is retired, not reassigned (`Tools/check_company_scope.py`
updated to match).

**2026-09-11 (superseded above) -- this repo (`Mohammadlali/Control-Room`,
on `ACC0`) is now the org's ONE canonical Control-Room, owner's direct
instruction.** Until this date its own docs described themselves as
belonging to `ACC6`/`07` (`mohammadlali0707-stack`) -- a second, then
believed superseded Control-Room that lived there. Do not trust any
reference below this block that still says `Mohammadlali/Control-Room` or
`ACC0` as the current host -- read `Team/COMPANY_SCOPE.md` for the current,
correct account map instead of assuming this file's older rows are current.

**2026-09-12 -- `status-dashboard` is a 4th tracked project (ACC0), and
this repo + `status-dashboard` are TEMPORARILY PUBLIC** (ACC0's private-repo
Actions quota ran out; owner plans to re-privatize both in ~3 weeks). A
real fleet-dispatch bug (`ACC0_PAT`..`ACC8_PAT` secret names that don't
exist -- real names are bare `ACC0`..`ACC8`) and a real AGY-output public-log
leak were both found and fixed today, propagated to all 9 accounts, and
verified live end-to-end. See `Team/WHERE_WE_ARE.md` for the full account
and `Team/CHANGELOG.md` (commits `9783033`..`67652d5`, `0cdb146`,
`2a05299`) for the detailed record.

| Workstream | Status | Lead / Runner | Target Repo |
|------------|--------|---------------|-------------|
| 1. Control-Room Core & Gates | ACTIVE | Local / AGY Bot / MCP | `mohammadlali0707-stack/Control-Room` (this repo, on `ACC6`) |
| 2. Cloud Runner Workflows | OPERATIONAL | GitHub Actions / AGY | `mohammadlali0707-stack/agw-workers` + the other 8 accounts' `agw-workers` (all 9 public, unlimited minutes) |
| 3. Topic-based issue routing | ACTIVE, 4 projects | `Tools/route_topic.py` via `control-agy.yml` | this repo |
| 4. Project Integrations (TEHRAN: BLIND SPOT) | ACTIVE, hosted elsewhere | TBD | `mohammadlali0707-stack/Claud-Cloud-Project` (`ACC6`/`07`) -- the ONLY home for TBS as of 2026-09-11; Private |
| 5. Project Integrations (AirboxVIP Coffeenet) | ACTIVE, hosted elsewhere | TBD | `momonakikugava-pixel/AirboxVIP_Coffeenet` (`ACC1`/Momona); Private |
| 6. Status Dashboard | ACTIVE, TEMP PUBLIC | GitHub Actions + cron-job.org (no Claude dependency) | `mohammadlali0707-stack/status-dashboard` (`ACC6`, moved from `ACC0` 2026-09-13) -- `status.airboxvip.top`, behind Vercel SSO regardless of repo visibility |
| 7. AGY-output leak fix + fleet-dispatch secret-name fix | DONE 2026-09-12, verified live | AGY worker output now committed to target repo's `Reports/agy/`, read via Contents API; fleet secrets renamed | `agw-worker.yml` (all 9 accounts) + `control-agy.yml` (this repo) |
| 8. Chat-with-@agy on status-dashboard | IN PROGRESS (backend not started) | Serverless functions + issue-based dispatch | `status-dashboard` (frontend/API) + this repo (issue target) |

---

## 1. Control-Room Core & Governance
- **Scaffolding:** `AGENTS.md`, `Team/`, `Tools/` completed and operational.
- **Verification Gates (100% Green - 6 of 6):**
  - `check_changelog.py`: Enforces 100% commit record compliance.
  - `poll_tasks.py`: Validates task format and `falsifiable_by` existence.
  - `verify_claims.py`: Validates file reference integrity in reports.
  - `check_links.py`: Mechanically verifies internal document markdown links and paths.
  - `check_source_quality.py`: Verifies `Team/WHERE_WE_ARE.md` contains at least one git hash reference (Issue #19).
  - `check_issue_protocol.py`: Mechanically checks planning checklist and `**Done**` report presence on closed @agy issues (Issues #22, #24; reports `006`, `007`).
  - `run_gates.py`: Master runner with zero-token silent pass across all 6 gates.
- **Governance & Analysis Methodology:**
  - `AGENTS.md`: Added Analysis Methodology — Cross-Reference Requirement rules (Issue #19) and Issue Response Protocol (Issue #23).
- **Bot & Automation:**
  - `control-agy.yml`: AGY bot listening for `@agy` mentions on Issues and Issue comments.
  - All tasks routed and executed through AGY issues.
  - Issues 1 through 25 fully resolved and addressed.
  - Bash injection resolved: issue body/title passed safely via environment variables and static printf formatting (`7cb6354`).
  - Sequential execution mode active (`EXECUTION MODE: sequential`), eliminating timeouts and preventing background subagents/tasks (`2408d7a`, Issue #16).
  - Double-trigger prevention active: issue_comment trigger scoped to body only, excluding bot comments (`bbf4237`).
  - Structured execution lifecycle active: STEP 0 planning checklist, live PATCH updates, and comprehensive report structure with evidence and gate counts (`7c9f22f`, `d1353eb`).
  - Verification test completed: `Team/tests/hello_test.md` verified checklist and reporting format; Persian summary documented in `Team/reports/005_issue_25_persian_summary.md` (Issue #25).
  - MCP Integration: Full operational access to Control-Room repository.
  - Authenticated Git operations enabled via `CONTROL_ROOM_PAT` for direct main delivery.
  - `batch-dispatch.yml`: 99-slot round-robin batch dispatch across 9 accounts ready.
  - Pre-push git hook (`.githooks/pre-push`) for offline gate enforcement.
  - Comprehensive user & agent guide in `Team/START_HERE.md` (Issue #11).
  - Pipeline execution verification & sequential mode stabilization documented in `Team/tests/pipeline_test.md` (Issue #16).

---

## 2. Cloud Runners & Workers
- Integration with `agw-workers` for distributed background task execution.
- 99-slot batch dispatch ready (`.github/workflows/batch-dispatch.yml`).
- Task intake driven directly by AGY Issue bot triggers, now topic-routed
  first (see workstream 3 below) rather than always executed locally.

---

## 3. Topic-based issue routing (built 2026-09-11)
- `Tools/route_topic.py` classifies every incoming issue against
  `Team/company_scope.json`: label first (`project:tbs`, `project:
  airboxvip`, `project:control-room`), keyword match second, and refuses to
  guess when nothing or too much matches (`Tools/probe_route_topic.py`
  proves all three paths).
- `.github/workflows/control-agy.yml`'s "Route by topic" step runs this
  before the Ack comment, so the owner sees where an issue is headed
  immediately, not after a worker already ran on the wrong account.
- A non-local decision forwards the issue as a fresh `@agy` issue on the
  target project's own host repo, using that account's own PAT (never
  ACC0's), then closes the Control-Room copy with a link to where the real
  work is tracked.
- `Tools/check_company_scope.py` keeps `Team/COMPANY_SCOPE.md` (human) and
  `Team/company_scope.json` (machine) from silently drifting apart.

---

## 4. Project Integrations
- **TEHRAN: BLIND SPOT** -- hosted exclusively on `mohammadlali0707-stack/
  Claud-Cloud-Project` (`ACC6`/`07`) as of 2026-09-11. `ACC0`'s own former
  copy of this repo is retiring; any TBS change still made there because a
  live session is already open must be merged into `ACC6`'s copy
  immediately, not left to diverge.
- **AirboxVIP Coffeenet** -- hosted on `momonakikugava-pixel/
  AirboxVIP_Coffeenet` (`ACC1`/Momona).
- See `Team/COMPANY_SCOPE.md` for the full per-account scope table,
  including which accounts currently host no project of their own and only
  serve as TBS domain-ring workers.
