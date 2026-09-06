# Changelog — Control-Room

Every commit modifying this repository must be recorded below with its short hash and impact summary.
Exempt: commits dedicated solely to recording the changelog (`changelog: record <hash>`).

---

### Inception — 2026-09-06

- `371278e`
  - **Initial commit:** Auto-initialized repository on GitHub.
  - **Impact:** Baseline `main` branch created for `mohammadlali0707-stack/Control-Room`.

- `1003f4d`
  - **Core Scaffolding:** Established AGENTS.md, Team/ coordination core, Tools/ gate suite, and GitHub Actions CI.
  - **Impact:** Control-Room is fully initialized with living documentation and mechanical verification rules.

- `373d29a`
  - **Scope Refinement:** Removed LifeOS references from workstream map and status records.
  - **Impact:** Aligned tracked project portfolios with current active focus.

- `b65e0e2`
  - **Gemini Issue Bot:** Integrated official `google-github-actions/run-gemini-cli` with an 8-account health-check pool and load balancing.
  - **Impact:** Enabled automated resolution of GitHub Issues tagged with `@gemini-cli` across 8 fallback accounts.

- `5dddedd`
  - **Live Model Quota Resolver:** Added live probing across candidate models (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-2.5-pro`) to ensure selection of an account and model with verified quota.
  - **Impact:** Fixed HTTP 429 limit:0 error caused by default model selection.

- `a504a4f`
  - **8-Tier Sequential Fallback:** Implemented native GitHub Actions fallback cascade across all 8 accounts with clean tree resets on quota limits.
  - **Impact:** Guarantees that if any account exhausts daily quota, the next account automatically takes over until execution succeeds.

- `a37f152`
  - **Model Schema Alignment:** Fixed `settings.json` model definition from string to object format `{"id": "gemini-2.5-flash"}` as required by `gemini-cli` v0.26+.
  - **Impact:** Resolves schema validator rejection `Error in: model. Expected object, received string`.

- `1d4dad2`
  - **Gemini Model Upgrade + Fallback Logic Fix:** Upgraded all 8 tiers from `gemini-2.5-flash` to `gemini-3.5-flash`; replaced broken `if: failure()` cascade with `continue-on-error: true` + outcome-based conditions.
  - **Impact:** Prevents all 8 tiers from firing simultaneously when Tier 1 succeeds.

- `699e633`
  - **Trigger Condition Fix:** Corrected broken `contains(A || B, '@gemini-cli')` expression by splitting into two separate `contains()` calls.
  - **Impact:** Bot now correctly triggers on both new issues and comments mentioning `@gemini-cli`.

- `e824308`
  - **GEMINI_MODEL Env Var:** Added `GEMINI_MODEL: gemini-3.5-flash` directly to `env:` block of all 8 tiers after discovering the `settings` JSON input was silently ignored by the action.
  - **Impact:** Ensures all accounts use `gemini-3.5-flash` instead of defaulting to `gemini-3.1-pro`.

- `16db43b`
  - **Round-Robin Batch Dispatch + Git Hooks:** Added `batch-dispatch.yml` (99-slot round-robin: 9 accounts x 11 runners, 5s stagger). Updated `control-agy.yml` to read `agy-acc:N` label for deterministic account selection. Initialized `Team/.agy-dispatch-state.json`. Added `.githooks/pre-push` (fail-hard gate enforcement, token-free, systematic).
  - **Impact:** Multiple AGY tasks dispatch in parallel with deterministic account assignment. Gates enforced before every push via git hook — no token cost.

- `f22c4b7`
  - **CHANGELOG Catch-up:** Recorded commits 1d4dad2, 699e633, e824308, e928bf2 that were missing from CHANGELOG.
  - **Impact:** check_changelog gate passes.

- `e928bf2`
  - **Switch to AGY:** Replaced broken `gemini-cli` bot with `control-agy.yml` using AGY CLI via cross-repo dispatch to `Mohammadlali/agw-workers`; deleted `control-gemini.yml`.
  - **Impact:** Bot no longer depends on Gemini API quota; uses 9 AGY OAuth tokens from the worker fleet instead.

- `91c843f`
  - **Workflow if-condition Fix:** Replaced `if: >-` multi-line block with single-line `${{ }}` format for the agy-bot job condition.
  - **Impact:** GitHub Actions parser correctly evaluates the condition; fixes workflow not triggering on issues.

- `39966bf`
  - **YAML Quote Fix:** Quoted `concurrency.group` value containing `${{ }}`; added `type: string` to workflow_dispatch input.
  - **Impact:** Fixes GitHub strict YAML parser rejecting the workflow (was showing file path instead of workflow name).

- `0a437d4`
  - **Full Workflow Rewrite:** Stripped all complex YAML constructs to fix persistent YAML parse error.
  - **Impact:** GitHub now correctly identifies and loads `Control-Room AGY Issue Bot` workflow.

- `1b9ac11`
  - **Bash-safe Prompt:** Replaced direct AGENTS.md embedding with a heredoc approach.
  - **Impact:** Avoided backtick command substitution crash from AGENTS.md content.

- `63e00fa`
  - **YAML Parse Fix (heredoc):** Replaced heredoc (content at column 0 was truncating `run: |` block) with indented `echo` commands inside a subshell redirect.
  - **Impact:** Eliminates the persistent YAML parse error; workflow now triggers on issues correctly.

- `5699d13`
  - **CHANGELOG Catch-up:** Recorded commits 91512c6, 1b9ac11, 63e00fa.
  - **Impact:** check_changelog gate passes.

- `1dcf383`
  - **Context-embedded Prompt:** Sanitizes and embeds AGENTS.md and WHERE_WE_ARE.md directly into AGY prompt. Instructs AGY not to clone or access external repos.
  - **Impact:** Eliminates 5-minute timeout caused by AGY attempting to clone Control-Room without credentials.

- `87657cc`
  - **Git Push Auth for AGY:** Added CONTROL_ROOM_PAT secret to Build prompt step so AGY receives authenticated git clone URL and can push commits back to Control-Room.
  - **Impact:** AGY can now make real code changes, commit, and push to main — not just read and report.

- `3d4b1e3`
  - **Status & Map Refresh (Issue #10):** Synchronized `WHERE_WE_ARE.md` and `MAP.md` with today's operational status, documenting the complete migration to AGY bot, active cross-repo dispatching, authenticated git push capabilities, and moved initial scaffolding task to done.
  - **Impact:** Living documentation accurately reflects current AGY capabilities and infrastructure state; zero information loss for incoming sessions.


