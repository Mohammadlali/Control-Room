# MAP -- the contract file

## CURRENT STATE -- read this block before anything else below it

### 2026-09-12 -- StatusFeed MOVED out of this repo entirely, to its own dedicated repo

**Owner's observation: the status dashboard covers CCP + Control-Room + all 9
accounts, so it isn't CCP-specific and shouldn't live inside CCP's repo at
all -- it belongs under ACC0 (Mohammadlali, the account that manages the
fleet), not bundled inside a product repo hosted on a different account
(ACC6).**

**Moved to `Mohammadlali/status-dashboard` (new, public).** Everything
verified against real runs, not assumed:
- Repo created via `gh repo create` using control-room's stored ACC0 PAT
  (this session's own direct GitHub App access got a 403 on repo creation
  specifically -- an App-install scope gap, not a real blocker).
- All source (`index.html`/`app.js`/`style.css` -- the Persian/RTL redesign
  already live on ACC6 at that point -- plus `manifest.json`, `sw.js`,
  `vapid_public.json`, `api/subscribe.js`, icons, and the three `Tools/*.py`
  scripts) copied byte-exact via git (staged into control-room first after
  log-dump reconstruction proved unreliable across separate clone dispatches).
- `deploy-status-feed.yml` rewritten for the new repo's flat layout (no
  `StatusFeed/` prefix), self-push credential switched to `ACC0_PAT` (its
  own account now), same Vercel project name (`claud-cloud-status`) so the
  live domain alias carries over unchanged. Written via base64 into its
  host workflow (its own `${{ secrets.X }}` expressions must survive as
  literal text, and control-room has no secrets of those names).
- All 15 secrets (`ACC0_PAT`..`ACC8_PAT`, `VERCEL_TOKEN`, `CF_API_TOKEN`,
  `CF_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`,
  `R2_S3_ENDPOINT`, `VAPID_PRIVATE_KEY`; `VAPID_PUBLIC_KEY` skipped -- never
  set on ACC6 either) migrated by a one-off workflow pushed onto ACC6 itself
  (secret values are never readable via API -- a workflow must run physically
  where they live to resolve them), using ACC6's own `ACC0_PAT` (Mohammadlali's
  PAT) as admin to `gh secret set` on the destination -- no plaintext ever
  printed, logged, or returned. Verified by `gh secret list` showing all 15
  names present on the destination.
- First real deploy dispatched and verified: real Vercel URL
  (`status-dashboard-d8auydnta-airbox-vip.vercel.app`), alias assigned to
  `status.airboxvip.top` on the first attempt, checker reported "Run
  succeeded." Confirmed from the raw job log, not the run's own conclusion.

**Two real, non-blocking gaps found during that first deploy, not yet fixed:**
- `status.json` will never actually get committed to the new repo's own git
  history: `git diff --quiet -- status.json` on a file that was never tracked
  reports "no difference" (git diff ignores untracked paths), so the
  "Commit updated status.json" step prints "unchanged" and never `git add`s
  it. The live site stays fresh regardless (Vercel deploys the freshly-generated
  workspace file, not the git-tracked one), but the repo's own copy will stay
  permanently stale. Fix: `git add -f` on first use, or `git status --porcelain`
  instead of `git diff` so untracked is also caught.
- R2 calls (push-subscription load + snapshot archive) failed with an SSL
  handshake error on that first run (see the raw log, run id in control-room's
  `check-status-dashboard-run.yml` history); non-fatal (both calls degrade
  gracefully), but uninvestigated -- could be the R2 endpoint value itself or
  a runner-side TLS issue, not yet distinguished.

**Removed from this repo in the same change:** `StatusFeed/` (entire
directory), `.github/workflows/deploy-status-feed.yml`, and
`Tools/collect_status_feed.py`/`Tools/send_push_notification.py`/
`Tools/ensure_cloudflare_dns.py`. `.github/workflows/backlog-dispatcher.yml`
left alone -- unrelated. The 15 secrets this repo held for the old pipeline
(`VERCEL_TOKEN`, `CF_*`, `R2_*`, `VAPID_*`, `ACC0_PAT`..`ACC8_PAT`) were NOT
removed from this repo -- they were copied, not moved, and `ACC0_PAT`..`ACC8_PAT`
in particular may still be used by other workflows here (e.g.
`backlog-dispatcher.yml`); removing them was out of scope for this change.

**Consequence for this repo's own gate suite:** `Tools/check_status_feed_freshness.py`
will now always report `no_status_file` since `StatusFeed/` is gone -- the
same class of permanent-red this project has already documented once before
for the now-deleted ACC0 checkout (see that checkout's own CHANGELOG.md if it
is ever reached again). Not fixed here: retiring the gate line itself from
this file's own "Before you stop" list (if one exists) and from
`Tools/run_gates.py`'s suite is real follow-up work, left for a session that
can actually run and verify the full gate suite on this repo rather than only
pushing files to it cross-account.


### 2026-09-11 (very latest) -- CCP IS MOVING FROM ACC0 TO ACC6 ENTIRELY;
this repo's own account will be emptied, not just supervised differently

**Owner's direct question and instruction: is this session working on
ACC0 or ACC6? Answer: ACC0** (`Mohammadlali/Claud-Cloud-Project`, this
exact repo -- confirmed, this session's scope has always been ACC0).
Per the owner's own stated branching logic for that answer: (1) delete
ACC6's current copy, (2) migrate ACC0's copy (which now has everything --
the Unreal cleanup, the status-feed fix, the Control-Room restructuring)
onto ACC6, (3) delete ACC0's copy. This is DIFFERENT from and supersedes
everything below about ACC0 doing "management only, TBS lives on ACC6" --
that assumed TWO copies with ACC0 as manager; the new instruction is ACC0
has NO copy of CCP at all, TBS's only host anywhere is ACC6.

**Measured before touching anything (`compare-ccp-acc0-acc6.yml`, run
`34599524791`): ACC6's copy has NOTHING ACC0 lacks.** Its HEAD on
`claude/gateway-auth-fix-nr7k0b` is `5019c6b`, the exact commit this
session's own `sync-tbs-intro-to-07.yml` pushed there earlier the same
day; everything before that in ACC6's history (`fad4af9`, `0500c1b`, the
account-naming fixes) is the same lineage already reconciled into ACC0's
own `org.json` earlier this session. Identical branch lists on both
sides. Safe to treat ACC0 as authoritative.

**Migration RUN and VERIFIED, two attempts:** `.github/workflows/
migrate-ccp-to-acc6.yml` deletes ACC6's copy, creates a fresh empty one at
the same name, mirror-clones ACC0 (every branch/tag) plus its full LFS
object history, pushes both into the new ACC6 repo, then verifies branch
list and HEAD commit match. First dispatch (run `34599897583`) pushed
every real branch and tag but exited non-zero because a bare mirror clone
also captures GitHub's own synthetic `refs/pull/N/head` refs, which the
destination refuses ("deny updating a hidden ref") -- ACC0 was never
touched, only ACC6's (already-being-replaced) copy was affected. Fixed
(`54afad4`): delete `refs/pull/*` from the local mirror before pushing.

**Second dispatch (run `34600123157`) succeeded end to end -- verified by
reading the job's raw log directly, not by trusting its green conclusion:**
ACC6's old copy deleted (confirmed via a follow-up 404), fresh empty
private repo created, mirror pushed clean (36 branches including
`claude/gateway-auth-fix-nr7k0b`, 2 tags, no `refs/pull/*` attempted),
233/233 LFS objects (19 MB) uploaded, and the verification step's own
output shows branch count 36 == 36 and identical HEAD
(`54afad48b13296a1dc8a10074d2326cc31d7aa2a`) on both sides. **ACC6 now
genuinely holds everything ACC0 has -- this is measured, not assumed.**

