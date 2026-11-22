---
name: project-handoff-reader
description: Interpret portable project handoffs and continuation briefs accurately. Use when receiving a TASK-HANDOFF.md, project export, agent continuation note, or development-history summary and asked to understand, review, or continue its work.
---

# Project Handoff Reader

Use a handoff as portable context, not as proof of the current repository, account access, deployment, or external-system state. Extract its intent and constraints first, then verify claims against the live source when available.

## Reading workflow

1. **Read the whole handoff.** Identify the goal, requested time span, requirements, constraints, current-state snapshot, decisions, unfinished work, setup, exclusions, and exact next actions. Do not jump to a file named in the handoff before understanding scope.
2. **Build a concise working model.** Separate:
   - user requirements and safety boundaries;
   - completed work and the evidence cited;
   - historical decisions or dated status;
   - current verified state;
   - open work, uncertainty, and blockers;
   - omitted files, credentials, services, or access.
3. **Resolve references carefully.** Treat repository paths, commit IDs, branch names, URLs, and filenames as pointers. They may be relative to another workspace, stale, private, or not included. Do not claim to have opened them unless you actually did. If the repository is available, inspect its current status and the cited branch/commit before changing code. Preserve unrelated and untracked user work.
4. **Reconcile time-sensitive claims.** Check branch/commit, working tree, remote refs, test/build outcomes, and deployment state against current evidence whenever possible. A past successful test does not prove the current checkout passes; a pushed commit does not mean it was merged or deployed. Report discrepancies explicitly.
5. **Honor omissions.** If the handoff is details-only, do not expect source files, datasets, model binaries, screenshots, secrets, or archives to accompany it. Clone or request only what is missing, using the recipient’s own authorized access. Never attempt to reconstruct credentials or private session data from context.
6. **Continue within authority.** Use the handoff to resume the named task, not to broaden it. Carry forward constraints, rejected approaches, clinical or other domain safety rules, and required confirmations. If a requirement conflicts with current source or is ambiguous enough to change behavior, ask the user before making that decision.
7. **Summarize understanding before consequential work.** State the objective, verified starting point, remaining task, and any mismatch/blocker in a few clear sentences. Then proceed with authorized, reversible work. Obtain explicit confirmation before deployment, production data/schema changes, public exposure, destructive actions, or other hard-to-reverse operations.

## Interpretation rules

- Treat the handoff as a curated summary, not a verbatim conversation transcript or an exhaustive commit log unless it says otherwise.
- Preserve distinctions such as proposed versus implemented, tested versus manually reviewed, local versus remote, pushed versus merged, and merged versus deployed.
- Treat historical metrics, user counts, database contents, model versions, and hosting configuration as time-bound claims.
- Keep clinical model results labelled as decision support. Do not turn a model prediction or synthetic example into a diagnosis or real patient fact.
- When a handoff has a `Not included` section, use it as an explicit boundary. Do not silently expand scope to recreate omitted artifacts.
- Do not create a second handoff, copy files, package archives, commit, push, or transfer content unless requested or clearly part of the task.

## Useful response shape

When asked only to interpret a handoff, reply with:

1. **Goal:** one sentence.
2. **Current position:** branch/commit and what has actually been verified, or state that no repository was available.
3. **Done:** key completed work and evidence.
4. **Next:** concrete next actions in priority order.
5. **Caveats:** missing access/artifacts, stale claims, blockers, or approvals needed.

When asked to continue implementation, keep this summary brief and move into the project’s normal inspection and test workflow. Do not repeat the entire handoff back to the user.
