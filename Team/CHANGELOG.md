# Control-Room Changelog

This file records every significant change with real commit hashes.

---

- `f563020` — feat: complete Issue #22 verification, reinforce gate and record task 012 (Issue #22).
- `ee34e21` — chore(tools): set executable permissions on check_issue_protocol and probe (Issue #24).
- `edde816` — feat: complete Issue #24 verification, document task 011 and align paths (Issue #24).
- `260f97b` — chore: trigger gates after protocol backfill for issues #23 and #24.
- `ed157b8` — docs: add comprehensive onboarding guide and update living state (Issue #11)
- `4a04519` — docs: enrich onboarding guide with prompt patterns, lifecycle flow, and align README
- `6dbe29f` — feat(gates): enhance check_links gate, record task 004 and update living state (Issue #12)
- `87a85a8` — fix(hooks): mark .githooks/pre-push as executable (100755)
- `a7c6d43` — fix(hooks): remove UTF-8 BOM from .githooks/pre-push
- `e8b9e42` — fix: pass issue body/title via env vars - prevent bash backtick injection
- `39acafa` — Pipeline Execution Fix Verification (Issue #16): verified sequential execution mode; created Team/pipeline_test.md and task 005.
- `09e0e6e` — Status & Map Refresh (Issue #17): updated WHERE_WE_ARE.md and MAP.md.
- `01b27d5` — Switch project to Tehran City (Issue #18): updated MAP.md and WHERE_WE_ARE.md.
- `d01df33` — Analysis Methodology & Source Quality Gate (Issue #19): added cross-reference requirement to AGENTS.md, created check_source_quality.py.
- `bbf4237` — AGY double-trigger prevention: scoped issue_comment trigger, excluded bot comments.
- `7c9f22f` — AGY structured planning & reporting format: mandated STEP 0 checklist and final report in control-agy.yml.
- `9c0e385` — Audit and complete CHANGELOG for recent commits (Issue #20).
- `d1353eb` — Real-time checkbox tick via PATCH: added gh api PATCH instructions to prompt.
- `082296c` — Fix: replace gh CLI with curl+token in prompt (portable across agw-worker accounts).
- `b9f2d83` — Issue Response Protocol in AGENTS.md (Issue #23): added mandatory checklist + final report section.
- `040cde5` — New gate: check_issue_protocol.py (Issue #24): enforces checklist + Done report on @agy issues.
- `007d3f2` — Probe for check_issue_protocol gate (Issue #24).
- `ba56e78` — Wire check_issue_protocol into run_gates.py (Issue #24). Gate count: 5 -> 6.
- `edecf8f` — CHANGELOG: record d1353eb..ba56e78 (Issues #23, #24 completed directly).
- `c3e46d2` — Fix: remove bash command substitution patterns from prompt (prevent shell injection in agw-worker).
- `13fb629` — Fix: use heredoc for prompt (broken - YAML indentation issue).
- `7cb6354` — Fix: use printf with single-quoted static text - no heredoc YAML issues, no double-quote injection.
  - Root cause chain resolved: $(gh) -> $(curl) -> heredoc YAML break -> double-quote PROMPT injection.
  - Impact: AGY checklist + real-time ticking + final report fully operational.
- `6599040` — test: add hello_test.md and verify checklist & report format (Issue #25) [AGY commit].
- `a317416` — docs: add Persian summary report for Issue #25 [AGY commit].
- `c865d33` — refactor: move Team/hello_test.md to Team/tests/ (cleanup).
- `00bda18` — refactor: move Team/pipeline_test.md to Team/tests/ (cleanup).
- `464067c` — refactor: delete Team/hello_test.md (original, now in Team/tests/).
- `4487a58` — refactor: delete Team/pipeline_test.md (original, now in Team/tests/).
  - Impact: Team/ root is clean. All test artifacts live in Team/tests/.
