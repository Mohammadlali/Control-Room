#!/usr/bin/env python3
"""
poll_tasks.py -- Validates structured task JSON files in Team/tasks/.
Enforces that every task has: id, assigned_to, title, question, falsifiable_by, touches.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_DIR = os.path.join(ROOT, "Team", "tasks")
REQUIRED_FIELDS = ["id", "assigned_to", "title", "question", "falsifiable_by", "touches"]


def validate_tasks():
    patterns = [
        os.path.join(TASKS_DIR, "pending", "*.json"),
        os.path.join(TASKS_DIR, "in_progress", "*.json"),
        os.path.join(TASKS_DIR, "done", "*.json"),
    ]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))

    errors = []
    for file_path in files:
        rel_path = os.path.relpath(file_path, ROOT)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            errors.append(f"{rel_path}: Invalid JSON - {exc}")
            continue

        for field in REQUIRED_FIELDS:
            val = data.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors.append(f"{rel_path}: Missing or empty required field '{field}'")
            elif field == "touches" and not isinstance(val, list):
                errors.append(f"{rel_path}: Field 'touches' must be a list of paths")

    if errors:
        print("FAIL: Task schema validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    return 0


def main():
    if "--validate" in sys.argv or len(sys.argv) == 1:
        return validate_tasks()
    print("Usage: poll_tasks.py [--validate]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
