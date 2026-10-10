# ANSWERS — Property Management track (Reality Test challenge cases)

System-generated results for the 30 **Property Management** cases in
[DwellyOrg/HackatonChallenges](https://github.com/DwellyOrg/HackatonChallenges) (commit `ce84e8c`).
Nothing in these folders was written or corrected by hand.

**Run status: 26 settled, 4 interrupted.** Cases 027–030 were stopped part-way when the operator's session
ended; their folders hold the partial evidence that had settled, marked `interrupted`. They are
not complete decisions and will be replaced only by a fresh system run, never by edited answers.

## How it ran

1. `python -m app.challenge_adapter` converted each case mechanically: history event 001 is the
   report; every later event is a separate source at its own timestamp; PDF attachments were
   text-extracted (pypdf) and made available at the case's decision cutoff (`Updated`). See
   [`_run/adapter-report.json`](_run/adapter-report.json) for source file hashes.
2. `python -m app.reality_test` ran each case in its own process, SQLite store and **native local
   Vercel Workflow** world, 8 cases in parallel, through the product's real API: Jev routing →
   Claude (`claude-opus-5`) reading → policy engine. Each source settled before the next was shown.
3. All operational adapters (messages, contractor booking, payments) are **simulated**. No human
   approvals were supplied, so the system stops at the people it escalates to.

Mode: `preparation` (not the frozen official mode), source commit `26542cf`. Config, manifest
and provenance: [`_run/`](_run/).

## Per case

Each folder: `ANSWER.md` (received → decision → actions → escalation → missing facts → failures →
result), `REASONING.md` (policy blockers, claims with quotes, every Jev/Claude reading per source),
`AUDIT.md` (every step with actor and tool), `input.json` (exact input), `records.jsonl` (raw
immutable records), `result.json`, `provenance.json`.

| Case | Title | Run (sources) | Decision | Proposed action | System cases | Actions executed | Open human checks |
|---|---|---|---|---|---|---|---|
| [001](001/ANSWER.md) | Bathroom leak and wall repair | settled (24/24) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [002](002/ANSWER.md) | Gas record and boiler visit | settled (25/25) | **HUMAN REVIEW** | `request_quote` | 4 | 0 | classification, identity, route, triage |
| [003](003/ANSWER.md) | Bathroom and kitchen maintenance | settled (24/24) | **HUMAN REVIEW** | `clarify` | 11 | 0 | classification, identity, route, supported, triage |
| [004](004/ANSWER.md) | Front entrance lock report | settled (23/23) | **STOP ACTION** | `confirm_appointment` | 5 | 0 | access, authority, classification, identity, route, schedule |
| [005](005/ANSWER.md) | Heating repair invoice and payment details | settled (21/21) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [006](006/ANSWER.md) | Solar generation readings | settled (17/17) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [007](007/ANSWER.md) | Television, bedroom light and door handle | settled (19/19) | **HUMAN REVIEW** | `confirm_appointment` | 6 | 0 | access, authority, classification, identity, route, schedule, triage |
| [008](008/ANSWER.md) | Water ingress affecting two flats | settled (24/24) | **HUMAN REVIEW** | `clarify` | 2 | 0 | identity, route, triage |
| [009](009/ANSWER.md) | Bedroom Window Maintenance Request | settled (21/21) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [010](010/ANSWER.md) | Kitchen cabinet maintenance request | settled (26/26) | **HUMAN REVIEW** | `request_quote` | 4 | 0 | classification, identity, route, supported |
| [011](011/ANSWER.md) | Kitchen ceiling leak inspection at 16 Brindlewick Mews | settled (24/24) | **HUMAN REVIEW** | `request_quote` | 1 | 0 | classification, identity, route, triage |
| [012](012/ANSWER.md) | Lock Maintenance Request | settled (25/25) | **HUMAN REVIEW** | `close_item` | 6 | 0 | classification, commitments, completion, identity, route, supported |
| [013](013/ANSWER.md) | Kitchen glazing maintenance request | settled (25/25) | **HUMAN REVIEW** | `confirm_appointment` | 1 | 0 | access, authority, identity, route, schedule, triage |
| [014](014/ANSWER.md) | Heating service request at 7 Mallowmere Walk | settled (19/19) | **HUMAN REVIEW** | `confirm_appointment` | 3 | 0 | access, authority, identity, route, schedule, supported, triage |
| [015](015/ANSWER.md) | Vacant Property Preparation | settled (23/23) | **HUMAN REVIEW** | `confirm_appointment` | 7 | 0 | access, authority, classification, identity, route, schedule, triage |
| [016](016/ANSWER.md) | Smoke alarm maintenance request | settled (17/17) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [017](017/ANSWER.md) | Flat entrance door maintenance request | settled (20/20) | **HUMAN REVIEW** | `request_quote` | 1 | 0 | identity, route, triage |
| [018](018/ANSWER.md) | Kitchen maintenance report | settled (19/19) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [019](019/ANSWER.md) | Move-out maintenance at 18 Brindle Row | settled (17/17) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [020](020/ANSWER.md) | Kitchen socket maintenance request | settled (25/25) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [021](021/ANSWER.md) | Hot-water service report | settled (21/21) | **HUMAN REVIEW** | `clarify` | 4 | 0 | identity, route, triage |
| [022](022/ANSWER.md) | Washer-dryer maintenance and replacement update | settled (31/31) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [023](023/ANSWER.md) | Heating maintenance at 7 Larkspur Fold | settled (25/25) | **HUMAN REVIEW** | `clarify` | 1 | 0 | identity, route, triage |
| [024](024/ANSWER.md) | End-of-occupancy property service request | settled (23/23) | **HUMAN REVIEW** | `close_item` | 1 | 0 | commitments, completion, identity, triage |
| [025](025/ANSWER.md) | Kitchen tap maintenance request | settled (23/23) | **HUMAN REVIEW** | `close_item` | 3 | 0 | classification, commitments, completion, identity, route, supported, triage |
| [026](026/ANSWER.md) | Moisture inspection and repair coordination | settled (20/20) | **HUMAN REVIEW** | `confirm_appointment` | 4 | 0 | access, authority, identity, route, schedule |
| [027](027/ANSWER.md) | Move-out maintenance at 46 Fernwick Lane | interrupted (18/19) | **HUMAN REVIEW** | `clarify` | 4 | 0 | classification, identity, route, triage |
| [028](028/ANSWER.md) | Move-out maintenance request | interrupted (17/27) | **HUMAN REVIEW** | `confirm_appointment` | 3 | 0 | access, authority, classification, identity, route, schedule, triage |
| [029](029/ANSWER.md) | Heating-system visit enquiry | interrupted (11/20) | **HUMAN REVIEW** | `clarify` | 2 | 0 | identity, route, triage |
| [030](030/ANSWER.md) | Maintenance report at 8 Brindlefern Walk | interrupted (13/15) | **HUMAN REVIEW** | `close_item` | 3 | 0 | classification, commitments, completion, identity, route, supported |
