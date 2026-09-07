#!/usr/bin/env python3
"""probe_check_issue_protocol.py -- probe for check_issue_protocol gate."""
import subprocess
import sys
import json


def main():
    r = subprocess.run(
        ['python3', 'Tools/check_issue_protocol.py'],
        capture_output=True, text=True
    )
    # exit 0 (pass) and exit 1 (violations found) are both valid
    ok = r.returncode in (0, 1)
    data = {
        "cases_run": 1,
        "cases_failed": 0 if ok else 1,
        "failing_cases": [] if ok else ["gate_runs_cleanly"],
        "gate_exit_code": r.returncode
    }
    status = "pass" if ok else "fail"
    print(json.dumps({"probe": "check_issue_protocol", "status": status, "data": data}))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
