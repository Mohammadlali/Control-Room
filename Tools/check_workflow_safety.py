#!/usr/bin/env python3
"""
Tools/check_workflow_safety.py
Gate 7: Static analysis of GitHub Actions workflow files.

Checks (no AI tokens consumed, agent-agnostic):
  1. Double-quotes inside printf content strings
     - Breaks agw-worker when GitHub injects ${{ inputs.prompt }} into bash
     - bash sees:  PROMPT="...some \"quoted\" text..."  -> parse error
     - Exception: lines with tr/sed (character-class args, not prompt content)
  2. Python inline code (-c) with insufficient YAML block indentation
     - YAML block scalar terminates on lines with less indentation than base
     - GitHub then shows the workflow file path instead of its name
  3. YAML syntax validity of all workflow files
     - Invalid YAML causes workflow to not register properly

Usage:
  python3 Tools/check_workflow_safety.py
  python3 Tools/check_workflow_safety.py .github/workflows
"""

import sys
import re
import os
import glob


C_OK   = "\033[92m\u2713\033[0m"
C_FAIL = "\033[91m\u2717\033[0m"
C_WARN = "\033[93m!\033[0m"

# Lines containing these patterns use single-quotes for character classes
# (tr -d, sed, etc.) rather than printf prompt content - skip them.
_CHAR_CLASS_PATTERNS = ("tr -d", "tr -", "sed ", "| tr", "| sed")


def check_1_double_quotes_in_printf(filepath, lines):
    """
    Check: no double-quotes inside single-quoted printf content strings.

    Root cause: when a prompt is built with `printf '%s\\n' 'some text'`
    and the content contains double-quotes, it ends up in the prompt variable.
    GitHub Actions then injects this via ${{ inputs.prompt }} LITERALLY into:
        run: |
          PROMPT="${{ inputs.prompt }}"
    producing:
          PROMPT="...some \"quoted\" text..."
    which breaks bash string parsing (exit code 1, silent failure).

    Fix: replace all \" in printf content strings with single-quote or
    rephrase the instruction text.

    NOTE: lines using tr/sed (e.g. tr -d '`\"\\\\$') are excluded because
    the single-quoted arg is a character class, not prompt content.
    """
    errors = []
    for i, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if "printf" not in line:
            continue
        # Skip lines where single-quotes are character classes for tr/sed
        if any(p in line for p in _CHAR_CLASS_PATTERNS):
            continue
        # Skip subshell printf used only for sanitization pipelines
        # e.g. SAFE_X=$(printf '%s' "$VAR" | somecommand)
        if "$(printf" in line and "|" in line:
            continue
        # Extract all single-quoted segments
        sq_parts = re.findall(r"'([^']*)'" , line)
        # Skip format string (first argument to printf), check content args
        for part in sq_parts[1:]:
            if '"' in part:
                errors.append(
                    (i, "[CHECK-1] double-quote in printf content string "
                     "(will break agw-worker bash injection)",
                     line[:100])
                )
    return errors


def check_2_python_inline_yaml_indent(filepath, lines):
    """
    Check: Python inline code in YAML run blocks must match block indentation.

    Root cause: YAML block scalars terminate when a line has LESS indentation
    than the block's base level. Python code lines at column 0 inside a run:
    block (base indent 10+) will silently terminate the block early.
    GitHub then shows the workflow file path instead of its name.

    Fix: use jq for JSON parsing, or write Python to a temp file.
    """
    errors = []
    for i, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip()
        # Detect start of inline Python
        if 'python3 -c "' not in line and "python3 -c '" not in line:
            continue
        # Get indentation of this line (the python3 command)
        py_cmd_indent = len(line) - len(line.lstrip())
        # Check next lines for Python code
        j = i  # 0-indexed next line
        while j < len(lines):
            next_raw = lines[j]
            next_stripped = next_raw.strip()
            # Closing quote ends the inline block
            if next_stripped in ('"', "'", '" 2>/dev/null', "' 2>/dev/null",
                                  '" 2>&1', "' 2>&1"):
                break
            if not next_stripped:
                j += 1
                continue
            next_indent = len(next_raw) - len(next_raw.lstrip())
            # Python code lines should be at least as indented as the py cmd
            if next_indent < py_cmd_indent and next_stripped:
                errors.append(
                    (j + 1,
                     f"[CHECK-2] Python inline code at col {next_indent} "
                     f"(need >={py_cmd_indent} to stay in YAML block)",
                     next_stripped[:80])
                )
            j += 1
    return errors


def check_3_yaml_syntax(filepath, content):
    """
    Check: YAML file must parse without errors.

    Invalid YAML causes GitHub Actions to use the file path as the workflow
    name and the workflow never triggers properly.
    """
    errors = []
    try:
        import yaml
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            errors.append((0, f"[CHECK-3] YAML parse error", str(e)[:160]))
    except ImportError:
        pass  # PyYAML not installed - skip (CI will have it)
    return errors


def check_file(filepath):
    errors = []
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError as e:
        return [(0, "cannot read file", str(e))]

    lines = content.splitlines()
    errors += check_1_double_quotes_in_printf(filepath, lines)
    errors += check_2_python_inline_yaml_indent(filepath, lines)
    errors += check_3_yaml_syntax(filepath, content)
    return errors


def main():
    search_dir = sys.argv[1] if len(sys.argv) > 1 else ".github/workflows"
    root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    wf_dir = os.path.join(root, search_dir)

    files = sorted(
        glob.glob(os.path.join(wf_dir, "*.yml")) +
        glob.glob(os.path.join(wf_dir, "*.yaml"))
    )

    if not files:
        sys.exit(0)

    all_errors = []
    for fp in files:
        rel = os.path.relpath(fp, root)
        for lineno, msg, snippet in check_file(fp):
            loc = f"{rel}:{lineno}" if lineno else rel
            all_errors.append(f"{loc}: {msg}\n        snippet: {snippet}")

    if all_errors:
        sys.stdout.write(
            f"check_workflow_safety: FAILED ({len(all_errors)} issue(s))\n"
        )
        for e in all_errors:
            sys.stdout.write(f"  {C_FAIL} {e}\n")
        sys.exit(1)

    sys.exit(0)  # silent on pass (saves tokens)


if __name__ == "__main__":
    main()
