#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove check_heredoc_backticks can fail, and does not false-positive on
GitHub Actions' own multiline-output idiom.

Ported from Claud-Cloud-Project's version 2026-09-13. That version resolved
its test fixtures from two real historical commits via `git show` (a real
incident on `write-cr-vision.yml` and a real false-positive on
`Cloud/runner/prebuilt.yml`). Neither commit is reachable from this repo's
own history -- confirmed by running the original probe here unmodified
first, which reported `unmeasured` on all three cases rather than silently
passing. This version uses SYNTHETIC fixtures instead, built to reproduce
the exact same three shapes (a real unescaped-backtick bug, the same
content fixed, and the GH-Actions multiline-output idiom that looks like a
heredoc but is not) -- labelled synthetic rather than claimed as a real
incident, since claiming otherwise would be exactly the kind of over-claim
this project's own gates exist to catch.

Usage:
    python Tools/probe_check_heredoc_backticks.py

Exit 0 pass, 1 fail. ASCII only.
"""

import json
import os
import sys

MARKER = "##TBS##"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "Tools"))
import check_heredoc_backticks as gate  # noqa: E402

# The real shape of the bug this gate exists for: an unquoted heredoc
# delimiter lets the shell read a markdown-formatting backtick as command
# substitution.
BUGGY_TEXT = (
    "      - name: Write changelog line\n"
    "        run: |\n"
    "          cat >> Team/CHANGELOG.md << EOF\n"
    "          - `${CONTENT_HASH}` -- did a thing\n"
    "          EOF\n"
)

# Same content, fixed the way this project actually fixes it: quote the
# delimiter so the shell treats the body as literal text.
FIXED_TEXT = (
    "      - name: Write changelog line\n"
    "        run: |\n"
    "          cat >> Team/CHANGELOG.md << 'EOF'\n"
    "          - `${CONTENT_HASH}` -- did a thing\n"
    "          EOF\n"
)

# GitHub Actions' own multiline-output idiom: "<<" appears inside a quoted
# string, which is not a heredoc redirect at all. A naive scanner mistakes
# it for one; this must never be flagged.
GH_ACTIONS_IDIOM_TEXT = (
    "      - name: Set multiline output\n"
    "        run: |\n"
    "          echo \"name<<EOF_MARKER\" >> \"$GITHUB_OUTPUT\"\n"
    "          echo 'some `backtick` text' >> \"$GITHUB_OUTPUT\"\n"
    "          echo \"EOF_MARKER\" >> \"$GITHUB_OUTPUT\"\n"
)


def emit(status, data):
    print(MARKER + json.dumps({"v": 1, "probe": "check_heredoc_backticks",
                               "status": status, "data": data},
                              ensure_ascii=True, sort_keys=True))


def main():
    cases = []
    buggy_findings = gate.scan_text(BUGGY_TEXT)
    cases.append(("buggy_synthetic_fails", bool(buggy_findings), True,
                 {"findings": buggy_findings}))
    cases.append(("fixed_synthetic_passes",
                 bool(gate.scan_text(FIXED_TEXT)), False, {}))
    idiom_findings = gate.scan_text(GH_ACTIONS_IDIOM_TEXT)
    cases.append(("gh_actions_output_idiom_not_a_false_positive",
                 bool(idiom_findings), False,
                 {"findings_count": len(idiom_findings)}))

    failures = [(name, got, want, detail)
               for name, got, want, detail in cases if got != want]

    status = "fail" if failures else "pass"
    emit(status, {
        "cases_run": len(cases),
        "cases_failed": len(failures),
        "failing_cases": [f[0] for f in failures],
        "note": "synthetic fixtures, not a real historical commit -- see "
                "this file's own docstring for why"})
    for f in failures:
        print("FAIL: case {0} expected {1} but got {2}"
             .format(f[0], f[2], f[1]))
    if status == "pass":
        print("{0}/{0} cases correct: the gate is red on the synthetic "
             "bug and green on its fix and on the GH Actions output "
             "idiom.".format(len(cases)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
