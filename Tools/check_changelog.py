#!/usr/bin/env python3
"""
check_changelog.py -- Enforces that every commit in git is recorded in Team/CHANGELOG.md.
Exempt: commits starting with 'changelog: record'.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG = os.path.join(ROOT, "Team", "CHANGELOG.md")


def main():
    if not os.path.exists(CHANGELOG):
        print(f"FAIL: {CHANGELOG} does not exist.")
        return 1

    with open(CHANGELOG, "r", encoding="utf-8") as f:
        changelog_content = f.read()

    # Get recent commits
    try:
        proc = subprocess.run(
            ["git", "log", "--oneline", "-n", "20"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except Exception as exc:
        print(f"FAIL: git log failed: {exc}")
        return 1

    unrecorded = []
    for line in proc.stdout.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split(" ", 1)
        short_hash = parts[0]
        msg = parts[1] if len(parts) > 1 else ""

        # Exempt changelog recording commits
        if msg.lower().startswith("changelog: record"):
            continue

        if short_hash not in changelog_content:
            unrecorded.append(f"{short_hash} ({msg})")

    if unrecorded:
        print("FAIL: The following commits are missing from Team/CHANGELOG.md:")
        for item in unrecorded:
            print(f"  - {item}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
