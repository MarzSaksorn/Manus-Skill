---
name: performant-ui-motion
description: Add or repair smooth browser interaction motion. Use when animating menus, selection feedback, cards, headers, scroll effects, hover states, or other UI interactions where 60fps performance and reduced-motion support matter.
---

# Performant UI Motion

Add restrained motion that communicates state without changing layout or making the interface feel busy.

## Performance rules

- Animate `transform` and `opacity` per frame whenever possible.
- Avoid animating `width`, `height`, `top`, `left`, `margin`, `padding`, `box-shadow`, or `filter` for interaction motion.
- Use CSS keyframes for simple entrance effects and GSAP for imperative timelines, selection feedback, or ScrollTrigger behavior when the project already uses GSAP.
- Do not add a second animation loop or a new motion library without a clear requirement.
- Clear temporary inline styles after GSAP tweens with `clearProps`.
- Do not leave `will-change` permanently on many elements; use it sparingly and remove it when idle.

## Interaction recipe

1. Preserve the existing DOM, keyboard behavior, focus order, and hit areas.
2. Animate an opening menu with a short `opacity` plus `translateY`/`scale` keyframe. Keep the duration roughly 160–220ms and use an intentional ease-out curve.
3. Animate selection confirmation on the existing trigger after the value and visible label are synchronized. A small `opacity`, `y`, or `scale` pulse is enough.
4. Keep selection feedback bounded: no infinite loops, layout-size changes, or animation on initial synchronization unless explicitly requested.
5. Gate JavaScript motion behind the project’s reduced-motion check. Ensure CSS motion is disabled or shortened under `prefers-reduced-motion: reduce`.
6. For scrubbed scroll motion, use `ease: 'none'`; register ScrollTrigger before use; call refresh after layout/content changes.

## Verification

Run the project build, focused UI tests, and `git diff --check`. Add regression assertions for the animation hook, easing, reduced-motion guard, and any protected selector. Perform executable browser acceptance only when explicitly requested. If profiling is available, confirm the animation does not produce per-frame layout or paint work.
