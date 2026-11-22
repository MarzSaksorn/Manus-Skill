---
name: deployed-frontend-migrator
description: Copy a public deployed frontend into an independent local app, preserve its assets and behavior, and optionally plan or implement migration into an existing backend repository. Use when extracting a Vercel or SPA frontend, creating a standalone local copy, moving it between Git repositories, replacing an old UI while preserving database/storage/YOLO services, or creating a pushed migration branch without rewriting history.
---

# Deployed Frontend Migrator

Extract a rendered frontend safely, keep it independent until integration is explicit, and make the boundary between compiled UI, editable source, and backend behavior clear.

## Core rules

- Treat a compiled deployment as a **bundle-level copy**, not recovered React source.
- Never combine a copied frontend with an old application by default.
- Preserve old Git history. “Remove traces” means a normal deletion commit unless the user explicitly authorizes history rewriting.
- Do not deploy, modify production schema/data, change access, or force-push without explicit confirmation.
- Keep private credentials out of the browser, bundle, logs, screenshots, and commits.
- When feature work is complete, push the authorized feature or migration branch and report the commit. Do not silently push `main`.
- If the user names GitHub, inspect the connector/session configuration before external repository work.

## Choose the workflow

1. **Exact snapshot** → capture the deployed bundle, localize assets, and serve it independently.
2. **Editable replacement UI** → recover source if available; otherwise reconstruct components from the deployed reference and keep the compiled copy as a visual oracle.
3. **Backend-connected replacement** → complete the snapshot workflow, audit the existing backend contracts, write an integration plan, then implement one vertical slice at a time.
4. **Repository migration** → use the branch and verification rules in [repo-migration.md](references/repo-migration.md).

## Workflow

### 1. Confirm scope and safety

Identify the public/authorized source URL, requested destination folder or repository, exact-copy versus editable reconstruction, old repository cleanup, and whether backend/database/model integration is requested.

Separate these actions:

- Copying a public frontend is safe within the request.
- Pushing to a named, authorized repository is allowed.
- Deleting paths from an old repository requires the exact approved scope.
- History rewriting or force-pushing always requires separate explicit authorization.
- Production deployment, schema changes, production data writes, and access changes require confirmation.

### 2. Inspect source and workspaces

Read the relevant scraping, frontend, accessibility, and repository guidance before acting. Check every local repository's remote, branch, working tree, package manager, and existing app structure. Do not overwrite a target clone before inspecting it.

Use Scrapling for rendered SPA capture when available. Follow its security guidance. Do not bypass authentication, CAPTCHAs, or anti-bot controls without authorization. Run `manus-config config load` before external connector work.

### 3. Capture the deployed SPA

Use rendered and raw captures:

```bash
mkdir -p artifacts/live
scrapling extract fetch "$SOURCE_URL" artifacts/live/live-home.md --ai-targeted --network-idle
scrapling extract fetch "$SOURCE_URL" artifacts/live/live-home.html --network-idle
curl -fsSL "$SOURCE_URL" -o artifacts/live/index.html
```

Record the document title, hashed CSS/JS names, asset references, external URLs, visible routes, and interaction behavior. Capture at least 1440×900 desktop and 390×844 mobile screenshots with Playwright. A raw SPA document often contains only `#root`; do not treat it as a complete capture.

Read [capture-and-assets.md](references/capture-and-assets.md) for dynamic SPA and asset details.

### 4. Preserve and localize assets

Start from `index.html`:

1. Copy exact CSS and JavaScript filenames.
2. Search CSS/JS for image, font, media, `/assets/`, and remote API references.
3. Download every permitted first-party asset needed by the requested routes.
4. Keep hashed filenames and root-relative `/assets/...` paths unless rewriting the bundle deliberately.
5. Localize Google Fonts with:

```bash
python /home/ubuntu/skills/deployed-frontend-migrator/scripts/localize_google_fonts.py /absolute/path/assets/index.css
```

Re-run the asset checker afterward. Local assets do not make remote APIs local; report any retained external service calls.

### 5. Build an independent local copy

Prefer this layout for a standalone bundle:

```text
standalone/
├── index.html
├── package.json              # optional static-server command
├── assets/
│   ├── index-*.js
│   ├── index-*.css
│   ├── fonts.css             # when fonts are localized
│   ├── fonts/
│   └── first-party images
├── .stitch/DESIGN.md         # extracted visual tokens, optional
└── reference/                # screenshots and capture notes, optional
```

