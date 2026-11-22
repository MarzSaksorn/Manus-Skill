---
name: preserve-mode-ui-maintenance
description: Preserve-mode maintenance for existing browser UIs. Use when making targeted visual, accessibility, theme, layout, or component-library changes without rewriting the page or changing protected behavior.
---

# Preserve-Mode UI Maintenance

Improve an existing browser UI with the smallest change that satisfies the request. Preserve information architecture, content, routes, component positions, interaction contracts, accessibility wins, and responsive behavior unless the user explicitly asks to change them.

## Workflow

1. Inspect the current source, styles, tests, and build configuration before editing. Treat generated output as output, not source.
2. Classify the change as a bounded extension or preserve-mode redesign. Do not turn a focused fix into a broad visual overhaul.
3. Identify protected contracts: navigation, form names and order, data allowlists, accessibility labels, selectors, persistent-state keys, and user-facing copy.
4. Use the project’s existing component library and design tokens. Follow its exact class names, prefixes, theme-controller conventions, and component structure.
5. Use theme-aware semantic colors for text and surfaces. Avoid fixed dark text colors on dark-theme surfaces.
6. Avoid collisions with framework-reserved CSS variables. For example, if a component library requires a numeric `--border` token, use a separate page token such as `--line` for border colors.
7. Keep public data boundaries intact. Never expose credentials, internal IDs, source metadata, audit details, or private records.
8. Add focused regression assertions for changed markup, styles, accessibility hooks, and theme behavior.
9. Run the project’s build, focused tests, and whitespace checks before delivery. Review the final diff and confirm only intended files changed.
10. Commit and push validated changes when the user’s workflow expects continuous GitHub delivery. Treat merge, deployment, production data, schema, and policy changes as separate approval-bound actions.

## Quality rules

- Prefer existing components and tokens over bespoke replacements.
- Preserve keyboard access, visible focus, labels, contrast, and touch targets.
- Keep the requested language and content voice.
- Respect reduced-motion preferences for new animation.
- Report what was changed, what was tested, the commit/branch state, and any remaining release caveats.
