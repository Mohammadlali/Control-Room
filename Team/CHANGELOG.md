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

- `bfec08d` -- `Team/CROSS_ACCOUNT_LESSONS.md`: committed a leftover file from the 2026-09-11 `NEW_SESSION_PROMPT.md` split (issue tracked as this repo's task #4) that was created locally in an earlier session but never staged or pushed -- found sitting untracked in this checkout while starting unrelated work. Content unchanged from what was already ported: the cross-account dispatch mechanism, the delegation policy, and the trust-nothing-without-a-second-read lessons, exactly as `Claud-Cloud-Project/Team/NEW_SESSION_PROMPT.md` already points readers here for.

- `fbbfc78` -- `.github/workflows/fix-gate-retirement-on-acc6.yml` (new): applies the already locally-verified `check_status_feed_freshness` gate retirement to ACC6, the live repo where this gate actually still executes (`Claud-Cloud-Project` on ACC0 committed the identical fix as `3b90c1c` but is a confirmed-deleted, permanently-orphaned remote -- see that repo's own CHANGELOG). Clones ACC6 with `secrets.ACC6`, applies three base64-embedded Python patches (`Team/MAP.md`'s CURRENT STATE block + gate list, `Team/NEW_SESSION_PROMPT.md`'s mirrored gate list, `Tools/verify_claims.py`'s new `RETIRED_2026_09_12` exemption set) each guarded by an exact-match assertion against the real current content (dry-run verified byte-for-byte against a saved copy of ACC6's actual files before this workflow was written), deletes the two retired tool files, regenerates `Team/RULES.md`, runs `check_handover.py`/`verify_claims.py --all`/`check_rules_index.py` before AND after two commits (placeholder-then-real-hash, this project's own convention), and finally dispatches and watches ACC6's own `tbs-gates.yml` for a genuine in-repo verification rather than trusting the ad hoc clone's file-level checks alone. Base64 used only because GitHub Actions' `run:` block is a YAML literal block scalar that cannot hold a heredoc'd Python file at column 0 (breaks the block's indentation contract) -- not because the content itself needs hiding; confirmed no literal `${{` appears in any of the three embedded scripts, so this is a formatting workaround, not the earlier `${{ secrets.X }}`-survival case `migrate-statusfeed-to-status-dashboard.yml` needed base64 for. Not yet dispatched as of this commit.

- `5e4d85a` -- `.github/workflows/check-status-dashboard-schedule.yml` (new): owner asked, mid-way through the gate-retirement work, that `status-dashboard`'s whole deploy/update process run automatically without needing a Claude session involved (a `@agy`-run pipeline if it needs one at all) -- i.e. confirm task #16 (the `*/5 * * * *` cron in `deploy-status-feed.yml`) is genuinely firing on its own, not just present in the YAML. Lists the last 20 real runs of `deploy-status-feed.yml` on `Mohammadlali/status-dashboard` (timestamps, trigger event, conclusion) via `secrets.ACC0`, plus re-reads the live workflow file's own `on:` block to confirm the schedule expression actually deployed matches what was intended. Read-only, no writes.

- `b4cac98` -- `.github/workflows/setup-cron-job-org-dispatch.yml` (new): fixes the unreliable-schedule finding from `check-status-dashboard-schedule.yml` (real gaps of 2-4.5h between `deploy-status-feed.yml`'s supposedly-every-5-minutes scheduled runs -- GitHub Actions' own `schedule:` trigger does not honor sub-15-minute crons reliably, undocumented SLA, worse under load). Owner chose an external pinger (`cron-job.org`) over a self-built Cloudflare Worker, added its API key as `secrets.AgentWorkflowGHCron`, and created a new fine-grained PAT scoped ONLY to `status-dashboard`'s Actions (read/write) as `secrets.STATUS_DASHBOARD_DISPATCH_PAT` specifically so the third-party service never holds a broad-scope credential. This workflow: (1) sanity-checks the PAT by actually dispatching a real `deploy-status-feed.yml` run before doing anything else (fail fast, not a guess), (2) checks cron-job.org's own `GET /jobs` for an existing job targeting the same dispatch URL so re-running this workflow is idempotent rather than creating duplicate jobs (which would double the fire rate), (3) if none exists, creates one via `PUT /jobs` with `schedule.minutes=[0,5,10,...,55]` (UTC) and the PAT embedded only in that one job's own request headers, (4) re-fetches and prints the job's real definition as proof, not the creation call's own claimed success. Two small Python helpers (`find_existing_job.py`, `create_cronjob.py`) are base64-embedded in the `run:` steps -- not because either contains a `${{ }}` literal (neither does, confirmed by grep before embedding), but because a heredoc'd Python file's un-indented top-level statements (starting at column 0) break a YAML literal block scalar's indentation contract when embedded directly, discovered the hard way while building the previous ACC6 gate-retirement workflow. Not yet dispatched as of this commit.

- `4032efc` -- `.github/deploy-staging/status-dashboard-update/{index.html,app.js,style.css,collect_status_feed.py}` (staged, not yet applied to status-dashboard): owner's redesign request for `status-dashboard` -- (1) replace the horizontally-scrolling `.tabnav` tab strip with a top expandable dropdown menu, sectioned ("بخش‌های صفحه" / "پروژه‌ها"), each section a list-style submenu; (2) track every product as its own project, independent of which account hosts it, since ACC0 now hosts both Control-Room and this dashboard while ACC6 hosts Claud-Cloud-Project (TBS) -- owner explicitly said the account-centric ACCOUNTS list and 9-account fleet grid should be dropped entirely, only the project list matters. `Tools/collect_status_feed.py`: removed `ACCOUNTS`/`collect_account_data`/the fleet grid data and the broken local-disk `collect_latest_gate_report()` (this repo has no `Reports/gates` of its own -- that path always returned `unmeasured`, a real bug since the 2026-09-11 migration, not by design); added a `PROJECTS` list (TEHRAN: BLIND SPOT on ACC6, Control-Room on ACC0, AirboxVIP Coffeenet on ACC1, this dashboard on ACC0) and `probe_repo_gates()`/`collect_project_status()` -- a live, per-project GitHub-API gate/commit/issue/run probe reused identically for every project, which also fixes TBS's gate card (previously always unmeasured) and Control-Room's (previously probing the deleted `mohammadlali0707-stack/Control-Room` duplicate instead of the real `Mohammadlali/control-room`). `index.html`/`app.js`/`style.css`: new `.menu-wrap`/`.menu-panel` dropdown (verified via a real headless-browser screenshot test, not just reading the diff -- caught and fixed one real bug this way: `.menu-panel`'s own unconditional `display: flex` silently overrode the `hidden` attribute's UA-stylesheet default, since author CSS always outranks UA CSS regardless of specificity, so the panel was rendering open on every page load until scoped to `:not([hidden])`), new `.projects-grid`/`.project-card` (replaces the two hardcoded gate cards and the whole 9-account fleet section), tasks table repointed at `feed.recent_runs` or now shows which project each run belongs to. Verified with a local static-file server plus a real headless Chromium run (Playwright): 4 project cards render, gate-number aggregation is correct (65/67 summed across 2 measured projects), menu opens/closes/scrolls on both desktop and a 390px mobile viewport with zero horizontal overflow. Not yet pushed to `Mohammadlali/status-dashboard` itself as of this commit -- that is the next, separate step.

- `ece8f7c` -- `.github/workflows/deploy-status-dashboard-update.yml` (new): applies the staged nav+per-project redesign (`4032efc`) onto `Mohammadlali/status-dashboard` for real. Clones that repo with `secrets.ACC0`, copies the four staged files into place, sanity-checks them (`ast.parse` on the Python collector, `node --check` on app.js, grep for the new menu/projects markers in index.html) before committing, then commits and pushes -- a no-op with exit 0 if there is nothing to commit, so re-running it is safe. Not yet dispatched as of this commit.

- `13991a8` -- `.github/workflows/fix-deploy-workflow-args.yml` (new): the nav+per-project redesign just pushed to `Mohammadlali/status-dashboard` (`0380351`) dropped `Tools/collect_status_feed.py`'s `--gates-dir` CLI argument (dead in the new design -- gate health is now a live per-project GitHub API probe, never a local directory read), but `deploy-status-feed.yml`'s own real invocation still passed `--gates-dir Reports/gates`, a caller I never looked at while rewriting the collector. Confirmed as a real production failure, not a guess: dispatched the real deploy right after pushing, watched it fail with `collect_status_feed.py: error: unrecognized arguments: --gates-dir Reports/gates` via `check-status-dashboard-run.yml`'s log. This workflow clones status-dashboard, `sed`s the now-stale flag out of the one `run:` line that has it, verifies via `grep` that it is gone and the YAML still parses, then commits and pushes. Not yet dispatched as of this commit.

- `90c1426` -- `.github/workflows/push-vercel-fix-workflow.yml` (new) + `.github/deploy-staging/status-dashboard-update/check-fix-vercel-protection.yml` (staged): the nav+per-project redesign deployed cleanly (real job log: `Build and Deploy Status Dashboard: success`, run `34685075205`), but a live curl afterward found `status.airboxvip.top` -- the WHOLE domain, `/` and `/status.json` alike -- returning a real `302` to `vercel.com/sso-api`: Vercel's own SSO/"Deployment Protection" wall, gating even production behind a Vercel account login. Not caused by today's redesign (it is a Vercel project-level setting, unrelated to any pushed file) -- most likely a default enabled when this Vercel project was (re)created during the September migration to this repo and never noticed because nobody tried an unauthenticated fetch until now. `check-fix-vercel-protection.yml` runs ON status-dashboard itself (native access to its own `secrets.VERCEL_TOKEN`, which control-room does not hold): reads the project's current `ssoProtection` via `GET /v9/projects/claud-cloud-status`, `PATCH`es it to `null` (Vercel's own documented way to fully disable SSO protection on all deployment types, prod included), reads it back again to confirm the change stuck rather than trusting the PATCH response alone, then polls the real public URL until it returns 200. `push-vercel-fix-workflow.yml` (this one, run from control-room) pushes that file onto status-dashboard via `secrets.ACC0` and dispatches+watches it. Not yet dispatched as of this commit.

- `(this repo's hash follows in a `changelog:` follow-up)` -- CORRECTION, owner's direct message: the Vercel SSO wall on `status.airboxvip.top` is NOT a bug -- the owner wants the site private (only reachable through their own Vercel login), specifically because the planned `@agy` chat feature will let this dashboard trigger real GitHub issues/work on the owner's repos, and that needs to stay owner-only. Reverting the earlier `ssoProtection: null` change (from this session's own mistaken assumption that the wall was an accidental misconfiguration): `.github/deploy-staging/status-dashboard-update/revert-vercel-protection.yml` PATCHes it back to `{"deploymentType": "all_except_custom_domains"}`, its exact value before today's change, and confirms via read-back. Net effect on the actual production URL is zero either way -- real curl checks throughout this whole investigation show `status.airboxvip.top` returned a 302 to `vercel.com/sso-api` both BEFORE and AFTER the `ssoProtection: null` change and a fresh redeploy, proving `ssoProtection` was never what gates this specific custom domain (something else does -- team-level policy or a mechanism not yet identified) -- but the field is restored to its original value regardless, since leaving it changed from what the owner had was still wrong even though it didn't move the one thing that actually matters here. Also added `.github/workflows/push-and-run-staged.yml`, a generic parameterized replacement for the several one-off `push-and-run-*.yml`/`push-vercel-fix-workflow.yml` wrappers this session accumulated (each pushes+dispatches+watches one file staged under `.github/deploy-staging/status-dashboard-update/`, now driven by a `filename` input instead of a new duplicate workflow per file) -- prompted by the owner also noting Control-Room and status-dashboard are now PRIVATE repos (agw-workers across all 9 accounts were made public instead), so this repo's own Actions minutes are no longer unlimited and duplicate one-off workflows are worth not accumulating further. Not yet dispatched as of this commit.