**Two more real gaps found before deleting ACC0, both closed and
verified:** a git+LFS mirror carries commits/blobs, never GitHub Issues or
repo-level Actions secrets. ACC0 had 17 open issues that would have been
lost outright, and `deploy-status-feed.yml`/`backlog-dispatcher.yml`
(mirrored onto ACC6 as files) read secrets (`ACC0_PAT`..`ACC8_PAT`, `R2_*`,
`VAPID_*`, `CF_API_TOKEN`, `CF_ACCOUNT_ID`, `VERCEL_TOKEN`) that only
existed in ACC0's repo settings. Owner confirmed: repair before deleting.
`.github/workflows/repair-acc6-before-acc0-deletion.yml` (run
`34609481039`) did both, verified from the raw job logs, not the run's own
conclusion: all 17 issues recreated on ACC6 (`acc0#100..33` ->
`acc6#1..17`, e.g. `acc0#92` -> `acc6#9`), and 13 secrets set
(`VAPID_PUBLIC_KEY` correctly skipped -- it was never set on ACC0 either,
so nothing to copy) with the target repo's own public key doing the
encryption, no plaintext ever leaving the job's memory.

**A third gap, found while writing this entry up: ACC6 was stale.** The
migration verified ACC6 matched ACC0 at commit `54afad4` -- but every
commit ACC0 made after that (recording the verification itself, this very
issue/secrets repair) only landed on ACC0, since a one-time mirror does
not keep following. Deleting ACC0 without re-syncing would have silently
thrown away the last several commits, this entry included. Fixed:
`.github/workflows/sync-ccp-branch-to-acc6.yml`, a plain fast-forward push
(ACC6's history already has the right fork point, so no delete-and-
recreate needed) -- dispatched as the LAST step before ACC0's deletion, so
whatever commit records that dispatch is itself the one being synced.

**Remaining, separate, deliberate step: delete ACC0's own copy**
(`Mohammadlali/Claud-Cloud-Project` -- this repo, this session's own
home) via the existing `delete-repo.yml` (`account: ACC0, repo:
Claud-Cloud-Project, confirm: Mohammadlali/Claud-Cloud-Project`). Not run
automatically by the migration workflow, and not run yet as of this
entry -- this repo is where this session executes, so the deletion has to
be the very last action this session takes on this checkout.

### 2026-09-11 (latest) -- `check_status_feed_freshness` FIXED, root cause
found and closed, not just recorded as evidence again

