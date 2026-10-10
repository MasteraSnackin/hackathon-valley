# Jev router evaluation (BUILD partition)

Generated 2026-10-10T12:14:35+00:00 · 25 cases · events 001–008 of each case, one message at a time · Jev `jev-1.13.0` (`property-router-2026-10-10`) · Claude `claude-opus-5` (`property-triage-2026-10-10.2`).

> Agreement with Claude, not accuracy. Chronological prefixes only; no outcome, later event, index summary or attachment used. Reproduce with `python -m app.route_eval --events 8`.

## 1. Jev against Claude on every message (shadow run)

Claude triaged every message as before; Jev answered the same message independently. Agreement compares Jev's route with Claude's route for the current case issue.

| Jev's own decision | Messages | Same route as Claude |
|---|---|---|
| Act alone (Claude skipped) | 64 | 89% (57/64) |
| Route, Claude extracts | 93 | 73% (68/93) |
| Hand off to Claude | 43 | 49% (21/43) |
| **All** (Jev's raw choice) | 200 | 74% (147/200) |

Jev would have set the route itself for 78% (157/200) of messages and handed 22% (43/200) to Claude.
Of the messages Jev would have handled alone, Claude's reading raised a triage hold (ambiguity, hazard or conflict) on 59% (38/64) and stated claims on 2% (1/64); a Jev-only reading has neither, which is why its category always waits for a person.

Hand-off reasons: low confidence 20, several issues 18, instructions to the system 7.

**Hazards:** Claude read 0 message(s) as a possible urgent hazard; Jev escalated 0 of them and handed 0 to Claude. Jev escalated 1 message(s) in total (1 that Claude did not read as a hazard; each goes to a person either way).

**Option order:** with the route options reversed, Jev chose the same route for 95% (190/200) of messages.

Most frequent differences (Claude → Jev): clarify → request_quote ×16, none → request_quote ×12, instruct_work → request_quote ×4, request_quote → clarify ×4, request_quote → confirm_appointment ×4, none → instruct_work ×2, none → clarify ×2, request_quote → supply_keys ×2.

## 2. End to end with Jev routing and hand-off (jev run)

| Path | Messages | Median seconds per message |
|---|---|---|
| Jev only (no Claude call) | 76 | 0.3 |
| Jev route + Claude extraction | 86 | 5.6 |
| Handed off to Claude | 38 | 9.4 |
| Shadow run (Claude on every message) | 200 | 7.4 |

- Claude was called for 62% (124/200) of messages (shadow run: 100% (200/200)).
- Where Jev set the route and Claude extracted, Claude objected or chose a different route for 5% (4/86) of messages. Each objection is a CONFLICT held for the case manager.
- Anchoring check: where Claude extracted under Jev's route without objecting, the independent shadow reading of the same message chose a different route for 29% (24/82).
- Jev-only messages on an existing case that kept the current route (no change): 82% (62/76).
- Final route matches the shadow run's route for the same message: 78% (155/200); policy outcome matches: 100% (200/200). Later messages can differ because the case history diverges.
- Outcomes (jev run): HUMAN REVIEW 200.
- Outcomes (shadow run): HUMAN REVIEW 200.

## 3. Cost and latency

| | Shadow (Claude on every message) | Jev run |
|---|---|---|
| Claude calls | 200 | 124 |
| Claude input tokens (uncached + cache read + cache write) | 200,264 + 823,400 + 0 | 128,938 + 510,508 + 0 |
| Claude output tokens | 91,955 | 49,816 |
| Jev input tokens | – | 309,256 |

Jev request latency: median 280 ms, p90 393 ms over 400 calls.

## 4. Reading these results

**What the numbers can and cannot show.** There are no route labels for the BUILD cases, and eventual outcomes are deliberately not used as labels. Claude's independent shadow reading is the reference, so "same route as Claude" measures agreement with the previous production behaviour, not correctness. Every BUILD property is outside the trusted demo directory, so identity and contact route are never verified, and every message ends in HUMAN REVIEW in both runs. The 100% outcome match is therefore a ceiling effect: it shows that Jev routing never released an action the Claude-only path held, but it cannot show that Jev releases actions correctly. Message-level effects (route, conflicts, Claude calls, latency) are the informative figures. The 25 cases and these thresholds are the development partition; the reserved partition has not been evaluated.

**Findings.**

- **Cost and latency.** Jev removed 38% of Claude calls (124 instead of 200) and about 46% of Claude output tokens. A Jev-only message is settled in about 0.3 s instead of about 7 s. Jev itself costs about 309k input tokens for 400 calls (about $0.013 at $0.042 per million).
- **Jev-only is mostly "no change".** 82% of Jev-only messages were later messages on an existing case where Jev kept the current route (system notes such as "Maintenance provider assigned"). Of the 7 Jev-only messages where Claude chose differently, Claude saw no actionable issue in 4 ("none"), wanted to clarify in 2, and moved the case on to `instruct_work` in 1 (BUILD 025 event 6). Jev's "keep the route" missed that progression, so it waits for a later message or a person.
- **What Jev-only misses.** On 59% of the messages Jev would handle alone, Claude's reading raised a triage hold, mostly a route-affecting ambiguity. A Jev-only reading never raises one. This is why a Jev-only category is never auto-accepted, and why `router_jev_only_routes` is limited to `archive` and `request_quote`.
- **Anchoring.** When Claude extracts under Jev's route, it objects rarely (5%), yet its independent reading of the same message chose a different route 29% of the time. Showing Jev's route to Claude saves conflicts but weakens Claude as an independent check. The most common pattern is Claude preferring `clarify` where Jev chose `request_quote`. Claude's extraction still records the route-affecting ambiguity in that case, which holds the case as CLARIFY or HUMAN REVIEW.
- **Hazards.** Claude read no BUILD message as a hazard, so this partition cannot measure hazard recall. Jev escalated 1 message in run 2 (BUILD 023: "Key lock not working, can't lock door") and 5 in run 1 (the same lock report and four shower-without-cold-water messages in BUILD 034), all with the same 0.3 threshold. Claude read none of them as a hazard; each goes to a person. The only hazard-recall evidence is the fictional gas-smell live test.
- **Option order.** With the route options reversed, Jev gave the same answer 95% of the time.

**Change made after run 1.** Run 1 (same settings) found that a disputed Jev route was still applied. In BUILD 021, "the key snapped and we don't have a spare" went to `supply_keys`. Claude objected correctly, but later readings anchored on the wrong route, ending in 4 STOP ACTION holds on keys. Since then, an objection applies Claude's route and still holds the case for a person; a Jev hazard escalation is never removed. Run 2 above includes that change and has no STOP ACTION drift. Run-to-run figures also move because Claude is not deterministic and Jev's context depends on the case history Claude produced (run 1: Jev would have acted on 85% of messages, run 2: 78%).

**Run 1 headline figures, before the change:** all-message agreement 76%, Claude calls 126/200, 6 objections out of 88, 4 STOP ACTION outcomes (BUILD 021), 5 hazard escalations.

Raw per-message rows (`var/evals/router-eval.json`, `var/evals/router-eval-run1.json`) are git-ignored. They contain BUILD message text and model outputs, and the summary regenerates from them with `python -m app.route_eval --from-json <file>`.
