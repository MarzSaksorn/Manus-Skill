---
name: github-branch-delivery
description: Validate, commit, and push authorized code changes to GitHub. Use when a development workflow expects every completed change pushed to the active branch while keeping merge and deployment approval separate.
---

# GitHub Branch Delivery

Deliver validated changes continuously to the active feature branch. Do not silently merge or deploy.

## Before committing

1. Confirm the repository, active branch, remote, and working-tree state.
2. Inspect the diff and stage only intended files. Preserve unrelated user changes.
3. Run the project’s appropriate build, tests, lint/type checks, and whitespace validation. Do not claim release readiness from a partial check without saying so.
4. Never commit credentials, tokens, private session data, real personal records, generated dependencies, or local environment files.

## Commit and push

Use the repository’s configured identity and active branch. If project instructions specify an identity or branch, follow them; otherwise do not invent one.

```bash
git status --short --branch
git diff --check
git add <intended-files>
git commit -m '<specific imperative message>'
git push origin <active-branch>
```

After pushing, verify:

```bash
git status --short --branch
git log -1 --oneline --decorate
git ls-remote origin refs/heads/<active-branch>
```

Report the commit hash, branch, validation results, and whether the remote is synchronized. If push fails, preserve the local commit and report the exact failure; never force-push or rewrite history unless explicitly authorized.

## Approval boundary

Merging to a protected branch, deploying, changing production secrets, importing or publishing production data, running rollback, or changing production schema/policy requires explicit approval even when ordinary feature-branch pushes are authorized.
