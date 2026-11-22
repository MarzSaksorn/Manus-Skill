# [Product]: replace the old UI with the deployed replica UI

**Date:** [YYYY-MM-DD]

**Status:** Proposed plan. No production integration performed.

**Implementation branch:** [owner/repo/tree/branch]

**Replica reference:** [source URL or repository]

**Backend baseline:** [owner/repo/commit]

## 1. Decision and boundaries

State whether this is an exact snapshot, editable reconstruction, or backend-connected UI replacement. State what remains unchanged: database, storage, auth, model, IDs, and Git history. State what is explicitly out of scope.

## 2. Evidence and audit findings

| Area | Replica behavior | Existing backend | Required change |
| --- | --- | --- | --- |
| Auth |  |  |  |
| Patients |  |  |  |
| Clinical records |  |  |  |
| Media |  |  |  |
| Model |  |  |  |
| Notifications/appointments |  |  |  |
| Thermal/native workflow |  |  |  |

Record mock/localStorage/random-output findings and whether live DB/storage/model verification happened.

## 3. Architecture and repository layout

```text
Browser UI → same-origin API → server auth/access checks
                         ├→ existing database
                         ├→ protected object storage
                         └→ server-side model runtime
```

List files to preserve, replace, add, and keep as a frozen visual reference.

## 4. Screen-to-backend contract map

| Screen/action | Existing route/procedure | Auth and patient scope | Persistence/audit | Missing work and test |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Mark proposed contracts as **proposed**. Do not invent undocumented APIs.

## 5. Database and record integrity

Document existing tables/IDs, imported versus registered records, timestamp rules, pagination, transactions, audit, idempotency, storage reconciliation, and additive migrations. Do not recreate or modify production schema without approval.

## 6. Model and clinical limits

Record model filename/hash, classes, preprocessing, output shapes, thresholds, coordinate transforms, packaging, runtime limits, and disclaimer. State what the model does not prove. Define no-detection, invalid-image, unavailable-model, timeout, and stale-result behavior.

## 7. Blocking defects

| Priority | Evidence | Required fix |
| --- | --- | --- |
| Blocking |  |  |
| Important |  |  |

## 8. Phases and exit gates

1. Baseline and access → [gate]
2. Editable replica foundation → [gate]
3. Secure vertical slice → [gate]
4. Clinical records/media → [gate]
5. Real model path → [gate]
6. Reports/settings/cutover → [gate]

Start with: real login → authorized patient → real image → server model → clinician review → save → reload history.

## 9. Acceptance tests

- Authentication, session expiry, logout, and production bypass rejection.
- Cross-patient and unauthorized-media denial.
- Database round trips, audit, timestamps, and pagination beyond the old limit.
- Upload format/size validation and protected storage retrieval.
- Exact model load, output contract, box transform, and no-detection behavior.
- No random/demo clinical output in the connected build.
- Mobile, desktop, keyboard, refresh, back button, and deep links.
- No secrets or patient data in browser bundles, logs, or screenshots.

## 10. Cutover, rollback, and approvals

List staging environment, target runtime, migration SQL, backup/rollback steps, deployment payload, and the actions requiring explicit approval. A pushed Git branch is not a deployment.

## 11. References

- [Backend router]
- [Schema/migrations]
- [Model pipeline]
- [Replica capture/design]
- [External platform guidance]
