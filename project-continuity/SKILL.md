---
name: project-continuity
description: Map an unfamiliar software repository and create or read portable continuation handoffs. Use when orienting before implementation, transferring work between agents/accounts, reconstructing project history, documenting current Git state, or preparing a handoff archive.
---

# Project Continuity

Create a trustworthy map of a codebase and a handoff another developer can act on without the original conversation. Separate verified facts, historical context, assumptions, blockers, and approvals.

## Repository mapping workflow

1. Locate the project root and read repository-local instructions first. Identify package manager, workspace boundaries, entrypoints, build/deploy configuration, tests, docs, and generated directories.
2. Capture Git state before changes: branch, HEAD, remote, status, recent history, and whether the working tree is clean. Preserve unrelated user changes and never reset or overwrite them.
3. Map runtime boundaries: frontend, API/serverless functions, workers, database/storage, authentication, external services, and deployment outputs. Record the source-of-truth file for each boundary.
4. Trace one representative user flow end to end. For a search UI, follow markup → event wiring → client request/cache → API route → service/data policy → rendered result. Identify privacy and authorization boundaries.
5. Read tests before editing. Treat test assertions, public field allowlists, URL routes, event names, and data contracts as protected contracts until confirmed otherwise.
6. Produce a concise structural summary with paths, responsibilities, dependencies, risks, and safe next actions. Do not duplicate entire source files in the map.

## Handoff creation workflow

1. Confirm scope: complete history or a focused phase; Markdown only, supporting files, or archive. Ask when the choice changes what is copied.
2. Inspect current state again. Verify branch/commit/remotes, working tree, relevant docs, tests, and deployment status. Never overwrite an existing handoff path; use a new descriptive path.
3. Reconstruct major phases from Git history, task notes, and docs. Include important requirements, reversals, rejected approaches, constraints, and unresolved issues. Use commit pointers for traceability.
4. Write one standalone `TASK-HANDOFF.md` containing: goal, requirements, project/current state, architecture, development history, completed work, verification, known issues, included files, continuation steps, setup commands, exclusions, and receiving-agent notes.
5. Keep source separate from the handoff. Link to repository paths and commits; copy only explicitly requested supporting artifacts. Exclude credentials, tokens, private session data, personal/regulated data, datasets, and unrelated configuration.
6. Distinguish `built`, `tested`, `committed`, `pushed`, `merged`, `transferred`, and `deployed`. Never imply one state from another.
7. Verify the brief by re-reading it. If an archive was requested, inspect its listing and integrity, and provide a checksum outside or alongside the archive without putting a self-referential checksum inside it.
8. Report exact deliverable links, archive contents, omissions, and recipient prerequisites. State clearly when the package was prepared but not transferred.

## Handoff template

```markdown
# Task Handoff: [project/task]
## Goal
## Requirements and constraints
## Project and current state
## Architecture
## Development history and decisions
## Status and verification
## Included files
## How to continue
## Setup and verification
## Not included
## Notes for the receiving agent
```

## Git and external-action boundaries

Use safe read-only inspection by default. Do not commit, push, merge, deploy, change production data, configure secrets, or transfer files unless the user authorized that exact action. When authorized to commit/push, record the exact branch and commit and keep merge/deployment approval separate. Never include raw environment variables or command output containing secrets in a handoff.

## Completion report

Return the handoff brief and archive links, scope, verified repository state, tests/builds actually run, known blockers, and whether any transfer or deployment occurred.
