#!/usr/bin/env python3
"""
check_issue_protocol.py
Gate: Verifies that AGY-processed issues follow the Issue Response Protocol.
Checks issues with @agy in body, closed in last 7 days, have:
  1. A planning checklist comment (contains 'Todo list' and '- [x]')
  2. A final report comment (contains '**Done**')
Requires gh CLI configured with GH_TOKEN.
Pass: silent (exit 0). Fail: print violations, exit 1.
If gh CLI unavailable or API unreachable: exit 0 silently (offline-safe).
"""
import subprocess
import json
import sys
import os
import re
from datetime import datetime, timezone, timedelta

REPO = "mohammadlali0707-stack/Control-Room"
DAYS_BACK = 7
CHECKLIST_PATTERN = re.compile(r'- \[x\]', re.IGNORECASE)
DONE_PATTERN = re.compile(r'\*\*Done\*\*|^Done\b', re.MULTILINE)
TODO_PATTERN = re.compile(r'Todo list|Working on it', re.IGNORECASE)


def gh(cmd):
    env = dict(os.environ)
    if 'GH_TOKEN' not in env and 'GITHUB_TOKEN' not in env and 'CTRL_TOKEN' in env:
        env['GH_TOKEN'] = env['CTRL_TOKEN']
    result = subprocess.run(['gh'] + cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def main():
    since = (datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)).strftime('%Y-%m-%d')
    raw = gh(['issue', 'list', '--repo', REPO, '--state', 'closed',
              '--search', f'@agy closed:>{since}', '--json', 'number,body',
              '--limit', '30'])
    if not raw:
        # gh CLI unavailable or not authenticated - skip silently
        sys.exit(0)

    try:
        issues = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    agy_issues = [i for i in issues if '@agy' in (i.get('body') or '')]
    if not agy_issues:
        sys.exit(0)

    violations = []
    for issue in agy_issues:
        n = issue['number']
        data = gh(['issue', 'view', str(n), '--repo', REPO, '--json', 'comments'])
        if not data:
            continue
        try:
            bodies = [c.get('body', '') for c in json.loads(data).get('comments', [])]
        except json.JSONDecodeError:
            continue

        has_checklist = any(
            TODO_PATTERN.search(b) and CHECKLIST_PATTERN.search(b)
            for b in bodies
        )
        has_final_report = any(DONE_PATTERN.search(b) for b in bodies)

        if not has_checklist:
            violations.append(
                f"  Issue #{n}: missing planning checklist (Todo list + checked items)"
            )
        if not has_final_report:
            violations.append(
                f"  Issue #{n}: missing final report comment (**Done**)"
            )

    if violations:
        print("FAIL check_issue_protocol:")
        for v in violations:
            print(v)
        sys.exit(1)


if __name__ == '__main__':
    main()
