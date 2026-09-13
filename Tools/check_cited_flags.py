#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reject a report that cites a repository tool with a flag the tool has not got.

`Team/LEARN.md` PART 10 names the open frontier: no gate can tell whether a
report's numbers came from running anything. On 2026-08-26 `agw-acc1-w09`
stopped arguing it and demonstrated it -- task 022 got `team_lint`,
`verify_claims`, `check_reviews` and `check_review_guild` to accept a report
whose latency and throughput figures were invented, citing

    python3 Tools/distill.py --benchmark --dry-run

a real file with flags that do not exist. `verify_claims` passed it because
`Tools/distill.py` is on disk: it checks that cited PATHS exist, never that a
cited COMMAND does.

Task 026 asked the same container for the cheapest rule that rejects that and
still accepts every real report. This is that rule, and the credit is theirs:

    a long flag passed to a repository python script must be a flag that
    script actually defines.

It closes a narrow slice and nothing wider. **A fabricated number attached to
a command that really exists still passes**, and no rule here can see that.
What it does catch is the cheapest tell of a command nobody ran, because a
flag is the part of a plausible-looking command an author invents without
noticing.

Two departures from the scratch version measured in report 026, both bought
by earlier mistakes in this repository:

- **Flags come from the parser, not from a grep of the source.** That version
  collected `--[a-zA-Z0-9_-]+` out of the whole file, so a flag named in a
  COMMENT counted as defined -- `probe_sync_runner_repos` found a dead
  variable by its own obituary and called it live, and this is the same hole.
  `add_argument` calls are read out of the syntax tree instead.
- **A script that cannot be parsed is not judged.** No `add_argument` found
  means the flags are unknown, and constitution 5 says an absent measurement
  is never a measurement of zero. Rejecting on it would make this gate loudest
  exactly where it knows least.

Usage:
    python Tools/check_cited_flags.py                # every report
    python Tools/check_cited_flags.py <file> [...]

Exit 1 if any report is rejected. ASCII only.
"""

import argparse
import ast
import glob
import io
import json
import os
import re
import shlex
import sys

MARKER = "##TBS##"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "Team", "reports")

# Fenced blocks whose language says they hold OUTPUT, not commands. A report
# quoting a tool's own output is quoting, not claiming to have run a flag.
NOT_COMMANDS = frozenset(["json", "text", "output", "markdown", "md", "yaml",
                          "yml", "python", "py", "diff", "ini", "log"])

FENCE = re.compile(r"```([A-Za-z]*)\n(.*?)```", re.DOTALL)

# Inline backticks are deliberately NOT read as commands, and that narrowing
# was bought rather than assumed.
#
# The first version scanned them too, and rejected report 026 -- the report
# whose whole subject is the invented citation from 022. It quotes
# `python3 Tools/distill.py --benchmark --dry-run` in prose, six times, in
# order to report it. Every hit came from inline code and none from a fenced
# block.
#
# That is the third time in two days this repository has read text ABOUT a
# thing as the thing: an echoed `::error::` guard counted as a failure, prose
# quoting `##TBS##` counted as a digest, and now a report naming a bad command
# counted as running one. The structural distinction is real and is this
# project's own house style: a claim to have run something is a fenced block
# with its output beneath it. Backticks in a sentence are how a report talks
# about a command.

# Wrappers that stand in front of the real command.
SKIP_HEAD = frozenset(["wsl", "-e", "sudo", "env", "time", "nice", "exec",
                       "python", "python3", "py"])

# Flags argparse provides without anyone declaring them.
FREE = frozenset(["--help"])


def emit(probe, status, data):
    print(MARKER + json.dumps({"v": 1, "probe": probe, "status": status,
                               "data": data}, sort_keys=True))


def declared_flags(path):
    """(flags, known). Every long option this script could possibly recognise.

    `known` is False ONLY when the file cannot be parsed at all. That
    distinction had to be sharpened once, and the sharpening is the reason
    this gate is not inert:

    The first version treated "no `add_argument` anywhere" as unknown and
    declined to judge. `Tools/distill.py` does not use argparse -- and it is
    the exact file report 022's fabricated command cited. So the gate built to
    catch that citation refused to look at it, accepted the fake, and accepted
    all 25 real reports too. Green, and incapable of failing. Caught by the
    probe's own `invented_flags_are_rejected` case, which exists because a
    rule that only ever says "ok" says nothing.

    A python file that never mentions a flag as a string CANNOT act on it,
    argparse or no argparse. So the set is the union of two readings:

      every string passed to `add_argument`, and
      every string CONSTANT in the module that begins with `--`.

    The second covers hand-rolled `sys.argv` parsing without assuming
    argparse, and it stays immune to the comment hole for a structural reason:
    comments are absent from the syntax tree entirely, and a docstring that
    merely mentions a flag is one constant that does not itself begin with
    `--`.
    """
    try:
        with io.open(path, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
    except (OSError, SyntaxError, ValueError):
        return set(), False

    flags = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            text = node.value
            if text.startswith("--"):
                flags.add(re.split(r"[\s=]", text, 1)[0])
            continue
        if not isinstance(node, ast.Call):
            continue
        if getattr(node.func, "attr", None) != "add_argument":
            continue
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if arg.value.startswith("-"):
                    flags.add(arg.value)
    return flags | set(FREE), True


def commands_in(text):
    """Command lines a report claims to have run."""
    out = []
    for lang, body in FENCE.findall(text):
        if lang.lower() in NOT_COMMANDS:
            continue
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("$ "):
                line = line[2:].strip()
            out.append(line.rstrip("\\").strip())
    return out


def tool_of(command):
    """The repository python script this command runs, or None.

    Anything that is not a script inside Tools/ is None on purpose: this gate
    has no business deciding whether `git push --force-with-lease` is real.
    """
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None, []
    while tokens and (tokens[0] in SKIP_HEAD or tokens[0].endswith("/python3")):
        tokens.pop(0)
    if not tokens:
        return None, []
    first = tokens[0].replace("\\", "/").lstrip("./")
    if not (first.startswith("Tools/") and first.endswith(".py")):
        return None, []
    path = os.path.join(ROOT, first)
    if not os.path.isfile(path):
        # verify_claims already owns "a cited path does not exist".
        return None, []
    return first, tokens[1:]


def problems_in(path):
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    found = []
    for command in commands_in(text):
        tool, rest = tool_of(command)
        if not tool:
            continue
        flags, known = declared_flags(os.path.join(ROOT, tool))
        if not known:
            continue
        for token in rest:
            if not token.startswith("--") or token == "--":
                continue
            flag = token.split("=", 1)[0]
            if flag not in flags:
                found.append("flag '{0}' is not defined in {1} (cited as: {2})"
                             .format(flag, tool, command[:90]))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*",
                    help="reports to check; default every report")
    args = ap.parse_args(argv)

    files = args.files or sorted(glob.glob(os.path.join(REPORTS, "*.md")))
    rejected = []
    for path in files:
        shown = os.path.relpath(path, ROOT).replace(os.sep, "/")
        found = problems_in(path)
        if found:
            rejected.append(shown)
            print("REJECT " + shown)
            for line in found:
                print("    - " + line)
        else:
            print("ok     " + shown)

    print("\n{0} checked, {1} rejected".format(len(files), len(rejected)))
    emit("cited_flags", "fail" if rejected else "pass",
         {"checked": len(files), "rejected": len(rejected),
          "files": rejected})
    return 1 if rejected else 0


if __name__ == "__main__":
    sys.exit(main())
