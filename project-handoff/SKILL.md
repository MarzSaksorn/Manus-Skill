---
name: project-handoff
description: Create portable developer handoffs from a project's repository, task history, and current state. Use when someone asks to export project context, summarize work for another agent/account, prepare a continuation brief, or package development history and next steps.
---

# Project Handoff

Create a portable, accurate account of work so another developer can continue without access to the original conversation, workspace, credentials, or connected services.

## Workflow

1. **Confirm the scope.** Identify which project/task and time span to cover, intended recipient/use, and output form (folder, archive, or both). Establish whether the user wants details only or supporting files. Ask a focused question only if a missing choice changes what should be included. Do not treat an attachment of a guide as authorization to export unrelated content.
2. **Inspect current state first.** Locate the project root and review the working tree, branch, remotes, recent commits, relevant README/docs, tests, and deployment/config files. Preserve untracked or user-owned assets. Never overwrite an existing handoff path; choose a new descriptive folder or ask if location matters.
3. **Reconstruct the history.** Use available Git history, task notes, conversation export, and project docs. Organize work into meaningful phases; retain important user requirements, reversals, architecture decisions, safety boundaries, and unresolved issues. Do not invent details or imply historical claims are current. Label dated or production-state facts as historical when appropriate.
4. **Separate source of truth from handoff.** Link to repository paths, branches, commits, or external references as pointers. Copy source files only if the user requests supporting artifacts and they are necessary. In a details-only handoff, create only the handoff brief; do not copy project files or produce an archive unless requested.
5. **Protect sensitive information.** Exclude credentials, API keys, tokens, private session data, hidden prompts, personal data, patient information, and unrelated account configuration. Use placeholders for required recipient secrets and explain that the recipient must obtain their own authorized access. Do not include private data merely because it appears in logs or chat.
6. **Write an actionable brief.** Use the template at `templates/TASK-HANDOFF.md` as a flexible structure. Include project goal, requirements, architecture, chronological phases, current branch/commit/state, completed work, verification, decisions, caveats, exact next steps, included/excluded items, and recipient prerequisites. Distinguish code completion, tests, push, transfer, and deployment; never claim a transfer or deployment that did not happen.
7. **Verify the result.** Confirm the new output exists, is complete, and includes only the intended materials. Re-read the brief, check branch/commit references and relative links, inspect archive contents if requested, and check that no secrets or unrelated files slipped in. Do not stage, commit, or push a handoff automatically unless asked.
8. **Report clearly.** Link the exact deliverable path. Summarize its scope and omissions, say whether it was merely prepared or actually transferred, and identify any recipient steps needed.

## Project-history practices

- For a long-lived codebase, report major development phases rather than dumping every commit. Include commit-level detail when the user asks for it or when a particular change needs traceability.
- Record current `git status` honestly. Note unrelated untracked files and leave them alone.
- Describe branch ancestry and remote state only when verified. Avoid presenting a feature branch as deployed or merged.
- Summarize tests/builds with counts and warnings only when the command actually ran. Call out unavailable Docker/cloud/browser environments rather than implying a runtime check passed.
- Include operational commands only when they were verified against the project docs/config. Warn about destructive commands and external actions.
- Preserve human context that affects engineering: why a change was made, constraints such as retaining navigation/title bars, rejected approaches, and decisions that must not be reversed casually.
- For clinical, financial, or otherwise safety-sensitive software, carry forward domain disclaimers, synthetic-data boundaries, and approval requirements.

## Output modes

- **Details only:** One portable Markdown brief. Do not copy source files, datasets, screenshots, binaries, secrets, or create an archive unless asked.
- **Supporting artifacts:** Copy only explicitly scoped files needed to reproduce, review, or continue the task. Keep useful relative paths and list omissions with reasons.
- **Archive:** Create only when requested or chosen during scope confirmation. Keep the standalone handoff brief available and verify the archive listing.

On Cloud/Sandbox environments, do not claim a handoff was transferred to another account. Provide the prepared file/folder for the user to share unless an actual transfer tool was authorized and verified.
