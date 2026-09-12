"""Surgically rewrite a leading-@agy trigger condition to trailing.

Replaces only the two startsWith(...) calls this fleet's agy-issue-bot.yml
files use for their @agy trigger with the equivalent endsWith(...) form
(matching '@agy', '@agy\\n' and '@agy\\r\\n'), leaving everything else in
the file untouched. Used by fix-agy-trigger-airbox-tbs.yml -- kept as a
real file rather than embedded in that workflow's own YAML, since a
multi-line Python block inside a `run: |` scalar is the exact indentation
trap Tools/check_changelog.py's sibling gates already warn against
elsewhere in this repo.
"""

import sys


def patch(text: str) -> str:
    text = text.replace(
        "startsWith(github.event.issue.body, '@agy')",
        "(endsWith(github.event.issue.body, '@agy') || "
        "endsWith(github.event.issue.body, '@agy\\n') || "
        "endsWith(github.event.issue.body, '@agy\\r\\n'))",
    )
    text = text.replace(
        "startsWith(github.event.comment.body, '@agy')",
        "(endsWith(github.event.comment.body, '@agy') || "
        "endsWith(github.event.comment.body, '@agy\\n') || "
        "endsWith(github.event.comment.body, '@agy\\r\\n'))",
    )
    return text


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    before = open(src).read()
    after = patch(before)
    open(dst, "w").write(after)
    print("CHANGED" if after != before else "NO_CHANGE")
