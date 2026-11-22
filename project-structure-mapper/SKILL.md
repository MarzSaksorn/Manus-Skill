---
name: project-structure-mapper
description: Map an existing software repository so future work can proceed with architectural context. Use when a user asks to understand, orient yourself in, document, or create a structural map of a project or codebase, especially before UI, frontend, or feature work.
---

# Project Structure Mapper

Build a concise, evidence-based mental model of an existing repository before implementation. Default to read-only inspection. Do not create or modify project files unless the user asks for a saved architecture document or source changes.

## Workflow

1. **Confirm the target.** Use the exact project directory selected by the user or established by the active workspace. Inspect existing agent/project instructions first, such as `AGENTS.md`, `CLAUDE.md`, or equivalent. Respect them and avoid printing secret values.
2. **Sketch the repository.** List top-level entries and a bounded source-file tree (typically depth 3). Exclude generated/vendor folders such as `.git`, `node_modules`, build outputs, and caches. Note the primary languages and framework from manifests and source files.
3. **Read the entry points and manifests.** Inspect package/build scripts, app bootstrap, root shell, router, global styles, and runtime/deployment configuration. Use the project README as context, but treat source and configuration as stronger evidence when they disagree.
4. **Trace the main architecture.** Follow the path from entry point through routes/screens, shared components, state/data loading, and service/API boundaries. Identify the main domain types, data fixtures or persistence layer, and calculation/business-logic utilities.
5. **Inspect by feature boundary.** Read representative files from each major area. For large files, use targeted ranges, symbol searches, or route/function inventories instead of dumping the entire file. Distinguish active code paths from components or services that exist but are not wired into the app.
6. **Extract UI conventions when relevant.** Record the actual theme tokens, typography, component patterns, chart/icon libraries, language, responsive behavior, and motion conventions from code. Do not infer a brand system from generic defaults.
7. **Check operational boundaries.** Summarize how to run/build/lint, how development and production differ, which environment variable names are expected (never disclose values), and where API routes or deployment rewrites are defined. Flag in-memory/mock/demo behavior separately from durable storage.
8. **Return a compact map.** Explain where future changes belong and which contracts should be preserved. Include useful file paths and note uncertainty or mismatches. Do not turn a structural orientation request into a code audit or redesign.

## What to Capture

Prioritize information that helps the next task:

- **App composition:** entry point, root shell, routing/navigation, major screens, shared layout.
- **Data flow:** state ownership, fetch/cache path, data types, fixtures, persistence, transformations.
- **Service boundaries:** API entry point, endpoint groups, request/response shapes when relevant, external services.
- **UI system:** styling method, global tokens, reusable components, visual conventions, charting and icon libraries.
- **Runtime:** commands, build/deploy shape, environment variable names, test/lint availability.
- **Constraints:** legacy/unwired modules, mock data, ephemeral in-memory state, notable coupling, and files likely to be protected contracts.

Be precise about certainty. Say “the source shows” for directly verified facts, “appears to” for a reasoned inference, and call out discrepancies rather than smoothing them over.

## Efficient Inspection

- Start with `git status` only when it is safe and useful; never reset, stash, clean, or otherwise alter repository state.
- Prefer bounded tree listings and focused file reads. Use search to inventory route declarations, exports, imports, and component references.
- Read relevant components in parallel when they are independent, but trace dependencies sequentially when one discovery determines the next file to inspect.
- Avoid broad recursive reads of large datasets, lockfiles, generated files, and secrets. Read a small representative sample when the file is primarily fixture data.
- Do not install packages, run migrations, start external services, or invoke deployment actions merely to understand structure.
- If runtime validation is requested, separate it from static mapping and follow the repository’s existing scripts. Do not claim tests passed unless they ran successfully.

## Default Response

Use a short narrative and a small set of sections tailored to the repository. A useful default is:

1. **Project structure** — key folders and what belongs in them.
2. **App/data flow** — entry point, shell, navigation, state, and data/services.
3. **Conventions** — UI and implementation patterns worth preserving.
4. **Operational notes** — run/build/test commands and runtime boundaries.
5. **Change map** — which files or modules are the likely home for future work.

Keep the result concise enough to reuse as working context. Link or cite paths inline. Save a separate architecture note only when requested or when it clearly improves continuity and the user authorizes a project-file change.