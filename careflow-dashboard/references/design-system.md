# Careflow design system

Use this reference when creating or extending Careflow dashboard screens.

## Brand position

Careflow is a clinical operations command center for care managers. It should feel **calm, precise, and alert**. Copy is direct and observant: “Steady flow across the morning shift.”, “Placement demand needs focus.”, and “Demo data refreshes with your selected period.”

## Color tokens

| Token | Light | Dark | Meaning |
| --- | --- | --- | --- |
| Paper | `#F7F8F5` | `#101916` | Page background |
| Surface | `#FFFFFF` | `#17231F` | Card and utility surface |
| Surface soft | `#F1F5F1` | `#1D2B26` | Subtle control fill |
| Surface mint | `#E7F4EE` | `#18372F` | Care-pulse emphasis |
| Ink | `#13201D` | `#EFF5F0` | Primary text |
| Ink soft | `#53605B` | `#A4B6AD` | Secondary text |
| Ink faint | `#80908A` | `#71867C` | Metadata and timestamps |
| Line | `#DDE5DF` | `#2D4038` | Borders and dividers |
| Spruce | `#0D6B62` | `#75C7B5` | Stable, improving, primary action |
| Spruce deep | `#084E48` | `#A0E1D2` | Hover and emphasis |
| Mint | `#CDEFE4` | `#254E43` | Stable status background |
| Amber | `#F2B84B` | `#F1C35E` | Watch or monitor |
| Coral | `#D9685E` | `#EB8C81` | Focus, risk, escalation |

Do not introduce new hues without a clear semantic reason. Use `color-mix()` to derive soft backgrounds where supported.

## Typography

- Load `Sora` for headings, navigation labels, status labels, and compact control text.
- Load `IBM Plex Sans` for body copy and supporting descriptions.
- Load `IBM Plex Mono` for KPI values, timestamps, period labels, and operational counts.
- Keep headings tightly tracked with a slight negative letter spacing. Make KPI values high contrast, but keep supporting metadata quiet.

## Layout

Use an asymmetrical 12-column grid with a persistent rail:

- Desktop: `92px` rail + flexible content area. The care-pulse card spans 8 columns and patient flow spans 4. KPI cards span all 12 columns in a four-card row. Lower modules use a 7/5 split.
- Around `1180px`: keep the rail compact, move care pulse and patient flow to full-width rows, and render patient-flow stages as a three-column strip.
- Around `900px`: two-column KPI cards and full-width lower modules.
- Around `680px`: collapse the rail into a top navigation strip, stack controls and modules, and render one KPI card per row.
- Keep page padding fluid with `clamp()` and use 13–16px gaps between modules.

Cards use an 18px radius, one-pixel low-contrast borders, no heavy shadow, and semantic HeroUI variants. The care-pulse card uses the mint surface with a quiet ring motif in the upper-right corner.

## Module contracts

### Navigation rail

Use the Careflow mark, four primary destinations, settings, and a small “Live” network indicator. Keep the active page visible through both color and surface fill. On mobile, turn it into a compact top strip with icon-only buttons and accessible labels.

### Utility bar

Show the current workspace title, an explicit `Illustrative demo data` badge, dark-mode toggle, notifications, and the signed-in operator avatar. Icon-only controls need `aria-label` and visible focus.

### Care pulse

Show the period/date, one short operating sentence, a stable/watch status, two summary metrics, a simple SVG pulse chart, and last-signal timestamp. Keep chart labels sparse and include a text alternative through `role="img"` plus `aria-label` or adjacent text.

### Patient flow

Use a vertical sequence of three or more stages with numbered steps, supporting counts, a status chip, and a subtle connector. Status text must remain visible without color.

### KPI cards

Every KPI card includes a label, status chip, prominent mono value, trend statement with direction icon, timestamp, and `Demo data` marker when the values are illustrative. Do not rely on a color alone to communicate a trend.

### Lower modules

Use capacity bars for care areas and a shift-handoff list for time-sensitive work. Include a clear action such as `View report` only when it opens a report, dialog, or detail state.

### Report dialog

Use a modal overlay with a short summary, selected period, department, prepared timestamp, close icon, and a clear return action. Keep the dialog readable on small screens and make the close affordance keyboard accessible.

## Copy rules

Prefer operational language over generic product copy. Good labels are short, factual, and time-bound. Never present illustrative metrics as real clinical evidence. Include “demo data” in the utility badge, metric footer, or module description.
