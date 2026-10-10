# Behaviour diagrams

These maps describe the implementation reviewed at commit `2732af60a920d0f9a88be18a36e078aa22fbfa6d`. They show the native local Workflow path. Claude is an implemented Anthropic API integration. Operational messages, contractor actions, bookings and payments are simulated. No live API call or case mutation was performed for this documentation work.

| Diagram | Reader's question | Editable source | GitHub source |
| --- | --- | --- | --- |
| [Tenant message](tenant-message.html) | What happens after a confirmed report reaches the case system? | [Sequence JSON](tenant-message.sequence.json) | [Mermaid](tenant-message.mmd) |
| [Human review](human-review.html) | How does a scoped response resume the workflow? | [Sequence JSON](human-review.sequence.json) | [Mermaid](human-review.mmd) |
| [Action decision](action-decision.html) | When can an action proceed, clarify, wait or need review? | [Workflow JSON](action-decision.workflow.json) | [Mermaid](action-decision.mmd) |
| [Policy publication](policy-publication.html) | How does a published policy affect work already in progress? | [Workflow JSON](policy-publication.workflow.json) | [Mermaid](policy-publication.mmd) |

## Tenant intake and case processing

Before the sequence starts, the tenant conversation gathers the tenant's name, address and problem list. It uses Claude when configured and a local parser as the intake fallback. The tenant checks a summary before the API creates the shared case. This intake fallback is separate from case triage: a failed case-triage call goes to staff. The submitted source is stored before the case coordinator asks Claude to interpret it.

The sequence combines each fresh policy cycle with the next due model step to keep the main path readable. The native coordinator actually calls `run_case_cycle`, inspects the returned work flags, invokes a separate triage or composition step, then loops through another fresh cycle. It limits model steps to eight per wake before waiting again. A received hook transports an event identifier and revision hint; the step reloads substantive evidence and policy from the application database.

Triage can split a separate issue into a child case and start that child's coordinator. The main sequence leaves that branch out. It also omits startup recovery, concurrent hook ownership and HTTP polling. The Mermaid version makes the failure and optional-question branches explicit.

Claude proposes a route, assertions and ambiguities. Quote checks discard unsupported quotations. Assertions remain unverified; policy can auto-accept only a derived category label at the configured confidence. Claude also proposes tenant questions and whether to send them. Deterministic checks then enforce the current policy, topics, risk flags, question coverage, identity and contact route. The stored tenant message uses a simulated in-app channel.

## Human review

Review responses are `approve`, `correct`, `reject`, `defer` and `more_evidence`. A response has to come from the review's permitted role and refer to a current review. An authority, finance or custom-rule grant needs an exact action scope, supporting evidence and an expiry within policy. Triage confirmation is a separate approval path. A correction verifies a selected source claim; it does not invent a new fact.

The two `If` messages in the interactive sequence show alternative outcomes after reassessment. They are not two consecutive actions that always happen. The Mermaid source uses an explicit `alt` block for these branches. The action ledger is a responsibility inside the same application database transaction, not a separate provider or deployment.

An approval changes only the requirement it covers. Missing access permission, an unverified completion claim or another unresolved blocker remains visible after the wake. An uncertain action result must be reconciled before retry. A successful simulated action is not proof that a contractor was contacted or a repair was completed.

## Action outcomes and policy versions

The action flow uses the exact outcome strings from the code: `ACT`, `STOP ACTION`, `HUMAN REVIEW`, `CLARIFY`, `WAIT` and `NO FURTHER ACTION`. The service preserves every blocker and chooses the headline in the order stop, review, clarify, wait. `NO FURTHER ACTION` means that the current business action already has a successful simulated receipt; the repair may still need a later proposal.

Custom rules can add requirements and holds but cannot remove the action's default checks. A clarification itself needs verified identity and a contact route. When a relevant source assertion arrives, a person may still need to verify it through the permitted role.

Policy suggestions are drafts. The bounded plain-English assistant does not rewrite code or publish rules. A policy editor saves the draft, previews impact and explicitly publishes. Publication requires a current preview saved by that editor. Unfinished actions then remain held until an authorised staff member explicitly requests reassessment. Completed business actions keep the original decision and policy version. Approvals bound to a previous policy may no longer satisfy fresh checks.

## Source evidence

The source ranges below refer to the reviewed commit. They are ordinary code references; the sequence and workflow schemas do not perform Archify's architecture-specific repository-link verification.

| Behaviour | Source |
| --- | --- |
| Pre-case Claude intake, quoted details and readiness | `app/ai.py:91-139`; `app/tenant.py:189-222`, `309-355`, `389-414` |
| Durable tenant message reservation and after-commit wake | `app/tenant.py:276-306`, `487-515` |
| Case source, event and wake intent committed before triage | `app/service.py:29-69`, `198-218` |
| API wake and response ordering | `app/main.py:21-46`, `129-140`, `167-180` |
| Native steps, model-step bound and hook/timer wait | `app/workflows.py:76-177`, `179-209` |
| Claude case reading outside the SQL transaction and checked persistence | `app/service.py:296-389`; `app/ai.py:193-253` |
| Tenant question selection, send checks and simulated channel | `app/service.py:419-491` |
| Review role, status, scope, source and expiry checks | `app/service.py:240-289` |
| Pure requirement evaluation, response precedence and custom rules | `app/domain.py:239-328` |
| Service clarification refinement and completed-action handling | `app/service.py:131-196` |
| Simulation, stable action identity and reconciliation | `app/service.py:536-571` |
| Draft, impact preview, explicit publication and pending reassessment | `app/service.py:574-613` |
| Plain-English policy interpretation and resolved-review suggestions | `app/policy_assistant.py:254-373` |

The original local review recorded the reviewed source hashes in `source-snapshot.json`; that working record is not part of the published package. The references above remain pinned to the reviewed commit. No dataset or reserved evaluation case was opened for these diagrams.

## Validation and visual review

All four interactive maps pass all nine Archify showcase checks with zero composition errors or warnings. Each has an exact-source delivery receipt. Automated Chrome checks pass at 1440 x 900, 1600 x 1000, 1920 x 1080 and 2048 x 1320. The final light view at 1440 x 900 and dark view at 2048 x 1320 were inspected for readable labels, route separation and page containment.

Published receipt paths are normalised to repository-relative paths; source and HTML hashes are unchanged. The [review summary](../review-summary.json) preserves the reported checks from the original diagram review.

The sequence layouts needed two focused layout correction rounds to fit the desktop page while preserving message text and readable type. The action flow needed none; the publication flow needed one width correction. The tenant label was then updated to state the confirmed-intake boundary and the artifact was validated, delivered and checked again.

The Mermaid sources are supplied for GitHub code fences. They were reviewed for meaning but were not rendered by a local Mermaid installation. Interactive search, route selection and export controls were not manually exercised in this pass. Diagram validation does not prove live model quality, hosted Vercel execution, provider delivery or repair completion.
