---
name: ui-preserve-migration
description: Preserve-mode integration and refinement of existing web UIs. Use when adding Tailwind, daisyUI, HeroUI, another component library, a theme switch, or a visual enhancement to an established page while keeping protected layout, behavior, typography, and accessibility stable.
---

# Preserve-Mode UI Migration

Extend an existing interface without turning a targeted change into an unsolicited redesign. Treat current geometry, interaction contracts, copy, accessibility, and visual vocabulary as protected until the user explicitly authorizes a redesign.

## Workflow

1. **Classify the request.** Decide whether it is an extension, preserve-mode migration, or redesign. Use preserve mode when the user asks to add a library/component/theme while keeping the page close to the original.
2. **Inspect before editing.** Read repository instructions, package manifests, build scripts, the actual entrypoint, relevant styles, tests, and the current Git state. Locate the protected markup and event wiring. Do not infer the framework from the requested library.
3. **Capture a baseline.** Record current dimensions/positions, typography, colors, responsive breakpoints, focus behavior, and test expectations. Use an existing screenshot or browser inspection when available; keep the image as a reference, not as a substitute for source inspection.
4. **Read the named library's official guidance.** Use the repository's applicable skill and official documentation for installation, configuration, prefixes, themes, accessibility, and exact component structure. Preserve local naming conventions and avoid importing an entire framework when a focused component layer is sufficient.
5. **Choose the smallest integration seam.** Prefer additive classes, tokens, wrappers, or adapters. Keep existing IDs, names, form values, event listeners, DOM relationships, and layout containers unless changing them is required and approved.
6. **Protect geometry explicitly.** Neutralize component-library defaults that alter font size, weight, padding, line height, width, height, border radius, or positioning. Do not stack conflicting frameworks casually. If native controls must be replaced, implement an accessible equivalent with keyboard, focus, escape, outside-click, and selected-state behavior.
7. **Preserve behavior.** Keep search, pagination, filter synchronization, loading/error/empty states, URL contracts, analytics boundaries, and privacy rules unchanged. Add regression tests for the new library classes and the protected behavior.
8. **Verify in layers.** Build the production artifact, run targeted UI/performance tests, run typecheck and broader tests when practical, and inspect the generated output. For a visual request, perform browser or screenshot checks at desktop and mobile widths when available.
9. **Deliver with traceability.** Report files changed, tests actually run, known limitations, current branch/commit, and whether changes were merely committed, pushed, merged, or deployed. Never claim visual acceptance without browser evidence.

## Component-library rules

- Use the library's documented component class/structure rather than approximating it with unrelated CSS.
- Confirm prefix behavior: a configured prefix may apply to component classes but not necessarily controller/selector classes.
- Keep design tokens mapped to existing semantic roles (`canvas`, `ink`, `muted`, `surface`, `border`, accent) so light/dark themes do not require scattered hard-coded colors.
- For theme switches, use the library's documented controller semantics, keep the control visibly sized, expose an accessible label, support reduced motion, and verify checked/unchecked contrast.
- Avoid adding labels, badges, gradients, icons, motion, or copy merely because the component library offers them.

## Safety and quality gates

Stop and ask before changing protected behavior, data contracts, authentication, production configuration, or a layout that the user required to remain fixed. Do not put secrets or private data in screenshots, tests, handoffs, or commits. Do not delete the old implementation until references, tests, build output, and rollback implications are understood.

## Completion report

Use a concise report with: `Design mode`, `Protected contracts`, `Changed files`, `Build/tests`, `Visual verification`, `Known issues`, `Branch/commit/push/deploy state`, and `Next approval needed`.
