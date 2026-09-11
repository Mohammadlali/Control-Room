# Company Scope — who does what, across all 9 accounts

**Why this file exists.** Before any issue can be routed by topic, the topics
themselves have to be named: which account hosts which project, and which
account may NOT host project work at all. This file is the human-readable
account-scope reference; the topic router itself reads the equivalent facts
from `Team/company_scope.json`, its machine-readable twin.
`Tools/check_company_scope.py` mechanically checks the two agree (every
account/repo pair named in the table below also appears in the JSON, and
vice versa) so this file cannot drift from what the router actually does.
Change both files together, in the same commit.

## The rule, stated once

**ACC0 (`Mohammadlali`, this account) does management only.** No game, no
website, no other project's code is ever developed here. Its only repo doing
substantive work is `Control-Room` itself (this repo) plus its own
`agw-workers` runner fleet, which executes Control-Room's own tasks — never
another project's.

**Every other project has exactly one canonical host repo.** A project's
code, issues, and history live in ONE place. An account can additionally
serve as a compute worker for TBS's own internal domain ring (see below)
without that making it TBS's host — hosting and working are different roles,
and only one account holds the host role per project.

## Routing table

| Account | GitHub login | Nickname | Hosts (canonical repo) | Also works TBS ring domain |
|---|---|---|---|---|
| ACC0 | `Mohammadlali` | 1997 | **Control-Room** (this repo) — management only | — (left the ring permanently, 2026-09-10) |
| ACC1 | `momonakikugava-pixel` | Momona | `AirboxVIP_Coffeenet` | D — Verification and Integration/CI (primary) |
| ACC2 | `lali94m-max` | 94 | — (no project of its own yet) | I — Tools and audit (primary), D (secondary) |
| ACC3 | `ngocgminh5-debug` | ngocg | — (no project of its own yet) | A — Visual Assets and AI Generation (primary), I (secondary) |
| ACC4 | `hmmletssee7-design` | lets | — (no project of its own yet) | B — VN Engine and Flow (primary), A (secondary) |
| ACC5 | `kidding602` | Just | — (no project of its own yet) | C — Persian UI and Typography QA (primary), O (secondary) |
| ACC6 | `mohammadlali0707-stack` | 07 | **`Claud-Cloud-Project`** — the ONLY home of TEHRAN: BLIND SPOT (TBS), as of 2026-09-11 | O — Operations and Fleet Orchestration (primary), B (secondary) |
| ACC7 | `mohammad97okk` | M2 | — (no project of its own yet) | E — Android Build and Packaging (primary), C (secondary) |
| ACC8 | `moradzahra85-png` | zahra | — (no project of its own yet) | F — Narrative and Audio (primary), E (secondary) |

The "TBS ring domain" column is `Claud-Cloud-Project`'s OWN internal
dispatch, defined in that repo's `Team/org.json`. Control-Room's router
does not re-implement it: an issue identified as TBS-topic is forwarded
whole to ACC6's `Claud-Cloud-Project`, which does its own domain-ring
dispatch from there via its own `agy-issue-bot.yml`.

## What changed 2026-09-11, and why

- **TBS's host moved from ACC0 to ACC6 exclusively.** Until this date, a
  second live copy of `Claud-Cloud-Project` existed on ACC0
  (`Mohammadlali/Claud-Cloud-Project` — the very repo this Control-Room's
  sibling session runs in) and TBS development happened there directly. The
  owner ended that: ACC0 does management only, full stop. Any TBS change
  still made on ACC0's copy (because a live session is already there) must
  be merged into ACC6's copy immediately, not left to diverge — ACC0's copy
  is retiring, not authoritative.
- **The `Mohammadlali0707-stack/Control-Room` repo (a second Control-Room,
  on ACC6) is retired** — this repo, on ACC0, is the one and only Control-Room
  from now on. See `Team/CHANGELOG.md` for the deletion attempt and its
  outcome.
- Accounts ACC2-ACC5, ACC7, ACC8 currently host no project of their own —
  their only role today is as TBS ring workers. That is a fact about today,
  not a rule: if the owner starts a new project, its host account is
  whichever one the owner names, recorded here with a CHANGELOG line, same
  as the AirboxVIP/TBS assignments were.

## Two hard rules the router enforces

1. **No project work is ever dispatched to ACC0's own `agw-workers`.**
   Anything ACC0's fleet runs must resolve to a Control-Room task, never a
   forwarded TBS or AirboxVIP task — the account-scope rule above is a
   platform invariant, not a preference to route around when convenient.
2. **An issue with no determinable topic is never guess-routed.** The router
   posts back asking for a `project:` label rather than picking a target on
   a coin flip — a wrong forward is a wasted worker run on the wrong
   account's quota, and worse, gives that account's `@agy` context about a
   project it may not otherwise touch.
