---
name: safe-git-delivery
description: Safely commit and push authorized software changes to Git. Use when a coding task requires branch creation, commit attribution, remote push, status verification, or a clear separation between pushing code and merging or deploying it.
---

# Safe Git Delivery

Make repository changes traceable and reversible. Treat commit, push, merge, deployment, and external transfer as separate operations with separate authorization.

## Workflow

1. **Inspect first.** Record the repository root, current branch, status, remotes, configured identity, and recent commit. Read applicable Git integration and attribution instructions.
2. **Choose the delivery boundary.** For isolated work, create or use a task branch. Do not switch branches over uncommitted user work. Preserve unrelated modifications and untracked files.
3. **Review the diff.** Run a whitespace/error check, inspect the exact diff, and verify that generated files, secrets, local state, credentials, datasets, and unrelated edits are not staged.
4. **Test before commit.** Run the narrowest relevant build and tests, then broader checks when practical. Report failures honestly; do not make a green claim from a partial run.
5. **Commit narrowly.** Stage only the intended files. Use an imperative, descriptive commit subject. Preserve repository/user attribution rules and include a body when the reason or constraint is non-obvious.
6. **Push only when authorized.** Push the exact branch to the configured remote. Never force-push or rewrite shared history unless explicitly approved. Confirm the remote ref resolves to the local commit.
7. **Verify final state.** Re-run `git status`, branch/commit inspection, and the relevant remote check. State whether the change is committed, pushed, merged, deployed, or merely prepared.
8. **Stop before high-impact steps.** Do not merge, publish, deploy, alter production data, configure secrets, or open a public release automatically after pushing. Ask for separate approval when required.

## Commit hygiene

Use one logical change per commit when possible. Never commit `.env` files, API keys, service-role credentials, private browser/session data, real personal records, generated dependency directories, or large build output unless explicitly required and reviewed. Inspect staged names and diff before committing.

## Recovery

If a test or push fails, inspect the error and current state before retrying. Do not create duplicate commits or rerun destructive commands blindly. Prefer a follow-up fix commit over rewriting a pushed commit. For rollback, use a new revert commit or the documented deployment/data rollback path; do not force-push.

## Completion report

Report `Branch`, `commit`, `remote push`, `tests/builds`, `working-tree status`, `merge/deploy state`, and `next approval needed`. Include exact commit IDs and distinguish local verification from remote verification.
