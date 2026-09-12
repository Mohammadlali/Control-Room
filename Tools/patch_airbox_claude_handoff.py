"""Add the @agy <-> @claude handoff to AirboxVIP_Coffeenet's agy-issue-bot.yml.

Three surgical changes, nothing else touched:

1. Trigger `if:` -- add a claude[bot] carve-out to the issue_comment
   branch's author_association gate, so a Claude-authored comment ending
   in trailing @agy can re-trigger this bot (the reverse handoff
   direction). Mirrors ACC6's own agy-issue-bot.yml.
2. The prompt built in "Build prompt" -- add the same instruction ACC6's
   prompt has: end with a trailing "@claude" line when fully done.
3. "Post result" -- currently appends the "AGY worker: URL | acc: N"
   footer AFTER agy's own output, which would swallow a trailing
   "@claude" agy printed (the footer becomes the real last line instead).
   Reordered so the footer comes first and agy's own content -- @claude
   marker included, if present -- is what the posted comment actually
   ends with.
"""

import sys

OLD_TRIGGER_COMMENT = (
    "(github.event_name == 'issue_comment' && "
    "(endsWith(github.event.comment.body, '@agy') || endsWith(github.event.comment.body, '@agy\\n') "
    "|| endsWith(github.event.comment.body, '@agy\\r\\n')) && "
    "(github.event.comment.author_association == 'OWNER' || github.event.comment.author_association == 'COLLABORATOR'))"
)
NEW_TRIGGER_COMMENT = (
    "(github.event_name == 'issue_comment' && "
    "(endsWith(github.event.comment.body, '@agy') || endsWith(github.event.comment.body, '@agy\\n') "
    "|| endsWith(github.event.comment.body, '@agy\\r\\n')) && "
    "(github.event.comment.author_association == 'OWNER' || github.event.comment.author_association == 'COLLABORATOR' "
    "|| github.event.comment.user.login == 'claude[bot]'))"
)

OLD_PROMPT_TAIL = (
    "            printf '%s\\n' 'STEP 4: Print a final report to stdout, including the commit hash you made.'\n"
    "          } > /tmp/prompt.txt"
)
NEW_PROMPT_TAIL = (
    "            printf '%s\\n' 'STEP 4: Print a final report to stdout, including the commit hash you made.'\n"
    "            printf '%s\\n' 'When you have COMPLETELY finished this task -- not a partial draft, nothing left"
    " to do -- end your final report with the line \"@claude\" on its own line, so Claude can continue from your"
    " result. If you are not fully done, do not include that line.'\n"
    "          } > /tmp/prompt.txt"
)

OLD_POST_RESULT = (
    '          printf \'%s\\n\\n---\\n*AGY worker: %s | acc: ${{ steps.prompt.outputs.acc_index }}*\\n\' '
    '"$(cat /tmp/final.txt)" "$WORKER_URL" > /tmp/comment.txt'
)
NEW_POST_RESULT = (
    '          printf \'*AGY worker: %s | acc: ${{ steps.prompt.outputs.acc_index }}*\\n\\n---\\n\\n%s\\n\' '
    '"$WORKER_URL" "$(cat /tmp/final.txt)" > /tmp/comment.txt'
)


def patch(text: str) -> str:
    text = text.replace(OLD_TRIGGER_COMMENT, NEW_TRIGGER_COMMENT)
    text = text.replace(OLD_PROMPT_TAIL, NEW_PROMPT_TAIL)
    text = text.replace(OLD_POST_RESULT, NEW_POST_RESULT)
    return text


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    before = open(src).read()
    after = patch(before)
    open(dst, "w").write(after)
    print("CHANGED" if after != before else "NO_CHANGE")
