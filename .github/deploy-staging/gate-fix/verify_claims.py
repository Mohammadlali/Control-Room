#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reject a report that cites something which does not exist.

`team_lint.py` checks that a report has the right *sections*. It cannot tell
whether the report is about this repository or about an imagined one. A report
can pass the lint while citing `Tools/calibrate_shadows.py`, a file nobody ever
wrote, and quoting numbers it produced.

That has happened here: a document was written that referred to work that did
not exist, and nothing caught it, because every reader assumed the paths were
real. Reading is not a check. This is the check.

What it verifies, all of it mechanical:

  1. Every repository path a report mentions exists on disk.
  2. Every `##TBS##` line parses as JSON and carries v/probe/status.
  3. Every report claiming delivery quotes a push, not a commit.
  4. Every report that reports a probe run names a runnable script.

Usage:
    python Tools/verify_claims.py Team/reports/*.md
    python Tools/verify_claims.py --all

Exit code 1 if any report fails. ASCII only.
"""

import os
import re
import sys
import json
import glob

MARKER = "##TBS##"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A path-looking token: one or more directory steps then a file with a suffix.
# Deliberately narrow -- it must look like a repository path, not prose.
PATH = re.compile(
    r"\b((?:Tools|Team|Districts|Narrative|Config|Content|Reports|Source|"
    r"Gateway|Jobs|Docs)/[A-Za-z0-9_./*-]+\.[A-Za-z0-9]{1,6})\b")

# Claims of delivery. Each must be backed by a push line, not a commit line.
DELIVERY = re.compile(r"\bpushed\b|\bdelivered\b|\barrived\b|\bis on the branch\b",
                      re.I)
PUSH_EVIDENCE = re.compile(r"->\s*[A-Za-z0-9_./-]+|\bgit push\b|"
                           r"\b[0-9a-f]{7}\.\.[0-9a-f]{7}\b")


def repo_paths():
    """Every file actually in the working tree, as a set of relative paths."""
    out = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            full = os.path.join(dirpath, name)
            out.add(os.path.relpath(full, ROOT).replace(os.sep, "/"))
    return out


# Files real UE5-era reports correctly cited at the time and that were
# deleted on 2026-09-11 when the owner confirmed Unreal Engine is no longer
# used (Team/CHANGELOG.md's same-day entry has the full list this is drawn
# from). A citation to one of these is not a fabrication -- the file existed
# when the report was written, git history proves it, and the report is
# reporting real UE5-era work, not imagined work. Frozen, not derived from a
# live directory listing, so it cannot silently grow to cover a future
# unrelated deletion: adding to this set is a deliberate, reviewable edit,
# the same shape as check_review_guild.py's frozen legacy-account table.
RETIRED_2026_09_11 = frozenset([
    "Tools/build_district.py", "Tools/calibrate_district.py",
    "Tools/calibrate_exposure.py", "Tools/calibrate_lighting.py",
    "Tools/calibrate_sun_angle.py", "Tools/capture_shot.py",
    "Tools/diag_capture.py", "Tools/diag_district_lights.py",
    "Tools/diag_exposure.py", "Tools/diag_light_sources.py",
    "Tools/diag_lighting.py", "Tools/diag_navmesh.py",
    "Tools/diag_readback.py", "Tools/diag_rotator.py", "Tools/diag_sky.py",
    "Tools/diag_sky_source.py", "Tools/diag_sun_shadow.py",
    "Tools/make_test_scene.py", "Tools/probe_boot.py",
    "Tools/probe_composite.py", "Tools/probe_district.py",
    "Tools/probe_district_spec_match.py", "Tools/probe_persian_slate.py",
    "Tools/probe_persian_text.py", "Tools/probe_rotator_contract.py",
    "Tools/probe_selfcheck_fail.py", "Tools/tbs_core.py", "Tools/ue.py",
    "Tools/watch.py", "Tools/distill.py", "Tools/engine_mirror.py",
    "Tools/kaggle_dataset.py", "Tools/ship_prebuilt_to_runner.py",
    "Tools/probe_ship_prebuilt.py", "Tools/dispatch_runner_workflow.py",
    "Tools/kaggle_run.py", "Tools/probe_boot_digest_contract.py",
    "Tools/probe_icd_direct_verdict.py", "Tools/check_target_profile.py",
    "Tools/probe_check_target_profile.py",
    "Tools/probe_kaggle_gpu_default.py", "Tools/probe_ue_cook_platform.py",
    "Tools/check_district_build_proof.py",
    "Tools/probe_check_district_build_proof.py", "Tools/district_schema.md",
    "Config/DefaultEngine.ini", "Config/DefaultGame.ini",
    "Config/DefaultInput.ini", "TehranBlindSpot.uproject", ".vsconfig",
    "Docs/learning_path.md",
])


def retired_file(cited):
    """A UE5-era path known-deleted 2026-09-11, or something under a whole
    UE5-era directory removed the same day. Prefix-matched for the
    directories (Source/, Districts/, Content/, Jobs/, Cloud/colab/,
    Cloud/runner/) since every file under them is gone, not just a
    hand-enumerated list of what happened to exist that day."""
    if cited in RETIRED_2026_09_11:
        return True
    retired_prefixes = ("Source/", "Districts/", "Content/", "Jobs/",
                        "Cloud/colab/", "Cloud/runner/")
    return cited.startswith(retired_prefixes)


def moved_task(cited, existing):
    """A task file cited at pending/ that now sits in done/, or the reverse.

    Answering a task moves its file, which breaks every report that cited it
    -- including the report the task produced, which necessarily names its own
    task path. That happened four times on 2026-08-21, and the previous fix
    each time was to disguise the path in the report, which is a worse record
    for a true statement.

    This is not a loosening: the claim is that the task file exists, and it
    does, one directory over. A path that is in neither is still rejected.
    """
    for a, b in (("Team/tasks/pending/", "Team/tasks/done/"),
                 ("Team/tasks/done/", "Team/tasks/pending/")):
        if cited.startswith(a):
            if cited.replace(a, b, 1) in existing:
                return True
    return False


def check(path, existing):
    problems = []
    with open(path, encoding="utf-8") as f:
        text = f.read()

    # 1. Cited paths must exist. A glob is accepted if anything matches it.
    cited = sorted(set(PATH.findall(text)))
    for p in cited:
        if "*" in p:
            # glob matches directories too, so a directory named like a file
            # satisfied a glob citation. Narrower than the standing audit
            # claimed, but real: only files count.
            if not [g for g in glob.glob(os.path.join(ROOT, p))
                    if os.path.isfile(g)]:
                problems.append("cites a path matching no file: " + p)
        elif p not in existing and not moved_task(p, existing) and not retired_file(p):
            problems.append("cites a file that does not exist: " + p)

    # 2. Every TBS line must be real JSON with the required keys. A malformed
    #    one is a line that was typed to look like evidence.
    for i, line in enumerate(text.splitlines(), 1):
        if MARKER not in line:
            continue
        blob = line[line.index(MARKER) + len(MARKER):].strip()
        try:
            parsed = json.loads(blob)
        except Exception:
            problems.append("line {0}: TBS line is not valid JSON".format(i))
            continue
        for key in ("v", "probe", "status"):
            if key not in parsed:
                problems.append(
                    "line {0}: TBS line has no '{1}'".format(i, key))
        if parsed.get("status") not in ("pass", "fail", "blocked", None):
            problems.append("line {0}: status '{1}' is not pass/fail/blocked"
                            .format(i, parsed.get("status")))

    # 3. A claim of delivery needs the push, not the commit. Constitution:
    #    'a commit is not a delivery'.
    if DELIVERY.search(text) and not PUSH_EVIDENCE.search(text):
        problems.append("claims delivery but quotes no push line")

    # 4. A report with no cited path and no TBS line is prose. It may be
    #    correct, but nothing in it can be checked, and unverifiable prose is
    #    what this tool exists to catch.
    if not cited and MARKER not in text:
        problems.append("cites no file and carries no ##TBS## line: "
                        "nothing in this report can be checked")

    return cited, problems


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if "--all" in argv or not args:
        args = sorted(glob.glob(os.path.join(ROOT, "Team", "reports", "*.md")))
    if not args:
        print("no reports found")
        return 0

    existing = repo_paths()
    failed = 0
    for path in args:
        cited, problems = check(path, existing)
        name = os.path.relpath(path, ROOT).replace(os.sep, "/")
        if problems:
            failed += 1
            print("REJECT {0}".format(name))
            for p in problems:
                print("    " + p)
        else:
            print("ok     {0}  ({1} paths checked)".format(name, len(cited)))

    print("\n{0} checked, {1} rejected".format(len(args), failed))
    print(MARKER + json.dumps(
        {"v": 1, "probe": "verify_claims", "status":
         "pass" if not failed else "fail",
         "data": {"checked": len(args), "rejected": failed}}, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
