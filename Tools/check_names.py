"""Fail on a name that is used but bound nowhere in its file.

Bought 2026-08-21. `bootstrap_containers.py` shipped referencing `REPO_PATH`,
a constant that exists in `worker_git.py` and not there. Every invocation died
with NameError, on the owner's machine, five commands in a row. Nothing caught
it: `ast.parse` sees valid syntax, and the probe suite never executed that
branch because the test seam it added skipped it.

Deliberately conservative, so it can be a gate rather than a nuisance. A name
is reported only if it is bound NOWHERE in the file -- not as a module global,
not as a parameter, not as any assignment target, import, comprehension
variable, `except as`, `with as`, or def/class name, anywhere. A name defined
in one function and used in another is therefore NOT reported, even though it
would be a real bug: this trades recall for zero false positives, because a
gate that cries wolf gets switched off.

pyflakes does this properly and more. It is not a dependency here because the
gates must run on the owner's machine too, and it is not installed there.

    python3 Tools/check_names.py            # Tools/*.py
    python3 Tools/check_names.py <paths>
"""
import ast
import builtins
import glob
import json
import os
import sys

MARKER = "##TBS##"
HERE = os.path.dirname(os.path.abspath(__file__))


def emit(probe, status, data):
    print(MARKER + json.dumps({"v": 1, "probe": probe, "status": status,
                               "data": data}, sort_keys=True))


def bound_names(tree):
    """Every name bound anywhere in the file, by any construct."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx,
                                                     (ast.Store, ast.Del)):
            names.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                               ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                names.add((alias.asname or alias.name).split(".")[0])
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names.add(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            names.update(node.names)
    return names


def undefined_in(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), path)
    known = bound_names(tree) | set(dir(builtins)) | {"__file__", "__name__",
                                                      "__doc__"}
    bad = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in known:
                bad.setdefault(node.id, node.lineno)
    return bad


def main(argv=None):
    paths = argv or sys.argv[1:] or sorted(
        glob.glob(os.path.join(HERE, "*.py")))
    findings = []
    for path in paths:
        try:
            bad = undefined_in(path)
        except SyntaxError as exc:
            findings.append({"file": os.path.basename(path),
                             "name": "<syntax error>", "line": exc.lineno})
            continue
        for name, line in sorted(bad.items()):
            findings.append({"file": os.path.basename(path), "name": name,
                             "line": line})

    for f in findings:
        print("UNDEFINED {0}:{1}  {2}".format(f["file"], f["line"], f["name"]))
    print("\n{0} files checked, {1} undefined".format(len(paths),
                                                      len(findings)))
    emit("names_defined", "pass" if not findings else "fail",
         {"checked": len(paths), "undefined": len(findings),
          "findings": findings[:20]})
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
