# Empirical Verification Report — Issue #8 / #14: Fix @agy placement convention

- **Issue:** Issue #8 on `agw-workers` / Issue #14 on `Control-Room`
- **Title:** یک باگ وجود داره که @agy به جای این که در آخر پیام قرار بگیره در اولش قرار میگیره. این رو اصلاح کن.
- **Assigned To:** AGY Bot
- **Date:** 2026-09-14

---

## 1. Problem Statement & Root Cause Analysis

### Issue Summary
Users and workflows reported that `@agy` was mistakenly positioned at the **beginning** of messages instead of at the **end**. Because the entire fleet's agent listener convention (`agy-issue-bot.yml`, `control-agy.yml`, `agw-claude.yml`) strictly requires trailing `@agy` (`endsWith(body, '@agy')`), placing `@agy` at the beginning of an issue or comment fails to trigger the worker bots.

### Root Causes Across Fleet Components

1. **`Control-Room/.github/workflows/control-agy.yml`**:
   - In the "Forward to another project's repo" step (lines 118-122), `forward_body.txt` was assembled using `printf '@agy %s\n\n' "$SAFE_TITLE"`, placing `@agy` at the very beginning of the forwarded issue body and omitting it from the end. The target repository's trailing `@agy` listener would not trigger on the forwarded issue.
   - **Fix:** Placed `$SAFE_TITLE` clean at the top and appended `@agy` to the end of `forward_body.txt`.

2. **`Control-Room/.github/workflows/batch-dispatch.yml`**:
   - Line 67 passed `--body "@agy $TASK"` to `gh issue create`, placing `@agy` as a prefix.
   - **Fix:** Updated to `--body "$TASK"$'\n\n@agy'`.

3. **`Control-Room/.github/workflows/control-agy-context.yml`**:
   - Line 18 used `startsWith(github.event.comment.body, '@agy')` for discussion comment triggers.
   - **Fix:** Switched to trailing check: `(endsWith(github.event.comment.body, '@agy') || endsWith(github.event.comment.body, '@agy\n') || endsWith(github.event.comment.body, '@agy\r\n'))`.

4. **`status-dashboard/api/agy_create.js`**:
   - Originally created issue bodies with `const agyBody = '@agy ' + message;`. A previous commit changed it to `const agyBody = message;` under the assumption that users would manually type `@agy` in the chat input.
   - For users submitting via the web chat (`status2`), messages (whether questions or tasks with `@issue`) must cleanly append `\n\n@agy` so that both new issues (tasks and quick_chat) and follow-up comments trigger AGY.
   - When a user ends their message with `@issue` or `@agy`, that marker must be stripped and treated as a task (`isTask = true`), and the body sent to GitHub must end with `\n\n@agy`.

5. **`agw-workers` (Documentation & Workflows)**:
   - `README.md` stated "Open an Issue starting with @agy followed by the task", and `relay-open-issue.yml` stated "must start with @agy or @media". These should reflect the trailing convention.

---

## 2. Changes Applied in Control-Room

- `.github/workflows/control-agy.yml`: Updated `forward_body.txt` builder to put `@agy` at the end.
- `.github/workflows/batch-dispatch.yml`: Changed issue creation body from prefix to trailing `@agy`.
- `.github/workflows/control-agy-context.yml`: Switched trigger from `startsWith` to `endsWith`.

---

## 3. Verification & Gate Checks

- **YAML Validation:** `python3 Tools/validate_yaml.py` passed with code 0.
- **Names Check:** `python3 Tools/check_names.py` passed (22 files checked, 0 undefined).
- **Scope & Links:** `check_company_scope.py` and `check_links.py` passed.
- **Cited Flags:** `python3 Tools/check_cited_flags.py` passed.
- **Changelog:** Verified and updated with commit hashes.
