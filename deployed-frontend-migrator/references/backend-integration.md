# Backend-Connected Frontend Migration

Read this reference when a copied deployed UI must replace an old UI while preserving its backend, database, protected storage, authentication, or ML model.

## 1. Establish evidence

Pin both baselines:

- deployed/replica commit or capture date;
- backend repository commit;
- model filename, SHA-256, label manifest, and runtime versions.

Inspect, preferably read-only:

```text
client routes and state
server routers and auth context
DB schema, relations, and migrations
media storage and protected delivery
model loader, preprocessing, decoder, and packaging
integration/browser tests
runtime and environment configuration
```

If credentials or connectors are unavailable, state that live connectivity was not tested. Empty fallback data is not proof that a database is empty.

## 2. Detect false backend claims

Search the compiled bundle and source for:

```text
Math.random
localStorage / sessionStorage / IndexedDB
mock / demo / simulated / sample
fetch( / axios / remote API URLs
model settings / private key / endpoint inputs
appointment / notification / risk / severity / thermal
```

Classify each result:

| Finding | Treatment |
| --- | --- |
| Demo users or role-selected credentials | Replace with real session/auth; never let a client role selection grant access. |
| Generated patients or local clinical records | Replace with authorized API reads/writes; keep demo mode explicit and isolated. |
| Random model result or fabricated measurement | Delete from connected mode; call the server model and render “inconclusive” honestly. |
| Browser-stored private API key | Remove; keep secrets server-side. |
| Remote endpoint | Document and verify its authorization/data-residency boundary; do not claim local processing. |
| Unsupported feature in UI | Disable or label unavailable until a real contract and data source exist. |

## 3. Build the contract map

For every screen and action, record:

```text
screen/action → existing API procedure or route
              → request/response fields
              → auth requirement and patient scope
              → persistence and audit behavior
              → missing work / acceptance test
```

Prefer existing typed contracts. Do not invent REST envelopes when the application already uses tRPC. If a new route is necessary, document its schema, auth, errors, idempotency, and versioning before coding.

Keep imported/de-identified cohort IDs separate from registered clinical-patient IDs. Do not match records by array position, display name, or guessed code. Preserve nullable values as unavailable instead of filling them with demo values.

## 4. Audit security and integrity before wiring screens

Check at minimum:

- identity-only protection versus patient/organization authorization;
- media signing by arbitrary key versus media-row access checks;
- development auth bypass in production;
- database TLS verification and server-only credentials;
- actual image MIME/format validation and decoded-size limits;
- UTC capture timestamps persisted and round-tripped;
- list limits that silently truncate patients;
- audit events, transactions, retries, and idempotency;
- object deletion versus database-row deletion;
- readiness checks that return healthy when dependencies are unavailable.

Treat missing patient authorization, arbitrary media access, production auth bypass, or secret exposure as blocking findings.

## 5. Preserve the real model contract

Record and test:

- model file and checksum;
- input size, channels, normalization, rotation, and letterboxing;
- output tensor layouts and NMS/IoU behavior;
- class IDs and localized labels;
- threshold and confidence semantics;
- model artifact inclusion in Docker/build output;
- inference latency, memory, and concurrency limits.

Do not equate labels from the replica with labels from the real model. A no-detection response is not a diagnosis. A detection box is not segmentation, centimeter measurement, staging, or treatment advice without validated clinical rules and calibration.

For a 640×640 letterboxed model, preserve the inverse transform when drawing boxes:

```text
scale = min(640 / originalWidth, 640 / originalHeight)
padX = (640 - originalWidth * scale) / 2
padY = (640 - originalHeight * scale) / 2
originalX = (modelX - padX) / scale
originalY = (modelY - padY) / scale
```

Test portrait, landscape, EXIF-rotated, no-detection, malformed, oversized, and missing-model cases.

## 6. Use an evidence-based plan structure

The plan should include:

1. decision and boundaries;
2. pinned baselines and audit findings;
3. target architecture and repository layout;
4. screen-to-backend contract map;
5. database and record-integrity rules;
6. model/inference connection and clinical limits;
7. blocking defects and required fixes;
8. implementation phases with exit gates;
9. acceptance tests proving real connectivity;
10. cutover, rollback, and decisions needing approval;
11. source links and external references.

Use [the bundled template](../templates/UI_BACKEND_MIGRATION_PLAN.md) as a starting point. Keep the plan honest: proposed contracts must be marked proposed, and “push branch” must not be described as “deploy.”

## 7. Start with a vertical slice

Implement and test this path first:

```text
real login
  → authorized patient list/detail
  → RGB capture or upload
  → server-side model inference
  → clinician review
  → protected image/prediction persistence
  → audit event
  → reload patient history
```

Only after this works should the team connect dashboard aggregates, reports, notifications, appointments, or thermal workflows. Unsupported UI panels should show a truthful unavailable state.

## 8. Release gates

Require evidence for:

- real session and logout behavior;
- cross-patient denial and media-access denial;
- DB round trips with audit and capture timestamps;
- upload validation and storage retrieval;
- exact model load and overlay transform;
- no mock/random output in production bundle;
- mobile/desktop/deep-link/browser behavior;
- no secrets or patient data in client bundles/logs;
- measured runtime memory/latency and model packaging;
- approved migration SQL, backup/rollback plan, and deployment payload.

Do not run production writes or schema changes merely to prove a UI integration.
