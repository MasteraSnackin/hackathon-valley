# Jev routing with hand-off to Claude

TypeSafe's Jev (`jev-1.13.0`) routes every stored message before Claude reads it. Jev is a classifier: it answers typed questions with calibrated probabilities and generates no text. It decides the route when it is sure and the message is simple. Everything that needs judgement or exact quotes goes to Claude. The policy engine and named staff still decide what may happen; Jev's route is a proposal, like Claude's.

## Where it runs

`route_case_messages` is a durable step in the native case coordinator (`app.workflows`), before `triage_case_messages`:

```
message stored (triage "pending", actions WAIT)
  → run_case_cycle reports needs_routing
  → route_case_messages: one Jev request per message → a routing record and one of three modes
      jev_only   Jev's route is applied; Claude is not called
      jev_route  Jev's route is applied; Claude extracts quotes, claims and answers, and may object
      claude     Jev is unsure or unavailable; Claude triages as before
  → triage_case_messages (jev_route and claude only)
  → run_case_cycle: gates re-evaluated
```

Routing records use the idempotent key `route:{source}:{attempt}`, so a retried step never routes or applies a reading twice. A triage retry starts a new attempt and asks Jev again. `WORKFLOW_MODE=manual_demo` and BUILD replay run the same service functions inline.

## The Jev request

One request per message (`app/jev.py`). The state is small and named, because Jev loses accuracy on long, irrelevant context. It holds the new message and its sender label, the case's next step, work item and category (left out for a new case, where they are placeholders), the last three earlier messages trimmed to 600 characters, and the open tenant questions. Questions:

| Key | Type | Purpose |
| --- | --- | --- |
| `route` | Choice over the nine `ROUTES` plus `unknown` | The next step. `unknown` is the explicit hand-off to Claude |
| `category` | Choice over the categories | Used only when its confidence reaches `router_min_confidence` |
| `hazard` | Noul | Possible immediate safety hazard |
| `multiple_issues` | Noul | Several separate problems (splitting needs Claude) |
| `states_facts` | Noul | Access, keys, appointment, completion or price stated (needs exact quotes) |
| `system_instructions` | Noul | Text trying to instruct the software |
| `sensitive` | Noul | Distress, complaint, legal threat or a vulnerable person |

The route criteria are written literally, with boundary cases, because Jev answers the words it is given.

## The decision, in code

`jev.decide` is a pure function over Jev's answers and the active policy:

1. `hazard ≥ router_hazard_threshold`, or Jev chose `urgent_hazard` → **jev_route** to `urgent_hazard`. Claude still reads it, and the existing triage hold sends it to a person. Jev can escalate; it never de-escalates. If Claude reads a hazard where Jev did not, Claude's hazard route wins.
2. Jev chose `unknown`, route confidence `< router_min_confidence`, possible multiple issues, or possible instructions to the system → **claude** (full triage, as before Jev).
3. **jev_only** only if all hold: the route is in `router_jev_only_routes` (`archive`, `request_quote`), route confidence `≥ router_jev_only_confidence`, no stated facts, no sensitive content, no open tenant questions, and either a new case with a confident category, the same route as the case already has, or `archive`.
4. Otherwise **jev_route**: Jev's route is applied, and Claude runs in extraction mode at `CLAUDE_EXTRACT_EFFORT` (default `low`) with a `<router_decision>` block. Claude keeps the route unless it is clearly wrong; then it gives its own route and a `route_objection`. Any difference becomes a `route_disagreement`: **Claude's route is applied** (so a disputed Jev route never anchors later readings; a Jev hazard escalation is kept) and a triage **CONFLICT → HUMAN REVIEW** holds the case until the case manager confirms the reading or sets the route.

A Jev-only reading has no generated text: the work item is the one recorded at intake, there are no claims, and the summary says that Claude did not read the message. Its derived category is recorded but **never auto-accepted**, because Jev does not look for ambiguity; the case manager confirms it. When Jev routed and Claude extracted, the classification auto-accept uses the lower of Claude's confidence and Jev's route confidence (bucketed: ≥ 0.8 high, ≥ 0.5 medium).

## Policy settings

| Setting | Default | Meaning |
| --- | --- | --- |
| `router` | `jev` | `jev`; `jev_shadow` (Jev routes and records, Claude decides every message); `claude` (Jev is not called) |
| `router_min_confidence` | 0.5 | Below this, Jev's route or category is not used |
| `router_jev_only_confidence` | 0.8 | Bar for skipping Claude |
| `router_jev_only_routes` | `archive`, `request_quote` | Validation allows only these two |
| `router_hazard_threshold` | 0.3 | Hazard probability that escalates |
| `router_signal_threshold` | 0.35 | Probability at which a yes/no signal counts |

These were set on fictional messages before the BUILD evaluation was run, not tuned on it. The evaluation led to one behaviour change (Claude's objection is applied), not to threshold changes.

## Failure handling

| Situation | Response |
| --- | --- |
| No `TYPESAFE_API_KEY`, rate limit, timeout or API error | Routing record with `error_type`; Claude triages as before |
| Staff chose the route | Jev is not called; Claude reads the message and never overrides the staff route |
| Claude unavailable after a Jev hand-off or Jev route | The existing failed-reading hold: a person triages or retries |
| Both unavailable | The same hold |

## Audit

Each routing record stores the router mode, Jev's full answers (route probabilities, category, signals), the decision and its reasons, the versioned model ID that answered, the TypeSafe request ID, latency and token usage, and `router_version`. Shadow runs also store `proposed_mode`, the mode Jev would have chosen. The case's `triage.router` and the dashboard interpretation panel show who routed the message and why. `/api/health` reports only whether a TypeSafe credential is configured.

## Verification

- `tests/test_jev_router.py` (offline, fake model answers): each mode, objection and hazard handling, unavailability, shadow and `claude` policies, staff routes, settings validation.
- `tests/test_jev_live.py` (markers `jev` and `claude`): real Jev and Claude calls on fictional messages, covering a clear fault, a gas smell and injected instructions.
- `tests/test_native_api.py::test_native_jev_route_step_routes_a_new_report`: the real Jev call inside the native workflow's `route_case_messages` step.
- `python -m app.route_eval`: the end-to-end BUILD evaluation. Results and their limits are in [evals/JEV_ROUTER_EVAL.md](evals/JEV_ROUTER_EVAL.md).

Tests not marked `jev` run with an empty `TYPESAFE_API_KEY`, so they keep exercising the Claude-only path.
