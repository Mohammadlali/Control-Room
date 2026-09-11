#!/usr/bin/env python3
"""Prove route_topic.classify() actually discriminates between projects,
defaults safely when nothing matches, and refuses to guess when matches tie
or a label names an unknown project.

Case 1 is the control: an issue with zero project signal must land on
Control-Room itself, not on a coin flip. Without it, a router that always
returned "control-room" would score full marks on the easy cases below.

Exit 1 if any case fails. ASCII only.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import route_topic as RT


def main():
    cases = []

    def check(name, got, want, note):
        cases.append({"case": name, "got": got, "want": want,
                      "pass": got == want, "note": note})

    scope = RT.load_scope()

    # 1. Control: no signal at all lands locally, not on a guess.
    r = RT.classify("routine housekeeping", "nothing project-specific here", "", scope)
    check("no_signal_defaults_local", (r["decision"], r["project"]),
          ("route", "control-room"),
          "an issue with no topic words must not be forwarded anywhere")

    # 2. A clear TBS-topic issue routes to ACC6's Claud-Cloud-Project.
    r = RT.classify("Rotator built positionally in build_district.py",
                     "Valiasr's sun aims into the sky again, same bug class.",
                     "", scope)
    check("tbs_keywords_route_to_acc6",
          (r["decision"], r.get("host_account"), r.get("host_repo")),
          ("route", "ACC6", "Claud-Cloud-Project"),
          "district/rotator/Valiasr language is TBS-shaped and nothing else")

    # 3. A clear AirboxVIP-topic issue routes to ACC1's own repo.
    r = RT.classify("Coffeenet kiosk menu ordering is slow",
                     "The AirboxVIP cafe menu screen lags on tap.", "", scope)
    check("airboxvip_keywords_route_to_acc1",
          (r["decision"], r.get("host_account"), r.get("host_repo")),
          ("route", "ACC1", "AirboxVIP_Coffeenet"),
          "coffeenet/kiosk language belongs to AirboxVIP, not TBS")

    # 4. An explicit, recognized label wins over keyword text entirely.
    r = RT.classify("random title", "random body mentioning coffee in passing",
                     "project:tbs, bug", scope)
    check("explicit_label_overrides_keywords",
          (r["decision"], r.get("project")), ("route", "tbs"),
          "an owner-set label is a stronger signal than incidental wording")

    # 5. An unrecognized label is refused, not guessed past.
    r = RT.classify("title", "body", "project:nonexistent-project", scope)
    check("unknown_label_is_unclear", r["decision"], "unclear",
          "a label naming a project not in company_scope.json must not "
          "silently fall back to keyword guessing")

    # 6. Tied keyword hits across two real projects must not be guess-broken.
    #    Exactly one keyword each, so neither count can outrank the other.
    r = RT.classify("tbs and coffee both mentioned in passing", "", "", scope)
    check("tied_keywords_are_unclear", r["decision"], "unclear",
          "equal signal for two different projects is not a topic yet")

    # 7. Every project in the JSON also appears in the markdown table --
    #    a project added to one and not the other would silently split the
    #    two files this scheme depends on staying identical.
    md_path = os.path.join(RT.ROOT, "Team", "COMPANY_SCOPE.md")
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    missing = [acc["login"] for acc in scope["accounts"].values()
               if acc["login"] not in md]
    check("every_account_login_named_in_scope_md", missing, [],
          "an account known to the router but absent from the human-"
          "readable table is undocumented, not routed correctly")

    failed = [c for c in cases if not c["pass"]]
    for c in cases:
        print("{0:5} {1:38} got={2!s:30} want={3!s:20}  {4}".format(
            "PASS" if c["pass"] else "FAIL", c["case"],
            str(c["got"])[:30], str(c["want"])[:20], c["note"][:60]))
    print("\n{0} cases, {1} failed".format(len(cases), len(failed)))
    print(json.dumps({"probe": "route_topic",
        "status": "pass" if not failed else "fail",
        "cases": len(cases), "failed": [c["case"] for c in failed]}))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
