---
name: motion-ui-performance
description: Design and implement smooth, accessible web motion. Use when adding GSAP, ScrollTrigger, CSS transitions, Framer Motion, card entrances, parallax, hover/press feedback, list transitions, or when fixing janky animation and layout thrashing.
---

# Motion UI Performance

Add motion that clarifies hierarchy and feedback without destabilizing layout, accessibility, or input. Prefer small, reversible changes over a motion-heavy rewrite.

## Workflow

1. **Inventory the interaction.** Identify the trigger, target elements, start/end states, duration, easing, interruption behavior, and reduced-motion alternative. Preserve existing timing and behavior unless the user asks for a new direction.
2. **Inspect the DOM and render lifecycle.** Find where elements are created, replaced, paginated, filtered, mounted, or removed. Animate the actual lifecycle boundary so cards do not replay unexpectedly or animate stale nodes.
3. **Choose the narrowest tool.** Use CSS for simple state changes; use GSAP/ScrollTrigger for coordinated timelines, staggered lists, or scroll-linked effects; use a framework motion library only when the UI already uses that framework. Do not introduce a runtime solely for a one-property transition.
4. **Animate compositor-friendly properties.** Prefer `transform` and `opacity`. Avoid animating `width`, `height`, `top`, `left`, margins, layout-dependent shadows, or filters unless there is no viable alternative. Use FLIP for layout changes and measure only at controlled boundaries.
5. **Keep scroll motion stable.** Use scrubbed transforms with bounded movement, avoid pinned layout surprises, refresh triggers after layout changes, and clean up instances/listeners when the page lifecycle requires it. Do not tie expensive work directly to every scroll event.
6. **Implement reduced motion.** Detect `prefers-reduced-motion: reduce` and provide an immediate or minimal state. Do not hide content or make functionality depend on motion. Ensure the reduced-motion path works in lightweight test harnesses where `matchMedia` may be absent.
7. **Respect input and accessibility.** Preserve focus order, keyboard behavior, hit targets, hover alternatives, and readable contrast. Never use motion to communicate the only state change. Avoid flashing, infinite attention loops, and large parallax on small screens.
8. **Test the lifecycle.** Assert the animation library/script is loaded only as intended, the target hook exists, fresh renders animate the right nodes, reduced motion is covered, and pagination/filter changes do not duplicate or leak animations.
9. **Measure and inspect.** Build the page, inspect the generated artifact, and use browser performance tooling when the request concerns jank or frame rate. Check mobile and low-motion behavior before delivery.

## Defaults

- Entrance cards: `opacity: 0` plus a small `translateY`, then a short stagger; do not animate layout.
- Hover/press: transform and color/border changes; keep feedback under a few hundred milliseconds.
- Parallax: small transform-only offsets, scrubbed to scroll, disabled or minimized for reduced motion.
- Cleanup: retain references to timelines/triggers and kill or disconnect them when content is replaced.
- Easing: use one coherent family per interaction; avoid dramatic bounce for information-dense interfaces.

## Completion report

Report `Trigger/lifecycle`, `Properties animated`, `Reduced-motion behavior`, `Cleanup`, `Tests`, `Browser/performance evidence`, and `Known limitations`. Distinguish source completion from visual acceptance.
