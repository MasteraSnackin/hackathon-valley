# Property Management — case 009: Bedroom Window Maintenance Request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 24 Bramblewick Lane, Alderfen, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-10T18:20:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 21 of 21
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `b3b37b35bb9d1a0b…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 20 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-08-12T09:10:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-08-12T10:05:00+00:00 | Event 002 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 2 | 2025-08-13T10:15:00+00:00 | Event 003 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 3 | 2025-08-13T13:40:00+00:00 | Event 004 — Email from Dorian Pike (Landlord) |
| 4 | 2025-08-14T09:20:00+00:00 | Event 005 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-17T11:00:00+00:00 | Event 006 — Email from Dorian Pike (Landlord) |
| 6 | 2025-08-17T11:25:00+00:00 | Event 007 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 7 | 2025-08-17T14:10:00+00:00 | Event 008 — Email from Elena Voss (Tenant) |
| 8 | 2025-08-18T09:00:00+00:00 | Event 009 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 9 | 2025-08-19T09:15:00+00:00 | Event 010 — Email from Dorian Pike (Landlord) |
| 10 | 2025-08-19T10:30:00+00:00 | Event 011 — Email from Dorian Pike (Landlord) |
| 11 | 2025-08-20T08:40:00+00:00 | Event 012 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 12 | 2025-08-27T10:05:00+00:00 | Event 013 — Email from Elena Voss (Tenant) |
| 13 | 2025-08-28T13:00:00+00:00 | Event 014 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 14 | 2025-08-28T13:20:00+00:00 | Event 015 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 15 | 2025-08-28T13:35:00+00:00 | Event 016 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-01T15:10:00+00:00 | Event 017 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-02T09:25:00+00:00 | Event 018 — Email from Elena Voss (Tenant) |
| 18 | 2025-09-10T09:05:00+00:00 | Event 019 — Email from Dorian Pike (Landlord) |
| 19 | 2025-09-10T18:20:00+00:00 | Event 020 — Email from Elena Voss (Tenant) |
| 20 | 2025-09-10T18:20:00+00:00 | Attachment forwarded-document.pdf (PDF text extraction) |

## Final decision — system case `3ca2e532ad72`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Reported maintenance (category windows)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** The new message is an extracted Landlord Gas Safety Record for 8 Thistledown Mews, Vellumby — a different property from the case address — dated 8 September 2025 with a satisfactory outcome. It contains nothing about the window work or its completion.

**Why:** Document relates to a different property and a different subject (gas safety), so it cannot evidence completion of the window work; clarification is needed before closing.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Jev routed this message to close_item, but Claude reads it as clarify: close_item is not appropriate: the only new material is a gas safety record for another property (8 Thistledown Mews), which provides no usable evide … | Attachment forwarded-document.pdf (PDF text extraction) |

### Missing information and conflicting facts

- **completion** (blocks the route): The forwarded document is a gas safety record, not evidence that the window work is complete; usable completion evidence is still needed from the contractor or landlord.
- **location** (blocks the route): The document names 8 Thistledown Mews, Vellumby, which does not match the case property at 24 Bramblewick Lane, Alderfen. Confirm whether it was sent to this case in error.
- 5 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
