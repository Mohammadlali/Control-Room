#!/usr/bin/env python3
"""
check_source_quality.py -- Gate: verify that Team/WHERE_WE_ARE.md references at least one git hash.

Enforces analysis methodology doctrine:
- If Team/WHERE_WE_ARE.md does not exist: pass (exit 0, silent).
- If Team/WHERE_WE_ARE.md is empty: pass (exit 0, silent).
- If Team/WHERE_WE_ARE.md exists and is non-empty, it MUST contain at least
  one git commit hash (7+ hex characters) as an empirical reference.
  Exit 0 = git hash reference found (silent).
  Exit 1 = no git hash reference found (prints failure report).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "Team", "WHERE_WE_ARE.md")

# Matches a git commit hash: 7 or more hex characters
GIT_HASH_RE = re.compile(r'\b[0-9a-fA-F]{7,64}\b')


def main():
    if not os.path.exists(TARGET):
        return 0

    try:
        with open(TARGET, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:
        sys.stderr.write(f"FAIL: Error reading {TARGET}: {exc}\n")
        return 1

    if not content.strip():
        return 0

    matches = GIT_HASH_RE.findall(content)
    if not matches:
        print("FAIL: Team/WHERE_WE_ARE.md must contain at least one git hash reference (7+ hex characters).")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
