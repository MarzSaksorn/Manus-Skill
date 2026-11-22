# Repository Migration and Branch Workflows

Read this reference when the user names a target Git repository, requests a migration branch, asks to move the copied frontend, or asks to remove it from an old repository.

## Before changing a repository

1. Inspect connector configuration when GitHub or another external service is involved.
2. Clone the exact repository and verify its default branch, remote, package manager, working tree, and current commit.
3. Inspect the target tree before copying. Do not overwrite an existing app root without a decision.
4. Pin the source and target commits in the plan.

## Empty target repository

Treat the target as the canonical home only when the user asks for that. Copy the standalone app to its root unless a nested folder is requested. Commit and push the authorized branch; don't create a second local remote by accident.

## Existing target repository

Use a dedicated folder when the repository already owns an application. If the user asks to replace its UI, keep backend/data paths intact and document the migration boundary. Preserve unrelated application code until the replacement is validated.

## Create a migration branch in an old repository

Use this when the user wants the new migration to live in the existing backend repository:

```bash
gh repo clone OWNER/REPO /tmp/repo-migration
cd /tmp/repo-migration
git switch -c migration/replica-ui-backend
```

For a plan-only branch, add only the approved plan and reference material. For implementation, keep the old `main` app available while replacing components incrementally.

```bash
git add -A
git diff --cached --check
git commit -m "docs: establish replica UI backend migration plan"
git push -u origin migration/replica-ui-backend
```

Verify:

```bash
gh api repos/OWNER/REPO/git/ref/heads/migration/replica-ui-backend --jq '.object.sha'
gh api repos/OWNER/REPO/git/ref/heads/main --jq '.object.sha'
git diff --stat origin/main...HEAD
git status --short --branch
```

Report the branch URL, commit hash, changed paths, and whether implementation has started. Do not merge, deploy, or change production configuration as part of branch creation.

## Old repository cleanup

Use the least destructive operation that satisfies the request:

1. Confirm exact paths to remove.
2. State that a normal deletion commit removes them from the current branch but keeps history.
3. Ask separately before rewriting history or force-pushing.
4. Delete only approved paths.
5. Run `git diff --cached --check`.
6. Commit with a cleanup message and push the current branch.
7. Verify the remote tree contains no approved paths.

Never interpret “remove traces” as permission to rewrite Git history. A history rewrite changes commit IDs, affects other clones, and can destroy auditability.

## One local linked folder

When the user wants one local folder tied to the target repository:

1. Push the target repository first.
2. Clean and push the old repository while its clone still exists.
3. Stop preview services using the old folder.
4. Remove or archive the old local clone as requested.
5. Move the target clone into the final path.
6. Verify `git status`, `git remote -v`, and the latest commit.
7. Restart the preview from the final path and rerun browser smoke tests.

## Useful GitHub checks

```bash
git push -u origin migration/replica-ui-backend
gh api repos/OWNER/REPO/git/trees/migration/replica-ui-backend?recursive=1 --jq '[.tree[].path]'
gh api repos/OWNER/REPO/git/ref/heads/main --jq '.object.sha'
```

A GitHub tree check proves the current branch contents. It cannot erase history and must not be described as doing so.
