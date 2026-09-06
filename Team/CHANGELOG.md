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

- `e928bf2`
  - **Switch to AGY:** Replaced broken `gemini-cli` bot with `control-agy.yml` using AGY CLI via cross-repo dispatch to `Mohammadlali/agw-workers`; deleted `control-gemini.yml`.
  - **Impact:** Bot no longer depends on Gemini API quota; uses 9 AGY OAuth tokens from the worker fleet instead.

- `f22c4b7`
  - **CHANGELOG Catch-up:** Recorded commits 1d4dad2, 699e633, e824308, e928bf2 that were missing from CHANGELOG.
  - **Impact:** check_changelog gate passes.

- `91c843f`
  - **Workflow if-condition Fix:** Replaced `if: >-` multi-line block with single-line `${{ }}` format for the agy-bot job condition.
  - **Impact:** GitHub Actions parser correctly evaluates the condition; fixes workflow not triggering on issues.

- `39966bf`
  - **YAML Quote Fix:** Quoted `concurrency.group` value containing `${{ }}`; added `type: string` to workflow_dispatch input.
  - **Impact:** Fixes GitHub strict YAML parser rejecting the workflow (was showing file path instead of workflow name).

