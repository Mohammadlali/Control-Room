# Control-Room Changelog

This file records every significant change with real commit hashes.

---

- `e29a713` — feat: document empirical verification report 007 for task 011 and update touches (Issue #24).
- `b2019ca` — fix: tighten trigger - require @agy at START of body, not just anywhere in text.
- `395be99` — feat(tools): harden check_issue_protocol against missing gh and clean imports (Issue #24).
- `d454802` — feat(tools): add token fallback for gh authentication in check_issue_protocol (Issue #24).
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
- `6d4f8c9` - feat: add control-agy-context.yml - context responder for commit and discussion comments.
  - Triggers on commit_comment and discussion_comment events.
  - CASE A: reads context, answers Q in-place. CASE B: creates issue with @agy for action requests.
- `e124e66` - test: minimal commit_comment workflow to diagnose context responder trigger issue.
- `15d5520` - test: remove minimal test workflow (cleanup).
- `0058fae` - test: ultra-minimal commit_comment workflow (diagnostic).
- `25522ed` - test: remove test (cleanup).
- `7f6e20a` - test: workflow_dispatch only to verify naming (diagnostic).
- `f63a404` - test: dispatch+commit_comment combo (diagnostic).
- `a647b1d` - test: commit_comment without types filter (diagnostic).
- `86f2b83` - test: discussion_comment only (confirmed working).
- `d886225` - test: cleanup test workflow files.
- `f0e0fe6` - fix: replace multi-line Python with jq in context responder - fix YAML indentation parse error.
- `4ade397` - fix: re-register context responder now that Discussions is enabled.
- `b2019ca` - fix: tighten trigger - require startsWith('@agy') not contains.
- `8f82004` - fix: remove commit_comment (unsupported in this repo), keep discussion_comment only.
  - Renamed to: Control-Room AGY Discussion Responder.
  - Discussion tab now supported: post @agy comment in any Discussion to trigger AGY.
- `0776697` - fix: workflow posts AGY output to Discussion directly via GraphQL (no longer relies on AGY to call APIs).
- `70b638f` - fix: remove double-quotes from prompt instructions - prevented bash parse error in agw-worker when prompt was injected via DOLLAR{{inputs.prompt}}.
- `3810d40` - feat: add Tools/check_workflow_safety.py - static analysis gate 7 (no AI tokens, agent-agnostic). Checks: double-quotes in printf content, Python YAML indentation, YAML syntax.
- `de38a36` - feat: add .githooks/pre-commit - runs check_workflow_safety before each commit.
- `4781d62` - feat: add Tools/install_hooks.sh - one-command hook activation.
- `3c065b7` - feat: register check_workflow_safety as gate 7 in run_gates.py.
- `8cecf54` - fix: check_workflow_safety - exclude tr/sed lines from printf double-quote check (false positive fix).
- `353554f` - docs: add Team/SECURITY_RULES.md (agent-agnostic GitHub Actions
  security). Recorded retroactively by the ACC0-hosted Control-Room rebuild
  session -- this entry was missing, which is what made `check_changelog.py`
  the first red gate encountered while adopting this repo as the canonical,
  central Control-Room (see the same session's entries below for why).

- `35cc8ae` — feat: rebuild this repo's identity as the org's ONE canonical
  Control-Room, hosted on `ACC0`/`Mohammadlali` (owner's direct instruction,
  2026-09-11). README.md, AGENTS.md, MAP.md and WHERE_WE_ARE.md no longer
  describe this repo as belonging to `07`/`mohammadlali0707-stack` -- that
  was a second, now-superseded Control-Room, being deleted separately (see
  the next entry below for that attempt's outcome). Added
  `Team/COMPANY_SCOPE.md` + `Team/company_scope.json`: which of ACC0-ACC8
  hosts which project (TBS only on ACC6, AirboxVIP only on ACC1, ACC0
  management-only, the rest currently TBS ring-workers with no project of
  their own). Added `Tools/route_topic.py` (deterministic label-then-
  keyword classifier, refuses to guess on a tie or an unknown label),
  `Tools/probe_route_topic.py` (7 cases, all pass), and
  `Tools/check_company_scope.py` (keeps the .md and .json twins from
  drifting apart) -- wired into `Tools/run_gates.py` as gates 9-10.
  Rewrote `.github/workflows/control-agy.yml`: a new "Route by topic" step
  runs before the Ack comment; a Control-Room-topic issue dispatches
  exactly as before (round-robin across ACC0-ACC8's own `agw-workers`), a
  recognized other-project issue is forwarded as a fresh `@agy` issue on
  that project's own host repo using that account's own PAT and the
  Control-Room copy is closed with a link, and an unclear topic gets a
  comment asking for a `project:` label instead of any dispatch at all.
  Also fixed two pre-existing gate failures found while rebuilding this:
  a missing CHANGELOG entry for `353554f`, and two `CHECK-1` (double-quote
  in printf content) violations in the old control-agy.yml prompt text.
  Impact: any issue opened on Control-Room from now on either stays here
  or lands on the correct project's own repo automatically -- it no longer
  matters which account happened to win the old `ISSUE_NUM % 9` round-robin
  for a TBS or AirboxVIP question.

- `a450f8d` — chore: remove a committed __pycache__ file from the
  previous commit and add .gitignore so it cannot happen again.

- `5240f99` -- `Team/START_HERE.md`: owner caught a leftover mistake from the 2026-09-11 identity rebuild -- this file's own "what is Control-Room" section still said it belonged to `07`/`mohammadlali0707-stack` (the deleted duplicate), missed while README.md/AGENTS.md/MAP.md/WHERE_WE_ARE.md were fixed the same day. Corrected with an explicit note pointing at the mistake, not a silent edit, and added a line on the topic router since this is the file's own "what is Control-Room" answer.
