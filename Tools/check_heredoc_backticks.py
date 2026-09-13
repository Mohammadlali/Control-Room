#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# check_heredoc_backticks -- fail on an unescaped backtick inside an
# unquoted shell heredoc in a workflow YAML file.
"""Fail if a workflow's `run:` block feeds a shell heredoc with an
UNQUOTED delimiter (`<<EOF`, not `<<'EOF'`/`<<"EOF"`/`<<\\EOF`) whose body
contains a backtick that is not escaped with a backslash.

Why this exists: `write-cr-vision.yml`'s first real dispatch (run
34342073324) built a `Team/CHANGELOG.md` line as
`` - `${CONTENT_HASH}` -- ... `` inside a heredoc left deliberately
unquoted so `${CONTENT_HASH}` would expand to the real commit hash. An
unquoted heredoc body is read like a double-quoted string: `$`, `\\` AND
backtick command substitution ALL fire. The backticks meant as markdown
code-formatting were read as `` `24274aa` `` -- run "24274aa" as a
command -- which failed with "command not found" and silently produced
EMPTY output, dropping the hash from the written line and failing
Control-Room's own `check_changelog.py` gate. Nothing caught this before
it reached a real dispatch; this tool is that catch, mechanical and free
of any token cost, run by the Stop hook like every other gate here.

Scope: this is a heuristic line-scanner, not a shell parser. It tracks
heredoc start/end state across each file's lines and is quoting-aware
(a heredoc whose delimiter carries any quote, or is backslash-escaped,
disables ALL expansion in its body per POSIX -- those are skipped, since
a literal backtick there is always safe). It is deliberately narrow: only
backticks are flagged, not `$(...)`, because this project's own
convention already uses `$(...)` for every INTENDED substitution and
backticks for nothing but markdown -- an unescaped backtick in an
unquoted heredoc has had zero legitimate uses here and one real bug.

Usage:
    python3 Tools/check_heredoc_backticks.py                 # every tracked workflow file
    python3 Tools/check_heredoc_backticks.py path/to/one.yml  # just these files

Exit 0 if none found, 1 otherwise. ASCII only.
"""

import io
import json
import os
import re
import sys

MARKER = "##TBS##"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_DIRS = [
    os.path.join(ROOT, ".github", "workflows"),
]

# Matches a heredoc start: <<WORD, <<-WORD, <<'WORD', <<"WORD", <<\WORD.
# Deliberately does NOT match YAML's own "<<:" merge-key syntax -- a colon
# right after "<<" satisfies none of the three alternatives below.
HEREDOC_START = re.compile(
    r"<<(?P<dash>-?)\s*"
    r"(?:'(?P<sq>[A-Za-z_][A-Za-z0-9_]*)'"
    r"|\"(?P<dq>[A-Za-z_][A-Za-z0-9_]*)\""
    r"|\\(?P<esc>[A-Za-z_][A-Za-z0-9_]*)"
    r"|(?P<bare>[A-Za-z_][A-Za-z0-9_]*))"
)


def find_default_files():
    found = []
    for d in DEFAULT_DIRS:
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".yml") or name.endswith(".yaml"):
                found.append(os.path.join(d, name))
    return found


def rel(path):
    return os.path.relpath(path, ROOT)


def has_unescaped_backtick(line):
    """True if `line` contains a backtick not immediately preceded by a
    single backslash. A run of N backslashes before a backtick escapes it
    only when N is odd (each \\\\ pair is a literal backslash, the
    leftover single \\ escapes the backtick)."""
    for m in re.finditer("`", line):
        i = m.start()
        n_backslash = 0
        j = i - 1
        while j >= 0 and line[j] == "\\":
            n_backslash += 1
            j -= 1
        if n_backslash % 2 == 0:
            return True
    return False


def find_real_heredoc_start(line):
    """Return the HEREDOC_START match for a genuine heredoc redirect on
    `line`, or None. Skips any "<<" that falls inside a quoted string --
    GitHub Actions' own multiline-output idiom writes literal text like
    `echo "name<<EOF_MARKER" >> "$GITHUB_OUTPUT"`, which is not a heredoc
    at all, and a naive scan mistook it for one (false-positive against
    Cloud/runner/prebuilt.yml, 2026-09-09). A "<<" is inside a string if
    an odd number of unescaped quote characters (of either kind) precede
    it on the same line -- true heredoc redirects are shell syntax, never
    inside quotes."""
    for m in HEREDOC_START.finditer(line):
        before = line[:m.start()]
        dq = len(re.findall(r'(?<!\\)"', before))
        sq = len(re.findall(r"(?<!\\)'", before))
        if dq % 2 == 1 or sq % 2 == 1:
            continue
        return m
    return None


def scan_text(text):
    """Return a list of {line, delimiter, content} dicts, one per
    offending body line, for a single file's raw text."""
    findings = []
    state = None  # None, or {"delim": str, "dash": bool}
    lines = text.split("\n")
    for lineno, line in enumerate(lines, start=1):
        if state is not None:
            probe = line.lstrip("\t") if state["dash"] else line
            if probe.rstrip("\r\n") == state["delim"]:
                state = None
                continue
            if has_unescaped_backtick(line):
                findings.append({"line": lineno, "delimiter": state["delim"],
                                 "content": line.strip()})
            continue
        m = find_real_heredoc_start(line)
        if not m:
            continue
        if m.group("bare"):
            state = {"delim": m.group("bare"), "dash": bool(m.group("dash"))}
        # sq/dq/esc forms disable expansion entirely -- nothing to track.
    return findings


def emit(status, data):
    print(MARKER + json.dumps({"v": 1, "probe": "heredoc_backticks",
                               "status": status, "data": data},
                              ensure_ascii=True, sort_keys=True))


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    paths = argv if argv else find_default_files()

    checked = []
    problems = []
    for path in paths:
        entry = {"path": rel(path)}
        if not os.path.isfile(path):
            entry["ok"] = False
            entry["error"] = "file does not exist"
            problems.append("%s: does not exist" % rel(path))
            checked.append(entry)
            continue
        with io.open(path, encoding="utf-8") as fh:
            text = fh.read()
        findings = scan_text(text)
        entry["ok"] = not findings
        entry["findings"] = findings
        if findings:
            for f in findings:
                problems.append(
                    "%s:%d: unescaped backtick in unquoted <<%s heredoc "
                    "body: %s" % (rel(path), f["line"], f["delimiter"],
                                  f["content"]))
        checked.append(entry)

    data = {"checked": checked, "problems": problems,
            "note": "Flags an unescaped backtick inside an UNQUOTED shell "
                    "heredoc body in a workflow's run: block -- the shell "
                    "reads it as command substitution, not literal text."}
    emit("fail" if problems else "pass", data)
    for p in problems:
        print("FAIL: " + p)
    if not problems:
        print("%d workflow file(s), no unescaped backticks in unquoted "
             "heredocs." % len(checked))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
