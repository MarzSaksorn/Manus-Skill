---
name: careflow-dashboard
description: Build, extend, or audit tablet-first clinical KPI dashboards in the Careflow visual system using HeroUI v3, Tailwind CSS v4, React, and @gsap/react. Use for Careflow dashboard screens, clinical operations KPI surfaces, patient-flow views, capacity monitoring, or requests to recreate or extend this dashboard’s calm high-trust UI and motion language.
---

# Careflow Dashboard

Use this skill to create or extend clinical operations dashboards that feel calm, high-trust, and operationally useful rather than like a generic analytics template. Keep the Careflow identity: warm paper surfaces, spruce signal color, explicit status labels, compact mono metrics, and restrained motion.

## Default stack

Use the current React setup in the target project. For a new or migration-ready project, use:

- React 19 + TypeScript + Vite.
- HeroUI v3 via `@heroui/react` and `@heroui/styles`.
- Tailwind CSS v4 through `@tailwindcss/vite`.
- GSAP plus `@gsap/react`; prefer the scoped `useGSAP()` hook.
- `pnpm` with a checked-in `packageManager` field and lifecycle policy.

Before implementation, verify current HeroUI docs at `https://heroui.com/`. HeroUI v3 is a living library. Do not rely on v2 APIs, old NextUI names, or guessed compound-component signatures.

## Workflow

1. **Inspect before editing.** If this is an existing Careflow project, read `src/App.tsx`, `src/styles.css`, `package.json`, the route manifest, and the project’s current task checklist. Preserve existing data contracts and routes unless the request changes them.
2. **Choose the surface.** Classify the request as a new dashboard, a new dashboard module, a visual refinement, or a data/interaction change. Keep content and data behavior separate from the visual system.
3. **Load references as needed.** Read [design-system.md](references/design-system.md) for tokens and layout. Read [implementation-patterns.md](references/implementation-patterns.md) when adding HeroUI components, GSAP motion, filters, charts, or accessibility states.
4. **Plan the composition.** Start with a persistent navigation rail, utility bar, period controls, a wide care-pulse area, patient-flow context, KPI cards, and one or two lower operational modules. Use the 12-column grid and keep the primary signal visible in the first viewport.
5. **Implement data honestly.** Label illustrative values as demo data. If real clinical data is unavailable, use visibly illustrative records and avoid claims that sound like live clinical reporting. Keep KPI display values, timestamps, trends, and status tones in a typed data model.
6. **Implement interactions.** Use HeroUI components for cards, buttons, chips, tabs, avatars, and select-style controls. Add working active navigation, date-range selection, department filtering, theme toggle, notifications, and report/detail actions when the dashboard scope calls for them.
7. **Add motion with cleanup.** Register `useGSAP`, pass a root ref as `scope`, use `contextSafe` for event callbacks, and keep animation setup client-only. Gate non-essential motion behind `prefers-reduced-motion`.
8. **Check responsive behavior.** Design tablet-first. Keep the rail usable around 768px, switch wide modules to full-width below 1180px, use two-column KPIs around 900px, and stack content below 680px. Preserve touch targets and readable labels.
9. **Validate.** Run the project build and resolve TypeScript/CSS diagnostics. Verify `/` and `public/manus-routes.json`. Capture at least tablet and mobile renderings for visual inspection when the environment supports screenshots. Check that keyboard focus, disabled states, selected tabs, select menus, report dialogs, and reduced-motion behavior remain understandable.
10. **Deliver cleanly.** Keep project metadata and a real Careflow mark in place. Update the checklist, commit the finished change, and push the canonical `main` branch. Report the preview URL or published URL only when it is actually confirmed.

## Careflow guardrails

- Keep status colors semantic: spruce/mint for stable or improving, amber for watch, coral for focus or risk. Never use them as decoration.
- Keep clinical values visually prominent but not sensational. Use `IBM Plex Mono` for values and timestamps.
- Prefer explicit labels such as `Within capacity`, `Improving`, `Watch list`, and `Focus` over color-only indicators.
- Avoid purple-to-pink gradients, neon dark themes, emoji icons, fake logo walls, fabricated patient stories, and giant generic chart grids.
- Use simple local SVG line icons or an existing icon system. Give icon-only controls an accessible label.
- Keep the brand mark distinct from the dashboard chart. Reuse [templates/careflow-mark.svg](templates/careflow-mark.svg) when a project needs the Careflow logo.

## Common requests

- **“Add a KPI card.”** Extend the typed metric model, use a HeroUI `Card`, add an explicit `Chip` status, mono value, trend direction, timestamp, and demo-data label. Keep the card in the responsive metrics grid.
- **“Add a new filter.”** Prefer a HeroUI `Select` with a visible text label, keyboard support, controlled state, and a reflected value in the relevant summary copy.
- **“Animate the dashboard.”** Use a scoped `useGSAP()` entry timeline, count-up values, and a subtle card hover lift. Skip or shorten non-essential motion when reduced motion is requested.
- **“Make it mobile.”** Preserve the hierarchy: utility bar → period controls → care pulse → patient flow → KPIs → lower operations modules. Do not just shrink the desktop grid.

Keep this file as the quick-start workflow. Put detailed tokens, breakpoints, component contracts, and code patterns in the linked references so future dashboard tasks load only what they need.
