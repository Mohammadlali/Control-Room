# RULES -- generated, do not edit

`python Tools/rules_index.py --write` regenerates this file from the tools
themselves. `check_rules_index` fails if it is stale, so it cannot drift from
the code the way `LEARN.md`'s hand-written table did -- that table said TWELVE
gates while the suite ran TWENTY-EIGHT.

**Each rule lives in ONE place: the file that enforces it.** The incident that
bought it is in that file's header, where whoever changes the rule will read
it. These lines are pointers, not the rules.

## Run before you stop (49)

- `check_archive_index` -- every archived block must say where its conclusion
- `check_changelog` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_cited_flags` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_digest_grep_contract` -- fail if a workflow greps a Python tool's
- `check_digest_provenance` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_gate_commit_reachable` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_handover` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_heredoc_backticks` -- fail on an unescaped backtick inside an
- `check_map_frontier` -- MAP.md must name the NEWEST run that has been
- `check_map_pending_blockers` -- a blocker a PENDING task depends on must be
- `check_morning_freshness` -- fail if the newest Reports/morning/ report is
- `check_names` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_org` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_review_guild` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_reviews` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_rules_index` -- Team/RULES.md must match the tools it describes.
- `check_status_feed_freshness` -- fail if StatusFeed/status.json's own
- `check_struck_terms` -- terms the owner has STRUCK from this project must not
- `check_task_quality` -- reject a pending task that cannot be falsified.
- `check_working_branch` -- HEAD must be the project's working branch, or a
- `poll_tasks` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_archive_map_blocks` -- can the trim tool actually REFUSE, and does it
- `probe_check_archive_index` -- can check_archive_index actually FAIL?
- `probe_check_changelog_invisible` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_changelog_merge_exempt` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_cited_flags` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_digest_grep_contract` -- prove check_digest_grep_contract can
- `probe_check_digest_provenance` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_gate_commit_reachable` -- can the gate actually FAIL, on the
- `probe_check_handover` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_heredoc_backticks` -- can check_heredoc_backticks actually
- `probe_check_map_frontier` -- can check_map_frontier actually FAIL, and does
- `probe_check_map_pending_blockers` -- can check_map_pending_blockers actually
- `probe_check_morning_freshness` -- can check_morning_freshness actually FAIL,
- `probe_check_org` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_review_guild` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_status_feed_freshness` -- can check_status_feed_freshness
- `probe_check_struck_terms` -- can check_struck_terms actually FAIL?
- `probe_check_task_quality` -- can check_task_quality actually FAIL, and does
- `probe_check_working_branch` -- can check_working_branch actually FAIL, and
- `probe_dispatch_runs` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_hook_gates_stop` -- can the Stop hook actually REFUSE, is it really
- `probe_hook_guard_bash` -- can the guard actually refuse, and does it refuse
- `probe_role_brief` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_run_worker` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_watch_runs` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_worker_deliver` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `team_lint` -- that is the lead's job and it is the harder half. What it can do is
- `verify_claims` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)

## Present, not in the suite (32)

Diagnostics and one-off probes. Not run before stopping.

- `check_cloud_stamp` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_image_public` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_map_asset_freshness` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `check_workflow_yaml` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `hook_gates_stop` -- a Stop hook that runs the whole gate suite itself, is
- `hook_guard_bash` -- a PreToolUse hook that refuses the mistakes this project
- `probe_agy_auth` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_agy_credential` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_agy_image` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_audit_github` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_chain_of_command` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_cloud_stamp` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_map_asset_freshness` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_check_reviews` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_collect_status_feed` -- test status feed collection across accounts and gate suites
- `probe_dispatch_backlog` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_docker_preflight` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_domain_restructuring` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_engine_comparison` -- how much real engine-level (C++) programming
- `probe_fix_all` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_image_credential` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_push_notification` -- verify Web Push VAPID keys, quiet green transitions, and payload encryption
- `probe_renpy_domain_scoping` -- how many of Team/org.json's 9 current
- `probe_renpy_persian` -- verify Persian text rendering in Ren'Py 8.5.3
- `probe_run_fleet` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_run_gates` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_sync_runner_repos` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_team_lint_margin` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_ue5_pivot_scope` -- re-measure Team/reports/ue5_pivot_scope.md's counts
- `probe_url_rewrites` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)
- `probe_verdict_empty_outputs` -- does the Verdict step compare a step output
- `probe_worker_pull` -- NO SUMMARY LINE IN THE TOOL (a debt, not a pass)

## Undocumented: 46 of 81

These carry no `# name -- summary` line, so this index cannot say what they
prevent. **That is a counted debt, not a pass.** Add the line to the tool, not
to this file.

