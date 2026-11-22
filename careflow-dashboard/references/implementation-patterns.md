# Careflow implementation patterns

Read this reference when implementing components or motion in a React Careflow dashboard.

## HeroUI v3 setup

Install the current packages:

```bash
pnpm add @heroui/react @heroui/styles
pnpm add gsap @gsap/react
pnpm add -D tailwindcss @tailwindcss/vite
```

In the main stylesheet, keep the HeroUI import order:

```css
@import "tailwindcss";
@import "@heroui/styles";
```

Use current HeroUI v3 compound APIs, for example:

```tsx
import { Card, Chip, Tabs } from "@heroui/react";

<Card variant="default">
  <Card.Header>
    <Card.Title>Capacity by care area</Card.Title>
    <Card.Description>Licensed beds used this morning · demo data</Card.Description>
  </Card.Header>
  <Card.Content>{/* metric content */}</Card.Content>
</Card>

<Chip color="warning" variant="soft">Watch list</Chip>

<Tabs selectedKey={range} onSelectionChange={(key) => setRange(String(key))}>
  <Tabs.ListContainer>
    <Tabs.List aria-label="Dashboard period">
      <Tabs.Tab id="today">Today</Tabs.Tab>
      <Tabs.Tab id="7d">7 days</Tabs.Tab>
    </Tabs.List>
  </Tabs.ListContainer>
</Tabs>
```

For filters, use a controlled `Select` with a visible label or `aria-label`, a `Select.Trigger`, `Select.Value`, `Select.Indicator`, `Select.Popover`, and `ListBox.Item` options. Keep the selected value reflected in the dashboard summary.

## GSAP React contract

Use the React integration rather than a raw effect:

```tsx
import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap } from "gsap";

gsap.registerPlugin(useGSAP);

const dashboardRef = useRef<HTMLDivElement>(null);
const { contextSafe } = useGSAP(() => {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  gsap.timeline({ defaults: { ease: "power3.out" } })
    .from(".rail-entry", { x: -16, opacity: 0, duration: 0.55 })
    .from(".top-entry", { y: -14, opacity: 0, duration: 0.45 }, "-=0.24")
    .from(".hero-entry", { y: 18, opacity: 0, duration: 0.62 }, "-=0.12")
    .from(".kpi-card", { y: 18, opacity: 0, stagger: 0.07, duration: 0.48 }, "-=0.36");
}, { scope: dashboardRef });
```

For event-handler animations, wrap callbacks with `contextSafe` so unmount cleanup reverts them:

```tsx
const handleEnter = contextSafe((event: ReactPointerEvent<HTMLElement>) => {
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    gsap.to(event.currentTarget, { y: -4, duration: 0.22, ease: "power2.out" });
  }
});
```

Never target unscoped selectors, call GSAP during SSR, or leave a raw event listener/tween running after unmount.

## Count-up and charts

- Store the real end value in `data-value`, plus `data-precision` and `data-suffix`.
- Animate a local `{ value: 0 }` object and update text in `onUpdate`.
- Keep the static text meaningful before the animation runs.
- Draw simple SVG charts with accessible labels and minimal gridlines. Use semantic color for the single signal line.
- For range changes, render the selected period’s values directly; do not assume the entry animation reruns after every filter change unless that behavior is intentional.

## Interaction states

- HeroUI buttons: use `onPress`, `isDisabled`, `isPending`, `isIconOnly`, `aria-label`, and visible `:focus-visible` styles.
- Tabs: use a controlled `selectedKey`, `aria-label`, and a selected-state surface or underline.
- Select: use keyboard-friendly listbox options and a visible `Department` label.
- Dialogs: use `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, a close button, and a return action.
- Theme toggle: use `aria-pressed`, change the label when the mode changes, and update semantic tokens rather than swapping arbitrary component colors.

## Validation checklist

Run these from the project root:

```bash
pnpm build
curl -fsS http://127.0.0.1:${PORT:-3000}/
curl -fsS http://127.0.0.1:${PORT:-3000}/manus-routes.json
```

Then inspect at least 768px and 375px widths. Confirm that the navigation, tabs, select, notification popover, theme toggle, and report action are all usable without relying on hover. Keep `public/manus-routes.json` synchronized with source routes.
