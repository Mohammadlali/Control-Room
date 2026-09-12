"""Surgically rewrite agw-claude.yml's @claude trigger to trailing-only.

The file's human-trigger condition is:
    contains(github.event.comment.body || github.event.issue.body, '@claude')
which matches '@claude' anywhere in the text. Replaces it with an
endsWith(...)-based trailing-only match (checking '@claude', '@claude\\n'
and '@claude\\r\\n' on both issue.body and comment.body, since contains()
accepted either field via the || fallback and endsWith has no equivalent
short-hand). Also drops the bot-handoff sub-clause's own separate
endsWith(...) check, since the top-level condition now already guarantees
it -- that sub-clause only needs to keep relaxing the author_association
gate for a bot-authored comment, not re-verify the text pattern.
Everything else in the file is left untouched.
"""

import sys

OLD_MAIN = "contains(github.event.comment.body || github.event.issue.body, '@claude')"

NEW_MAIN = (
    "(\n"
    "        endsWith(github.event.comment.body, '@claude') || endsWith(github.event.comment.body, '@claude\\n') || endsWith(github.event.comment.body, '@claude\\r\\n') ||\n"
    "        endsWith(github.event.issue.body, '@claude') || endsWith(github.event.issue.body, '@claude\\n') || endsWith(github.event.issue.body, '@claude\\r\\n')\n"
    "      )"
)

OLD_BOT_CLAUSE = (
    "github.event.comment.user.login == 'github-actions[bot]' &&\n"
    "          (endsWith(github.event.comment.body, '@claude') || endsWith(github.event.comment.body, '@claude\\n') || endsWith(github.event.comment.body, '@claude\\r\\n'))"
)
NEW_BOT_CLAUSE = "github.event.comment.user.login == 'github-actions[bot]'"

# @agy's own trigger moved from leading to trailing fleet-wide (see
# CHANGELOG.md) -- this exclusion (skip @claude on an issue meant for
# @agy) was written against the old startsWith convention and is now
# stale against the real one.
OLD_AGY_EXCLUSION = "!startsWith(github.event.issue.body, '@agy')"
NEW_AGY_EXCLUSION = (
    "!(\n"
    "        endsWith(github.event.issue.body, '@agy') || endsWith(github.event.issue.body, '@agy\\n') || endsWith(github.event.issue.body, '@agy\\r\\n')\n"
    "      )"
)


def patch(text: str) -> str:
    text = text.replace(OLD_MAIN, NEW_MAIN)
    text = text.replace(OLD_BOT_CLAUSE, NEW_BOT_CLAUSE)
    text = text.replace(OLD_AGY_EXCLUSION, NEW_AGY_EXCLUSION)
    return text


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    before = open(src).read()
    after = patch(before)
    open(dst, "w").write(after)
    print("CHANGED" if after != before else "NO_CHANGE")