**Owner asked directly: "مشکل check_status_feed_freshness رو حل کن."**
This gate had been red for 30+ hours (since 2026-09-10 06:51), surviving
past sessions' Stop-hook housekeeping (commit the evidence file, move on)
without anyone reading WHY `deploy-status-feed.yml`'s schedule kept
missing. Read the real job logs instead of guessing: **every single
scheduled run since the workflow was created failed identically** with
`remote: Duplicate header: "Authorization"` / `fatal: ... 400` on its
push step (run `34584736801`, confirmed from the job's own log).

**Root cause:** `actions/checkout@v4` writes its own
`http.https://github.com/.extraheader` into the workspace's LOCAL git
config, carrying the default `GITHUB_TOKEN`. The workflow's push step
added a SECOND one via `git -c http.https://github.com/.extraHeader=...`
for `ACC0_PAT`, meaning to override it -- but `extraHeader` is
MULTI-VALUED in git, so both were sent, and GitHub's server rejects a
request carrying two `Authorization` headers outright. This was true on
every scheduled run since the workflow's creation, not an intermittent
flake.

**Fix:** `git config --local --unset-all http.https://github.com/.extraheader`
before setting the new one. **Found the identical bug latent in
`backlog-dispatcher.yml`** (checkout + push-to-self, same at-risk shape,
an unscoped `http.extraheader`) and fixed it the same way before it
caused a visible failure, not after.

**Verified against a real run, not assumed from the diff:** manually
dispatched `deploy-status-feed.yml` (run `34598884090`) after pushing the
fix. It pushed `593a655` on the first attempt, no duplicate-header error.
`git fetch` picked up that commit on the remote, and
`Tools/check_status_feed_freshness.py` independently re-measured the
file's age afterward: 0.02h, against a 3h limit. Full gate suite: 49/49
pass -- the first fully green run since this cleanup began.

**GOVERNANCE IS OPEN AGAIN. The owner REOPENED it on 2026-08-27:** *"قانون
گذاری و اجرای قانون ها لازم است و نباید آن ها را به سادگی کنار گذاشت"* --
lawmaking and enforcing the laws are necessary and must not be set aside
lightly. ~~GOVERNANCE IS CLOSED, ended 2026-08-26~~ -- **that instruction is
SUPERSEDED and every appearance of it in this file is stale.** A gap in the
rules is now work, not a distraction. The two limits that did not change:
**do not weaken a gate so a document passes**, and do not build a gate that
cannot fail.

This file keeps superseded sections inline with the reasoning that made them
worth keeping, so **a reader who skims headings will land on one and report a
solved thing as open.** That happened on 2026-08-21: a fresh manager reported
the `insteadOf` credential as still present on 98 of 99 and proposed clearing
it, hours after it had been cleared fleet-wide and verified. Everything below
this block is history unless this block says otherwise.

### 2026-09-11 (later still) -- COMPLETE Unreal-Engine tooling cleanup;
engine is Ren'Py, and the codebase finally says so

**Owner's explicit instruction, after confirming Unreal is no longer used
at all: "پاک‌سازی کامل ابزارهای مخصوص Unreal را انجام بده."** Investigation
first (this project's own rule, measure before act) found the engine
decision was already made and partly executed 2026-09-09 -- `Team/
MAP_ARCHIVE.md`'s "ENGINE DECIDED: Ren'Py" block, owner's own words: `با
توجه به مقایسه ی Ren'Py و Godot، من Ren'Py رو تعیین میکنم` -- and domain
restructuring already applied to `Team/org.json` (commit `f7b36ac`,
visible live: `A`=Visual Assets and AI Generation, `B`=VN Engine and Flow,
`E`=Android Build and Packaging). What had NOT happened: the actual UE5
tooling, C++ module, and binary content were all still in the tree,
`CLAUDE.md` still opened with "Unreal Engine 5.8", and nothing enforced
the new direction.

**Deleted, all confirmed via `git rm` + full gate re-run, not assumed
safe:** 45 `Tools/*.py` files (27 `import unreal` directly, plus `ue.py`,
`watch.py`, `distill.py`, and 15 UE5/Kaggle-build-specific checks/probes),
`Source/TehranBlindSpot/` (C++ module), `Districts/` (3D level JSON),
`Content/` (`.umap`/`.uasset` binaries), `Jobs/` (the whole laptop-Unreal
queue), `Cloud/colab/` (11 Kaggle/Colab UE5-hosting scripts),
`Cloud/runner/prebuilt.yml` (already dead per `Mohammadlali/Runner`'s
deletion earlier the same day), `TehranBlindSpot.uproject`, `.vsconfig`,
the three UE5 `.ini` files, `Docs/learning_path.md`. Full list and reasons:
`Team/CHANGELOG.md`'s same-timestamp entry.

**Kept, deliberately:** `Config/target_device.json` (hardware facts
survive per `Team/reports/ue5_pivot_scope.md`'s own verdict -- edited to
strip the embedded UE5 renderer-CVar pin arrays), every UE5-pivot
decision-history report (`ue5_pivot_scope.md`, `renpy_domain_scoping.md`,
`engine_comparison.md`), and all of `Reports/` (measurement history is
never purged when an engine changes).

**9 gates retired** from this file's own "Before you stop" list (see that
heading below for which and why) -- 58 down to 49, still comfortably over
`MIN_GATES = 25`. **5 gates broken by the deletions were fixed, not
weakened** -- each was a real historical-citation problem (a report
correctly citing a file that existed when it was written, now gone):
`verify_claims.py` gained a frozen `RETIRED_2026_09_11` exemption set
(same technique as `check_review_guild.py`'s frozen legacy-account table);
`probe_check_heredoc_backticks.py`'s case 3 now reads the deleted
`Cloud/runner/prebuilt.yml`'s last real content via `git show 3439e3f:...`
instead of a live file; `Team/MAP_ARCHIVE.md`'s one bad archive-index
destination was changed to the existing `superseded` convention;
`Team/RULES.md` was regenerated (`rules_index.py --write`);
`probe_check_cited_flags.py`'s fixture was re-pointed from the deleted
`Tools/distill.py` to the still-real, still-non-argparse
`Tools/verify_claims.py`, preserving the exact property the original test
proved. Full suite: 48/49 pass, only the pre-existing, unrelated
`check_status_feed_freshness.py` red.

**`CLAUDE.md` substantially rewritten**, not just patched: engine
declaration, layout table, hard rules 1/2/3/5 struck through as
UE5-API-specific, target-device section (hardware kept, renderer pins
removed), Persian-text section (UE5 solution marked historical, the real
measured Ren'Py solution -- `config.rtl` + HarfBuzz, `Tools/
probe_renpy_persian.py` -- documented in its place), "Running things"
(UE5 gateway removed, no Ren'Py equivalent built yet), "The sun was aimed
at the sky" and "Open issues" marked HISTORICAL/ARCHIVED, "Working
arrangement" (the UE5-specific cloud/laptop division no longer assumed).

**What still does not exist, stated plainly so nobody assumes otherwise:**
no `game/` Ren'Py project directory, no `.rpy` dialogue, no build/verify
pipeline for whatever comes next. This cleanup removed dead weight and
corrected the record; it did not build the new thing.

### 2026-09-11 (later) -- ACC0 becomes management-only; TBS's only home is
now ACC6/07; topic-based issue routing BUILT (in Control-Room, not here)

**Owner's decisive restructuring instruction, superseding "resume as fleet
manager" below only in scope, not in spirit.** Four things changed at once:

1. **`Mohammadlali/Control-Room` (on `ACC0`) is now the org's ONE canonical
   Control-Room**, not `mohammadlali0707-stack/Control-Room` (which this
   file's own earlier entries, and that repo's own docs, had assumed was
   the real one). The `07` copy is being deleted -- see that repo is not
   this one; check `Mohammadlali/Control-Room`'s own `Team/CHANGELOG.md`
   for the deletion attempt's outcome, not this file.
2. **The topic-based issue router the owner asked for is BUILT**, but in
   Control-Room, not in this repo: `Tools/route_topic.py` +
   `Team/company_scope.json` there classify every incoming issue (label
   first, keyword fallback, refuses to guess on a tie) and either handle
   it locally or forward it as a fresh `@agy` issue to the right project's
   own repo. This repo's own `agy-issue-bot.yml` is unaffected -- it still
   dispatches round-robin across TBS's own 8-account ring, which is a
   different, already-solved problem (which TBS worker gets an issue) from
   the one the router solves (which PROJECT an issue is even about).
3. **TEHRAN: BLIND SPOT now lives EXCLUSIVELY on `mohammadlali0707-stack/
   Claud-Cloud-Project` (`ACC6`/`07`).** This repo (`Mohammadlali/
   Claud-Cloud-Project`, `ACC0`/`1997`) is retiring for TBS purposes --
   `ACC0` does management only, permanently, not just "no ring
   membership" as the 2026-09-10 entries below describe. Any TBS change
   still made here, because a session is already open, must be merged
   into `ACC6`'s copy immediately rather than left to diverge.
4. **`Team/NEW_SESSION_PROMPT.md` narrowed from "the whole company's
   bootstrap" to "TBS's own bootstrap only."** The nine-account scope,
   delegation policy, cross-account bridge pattern, and the
   trust-nothing-without-a-second-read lessons all moved to
   `Mohammadlali/Control-Room`'s new `Team/COMPANY_SCOPE.md` and
   `Team/CROSS_ACCOUNT_LESSONS.md` -- read them there, this file's own
   `NEW_SESSION_PROMPT.md` entry point no longer restates them.

Full 58-gate suite here: 57 pass, only the known
`check_status_feed_freshness.py` red (unchanged, unrelated to this work).

**UPDATE, same day:** `Team/NEW_SESSION_PROMPT.md` -> `Team/Project TBS
Intro.md` synced to ACC6/07's copy (`sync-tbs-intro-to-07.yml`, push line
`f4f15ff..5019c6b`, verified from the job's own log). `mohammadlali0707-
stack/Control-Room` is DELETED (`delete-07-control-room.yml`, `ACC6_PAT`
does carry delete_repo scope; confirmed by re-querying the repo after the
DELETE call and getting `404`, not by trusting the call's own exit code).
`Mohammadlali/Control-Room` is now unambiguously the org's only
Control-Room.

**UPDATE, same day: collaborator survey done, all 24 removed and
verified.** `survey-all-collaborators.yml` (run 34589873706) found:
`ACC0/Claud-Cloud-Project` had all 8 other accounts as write
collaborators; `ACC1/AirboxVIP_Coffeenet` had `Mohammadlali` plus the
other 7; every account's own `agw-workers` had `Mohammadlali` as a write
collaborator. `remove-all-collaborators.yml` (run 34590101462) removed
all 24 and re-listed every touched repo afterward to confirm zero remain
-- not assumed from the removal call's exit code. Cross-account
automation is unaffected: every bridge authenticates as the target
account's own `ACC{N}_PAT`, never as a collaborator grant.

**RESOLVED, then resolved further the same day: every surfaced repo now
has a final answer.** `Mohammadlali/AirboxVIP_Coffeenet`,
`mohammadlali0707-stack/Runner`, `momonakikugava-pixel/P`, `/P2`,
`momonakikugava-pixel/PathWeaver`, and **`Mohammadlali/Runner` itself**
are all DELETED (`delete-repo.yml`, each confirmed gone by a follow-up
GET returning 404). `Mohammadlali/Runner` was first investigated and
recommended KEPT (see the superseded paragraph this replaces) because it
was load-bearing for the Unreal Engine build pipeline -- but the owner's
own follow-up instruction removed both reasons at once: every repo in
this org is now public (so this repo's own runners already get the
bigger public-repo machine directly, without a separate repo), and
**Unreal Engine is no longer used by this project** (owner's own words).
`AGENTS.md` rule 6 is rewritten accordingly: `runner-ship` has no target
anymore, and `Cloud/runner/prebuilt.yml` plus five tools
(`Tools/engine_mirror.py`, `Tools/kaggle_dataset.py`,
`Tools/probe_ship_prebuilt.py`, `Tools/dispatch_runner_workflow.py`,
`Tools/ship_prebuilt_to_runner.py`) are flagged as Unreal-era tooling not
yet formally retired -- their presence is not evidence they still
matter. **Any Unreal-specific claim anywhere in this project's docs
(including this file's own Android/Unreal-pivot history further down)
needs re-verifying against the non-Unreal direction before being
trusted; that re-verification has not been done yet.**

`.github/workflows/delete-repo.yml` and `.github/workflows/inspect-repo.yml`
are now the generic, reusable versions of this pattern (parameterized by
account+repo, `confirm` must equal the exact resolved `owner/repo` string)
for any future repo decisions -- prefer them over one-off workflow files.

### 2026-09-11 -- Reconciled with 07's own restructuring: ACC0/ACC9
retired PERMANENTLY (not the temporary stand-in below), domain H merged
into D, 88 members; 15 of THIS repo's own pending tasks were ALSO
orphaned on `agw-ACC0-w0N` since yesterday and nobody had caught it

**Owner's instruction: resume as fleet manager, delegate routine work to
ACC1-ACC8's own bots, keep this account (ACC0) for Control-Room-level
management decisions only, and reconcile whatever 07 has done in the
meantime.** First measured, not assumed, that this session's own
`add_repo`/`get_file_contents` still cannot reach
`mohammadlali0707-stack` even now that both repos are public --
"cross-tier adds are not supported" is an owner-identity lock, unrelated
to visibility. Worked around it the same way this project always has:
`.github/workflows/inspect-control-room.yml` repurposed (again) to clone
07's repo with `ACC6_PAT` inside a dispatched job and upload the real
files as an artifact, downloaded and read directly here -- not a
description of 07's changes, the actual bytes.

**What 07 had done, found by reading its `Team/MAP.md` directly:** after
`ACC9`'s own GitHub Actions turned out to be disabled for the whole
account (measured twice, identically, by `probe-acc9-operational.yml` --
`HTTP 422: Actions has been disabled for this user`, unaffected by the
owner re-enabling anything), the owner told 07 to stop chasing either
account's outage and cut the ring to the 8 that work, folding domain H
(Integration and CI) into D. This is a PERMANENT decision, not the
TEMPORARY ACC9-stands-in-for-ACC0 arrangement this file recorded
yesterday (see the two blocks below, both now superseded) -- and it
lines up with today's own instruction to keep ACC0 out of routine
domain-ring work regardless of whether its Actions cap is clear.

**Applied here, verified against 07's own files rather than
re-derived:** `Team/org.json`, `Tools/check_org.py`,
`Tools/probe_check_org.py`, `Team/ORG.md`, `Team/ROSTER.md` all
overwritten with 07's real content after diffing member-by-member --
only 2 of 88 shared members actually differ (ACC1's w06/w10 secondary
slots move from guild H to guild F, since D absorbed H), confirming this
is a straight adoption, not a guess. `.github/workflows/agy-issue-bot.yml`
patched the same way 07 patched its own copy: dispatch case `0`
(`stranger77777777`) and the now-unused `ACC0_PAT`/`ACC9_PAT` removed,
modulo 9 -> 8. `check_org.py` "88 members, 0 problems";
`probe_check_org.py` 18/18. `Tools/probe_role_brief.py`'s own fixture
(`agw-ACC9-w06`, stale since yesterday's temporary substitution) fixed
to `agw-ACC1-w06`, the real post-merge secondary-domain example.

**A second, independent orphaned-task bug found on THIS side, same
shape as 07's own `0500c1b` fix:** 15 pending tasks here (`036`, `037`,
`040`, `041`, `200`-`210`) were still `assigned_to` `agw-ACC0-w0N` from
BEFORE yesterday's ACC0->ACC9 substitution and were never reassigned
then either -- `poll_tasks.py --validate` did not catch it for the
identical reason 07 diagnosed (`chain_problem()` short-circuits on
`assigned_by: architect` without checking the assignee's account still
has members). Fixed the same way 07 fixed its own 15: `assigned_to`
changed from `agw-ACC0-w{NN}` to `agw-ACC1-w{NN}`, same slot number,
nothing else touched. `poll_tasks.py --validate`: `malformed: 0`,
`pending: 107`, both before and after (this fix makes assignments
reachable, it does not change what that gate checks).

Full 58-gate suite: after these fixes, 57 pass, only the known
`check_status_feed_freshness.py` red -- reverify after any further
edit, do not assume it stays clean.

### 2026-09-10 (later still) -- Domain ring reshaped twice more, owner's
explicit instruction: `O`/`C` moved BACK onto `ACC6`(07)/`ACC5`(Just),
and `ACC9` TEMPORARILY replaced `ACC0` in the ring while 1997 is capped;
`Tools/check_review_guild.py`'s legacy-report lookup rebuilt as a FROZEN
table after live-derived data broke it twice in one afternoon

**SUPERSEDED 2026-09-11, see the block at the top of this file: the
`ACC9`-TEMPORARILY-replaces-`ACC0` arrangement below did not last the
day.** `ACC9`'s own Actions turned out to be disabled account-wide (not
fixable from here), so the owner had 07 cut both `ACC0` and `ACC9` from
the ring PERMANENTLY and fold domain H into D -- reconciled into this
repo too. The `O`/`C` correction in this block is still current and
unaffected. `Tools/check_review_guild.py`'s frozen legacy table is also
still current -- it never depended on ACC9 or the ring's current size.

**Owner's answer to the two open questions from the block below:**
*"حلقه رو جابه جا کن. بله دامنه ی O باید به ACC6 یا همون 07 برگرده. بله
ok/ACC9 باید به صورت موقت به جای 1997/ACC0 به حلقه ی دامنه ها اضافه
بشه."* -- move the ring; yes, O goes back to ACC6/07; yes, ACC9
temporarily replaces 1997/ACC0 in the ring.

**Change 1: `O`/`C` swapped back.** The identity correction two blocks
below (acc6=Just, acc7=07) had, as a side effect, moved domain O
(Operations and Fleet Orchestration) off ACC6/07 and onto ACC5/Just --
correct on IDENTITY, wrong on the ORIGINAL DESIGN REASON (`O` was placed
next to Control-Room's real host on purpose). Fixed: `O` primary is
`ACC6` again, secondary `ACC5`; `C` primary is `ACC5` again, secondary
`ACC7` (unchanged). `B`'s secondary_account (whoever's own secondary is
B) moved from `ACC5` to `ACC6` accordingly -- this is a full ring
re-derivation (`Team/org.json`'s `domains`/`accounts`/member `guild`
fields for ACC5 and ACC6 only), not a relabeling.

**Change 2: `ACC9` replaces `ACC0` in the ring, TEMPORARILY.** Same
substitution `agy-issue-bot.yml`'s dispatch table already made for
slot 0 -- now applied to the domain ring too, since ACC0's Actions cap
makes it unable to do H's work right now. `Team/org.json`'s `ACCOUNTS`-
equivalent slot 0 (domain H primary, F secondary, 11 members, ids
`agw-ACC0-w01..w11`) fully relabeled to `ACC9` (`agw-ACC9-w01..w11`);
`ACC0` has ZERO members in `org.json` right now, not a data error --
that is exactly what "replaced" means here. `ACC0` the real GitHub
account is untouched; this is only about who `org.json`'s ring
currently names. `Tools/check_org.py`'s `ACCOUNTS` list and `PINNED["H"]`
both updated to `ACC9`, with an explicit comment naming what to revert
and when (1997's Actions cap clearing). `Team/ROSTER.md`'s H row's lead
column updated to `agw-ACC9-w01` (its "acc1"/email columns describe the
REAL, permanent account and were left alone -- the container id is what
changed).

**This is a BOOKKEEPING change, not an infrastructure one -- no real
`ACC9` container exists.** The owner asked directly whether 11 real
runners `agw-ACC9-w01..w11` had been created, and whether there was a
plan for injecting an `agy`/Antigravity CLI token into them. Neither: no
runners exist, no token-injection plan exists, and this session cannot
do either from here. `stranger77777777/agw-workers2` (the repo that
would host them) is still EMPTY per section 2 below -- no
`agw-worker.yml`/`agy-issue-bot.yml` pushed yet, so nothing would
receive a task dispatched to `agw-ACC9-w05` right now even though
`org.json`/the gates all say it should exist. `Tools/bootstrap_containers.py`
(the docker-mode provisioning tool, deliberately untouched by today's
rename -- see the exclusion note above) runs from the OWNER'S OWN
machine via WSL; if the live architecture is GitHub-Actions-mode instead
(per `Team/NEW_SESSION_PROMPT.md`: "NOT as docker containers... driven
by dispatch_runs"), the missing piece is pushing the standard workflow
template into `agw-workers2` and confirming `ACC9_PAT` is wired --
neither done. Real next step: an `@agy` task on the owner's own account,
or 07 doing it directly once back, not something to guess at further
from here.

**Every `[0-8]` account-digit regex across the fleet's scripts was
`[0-9]`-widened, not just `org.json`'s data**, because `ACC9` now has
real members needing to pass real checks: `poll_tasks.py` (both
regexes), `check_review_guild.py`, `check_task_quality.py`,
`dispatch_backlog.py`, `make_audit_tasks.py`, `worker_git.py`'s delivery
format check (this one is a hard block -- an unwidened regex would have
made it impossible for an `ACC9` container to ever deliver a report).
Verified functionally, not just data-consistency: `poll_tasks.leads()`
finds `ACC9`'s lead, `chain_problem()` correctly accepts `ACC9`'s own
lead and rejects an outside one, `worker_git.py`'s format check accepts
`agw-ACC9-w05`.

**`Tools/check_review_guild.py` broke twice from live-derived legacy
data in one afternoon, and got a real redesign, not a second patch.**
First break: `ACC0` leaving the live ring meant the "acc1" legacy slug
(used by 19 old reports, 013-035) had no live member to derive its
guild/account from anymore. Second break, found by RUNNING the gate
after the O/C swap, not assumed clean: reports 031-033 (`agw-acc5-w01`/
`agw-acc6-w10` etc., pre-2026-09-09, before domain O even existed)
started failing "reviewer outside the domain," because their old
container-id citations were being interpreted against TODAY's live
guild assignment, which had just changed for reasons those reports
never depended on. **Root cause of both: `load_org()` derived the
legacy-id lookup from CURRENT `org.json`, which is safe only if ring
occupancy and domain assignment never change again -- false twice in
one session.** Fixed properly: a FROZEN `LEGACY_ACCOUNT`/`LEGACY_PRIMARY`/
`LEGACY_SECONDARY` table, hardcoded to the pre-2026-09-09 natural
sequential ring (acc1..acc9 = ACC0..ACC8 in numeric order, domains
H,D,I,A,B,C,E,G,F assigned in that same order -- retired letters G
included on purpose, since that is what was true when these reports
were written), used ONLY for legacy (`agw-accN-w..`) ids; new-style
(`agw-ACCn-w..`) ids still resolve from live `org.json`, correctly,
since NEW reports should be judged against CURRENT reality. Verified:
all 41 real reports pass (23 guild-checked, 0 rejected -- was 19
rejected mid-fix), `probe_check_review_guild.py`'s own fixture updated
to name the account that now actually holds guild B's secondary slot
(`ACC6`, not `ACC5`) and re-verified 8/8.

Full 58-gate suite: 57 pass, only the known `check_status_feed_freshness.py`
red. `Team/PREP_FOR_07_RETURN_20260910.md` updated again (fourth
rewrite) with all of this.

### 2026-09-10 (later same day) -- Container-id slugs renamed
`agw-acc1-w01..agw-acc9-w11` -> `agw-ACC0-w01..agw-ACC8-w11`
project-wide, owner's explicit instruction ("میخوام الان انجام بشه");
uncovered and fixed a REAL error in the block below: `acc6`=Just and
`acc7`=07, not the reverse this session had applied hours earlier; 58
gates re-verified, 57 pass (only the known status-feed one red)

**The rename itself, exactly the rule the owner stated (N-1: the digit
in `accN` becomes the digit in `ACC{N-1}`), applied to:** `Team/org.json`
member `id`/`lead` fields (99 members); all 141 files under
`Team/tasks/pending/` and `Team/tasks/done/` that cited a container id
(160 replacements: `assigned_to`, `assigned_by`, prose); `Tools/`
scripts that PARSE the id format, each fixed for its own arithmetic, not
just the string -- `poll_tasks.py` (ROSTER-lead regex and the
`assigned_to` chain-of-command regex), `check_review_guild.py`,
`check_task_quality.py`, `dispatch_backlog.py`, `worker_git.py`
(delivery format check), `make_audit_tasks.py` (ROSTER-table regex,
bare `accN` roster-column half left alone -- that column was never
renamed), `run_fleet.py` (`slots_for_account` and `--account` now take
the `ACCn` digit directly, 0-8, not the old 1-9), `auto_assign_reviews.py`
(next-reviewer wraparound changed from `(n % 9) + 1` over 1-9 to
`(n + 1) % 9` over 0-8), and `dispatch_runs.py` / `.github/workflows/
tbs-manager.yml` (both now do `+1` explicitly before using the digit as
`secrets.TBS_TOKENS`' own separate, UNRENAMED 1-9 "num" -- that secret's
own numbering was never part of this rename and still means what it
always meant, `num 1 = Mohammadlali/ACC0`). Every live probe re-run
after its own fix, not assumed: `probe_dispatch_runs.py`,
`probe_run_fleet.py`, `probe_chain_of_command.py`,
`probe_check_review_guild.py`, `probe_role_brief.py`,
`probe_worker_deliver.py`, `probe_run_worker.py` all green.

**Deliberately EXCLUDED, and left on the old `acc1..acc9` naming:**
`Tools/bootstrap_containers.py`, `Tools/team_health.py`,
`Tools/probe_concurrent_deliver.sh` -- all three run `docker exec`
against real, physically-named local Docker containers on the owner's
own machine (via WSL), which this session cannot see, verify, or
rename. Renaming their accepted id format would break them against
containers that still answer to the old name until the owner renames
them too, or confirms Docker mode is no longer used. `Tools/run_fleet.py
--via docker` inherits the same limit, since it shells out to
`bootstrap_containers.py` with whatever id it was given -- flagged, not
silently patched around. Historical narrative (specific incidents named
in `Team/CHANGELOG.md`, this file's own older blocks, and comments like
"Measured 2026-08-26 on account 8" inside `Tools/*.py`) was also left
alone on purpose: it describes what a container was called at the time
of that event, and rewriting it would misattribute history exactly the
way renaming `Team/tasks/done/` would have if the owner had not
explicitly approved that specific case.

**The identity correction, found by actually applying the owner's
stated rule and comparing it against what this session had applied
hours earlier (see the block below): they disagreed for exactly `acc6`
and `acc7`.** Surfaced to the owner rather than guessed past
(`AskUserQuestion`); the owner's answer: *"acc6 همان Just است و acc7
همان 07 است"* -- `acc6` really is Just (`kidding602`), `acc7` really is
07 (`mohammadlali0707-stack`), confirming `Team/ROSTER.md`'s ORIGINAL
account table was right all along and this session's earlier
ORG.md-favoring resolution (logged in the block below) was wrong. Fixed
by swapping every `"ACC5"`/`"ACC6"` value in `Team/org.json` (14 each,
disjoint from every other label, verified before swapping), the two
swapped entries in `Tools/check_org.py`'s `CONTAINER_SLUG`, and one
probe fixture (`guild_in_one_account` in `probe_check_org.py`, which
picks whichever account holds guild B's secondary and needed to follow
the swap). **Consequence for `Team/ORG.md`: domain `O` (Operations and
Fleet Orchestration) is now on Just (`ACC5`), not 07 (`ACC6`) --
reversing the table two blocks below.** The ORIGINAL reason for putting
`O` next to Control-Room's host (07) was sound; it had just been
attached to the wrong ring position. Documented as a correction in
`ORG.md` rather than re-deriving the whole ring again the same day --
whether `O` should be moved back onto `ACC6` is an owner call, not a
naming fix, since it would reshape the ring's secondary assignments
again.

**`Tools/check_org.py`'s `CONTAINER_SLUG` bridge is now the identity
function** (`ACC{k}` -> `acc{k+1}` for every k, no more exceptions) --
kept rather than removed, so `roster_leads()` and the expected-id
generator still have one named place documenting the relationship, but
it could be deleted in favor of inline arithmetic without changing any
result. `Tools/check_review_guild.py` needed a real fix, not a
find-replace: it validates `Report-by`/`Reviewed-by` signers on EVERY
`Team/reports/*.md`, including pre-2026-09-10 reports that correctly
cite the OLD container form and are never rewritten -- its `CONTAINER`
regex now accepts both forms, and `load_org()` registers each member
under its legacy id too (`agw-acc{k+1}-w..` alongside `agw-ACC{k}-w..`),
so an old report's reviewer still resolves to the same guild/account it
always had. Without this fix the gate would have gone from 0 rejected
to 25 rejected on reports nothing about actually changed -- caught by
running the full 58-gate suite, not assumed clean from the targeted
fixes alone.

`Team/PREP_FOR_07_RETURN_20260910.md` updated again (third rewrite) to
carry this forward to the 07 session, so it does not need to re-derive
or redo any of the above.

### Carried forward before archiving eight 2026-09-09 blocks (this pass,
`Tools/archive_map_blocks.py --to-target`): what the orienting read
still needs from them

- **Task 036 (Kaggle P100 boot) was still open, still `pending`, as of
  the archived blocks** -- kernel `tbs-boot-036` failed at the
  `listing` stage with "the dataset never mounted", confirmed by a real
  A/B/C contrast, not inferred. Check `Team/tasks/pending/` and
  `Team/CHANGELOG.md` for whether this has moved since; do not assume
  it is still open just because this note says so.
- **The RHIThread render crash on hosted runners (lavapipe) was the
  KNOWN wall**, not a new one: `vkCmdSetRenderingInputAttachmentIndicesKHR`
  (`VK_KHR_dynamic_rendering_local_read`) does not exist on lavapipe,
  confirmed twice, same crash offset both times (runs `34089032964` and
  `34094442694`). No engine/workflow change fixes this; it needs a real
  GPU driver -- Kaggle's P100 (task 036 above) was the untested route,
  still blocked on the dataset-mount failure.
- **`engine_prebuilt_34094442694`** -- run `34094442694`
  (2026-09-07T07:36:13Z) is the newest measured hosted-runner run and
  still has no dedicated CURRENT STATE block; task
  `040_name_run_34094442694_in_map.json` (pending) owns writing one,
  with four findings it names (crash symboliser now live but the
  actually-crashed `RHIThread`'s own callstack is empty; this may be a
  startup-phase crash, not the same render/capture-phase one
  `34089032964` hit; task 041 is already answered but stuck in
  `pending/` because `probe_check_task_quality.py` hard-codes its path
  as a fixture; every `androidfix` variant reports `ubt_rc: 6`). Read
  the task file and its two named reports
  (`Reports/cloud_host/engine_prebuilt_34094442694.txt`,
  `crash_report_34094442694.txt`) rather than re-deriving this.
- **`check_map_asset_freshness`** -- `Tools/check_map_asset_freshness.py`
  was retired 2026-09-06 in favor of `check_district_build_proof.py`; not
  called by any gate or workflow. Task `284.json` (pending,
  diagnosis-only) asks whether it emits a `##TBS##` line at all and
  whether it is truly dead code, as a proposal for the owner.
- **The engine decision (Ren'Py, superseding UE5) and the owner's
  company-loop vision (`Team/COMPANY_LOOP.md`) are both already
  reflected in this project's live files** (`CLAUDE.md`'s own header,
  `Team/ORG.md`'s domain ring, `Team/NEW_SESSION_PROMPT.md`'s pointer to
  `COMPANY_LOOP.md`) -- their archived MAP.md blocks were the
  announcement, not the only record, so nothing here depends on reading
  the archive to know either happened.
- Full detail for all eight archived blocks: `Team/MAP_ARCHIVE.md`,
  indexed as `unreviewed` by `Tools/check_archive_index.py` -- read
  there, not re-derived, if one of them turns out to matter.

## Handing a command to the owner

The owner's shell is **Windows PowerShell 5.1**, and the tools live in WSL.
Six commands handed over on 2026-08-21 failed before they ran, all of this one
class. The rules, so the seventh does not:

- **Put the pull in the SAME line, with `;`.** PowerShell 5.1 rejects `&&`
  but accepts `;`, and `;` does not short-circuit -- which is safe here
  precisely because the guards refuse to run when the checkout is behind. So:

      git pull origin claude/gateway-auth-fix-nr7k0b; wsl -e python3 Tools/...

  A failed pull leaves the tool refusing rather than acting on stale code.
  This exists because the ordering rule was written down and then dropped four
  times, always when there was something interesting on the other side of it.
  A new flag is the one case no guard can catch: argparse rejects it before
  any of this project's code runs, so the only defence is not separating the
  pull from the command that needs it.
- **One command per line otherwise. Never chain with `&&`** -- PowerShell 5.1 rejects it
  as "not a valid statement separator". `;` chains but does not short-circuit,
  so a failed first command still runs the second. Separate lines.
- **No `<file>` placeholders.** PowerShell parses `<` as a redirect and dies.
  Write a real path.
- **Docker lives in WSL, not on the Windows PATH.** Prefix with `wsl -e`.
- **Never hand-type `docker exec`** -- use
  `bootstrap_containers.py --run`, which owns the container working directory.
- **Anything touching `git remote` must redact:**
  `| sed 's#//[^@]*@#//REDACTED@#'`.
- **A tool only exists on the host after a pull.** Start a handover with it.
- **Never put backticks in a double-quoted `git commit -m`.** The shell runs
  what is between them and eats the word. A message here lost `check` that
  way, and the mangling is invisible until someone reads the commit. Use
  `git commit -F -` with a quoted heredoc.
- **`git mv` only moves TRACKED files.** An untracked file is renamed with
  `Rename-Item` and then `git add`. `git mv` on one fails with
  `fatal: not under version control`.
- **`git add <path>` on a file that may not exist gets its own line**, because
  without `&&` the rest of a chain runs anyway and a failed pathspec is easy to
  miss in the scrollback.

## Starting a fresh session

`Team/NEW_SESSION_PROMPT.md` holds the block to paste. A new chat costs
one read of this file and `Team/LEARN.md`, and nothing else -- that is
what the handover doctrine buys. Say that cost out loud when recommending
a fresh chat; error 4 on the list below is having recommended one without
mentioning it.

## Handing command to someone else

**Handed to the Antigravity IDE 2026-08-21.** It proposed storing the briefing
as a skill at `C:\Users\Mohammad\.gemini\config\skills\...` -- which is
exactly what line 14 of this file forbids: a rule in an IDE's private config is
invisible to the other 99 agents and every other manager. Approved with two
conditions: the skill must carry a header naming `Team/LEARN.md` at `2bca290`
as authoritative and itself as a cache, and its first actions must re-read the
briefing when `MAP.md` says it changed. Same fix as `INTERIM_COMMAND.md` --
two documents that disagree is the failure, so one defers in writing.

Not yet known: whether that manager *acts* or only writes well. The test is to
ask it for the state and the twelve gates unaided, and see whether digests come
back or a summary does.

**Owner's standing instruction, 2026-08-21: do not read extra files. Token
cost is watched.** `MAP.md` is the orienting read; open anything else only to
change it.


**`Team/LEARN.md` is the briefing.** 415 lines, written 2026-08-21 to be
pasted whole into a fresh agent as a `/learn` prompt -- the Antigravity IDE
acting as interim manager, a local Claude, anyone. It carries the one rule,
the twelve gates with what each let through before it existed, all twelve
constitution rules **each with the incident that bought it**, how orders are
given, the handover rules for the owner's shell, the reporting contract, and
Part 10: the gaps that are NOT solved.

It is written on the assumption that a briefing is weak. `agy` gets a fresh
process per task, so nothing told to a worker persists; a manager pasted this
once will forget it. **The gates are the mechanism; this document explains
why they are not negotiable.** Its closing paragraph is the Architect's own
four failures of the day, because a manager who believes the author of the
rules was immune to them will not run the checks.

`Team/INTERIM_COMMAND.md` is superseded by it and says so at the top. It says
"four gates"; there are six. Two manager documents disagreeing is the failure
this project keeps paying for, so one of them now defers to the other in
writing.

## Giving orders

Managers do not message containers. They commit task files:

    Team/tasks/pending/<id>_<slug>.json

Workers ask git what is addressed to them:

    python Tools/poll_tasks.py --me agw-acc4-w03 --pull

Tasks are **assigned**, never claimed -- each names its `assigned_to`
container, so 99 workers never race for the same file. Required keys: `id`,
`assigned_to`, `title`, `question`, `falsifiable_by`, `touches`. A task that
cannot say what result would end it is a wish, and `--validate` rejects it.

## Before you stop, whoever you are

**9 gates retired 2026-09-11, not weakened -- their subject matter is
gone, not merely passing.** `check_cloud_stamp`/`probe_check_cloud_stamp`
(Cloud/colab/ deleted), `probe_icd_direct_verdict` (the Kaggle-Vulkan
diagnostic it pinned is deleted), `check_target_profile`/
`probe_check_target_profile` (the UE5 renderer pins it enforced are
deleted, `Config/DefaultEngine.ini` is gone), `probe_kaggle_gpu_default`
(Kaggle was Unreal-GPU-only), `probe_ue_cook_platform` (`Tools/ue.py` is
deleted), `check_district_build_proof`/`probe_check_district_build_proof`
(`Districts/`, `Content/Maps/` deleted). Removing a gate whose subject no
longer exists is not the same failure mode as removing one to let a red
suite pass -- see `Team/CHANGELOG.md`'s 2026-09-11 entry for the full
Unreal-to-Ren'Py cleanup this was part of. 49 gates remain, comfortably
over `run_gates.py`'s `MIN_GATES = 25` floor.

    python Tools/check_changelog.py      # every commit written down
    python Tools/verify_claims.py --all  # no report cites a file that is not there
    python Tools/poll_tasks.py --validate
    python Tools/check_names.py          # no tool references a name that is bound nowhere
    python Tools/team_lint.py            # every report has a verdict, a falsification and its gaps
    python Tools/check_reviews.py        # no report is reviewed by its own author
    python Tools/probe_check_changelog_invisible.py  # no commit subject carries an invisible character
    python Tools/probe_check_changelog_merge_exempt.py  # a merge commit is exempt by parent count, never by title
    python Tools/check_org.py            # the company structure still holds
    python Tools/probe_check_org.py      # ...and that check can still fail
    python Tools/probe_role_brief.py     # every container is told who it is
    python Tools/check_review_guild.py   # a reviewer is qualified, not merely named
    python Tools/probe_check_review_guild.py  # ...and that check can still fail
    python Tools/check_handover.py      # MAP.md is still cheap enough to read
    python Tools/probe_check_handover.py     # ...and that check can still fail
    python Tools/probe_dispatch_runs.py  # a dispatch that started nothing is not a start
    python Tools/check_cited_flags.py    # no report cites a flag its tool has not got
    python Tools/probe_check_cited_flags.py   # ...and that check can still fail
    python Tools/probe_watch_runs.py     # the Actions watcher still reads a run correctly
    python Tools/probe_run_worker.py     # every task still carries the rules with it
    python Tools/probe_worker_deliver.py # a delivery still lands, and keeps the last one
    python Tools/check_digest_provenance.py  # a report's numbers exist outside its own prose
    python Tools/probe_check_digest_provenance.py # ...and that check can still fail
    python Tools/check_archive_index.py  # every archived block says where its conclusion went
    python Tools/probe_check_archive_index.py # ...and that check can still fail
    python Tools/probe_hook_guard_bash.py # the repeated-mistake hook still refuses, and only what it should
    python Tools/check_rules_index.py  # Team/RULES.md still matches the tools it describes
    python Tools/check_map_frontier.py   # MAP.md names the newest measured run
    python Tools/probe_check_map_frontier.py # ...and that check can still fail
    python Tools/probe_hook_gates_stop.py # the Stop hook still refuses a red suite, and stays silent on a green one
    python Tools/check_struck_terms.py # a term the owner struck has not come back
    python Tools/probe_check_struck_terms.py # ...and that check can still fail
    python Tools/probe_archive_map_blocks.py # the MAP trim tool still refuses, and never touches the gate list
    python Tools/check_morning_freshness.py # the morning report is not more than 48h stale
    python Tools/probe_check_morning_freshness.py # ...and that check can still fail
    python Tools/check_task_quality.py # a pending task names something checkable, or it is rejected
    python Tools/probe_check_task_quality.py # ...and it rejects the real d523395 task, not a lookalike
    python Tools/check_digest_grep_contract.py # no workflow greps a Python digest with a no-space pattern
    python Tools/probe_check_digest_grep_contract.py # ...and it tells a grep READ from a printf WRITE
    python Tools/check_map_pending_blockers.py # a pending task's blocker term is not archive-only
    python Tools/probe_check_map_pending_blockers.py # ...and it fails on the real 0bcc5b3 incident
    python Tools/check_working_branch.py # HEAD is the working branch, not a stray claude/issue-N-* one
    python Tools/probe_check_working_branch.py # ...and it fails on the real issue #66 branch, 9a2dfda
    python Tools/check_heredoc_backticks.py # no unquoted heredoc's body has a live backtick command substitution
    python Tools/probe_check_heredoc_backticks.py # ...and it fails on the real 982d6b1 incident, not a lookalike
    python Tools/check_gate_commit_reachable.py # a gate_suite digest's own commit hash still exists somewhere
    python Tools/probe_check_gate_commit_reachable.py # ...and it fails on the real 847e9fb incident, not a lookalike
    python Tools/check_status_feed_freshness.py # the cross-account status feed is not more than 3h stale
    python Tools/probe_check_status_feed_freshness.py # ...and it rejects stale, malformed, and missing status.json alike

**`team_lint.py` existed all along and was never in this list.** Run against
the reports on 2026-08-21 it rejected four of nine, three of them written by
the Architect -- including a report arguing at length that a claim needs a
falsification, which had no falsification section. A gate nobody runs is a
preference. That is the whole lesson of this project, applied to itself.

The fourth was added 2026-08-21 after `bootstrap_containers.py` shipped
referencing `REPO_PATH`, a constant that exists in `worker_git.py` and not
there. Every invocation died with NameError on the owner's machine, five
commands in a row, and nothing caught it: the syntax was valid and the probe
suite never executed that branch. It reports a name only if it is bound
nowhere in the file, so it has no false positives and can be a gate. It has no
dependencies, deliberately -- pyflakes does this better and is not installed
on the owner's machine.

Then update this file.

---

Last update: 2026-08-21. Owner revoked the classic token and created a
fine-grained one; `--install-token` has still not run. Task 006 queued to
measure worker-git inside ONE container before 99 rely on it.
`--check` was found twice reporting what it had not measured (`5a75a97`,
`71936cb`); both fixed and both now fail on the pre-fix file.
`agw-acc1-w01` re-synced to `b30b350` and holds the token.
**Task 006 is BLOCKED on two things: `b30b350` is not on origin, and the file
sync leaves a dirty tree that `poll_tasks --pull` cannot merge (`59aa3d7`).**
Earlier: acc3 restored to Pro; company is 99. Task 001 closed.
Cycle closed: gateway-auth accepted, task-001-instrument REJECTED.
All 99 containers bootstrapped (`7b5c17b`). Token not installed; worker-git
still unexercised against a real container.

```
TEHRAN: BLIND SPOT
|
+-- GAME (headless UE 5.8, GTX 960M)                      [not touched today]
|   +-- Districts/district_01_valiasr.json ......... built, lit, probed OK
|   +-- lighting ............... SETTLED  sun 25 lux / fill 40 lux
|   +-- Persian text ........... SOLVED   Runtime font + Slate, 8/8 cases
|   +-- rotator bug ............ FIXED    tbs_core.rotator(), contract probe
|   +-- sky light .............. REMOVED  measured 0.000 effect. No ambient.
|   +-- camera exposure ........ DEAD END spread exactly 0.0 on every lever
|   \-- calibrate_exposure.py RETIRED 2026-08-21, superseded, never re-run
|
+-- COMPANY (99 agents, 9 accounts, git is the only channel)
|   +-- Team/CONSTITUTION.md ... 12 rules, each bought by a named failure
|   +-- Team/PROTOCOL.md ....... who owns which files, tasks down, reports up
|   +-- Team/ROSTER.md ......... A-I mapped to acc1..acc9; ALL 99 in service
|   \-- Team/MAP.md ............ this file
|
+-- GATEWAY  (Gateway/gateway_win.py)                          [DONE, pushed]
|   +-- auth ................... FIXED    bearer token, all 4 routes
|   +-- startup ................ FIXED    refuses to run without a token
|   +-- container-name injection  NEVER EXISTED -- premise was wrong
|   |                            name comes from fixed 99-roster queue
|   +-- prompt injection ....... NOT POSSIBLE  argv list, no shell
|   +-- probes ................. 7/7 pass, and FAIL on the pre-fix file
|   +-- VERIFIED ............... live container agw-acc1-w01 (Task 003, 3/3 pass)
|   \-- TUNNEL ................. still closed. Use SSH port-forward, not TLS.
|
\-- TASK 001  "tell a lapsed account from a healthy one"   [CLOSED - overtaken]
    +-- outcome ............... owner put a Pro account into acc3.
    |                           All 9 accounts Pro. No known-different case
    |                           remains, so the detector cannot be calibrated.
    +-- Tools/team_health.py .. KEPT. 8/8 probes. Reusable for any
    |                           "does field X separate account A from the rest"
    +-- reusable byproducts ... reads tokens from all 99 containers;
    |                           path + exec-user + nested-JSON all solved
    \-- CORRECTION (owner) .... 400/401 from these endpoints fire SPURIOUSLY
                                with a good credential behind them. This tool
                                read them as "expired token" and wrote off
                                three healthy accounts. Now treated as a
                                failure to measure, never as a value.
```

## Branches

| branch | what is on it |
|---|---|
| `claude/project-zero` | the trunk: game, Team docs, acc_state samples |
| `claude/gateway-auth-fix-nr7k0b` | **current.** project-zero + gateway auth + task 001 |

**Remote branch accounting, 2026-09-07.** 33 remote branches exist (`git
branch -a`, excluding the symbolic `origin/HEAD` ref). Measured with
`git merge-base --is-ancestor <branch> origin/claude/gateway-auth-fix-nr7k0b`
against tip `32d9b97` (after this issue's #60/#61 merges). **No branch was
deleted in this pass** -- deletion is irreversible and is the owner's call;
this only records what is safe to consider.

| branch | status | evidence |
|---|---|---|
| `claude/issue-59-20260906-0957` | DUPLICATE | `Tools/run_gates.py` byte-identical to base; the same change already landed in base as `009bc23` |
| `claude/issue-20-20260904-0837` | STALE | only diff from base is `tbs-ask.yml`'s `max-turns 150`->`80` (not `80` vs a claimed `150`-everywhere -- verified by diff, not assumed); its real work, dropping the PR flow, is already in base |
| `claude/issue-17-20260904-0820` | SUPERSEDED | base already has `Reports/archive_map_blocks/dry_run_2026-09-0{4,5}.txt`, and this file already cites `archive_map_blocks` |
| `workers/agw-acc1-w01` .. `agw-acc9-w01` (9) | unmerged, one commit each, untouched since 2026-09-02 | `git merge-base --is-ancestor` fails for all nine |
| 18 other `claude/*` branches | MERGED, safe to ignore | `git merge-base --is-ancestor` passes for all 18 |
| `claude/issue-66-20260907-0857` | MERGED by issue #67 (content merge, not fast-forward) -- **safe to delete, not deleted here; deletion is the owner's call** | its four commits (`6192331`, `d089235`, `760c643`, `9a2dfda`) are folded into this branch's merge commit; `MAP.md`/`MAP_ARCHIVE.md` conflicts resolved by hand, nothing from either side lost or duplicated |

18 merged, not the 19 an earlier unpushed measurement claimed -- recount
before trusting that number again.

---

**History lives in `Team/MAP_ARCHIVE.md`.** Everything there is superseded
unless this file repeats it. It is the reasoning behind the lines above -- read
it when you need to know why, never to find out where things stand.

`Tools/check_handover.py` fails if this file passes **900 lines**; when it
does, move the oldest dated blocks into the archive until it is back to
**600**, and never delete one. (This paragraph named `Tools/check_map_size.py`
until 2026-08-26. **No such file has ever existed** -- `verify_claims` checks
the paths reports cite, not the ones MAP.md cites, so it sat here unread and
uncaught. Anyone who went looking for it: it is `check_handover`.)
