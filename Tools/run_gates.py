#!/usr/bin/env python3
"""
run_gates.py -- Master Verification Gates Runner for Control-Room.
Silent on full pass (exit 0, zero output = zero token consumption).
Prints concise diagnostic and exits non-zero if any gate fails.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATES = [
    ("check_changelog", [sys.executable, os.path.join(ROOT, "Tools", "check_changelog.py")]),
    ("poll_tasks", [sys.executable, os.path.join(ROOT, "Tools", "poll_tasks.py"), "--validate"]),
    ("verify_claims", [sys.executable, os.path.join(ROOT, "Tools", "verify_claims.py")]),
    ("check_links", [sys.executable, os.path.join(ROOT, "Tools", "check_links.py")]),
    ("check_source_quality", [sys.executable, os.path.join(ROOT, "Tools", "check_source_quality.py")]),
    ("check_issue_protocol", [sys.executable, os.path.join(ROOT, "Tools", "check_issue_protocol.py")]),
]


def main():
    failed = []
    for name, cmd in GATES:
        res = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if res.returncode != 0:
            failed.append((name, res.stdout.strip()))

    if not failed:
        # Zero output on pass - saves tokens completely
        sys.exit(0)

    # Print failures
    sys.stderr.write("GATES FAILED in Control-Room:\n")
    for name, output in failed:
        sys.stderr.write(f"\n--- Gate: {name} ---\n")
        sys.stderr.write(output + "\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
