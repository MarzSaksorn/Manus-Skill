# Capture and Asset Discovery

Read this reference when the source is a Vercel, Vite, or other client-rendered SPA.

## Capture sequence

1. Fetch the rendered page with Scrapling and save both Markdown and HTML.
2. Fetch the raw document with `curl` to record exact CSS/JS filenames.
3. Download referenced CSS and JavaScript bundles.
4. Search the bundles for first-party assets and external dependencies.
5. Render the page in Playwright at desktop and mobile sizes.

Example inspection commands:

```bash
curl -fsSL "$SOURCE_URL" -o artifacts/live/index.html
python3 - <<'PY'
from pathlib import Path
import re
html = Path('artifacts/live/index.html').read_text(errors='ignore')
for ref in re.findall(r'(?:src|href)=["\']([^"\']+)', html):
    print(ref)
PY

rg -o '(/assets/[^"'"'"'` )]+|https?://[^"'"'"'` )]+)' artifacts/live/index.js artifacts/live/index.css | sort -u
```

When a hashed bundle references a logo such as `/assets/logo-abc.jpg`, save it with that exact path and filename under the standalone root. Root-relative paths are part of the deployed bundle contract.

## Dynamic SPA cautions

- Raw HTML often contains only `<div id="root"></div>` and asset tags. It is not enough to prove that the UI loaded.
- Use `--network-idle` or an equivalent rendered fetch so the capture includes hydrated text and controls.
- Some apps use an empty initial login form and populate demo credentials only after a role button is clicked. Test the real interaction sequence instead of assuming defaults.
- A successful login may replace the login screen with a dashboard in the same URL. Assert the post-login heading or landmark, not only the URL.
- If a copied bundle points to `/assets/...`, serve it from the domain root. Serving the folder under `/vercel-frontend/` without rewriting the bundle will break those paths.

## Asset categories

Classify references before copying:

| Category | Action |
| --- | --- |
| Hashed CSS/JS/image asset | Copy locally with the exact filename. |
| Font import | Localize with `localize_google_fonts.py`, then verify. |
| SVG fragment such as `url(#clipPath)` | Keep inside the bundle; it is not a file request. |
| Remote API endpoint | Document it; don't pretend the service is local. |
| Analytics/debug runtime | Remove only if it is clearly platform-injected and not part of the deployed UI. |
| External image/media | Copy only when permitted and needed by the requested screen. |

## Screenshot acceptance

Capture at least:

- 1440×900 desktop login.
- 390×844 mobile login.
- A post-login dashboard screen when the public demo supports it.

Use screenshots to catch missing fonts, broken asset paths, wrong viewport behavior, and accidental reuse of the old application.
