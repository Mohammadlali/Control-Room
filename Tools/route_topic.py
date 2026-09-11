#!/usr/bin/env python3
"""Decide which project an issue is about, from Team/company_scope.json.

Used by .github/workflows/control-agy.yml BEFORE dispatch: an issue opened
on Control-Room is either about Control-Room itself (handled locally, same
as before) or about a project hosted on a different account (TBS on ACC6,
AirboxVIP on ACC1 today) and must be FORWARDED there rather than executed
here. Deterministic and label-first on purpose: a topic router that guesses
wrong burns another account's quota on the wrong project and hands its
`@agy` context it should never have seen.

CLI usage (what the workflow actually calls):
    python3 Tools/route_topic.py --title "..." --body "..." --labels "a,b"
Prints one JSON object to stdout. Exit code is always 0 -- "unclear" is a
valid, successful classification, not a tool failure.

Library usage: `classify(title, body, labels)` returns the same dict.
"""

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPE_PATH = os.path.join(ROOT, "Team", "company_scope.json")


def load_scope(path=SCOPE_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def classify(title, body, labels="", scope=None):
    scope = scope or load_scope()
    projects = scope["projects"]
    text = ((title or "") + " " + (body or "")).lower()
    label_list = [l.strip().lower() for l in (labels or "").split(",") if l.strip()]

    for label in label_list:
        if label.startswith("project:"):
            key = label.split(":", 1)[1].strip()
            if key in projects:
                return {"decision": "route", "project": key,
                        "via": "label", **projects[key]}
            return {"decision": "unclear",
                     "reason": "label names unknown project '{0}'".format(key)}

    hits = {}
    for name, proj in projects.items():
        count = sum(1 for kw in proj["keywords"] if kw in text)
        if count:
            hits[name] = count

    if not hits:
        return {"decision": "route", "project": "control-room",
                "via": "default", **projects["control-room"]}

    ranked = sorted(hits.items(), key=lambda kv: -kv[1])
    if len(ranked) == 1 or ranked[0][1] > ranked[1][1]:
        name = ranked[0][0]
        return {"decision": "route", "project": name,
                "via": "keywords", "hits": hits, **projects[name]}

    return {"decision": "unclear",
            "reason": "tied keyword matches across projects: {0}".format(
                ", ".join(sorted(hits))),
            "hits": hits}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default="")
    ap.add_argument("--body", default="")
    ap.add_argument("--labels", default="")
    args = ap.parse_args()
    result = classify(args.title, args.body, args.labels)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
