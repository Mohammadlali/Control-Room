# Agent Rules for Control-Room (07-Stack)

Applies to every agent, manager, and tool interacting with this repository.
The non-negotiable laws below are written once here and enforced mechanically.

---

## 1. Branch and Delivery
- Work happens on `main`.
- Commit and push directly to `main` unless an explicit branch is requested by the owner.
- A commit is NOT a delivery. A delivery is completed only when `git push` succeeds and is verified.

## 2. Living Documentation as Single Source of Truth
- Orient yourself from `Team/WHERE_WE_ARE.md` and `Team/MAP.md` at the start of every session.
- Never dump or `cat` entire large source trees. Use targeted line inspection (`grep`, `sed -n`, slice notation).
- Do not guess the state of projects: check `Team/MAP.md`.

## 3. Record Everything and Push
Every turn or session that modifies files must do all four before stopping:
1. **Add an entry to `Team/CHANGELOG.md`** with the real short hash. Explain what changed and what it means for dependent components.
2. **Push.** `git push -u origin main`.
3. **Quote the push line** in your report (the `a1b2c3d..e4f5g6h` output).
4. **Update `Team/WHERE_WE_ARE.md` and `Team/MAP.md`** so the next session does not re-derive state.

## 4. Gates Before You Stop
Before completing any turn or milestone, the verification gate suite must be green:

```bash
python Tools/run_gates.py
```

- If all gates pass: zero output (silent success).
- If any gate fails: the stop is refused. Fix the failure before pushing. Never weaken a gate to let broken code pass.

## 5. No Claim Without a Probe
- Never assert "tests passed", "working fine", or "fixed" without providing the exact probe command, the exit code, and the output.
- All task definitions in `Team/tasks/` MUST include `falsifiable_by`: the empirical test that defines success or refutes failure.
