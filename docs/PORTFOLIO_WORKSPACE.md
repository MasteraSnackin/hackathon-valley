# Portfolio workspace

The Portfolio workspace extends the live Property Desk application with six staff tools. It uses the same case records, source evidence and published policies as the case queue. A building link, shared incident or visit plan does not grant identity, access or spending authority.

## Start here

Open `/dashboard`, then choose **Portfolio**. The workspace uses cases already in the application; it does not import examples automatically.

1. With the **property manager** role, open **Related incidents** and select a case. Record a confirmed building identifier, required trade and the source of those details. Add an asset and time window only when known. Use the same building identifier for cases that staff have confirmed belong together.
2. Review possible connections. Confirm a shared incident with a reason, or dismiss the suggestion. Both decisions are saved. New supporting information can cause a dismissed connection to need another review.
3. Open **Visit planning**, record a contractor's trade and supplied availability, then select cases and a compatible window. The saved plan shows each case's outstanding checks. Cancel an obsolete plan before replacing its reserved slot.
4. Use **Property history** to find earlier linked reports, **Evidence comparison** to inspect disagreements, and **Case playback** to move between saved decisions.
5. For **Policy comparison**, use the policy editor role and select a draft already saved in **Policies**. Choose the cases to compare, then run the preview. Publishing still requires the separate policy-editor process.

## Related incidents

Staff first link cases to a building or property group and, where known, an asset. These are explicit organisational links with a recorded reason. Suggestions use the recorded grouping and similarities between cases. They describe a possible relationship, not a diagnosis.

A case manager can confirm a shared incident or dismiss it. Each linked case keeps its own conversation, evidence, reviews and operational permissions. Resolving an incident does not resolve its member repairs.

## Evidence comparison

Comparison groups source assertions by fact and scope. The panel shows original quotations, source labels, recording times and verification state. Different statements are not automatically a verified conflict: supersession, scope and verification matter. Staff continue to resolve facts through the existing role-checked case review.

## Contractor planning

Staff supply trade and availability details, select cases and propose a visit window. The planner checks compatibility and overlapping plans and exposes outstanding policy requirements. Plans are tentative internal records. Saving one does not contact a contractor, confirm an appointment or instruct work.

Planning records retain the case revisions used when they were made. Later changes are surfaced as stale plans requiring review. Contractor availability is staff-entered information, not a live contractor-system integration.

The browser labels its local timezone and sends timestamps with an explicit offset. Nonexistent or repeated local times around daylight-saving changes require a different unambiguous time; the form does not silently shift an appointment. This board does not optimise routes, estimate travel or establish job durations.

## Property and asset history

The history view brings together cases linked to the same property group or asset. It shows their recorded outcomes and links back to the original cases. Repeated reports can justify an investigation, but do not establish a common cause or a failed previous repair on their own.

## Recorded case playback

Playback steps through saved policy decisions and the evidence recorded by each point. It does not rerun today's model or policy against old history. A source received later is excluded from earlier frames even if its stated event date is older.

The controls are read-only. Rewinding does not change the live case, reopen a repair or send a message.

## Policy comparison

A policy editor selects a saved draft and compares its rule results with the current published policy at the same evaluation time. The comparison shows individual checks and blockers, not just the headline outcome. The workspace describes its assumptions, including how policy versions affect approvals and how rule evaluation differs from operational question or reminder handling.

Comparison does not publish the draft or update cases. The existing policy editor still owns preview, explicit publication and reassessment. Completed actions retain their recorded history.

## Data and access

- All endpoints use the existing staff authentication boundary.
- Grouping and planning changes require the case-manager role. Policy comparisons require the policy-editor role.
- New inputs are validated, recorded with their actor and time, and kept separately from source claims and permissions.
- The workspace loads live case data. It does not automatically load the BUILD corpus, inspect reserved evaluation cases or seed demonstration records.
- The separate dataset map remains a historical exploration surface. It does not establish the current state or permissions of a live case.

## Verification

Local checks on 10 October 2026 used an isolated SQLite database, a separate native Workflow directory and three fictional maintenance reports. No model credentials or external operational adapters were used.

- Backend and HTTP tests cover role/origin checks, grouping without inherited permissions, source disagreement, historical evidence cut-offs, pure policy comparisons, overlapping plans, cancellation, changed case/policy/profile data, and restart persistence.
- Browser checks covered all six sections: dismissing and confirming incidents; viewing both sources in a dispute; advancing and rewinding without future sources; saving, rejecting an overlapping visit and cancelling; following a history link to its case; and comparing a saved draft without publishing it.
- The six sections were checked at 1440px desktop width and at 390px and 320px mobile widths. Desktop and mobile screenshots were inspected. These are local interface checks, not a usability study or hosted deployment verification.

The [verification record](PORTFOLIO_VERIFICATION.md) lists the commands and results. External operations remain simulated.
