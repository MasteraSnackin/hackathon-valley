# Architecture map source notes

The [interactive map](property-workflow.html) describes the local Property Desk application reviewed on 10 October 2026. It is an architecture explanation based on inspected source, not a runtime trace or deployment certificate. The workspace is not a Git repository, so the map makes no revision-pinned repository verification claim. Implementation work continued outside this documentation task; the frozen diagram does not automatically track those changes.

## Scope and source links

| Map component | Reviewed sources | What the component represents |
| --- | --- | --- |
| Browser views | [index.html](../../static/index.html), [app.js](../../static/app.js), [style.css](../../static/style.css) | Tenant conversations and staff case/policy views in one static client |
| FastAPI boundary | [main.py](../../app/main.py), [tenant.py](../../app/tenant.py) | Same-origin APIs, server-owned roles, separate tenant sessions, conversation ownership and a restricted tenant projection |
| Case service | [service.py](../../app/service.py) | Evidence, claims, reviews, approvals, policy versions, action revisions and transactional events |
| Application store | [store.py](../../app/store.py) | Local SQLite: append-only `records`, mutable `cases` and `meta`; the PostgreSQL path is unverified |
| Native Workflow | [workflows.py](../../app/workflows.py), [pyproject.toml](../../pyproject.toml) | Native Python SDK coordinator, registered steps, typed hook, durable waits and local lifecycle/recovery adapter |
| Workflow events | [workflows.py](../../app/workflows.py), [runtime notes](../WORKFLOW_RUNTIME.md) | The SDK's separate local event directory; the embedded delivery queue itself is in memory |
| Action policy | [domain.py](../../app/domain.py), [service.py](../../app/service.py) | All requirements for the current action, scoped and expiring grants, and explicit reassessment after policy publication |
| Simulated actions | [service.py](../../app/service.py) | Transactional intent and a deduplicated simulated receipt; uncertain outcomes need reconciliation |
| Source interpreter | [ai.py](../../app/ai.py) | Default literal interpretation and exact-quote validation; generated assertions do not grant authority |
| OpenAI Responses | [ai.py](../../app/ai.py), [.env.example](../../.env.example) | Optional external API path enabled only by explicit live mode; no live model request was made for this map |

The tenant bridge and policy assistant are included within the API/application responsibilities to keep the overview readable. [tenant.py](../../app/tenant.py) durably reserves message delivery, then uses the shared intake/evidence service. [policy_assistant.py](../../app/policy_assistant.py) is a deterministic drafting aid: a staff member may explore supported wording, but a policy editor must save, preview and publish the result. Neither parser establishes real identity, consent or authority.

The diagram shows logical responsibilities. In native local mode, FastAPI, the case service and the SDK's embedded queue share one application process. The simulated action ledger is also application code and records, not a separate provider. The source-interpreter arrow represents interpretation calls; the interpreter's return is a proposal, not a policy decision. Both the case store and SDK event directory must be retained for supported local restart recovery.

## Evidence and limitations

- [ARCHITECTURE.md](../../ARCHITECTURE.md) gives the full component, action-requirement and data-model descriptions; [README.md](../../README.md) gives isolated local startup instructions.
- [WORKFLOW_RUNTIME.md](../WORKFLOW_RUNTIME.md) records prior local native execution, hooks, timers, duplicate prevention and restart/interrupted-step checks. This map generation did not rerun those application tests.
- [VERIFICATION.md](../VERIFICATION.md) is a historical test snapshot. Its result is not a claim that every later change has passed that suite.
- Vercel cloud execution, shared PostgreSQL, production staff/tenant identity, live model calls, attachment storage/extraction and real outbound adapters remain unverified or unimplemented as described in the architecture document.
- Operational effects are simulated. A hook receipt is not processed-event acknowledgement; a simulated action receipt is not evidence of delivery, booking, access, payment or physical repair.
- The local prototype serialises transactions and uses one application process. No throughput, high availability, failover, encryption-at-rest, regulatory compliance or multi-organisation isolation claim is made.
- The BUILD loader/replay is a supporting development path, omitted from the primary diagram. It is documented in [build_data.py](../../app/build_data.py), [replay.py](../../app/replay.py) and [BUILD_REPLAY_BOUNDARY.md](../BUILD_REPLAY_BOUNDARY.md). The existing shared-runtime exposure disclosure remains applicable. No case data, evaluation material, private environment file or runtime database was inspected to author this map.

## Diagram artefacts

- [Editable architecture JSON](property-workflow.architecture.json)
- [Self-contained HTML](property-workflow.html)
- [Deterministic validation result](property-workflow.validation.json)
- [Atomic delivery receipt](property-workflow.delivery.json)
- [Automated browser evidence](property-workflow.visual-check.json)
- [Light and dark screenshot contact sheet](property-workflow.visual-check.html)
- [Handoff and visual-review record](property-workflow.handoff.json)

The three guided views focus the report path, native orchestration, and the permission/interpretation boundary. Search, focus and route tracing use the authored graph. They do not measure live traffic, runtime health or production failure impact. Animation is disabled; the reader controls navigation.
