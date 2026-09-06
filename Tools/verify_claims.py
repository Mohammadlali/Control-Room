#!/usr/bin/env python3
"""
verify_claims.py -- Checks that files cited in tasks' 'touches' exist in the repository.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_DIR = os.path.join(ROOT, "Team", "tasks")


def main():
    task_files = glob.glob(os.path.join(TASKS_DIR, "**", "*.json"), recursive=True)
    missing = []

    for tf in task_files:
        try:
            with open(tf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        touches = data.get("touches", [])
        for cited in touches:
            target = os.path.join(ROOT, cited)
            if not os.path.exists(target):
                missing.append(f"{os.path.relpath(tf, ROOT)} cites non-existent file: '{cited}'")

    if missing:
        print("FAIL: Claims verification failed (cited files missing):")
        for m in missing:
            print(f"  - {m}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
