# Control-Room CHANGELOG

All commits must be recorded here. Exempt: commits dedicated solely to recording the changelog (`changelog: record <hash>`).

---

- `a37f152` — settings.json schema fix
- `1d4dad2` — Model Upgrade + Fallback Fix
- `699e633` — if-condition Fix
- `e824308` — GEMINI_MODEL Env Fix
- `e928bf2` — Switch to AGY bot
- `91c843f` — Workflow if-condition Fix
- `0a437d4` — Full Workflow Rewrite
- `1b9ac11` — Bash-safe Prompt
- `63e00fa` — YAML Parse Fix
- `1dcf383` — Context-embedded Prompt
- `87657cc` — Git Push Auth for AGY
- `3d4b1e3` — Status & Map Refresh (Issue #10)
- `16db43b` — Round-Robin Batch Dispatch + Git Hooks
- `92be0b1` — FAQ & Verification Report (Issue #11) by AGY Bot
- `e064c77` — check_links gate added (Issue #12)
- `2408d7a`
  - **EXECUTION MODE prompt fix:** Added explicit sequential-execution instructions to AGY prompt. Prevents AGY from spawning subagents/background tasks/timers that caused timeout on issues #12 and #13.
  - **Impact:** AGY now runs all steps synchronously within the 5-minute window. All tasks (simple and complex) go through AGY issues.
- `ed157b8` — docs: add comprehensive onboarding guide and update living state (Issue #11)
- `4a04519` — docs: enrich onboarding guide with prompt patterns, lifecycle flow, and align README
- `6dbe29f` — feat(gates): enhance check_links gate, record task 004 and update living state (Issue #12)
- `87a85a8` — fix(hooks): mark .githooks/pre-push as executable (100755)
- `a7c6d43` — fix(hooks): remove UTF-8 BOM from .githooks/pre-push
- `e8b9e42` — fix: pass issue body/title via env vars - prevent bash backtick injection
- `39acafa`
  - **Pipeline Execution Fix Verification (Issue #16):** Verified sequential execution mode without subagent/task timeouts; created `Team/pipeline_test.md` and task 005.
  - **Impact:** Confirms AGY bot pipeline executes cleanly and synchronously on GitHub Actions runner.
- `09e0e6e`
  - **Status & Map Refresh (Issue #17):** Updated `Team/WHERE_WE_ARE.md` and `Team/MAP.md` reflecting full AGY Issue Bot operational state, bash injection fix, sequential execution mode, verification gates suite, 99-slot batch dispatch, full MCP access, and closure of issues 1-16.
  - **Impact:** Keeps living documentation synchronized with the current system state.
