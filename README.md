# Control-Room

> **Central Command Center & Governance for the whole organization — hosted
> on `ACC0` (`Mohammadlali`), the org's dedicated management account.**

`Control-Room` is the operational headquarters for a 9-account GitHub
organization (`ACC0`..`ACC8`). It orchestrates projects, dispatches cloud
workers, and enforces mechanical verification gates across every repository
the org runs — but it never runs another project's code itself. **`ACC0`
does management only.** Each project has exactly one canonical host
elsewhere in the org; see `Team/COMPANY_SCOPE.md` for the full map.

---

## The one rule this repo exists to enforce

**A topic router, not a round-robin.** An issue opened here is classified by
`Tools/route_topic.py` against `Team/company_scope.json` before anything
runs:

- About Control-Room itself (governance, accounts, dispatch) -> handled
  locally, dispatched to the org's `agw-workers` fleet round-robin.
- About a project hosted elsewhere (TEHRAN: BLIND SPOT on `ACC6`, AirboxVIP
  Coffeenet on `ACC1`, ...) -> **forwarded** as a fresh `@agy` issue on that
  project's own repo, using that account's own credential. Control-Room
  never executes another project's work itself.
- Topic unclear -> no dispatch. The router asks for a `project:` label
  instead of guessing -- a wrong forward burns another account's quota on
  the wrong project.

---

## Architecture

```
Control-Room/
├── AGENTS.md                  # Non-negotiable laws and operational invariants
├── README.md                  # System overview and entry point (this file)
├── Team/
│   ├── COMPANY_SCOPE.md       # Which account hosts which project, and why
│   ├── company_scope.json     # Same facts, machine-readable (route_topic.py reads this)
│   ├── WHERE_WE_ARE.md        # Instant pulse of current tasks and next steps (Persian)
│   ├── MAP.md                 # Living workstream status (target: 600 lines)
│   ├── MAP_ARCHIVE.md         # Historical workstream rollover
│   ├── CHANGELOG.md           # Commit journal with impact analyses
│   ├── START_HERE.md          # Persian onboarding guide for users & agents
│   ├── tasks/                 # File-based task lifecycle
│   │   ├── pending/           # Tasks awaiting assignment
│   │   ├── in_progress/       # Active work items
│   │   └── done/              # Completed and verified tasks
│   └── reports/               # Standardized empirical test reports
├── Tools/                     # Mechanical verification gates and hooks
│   ├── run_gates.py           # Master gate suite runner (silent on pass)
│   ├── route_topic.py         # The topic classifier described above
│   ├── check_company_scope.py # Keeps COMPANY_SCOPE.md and its JSON twin in sync
│   ├── check_changelog.py     # Ensures every commit is recorded
│   ├── poll_tasks.py          # Validates task structure & falsifiable_by
│   └── verify_claims.py       # Prevents hallucinated file citations
└── .github/
    └── workflows/
        ├── control-agy.yml    # Topic-routed issue & comment listener
        ├── batch-dispatch.yml # 99-slot round-robin batch dispatch
        └── control-gates.yml  # Cloud CI verification on GitHub Actions
```

---

## Quick Start for Users & Operators

- **راهنمای شروع به زبان فارسی:** مستند جامع [Team/START_HERE.md](Team/START_HERE.md) را مطالعه فرمایید.
- **واگذاری تسک به ایجنت:** کافی است در بخش **Issues** یک ایشو جدید باز کرده یا در کامنت، با تگ `@agy` دستور خود را بنویسید. موضوع ایشو مشخص می‌کند که کار در همین ریپو انجام می‌شود یا به ریپوی پروژه‌ی مربوطه ارسال می‌شود.
- **گردش کار خودکار:** بات AGY به طور خودکار فراخوانی شده، موضوع را تشخیص می‌دهد، وظیفه را به مقصد درست می‌سپارد، دروازه‌های اعتبارسنجی را بررسی و تغییرات را مستقیماً روی برنچ `main` تحویل می‌دهد.

---

## Quick Start for AI Agents

1. Read **[`AGENTS.md`](AGENTS.md)** first.
2. Run `git pull origin main`.
3. Read **[`Team/WHERE_WE_ARE.md`](Team/WHERE_WE_ARE.md)** and **[`Team/COMPANY_SCOPE.md`](Team/COMPANY_SCOPE.md)** for immediate status and who owns what.
4. Execute required work, update `Team/CHANGELOG.md`, and run:
   ```bash
   python Tools/run_gates.py
   ```
5. Push to `main` and quote the push output line.