Use a clearly named nested folder when the destination repository already owns another application. Do not import old React components, CSS, routing, assets, or runtime state into the copy. Add a README with source URL, run command, copy boundary, compiled-source limitation, known demo credentials if publicly documented, and external dependencies.

### 6. Validate the copy

Serve the folder on a separate port and bind `0.0.0.0` only when a public preview is needed:

```bash
python3 -m http.server 5174 --bind 0.0.0.0
python /home/ubuntu/skills/deployed-frontend-migrator/scripts/verify_static_copy.py /absolute/path/to/standalone
```

Browser-check:

- title, logo, fonts, and root-relative assets render;
- login fields, role selector, password visibility, and validation work;
- the supported demo flow reaches its next screen;
- desktop, mobile, and keyboard layouts work without overflow;
- no missing asset requests or unexpected old-app routes appear;
- localized fonts no longer request Google font hosts;
- retained remote APIs are identified and documented.

### 7. Plan backend-connected replacement when requested

Do not wire a minified demo bundle directly to production services. Read [backend-integration.md](references/backend-integration.md).

The repeatable sequence is:

1. Clone or inspect the existing backend read-only and pin its baseline commit.
2. Inventory auth/session, API routers, database schema/migrations, storage, inference/model files, frontend routes, and tests.
3. Compare the deployed bundle with the backend source. Identify simulated users/patients, `localStorage` clinical records, random model output, fake notifications, browser-stored private keys, unsupported thermal/appointment features, and remote endpoints.
4. Map every replica screen/action to an existing contract, a proposed contract, or an honest unavailable state. Never invent an API because the UI suggests one.
5. Record model filename, hash, class order, preprocessing, output shape, threshold, coordinate transform, and runtime packaging.
6. Identify authorization, media access, TLS, timestamp, MIME, pagination, transaction, audit, and delete-semantics defects before integration.
7. Write a plan with baseline commits, evidence, phases, exit gates, acceptance tests, rollback, and decisions still needing user input.
8. Start with one vertical slice: real login → authorized patient → real image → server model → clinician review → persisted record → reload history.

The plan must state whether live database/storage/model verification occurred. Missing credentials or disabled connectors mean “not verified,” not “healthy.”

### 8. Implement on a migration branch

When the user requests a new branch in an existing repository:

```bash
gh repo clone OWNER/REPO /tmp/repo-migration
cd /tmp/repo-migration
git switch -c migration/replica-ui-backend
```

Keep `main` unchanged. A plan-only branch may add `docs/UI_BACKEND_MIGRATION_PLAN.md`; an implementation branch may then replace UI and preserve server/data contracts. Stage, check, commit, and push:

```bash
git add -A
git diff --cached --check
git commit -m "docs: establish replica UI backend migration plan"
git push -u origin migration/replica-ui-backend
```

Verify both the remote branch commit and `main` commit. Report the branch URL, commit hash, diff scope, and whether implementation has started. Do not merge or deploy as part of branch creation.

### 9. Deliver clearly

Report:

- standalone local path and preview URL, if created;
- target repository, branch, and commit hash;
- old-repository cleanup commit, if applicable;
- validation results and known remote dependencies;
- whether the output is compiled bundle-level or editable source;
- whether backend/database/storage/model connectivity was actually tested;
- explicit blockers and the next vertical slice.

## Do not

- scrape private pages or use credentials without authorization;
- call a compiled bundle original source code;
- combine copied UI with an old app unless integration is requested;
- patch minified code to fake a backend connection;
- present random/demo patients, predictions, measurements, or alerts as clinical data;
- expose DB passwords, service keys, model credentials, or private storage URLs in client code;
- send thermal images to an RGB YOLO model or turn a no-detection result into a diagnosis;
- delete old files, rewrite history, modify production data/schema, or deploy without the required approval.

## Bundled resources

- [capture-and-assets.md](references/capture-and-assets.md) — rendered SPA capture and asset discovery.
- [backend-integration.md](references/backend-integration.md) — API/database/storage/model audit and migration-plan requirements.
- [repo-migration.md](references/repo-migration.md) — target, cleanup, branch, and one-folder Git workflows.
- [UI_BACKEND_MIGRATION_PLAN.md](templates/UI_BACKEND_MIGRATION_PLAN.md) — concise reusable plan structure.
- `scripts/localize_google_fonts.py` — localize Google Font imports.
- `scripts/verify_static_copy.py` — detect missing local assets and list retained external URLs.
