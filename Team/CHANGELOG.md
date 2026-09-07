# Control-Room CHANGELOG

All commits must be recorded here. Exempt: commits dedicated solely to recording the changelog (`changelog: record <hash>`).

---

- `a37f152`
  - **settings.json schema fix:** Aligned `model` field to object format `{id: ...}` as required by AGY CLI.
  - **Impact:** Bot can now successfully call the Gemini API without schema validation errors.

- `1d4dad2`
  - **Model Upgrade + Fallback Fix:** Upgraded to `gemini-3.5-flash`; rewrote fallback logic using `continue-on-error: true` and `if: steps.X.outcome == 'failure'` pattern.
  - **Impact:** Eliminates the "model not found" 404 error; fallback now correctly triggers when primary step fails.

- `699e633`
  - **if-condition Fix:** Split `contains()` calls into separate OR clauses to fix GitHub Actions expression parser rejecting comma-separated arguments.
  - **Impact:** Workflow now correctly triggers on issues and issue comments containing `@gemini-cli`.

- `e824308`
  - **GEMINI_MODEL Env Fix:** Set model via `GEMINI_MODEL=gemini-3.5-flash` environment variable instead of `settings.json` (which is ignored by the action).
  - **Impact:** Correct model is now used without relying on config file parsing.

- `e928bf2`
  - **Switch to AGY:** Replaced broken `gemini-cli` bot with `control-agy.yml` using AGY CLI via cross-repo dispatch to `Mohammadlali/agw-workers`; deleted `control-gemini.yml`.
  - **Impact:** Functional AI bot infrastructure using AGY Pro accounts with OAuth tokens.

- `91c843f`
  - **Workflow if-condition Fix:** Replaced `if: >-` multi-line block with single-line `${{ }}` format for the agy-bot job condition.
  - **Impact:** GitHub Actions parser correctly evaluates the condition.

- `0a437d4`
  - **Full Workflow Rewrite:** Stripped all complex YAML constructs to fix persistent YAML parse error.
  - **Impact:** GitHub now correctly identifies and loads `Control-Room AGY Issue Bot` workflow.

- `1b9ac11`
  - **Bash-safe Prompt:** Replaced direct AGENTS.md embedding with a heredoc approach.
  - **Impact:** Avoided backtick command substitution crash from AGENTS.md content.

- `63e00fa`
  - **YAML Parse Fix (heredoc):** Replaced heredoc with indented `echo` commands inside a subshell redirect.
  - **Impact:** Eliminates the persistent YAML parse error; workflow now triggers on issues correctly.

- `1dcf383`
  - **Context-embedded Prompt:** Sanitizes and embeds AGENTS.md and WHERE_WE_ARE.md directly into AGY prompt.
  - **Impact:** Eliminates 5-minute timeout caused by AGY attempting to clone Control-Room without credentials.

- `87657cc`
  - **Git Push Auth for AGY:** Added CONTROL_ROOM_PAT secret to Build prompt step so AGY receives authenticated git clone URL and can push commits back to Control-Room.
  - **Impact:** AGY can now make real code changes, commit, and push to main.

- `3d4b1e3`
  - **Status & Map Refresh (Issue #10):** Synchronized `WHERE_WE_ARE.md` and `MAP.md` with today's operational status.
  - **Impact:** Living documentation accurately reflects current AGY capabilities and infrastructure state.

- `16db43b`
  - **Round-Robin Batch Dispatch + Git Hooks:** Added `batch-dispatch.yml` (99-slot round-robin: 9 accounts x 11 runners, 5s stagger). Updated `control-agy.yml` to read `agy-acc:N` label. Initialized `Team/.agy-dispatch-state.json`. Added `.githooks/pre-push` (fail-hard gate enforcement).
  - **Impact:** Multiple AGY tasks dispatch in parallel with deterministic account assignment. Gates enforced before every push via git hook.

- `ed157b8`
  - **Onboarding Guide & Living State Refresh (Issue #11):** Expanded `Team/START_HERE.md` with comprehensive repository overview, AGY bot invocation patterns, batch-dispatch architecture, task authoring rules, and synchronized `WHERE_WE_ARE.md` and `MAP.md` with current round-robin and hook infrastructure; added task 003.
  - **Impact:** Users and incoming agents have an immediate, actionable guide on navigating and commanding Control-Room and dispatching jobs to AGY; living state reflects all operational mechanisms.

- `4a04519`
  - **Onboarding Guide Enrichment & Architecture Alignment (Issue #11):** Added practical prompt patterns, verification gates philosophy (Silent Pass, No Claim Without a Probe), and end-to-end request lifecycle diagram to `Team/START_HERE.md`; updated `README.md` architecture to reflect all active workflows (`control-agy.yml`, `batch-dispatch.yml`, `control-gates.yml`) and Persian onboarding links; initialized `Team/tasks/pending/.gitkeep`.
  - **Impact:** Provides operators and developers with actionable templates to immediately assign tasks to AGY Bot; aligns documentation tree with actual repo infrastructure.

- `92be0b1`
  - **FAQ & Verification Report (Issue #11):** AGY added FAQ reference and empirical verification report.
  - **Impact:** Documentation enriched with empirical evidence of AGY capabilities.

- `e064c77`
  - **check_links gate (Issue #12):** Added `Tools/check_links.py` — scans all .md files for broken internal file links (skips external URLs to avoid non-deterministic failures). Registered in `run_gates.py` as fourth gate.
  - **Impact:** Broken internal links now caught automatically before every push.

- `6dbe29f`
  - **check_links gate enhancement & verification (Issue #12):** Hardened `Tools/check_links.py` to support link titles, ignore code blocks, handle root-relative links, and unquote URLs. Added task 004 in `Team/tasks/done/` and empirical verification report `Team/reports/004_issue_12_verification.md`. Restored missing CHANGELOG commits `ed157b8` and `4a04519`.
  - **Impact:** Robust documentation link verification gate protects against broken internal references; all verification gates pass silently with zero token consumption.
