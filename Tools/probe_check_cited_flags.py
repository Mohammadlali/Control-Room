#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prove check_cited_flags rejects an invented flag and nothing else.

The rule came from `agw-acc1-w09` (task 026), which demonstrated the hole it
closes rather than arguing it: a report citing
`python3 Tools/distill.py --benchmark --dry-run` -- a real file, invented
flags -- was accepted by all four report gates.

A gate that rejects an invented flag is easy. A gate that rejects an invented
flag AND accepts every real report is the whole difficulty, so the 25 files in
Team/reports/ are a case here, not a footnote: a rule that rejects real work
is noise, and noise gets switched off.

Two controls carry the weight, because both are mistakes this repository has
already made once:

  A flag named only in a COMMENT must not count as declared. The scratch
  version in report 026 collected `--[a-z-]+` from the whole source, which is
  how `probe_sync_runner_repos` found a dead variable by its own obituary and
  called it live. The control implements that grep and requires it to give the
  WRONG answer here.

  A tool whose flags cannot be read must not be judged. Constitution 5: an
  absent measurement is never a measurement of zero, and a gate that is
  loudest where it knows least is worse than no gate.

Usage:
    python Tools/probe_check_cited_flags.py

Exit 1 if any case fails. ASCII only.
"""

import io
import os
import re
import sys
import json
import shutil
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_cited_flags as G   # noqa: E402

MARKER = "##TBS##"
ROOT = os.path.dirname(HERE)

# Ported from Claud-Cloud-Project 2026-09-13, where this cited
# `Tools/verify_claims.py --benchmark --dry-run`: a real file there with
# invented flags, since that repo's verify_claims.py takes no argparse
# flags at all (manual `"--all" in argv` parsing). Control-Room's own
# `Tools/verify_claims.py` takes no CLI flags whatsoever (confirmed: no
# argparse, no sys.argv reference at all), so it serves the identical role
# here unmodified -- any flag cited against it is invented by definition.
FAKE = """# Task 999

Report-by: agw-acc1-w09

## What was measured

```bash
python3 Tools/verify_claims.py --benchmark --dry-run
```

Output:
```
latency_ms: 14.82
```
"""

# `Tools/poll_tasks.py --validate` is Control-Room's own real, live-gate
# citation (see Tools/run_gates.py) and, like the ported fixture's original
# target, is manually parsed (`"--validate" in sys.argv`) rather than via
# argparse -- preserving the same non-argparse-tool property the original
# fixture tested.
REAL = """# Task 999

```bash
python3 Tools/poll_tasks.py --validate
```
"""

QUOTED_OUTPUT = """# Task 999

The tool printed:

```text
python3 Tools/distill.py --benchmark
```
"""

FOREIGN = """# Task 999

```bash
git push --force-with-lease origin HEAD
docker run --rm ghcr.io/x/y --nonsense
```
"""

# A tool that MENTIONS a flag in a comment and does not declare it.
COMMENTED_TOOL = '''#!/usr/bin/env python3
"""A tool. Historically this had a --benchmark mode; it was removed."""
import argparse


def main():
    ap = argparse.ArgumentParser()
    # --benchmark used to live here
    ap.add_argument("--real", action="store_true")
    return ap.parse_args()
'''

UNPARSEABLE_TOOL = "this is not python at all ((((\n"

MENTIONED = """# Task 999

The fabricated report cited `python3 Tools/distill.py --benchmark --dry-run`,
a real file with flags that do not exist.

```bash
python3 Tools/poll_tasks.py --validate
```
"""


def naive_flags(path):
    """The grep the scratch version used: every --flag anywhere in the file."""
    with io.open(path, encoding="utf-8") as fh:
        return set(re.findall(r"--[a-zA-Z0-9_-]+", fh.read()))


def write(tmp, name, body):
    path = os.path.join(tmp, name)
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return path


def main():
    results = []

    def case(name, got, want, note, control=None):
        blind = control is not None and control[0] == want
        results.append({"case": name, "got": got, "want": want,
                        "pass": got == want and not blind, "note": note,
                        "control": None if control is None else control[1],
                        "blind": blind})

    tmp = tempfile.mkdtemp(prefix="tbs_flags_")
    try:
        case("invented_flags_are_rejected",
             len(G.problems_in(write(tmp, "fake.md", FAKE))), 2,
             "both --benchmark and --dry-run, named one by one")

        case("a_real_flag_is_accepted",
             G.problems_in(write(tmp, "real.md", REAL)), [],
             "flags these tools really declare, in a fenced block")

        case("prose_about_a_command_is_not_running_it",
             G.problems_in(write(tmp, "prose.md", MENTIONED)), [],
             "report 026's whole subject is a bad command it must be able "
             "to name")

        case("quoted_output_is_not_a_command",
             G.problems_in(write(tmp, "quoted.md", QUOTED_OUTPUT)), [],
             "a report quoting a tool's output is quoting, not claiming")

        case("foreign_commands_are_not_judged",
             G.problems_in(write(tmp, "foreign.md", FOREIGN)), [],
             "this gate has no business ruling on git or docker flags")

        # -- the comment hole, and the grep that falls into it ---------------
        tools = os.path.join(tmp, "Tools")
        os.makedirs(tools)
        commented = write(tools, "commented_tool.py", COMMENTED_TOOL)
        declared, known = G.declared_flags(commented)
        case("comment_does_not_declare_a_flag",
             ("--benchmark" in declared, "--real" in declared, known),
             (False, True, True),
             "read from add_argument, not from the file's prose",
             control=(("--benchmark" in naive_flags(commented),
                       "--real" in naive_flags(commented), True),
                      "a grep of the source finds the flag in its own obituary"))

        unparseable = write(tools, "broken_tool.py", UNPARSEABLE_TOOL)
        flags, known = G.declared_flags(unparseable)
        case("unparseable_tool_is_not_known",
             known, False,
             "flags unknown; the caller must not reject on this")

        # Deliberate contract, and the reason this gate is not inert: a file
        # that parses is judged whether or not it uses argparse. distill.py
        # has no argparse and is exactly the file the fabricated command
        # cited; treating "no parser" as unknown made the gate accept
        # everything, including the attack it was built for.
        noargs = write(tools, "plain_tool.py", "print('hello')\n")
        flags, known = G.declared_flags(noargs)
        case("parseable_tool_is_judged_without_argparse",
             (known, sorted(flags)), (True, ["--help"]),
             "a file that never names a flag cannot act on one")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # -- and it must still accept every real report ------------------------
    live = sorted(f for f in os.listdir(os.path.join(ROOT, "Team", "reports"))
                  if f.endswith(".md"))
    noisy = [f for f in live
             if G.problems_in(os.path.join(ROOT, "Team", "reports", f))]
    case("every_real_report_is_accepted", noisy, [],
         "{0} reports on this checkout; a rule that rejects real work "
         "gets switched off".format(len(live)))

    failed = [r for r in results if not r["pass"]]
    for r in results:
        print("{0:5} {1:36} got={2!s:26} want={3!s:20} {4}".format(
            "PASS" if r["pass"] else ("BLIND" if r["blind"] else "FAIL"),
            r["case"], str(r["got"])[:26], str(r["want"])[:20],
            (r["control"] or r["note"])[:44]))
    print("\n{0} cases, {1} failed".format(len(results), len(failed)))
    print(MARKER + json.dumps(
        {"v": 1, "probe": "cited_flags_discriminates",
         "status": "pass" if not failed else "fail",
         "data": {"cases": len(results), "reports_checked": len(live),
                  "failed": [r["case"] for r in failed]}}, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
