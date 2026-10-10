# ANSWERS — Property Management track (Reality Test challenge cases)

System-generated results for the 30 **Property Management** cases in
[DwellyOrg/HackatonChallenges](https://github.com/DwellyOrg/HackatonChallenges) (commit `ce84e8c`).
Nothing in these folders was written or corrected by hand.

**Run status: 29 settled, 1 worker_failed.** Final policy outcomes: 18 WAIT, 9 HUMAN REVIEW, 2 NO FURTHER ACTION, 1 STOP ACTION.

Case 022 failed: its native Vercel Workflow coordinator step (`run_case_cycle`) exceeded its
retries on the 31st and last source, after 30 sources had settled. Its folder holds the recorded
partial state and the error; it was not rerun or corrected.

## Run assumption: identity and contact route set aside

The product cannot verify who sent a message or the permitted way to reply, so by default every
case stops at those two checks. For this run the policy setting `assumed_checks: ["identity", "route"]`
treats them as satisfied **unless a source contradicts them**. Nothing was verified. Every other
gate still applies: access consent, landlord authority, schedule, completion evidence, cost, triage
and urgent-hazard rules. This shows what the agent would do once identity is established.

## How it ran

1. `python -m app.challenge_adapter` converted each case mechanically: history event 001 is the
   report; every later event is a separate source at its own timestamp; PDF attachments were
   text-extracted (pypdf) and made available at the case's decision cutoff (`Updated`). See
   [`_run/adapter-report.json`](_run/adapter-report.json) for source file hashes.
2. `python -m app.reality_test` in **official** mode from frozen commit `281c95a` (two batches of 15,
   8 cases in parallel). Each case ran in its own process, SQLite store and **native local Vercel
   Workflow** world through the product's real API: Jev routing → Claude (`claude-opus-5`) reading →
   policy engine. Each source settled before the next was shown. Source hashes were unchanged after
   both batches.
3. All operational adapters (contractor requests, bookings, messages to tenants/landlords/contractors)
   are **simulated**: no real person was contacted. Messages marked *held* wait for staff approval.
   No human review answers were supplied.

The markdown files were rendered from the recorded evidence by commit `545191c` (formatting only:
it adds the settled-source count and native error text for failed cases). Config, manifests,
provenance and summaries: [`_run/`](_run/).

## Per case

Each folder: `ANSWER.md` (received → decision → actions → escalation → missing facts → failures →
result), `REASONING.md` (policy gates, claims with quotes, every Jev/Claude reading per source),
`AUDIT.md` (every step with actor and tool), `input.json` (exact input), `records.jsonl` (raw
immutable records), `result.json`, `provenance.json`, `worker.log`.

| Case | Title | Run (sources) | Decision | Proposed action | System cases | Simulated actions done | Messages (simulated) | Open human checks |
|---|---|---|---|---|---|---|---|---|
| [001](001/ANSWER.md) | Bathroom leak and wall repair | settled (24/24) | **WAIT** | `clarify` | 1 | `request_quote` | 3 sent / 4 held | — |
| [002](002/ANSWER.md) | Gas record and boiler visit | settled (25/25) | **WAIT** | `clarify` | 3 | — | 1 sent / 6 held | classification, completion |
| [003](003/ANSWER.md) | Bathroom and kitchen maintenance | settled (24/24) | **WAIT** | `clarify` | 14 | `clarify`, `request_quote` | 7 sent / 2 held | classification, completion, supported |
| [004](004/ANSWER.md) | Front entrance lock report | settled (23/23) | **WAIT** | `clarify` | 5 | `clarify` | 4 sent / 4 held | authority |
| [005](005/ANSWER.md) | Heating repair invoice and payment details | settled (21/21) | **WAIT** | `clarify` | 1 | — | 4 sent / 7 held | — |
| [006](006/ANSWER.md) | Solar generation readings | settled (17/17) | **NO FURTHER ACTION** | `clarify` | 1 | `clarify` | 0 sent / 0 held | — |
| [007](007/ANSWER.md) | Television, bedroom light and door handle | settled (19/19) | **HUMAN REVIEW** | `confirm_appointment` | 7 | `clarify` | 4 sent / 2 held | authority, classification, supported, triage |
| [008](008/ANSWER.md) | Water ingress affecting two flats | settled (24/24) | **HUMAN REVIEW** | `clarify` | 2 | — | 1 sent / 2 held | triage |
| [009](009/ANSWER.md) | Bedroom Window Maintenance Request | settled (21/21) | **HUMAN REVIEW** | `close_item` | 1 | — | 1 sent / 3 held | completion |
| [010](010/ANSWER.md) | Kitchen cabinet maintenance request | settled (26/26) | **HUMAN REVIEW** | `request_quote` | 2 | — | 2 sent / 5 held | classification, supported |
| [011](011/ANSWER.md) | Kitchen ceiling leak inspection at 16 Brindlewick Mews | settled (24/24) | **WAIT** | `clarify` | 1 | — | 2 sent / 8 held | — |
| [012](012/ANSWER.md) | Lock Maintenance Request | settled (25/25) | **WAIT** | `clarify` | 4 | `clarify` | 4 sent / 4 held | classification, supported |
| [013](013/ANSWER.md) | Kitchen glazing maintenance request | settled (25/25) | **WAIT** | `clarify` | 1 | `request_quote` | 4 sent / 5 held | — |
| [014](014/ANSWER.md) | Heating service request at 7 Mallowmere Walk | settled (19/19) | **HUMAN REVIEW** | `clarify` | 2 | — | 1 sent / 3 held | triage |
| [015](015/ANSWER.md) | Vacant Property Preparation | settled (23/23) | **WAIT** | `clarify` | 5 | `clarify`, `request_quote` | 0 sent / 11 held | — |
| [016](016/ANSWER.md) | Smoke alarm maintenance request | settled (17/17) | **NO FURTHER ACTION** | `clarify` | 1 | `clarify` | 0 sent / 2 held | — |
| [017](017/ANSWER.md) | Flat entrance door maintenance request | settled (20/20) | **WAIT** | `clarify` | 1 | — | 3 sent / 7 held | — |
| [018](018/ANSWER.md) | Kitchen maintenance report | settled (19/19) | **WAIT** | `clarify` | 2 | `clarify` | 1 sent / 2 held | — |
| [019](019/ANSWER.md) | Move-out maintenance at 18 Brindle Row | settled (17/17) | **WAIT** | `clarify` | 1 | `request_quote` | 0 sent / 5 held | triage |
| [020](020/ANSWER.md) | Kitchen socket maintenance request | settled (25/25) | **HUMAN REVIEW** | `clarify` | 1 | — | 0 sent / 1 held | triage |
| [021](021/ANSWER.md) | Hot-water service report | settled (21/21) | **WAIT** | `clarify` | 4 | `clarify` | 0 sent / 5 held | triage |
| [022](022/ANSWER.md) | Washer-dryer maintenance and replacement update | worker_failed (30 settled/31) | **WAIT** | `clarify` | 1 | `clarify` | 7 sent / 6 held | — |
| [023](023/ANSWER.md) | Heating maintenance at 7 Larkspur Fold | settled (25/25) | **WAIT** | `clarify` | 1 | — | 2 sent / 5 held | — |
| [024](024/ANSWER.md) | End-of-occupancy property service request | settled (23/23) | **WAIT** | `clarify` | 1 | — | 0 sent / 6 held | — |
| [025](025/ANSWER.md) | Kitchen tap maintenance request | settled (23/23) | **HUMAN REVIEW** | `clarify` | 4 | `clarify` | 2 sent / 3 held | supported, triage |
| [026](026/ANSWER.md) | Moisture inspection and repair coordination | settled (20/20) | **STOP ACTION** | `confirm_appointment` | 4 | `clarify` | 3 sent / 4 held | authority, schedule, supported |
| [027](027/ANSWER.md) | Move-out maintenance at 46 Fernwick Lane | settled (19/19) | **WAIT** | `clarify` | 8 | — | 0 sent / 5 held | classification, supported, triage |
| [028](028/ANSWER.md) | Move-out maintenance request | settled (27/27) | **HUMAN REVIEW** | `instruct_work` | 1 | `clarify` | 0 sent / 8 held | authority, classification, total |
| [029](029/ANSWER.md) | Heating-system visit enquiry | settled (20/20) | **WAIT** | `clarify` | 2 | `request_quote` | 0 sent / 2 held | — |
| [030](030/ANSWER.md) | Maintenance report at 8 Brindlefern Walk | settled (15/15) | **HUMAN REVIEW** | `archive` | 4 | `clarify` | 0 sent / 2 held | authority, triage |
