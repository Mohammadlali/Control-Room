# Control-Room

> **Central Command Center & Autonomous Project Governance for 07-Stack (`mohammadlali0707-stack`)**

`Control-Room` is the operational headquarters for orchestrating projects, dispatching cloud workers, and enforcing rigorous software verification across repositories.

---

## 🏛️ Architecture

```
Control-Room/
├── AGENTS.md                  # Non-negotiable laws and operational invariants
├── README.md                  # System overview and entry point
├── Team/
│   ├── WHERE_WE_ARE.md        # Instant pulse of current tasks and next steps
│   ├── MAP.md                 # Living workstream status (target: 600 lines)
│   ├── MAP_ARCHIVE.md         # Historical workstream rollover
│   ├── CHANGELOG.md           # Commit journal with impact analyses
│   ├── START_HERE.md          # 5-step onboarding guide for any agent
│   ├── tasks/                 # File-based task lifecycle
│   │   ├── pending/           # Tasks awaiting assignment
│   │   ├── in_progress/       # Active work items
│   │   └── done/              # Completed and verified tasks
│   └── reports/               # Standardized empirical test reports
├── Tools/                     # Mechanical verification gates and hooks
│   ├── run_gates.py           # Master gate suite runner (silent on pass)
│   ├── check_changelog.py     # Ensures every commit is recorded
│   ├── poll_tasks.py          # Validates task structure & falsifiable_by
│   └── verify_claims.py       # Prevents hallucinated file citations
└── .github/
    └── workflows/
        └── control-gates.yml  # Cloud CI verification on GitHub Actions
```

---

## 🚀 Quick Start for New Agents

1. Read **`AGENTS.md`** first.
2. Run `git pull origin main`.
3. Read **`Team/WHERE_WE_ARE.md`** for immediate status.
4. Execute required work, update `Team/CHANGELOG.md`, and run:
   ```bash
   python Tools/run_gates.py
   ```
5. Push to `main` and quote the push output line.
