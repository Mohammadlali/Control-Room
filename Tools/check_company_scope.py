#!/usr/bin/env python3
"""Team/COMPANY_SCOPE.md (for humans) and Team/company_scope.json (for
route_topic.py) must describe the same accounts and projects. A change made
to only one of them is exactly the kind of drift this project's gates exist
to catch: the router would act on facts the human-readable doc no longer
states, or the doc would promise routing the router cannot actually do.

Checks, each one a real failure mode seen elsewhere in this project's
history when a JSON and its prose twin were edited separately:
  - every account login in the JSON appears somewhere in the markdown
  - every project's host_repo in the JSON appears somewhere in the markdown
  - ACC0 is marked management_only in the JSON (the one hard invariant)
  - the JSON parses at all

Exit 1 on any failure. ASCII only.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "Team", "company_scope.json")
MD_PATH = os.path.join(ROOT, "Team", "COMPANY_SCOPE.md")


def main():
    problems = []

    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            scope = json.load(f)
    except (OSError, ValueError) as exc:
        print("FAIL: {0} did not parse: {1}".format(JSON_PATH, exc))
        return 1

    with open(MD_PATH, encoding="utf-8") as f:
        md = f.read()

    for acc_id, acc in scope["accounts"].items():
        if acc["login"] not in md:
            problems.append("account {0} login '{1}' not named in {2}".format(
                acc_id, acc["login"], os.path.basename(MD_PATH)))

    for name, proj in scope["projects"].items():
        if proj["host_repo"] not in md:
            problems.append("project '{0}' host_repo '{1}' not named in {2}".format(
                name, proj["host_repo"], os.path.basename(MD_PATH)))

    acc0 = scope["accounts"].get("ACC0", {})
    if not acc0.get("management_only"):
        problems.append("ACC0 is not marked management_only in company_scope.json")

    if problems:
        print("FAIL: {0} problem(s)".format(len(problems)))
        for p in problems:
            print(" - " + p)
        return 1

    print("PASS: company_scope.json and COMPANY_SCOPE.md agree "
          "({0} accounts, {1} projects)".format(
              len(scope["accounts"]), len(scope["projects"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
