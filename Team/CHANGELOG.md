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




