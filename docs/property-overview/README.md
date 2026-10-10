# Property street map and known reported issues

This is a read-only view of the 25 authorised BUILD cases. It shows the issues and follow-up matters recorded against each synthetic property address, with source quotations and links to the pinned public records.

Open `index.html` through the local server to browse the overview. Switch between Map and List, search by address, case number or issue, and combine case-type and evidence-gap filters. Both views select the same property panel. The view, filters and selection are retained in the local page URL for reloading or bookmarking.

The shared panel has Summary, Questions and Evidence tabs. Summary shows every recorded item with its own evidence state, plus a proposed next question. “Why this needs checking” expands the reasoning. The persistent “View evidence” button opens the source quotations; the equivalent button beside an issue goes directly to that issue's evidence. Historical case status remains separate from issue evidence states.

## Walkthrough

![Looping overview walkthrough: filter Garden, select case 019, check item states, read evidence and use List](property-overview.gif)

The GIF uses real screens from this overview. It shows how to find a record and check what its evidence supports. These are historical synthetic cases with invented map positions, not live repair progress. A [static map preview](updated-map.jpg) is also available.

To follow the example after starting the local page:

1. Choose **Garden** in the case-type filter and select **case 019**.
2. Read the proposed next check and expand **Why this needs checking** for its reasoning.
3. Compare the item states in **Summary**. Garden clearance is reported complete, while levelling, gravel and final usability remain unconfirmed.
4. Use an item's **View evidence** button to open its supporting quotation. The **Questions** tab collects gaps and uncertainties in the record.
5. Switch to **List** to browse without using the map. Both views keep the same selected property; clear the filters to see all 25 records again.

No step sends a message, books a visit, updates a policy or confirms a physical repair. The walkthrough is a snapshot of a prototype that is still changing.

## Run locally

From the repository root:

```sh
python3 -m http.server 54037 --bind 127.0.0.1 --directory docs/property-overview
```

Open `http://127.0.0.1:54037/index.html`. Use another port if 54037 is occupied. The overview needs no API key, application database or running workflow engine. Street tiles require internet access. GitHub shows the HTML source; use the local server to interact with the page.

To rebuild the embedded inventory and verify its source references:

```sh
python3 docs/property-overview/assemble.py
```

## Coverage

- 25 case records with 25 different property-address labels.
- 47 reported issue, work or follow-up entries across 752 history events. These entries are not a count of unique active defects.
- 272 original source-quotation checks plus 188 checks supporting the new evidence states and next questions (460 exact checks in total; reused quotations are counted again).
- 47 evidence states and 25 suggested next checks, with exact source references. No issue is labelled independently verified. A broad case-completion statement does not automatically establish every subitem's completion.
- Eight supplied attachment files across three cases. The PDFs were not re-examined for this overview.
- Some synthetic event dates are after the review date of 10 October 2026. All 25 final case metadata records say `Completed`. This is a recorded case status, not a new finding that the property is currently free of defects.
- Both Markdown files for every case were checked against the BUILD manifest: 50 matching source hashes.
- Only the BUILD partition was accessed. Reserved evaluation cases were not read or used.

Source dataset revision: `9bcdca585955dfb930005ed742572606e68f5688`.

Case material and quoted evidence come from [DwellyOrg/HackatonPublicCases at the pinned revision](https://github.com/DwellyOrg/HackatonPublicCases/tree/9bcdca585955dfb930005ed742572606e68f5688/Property%20Management). The project's Apache licence does not relicense third-party dataset material. Leaflet retains its [bundled licence](vendor/leaflet/LICENSE); OpenStreetMap attribution remains visible on the map.

## How the inventory was prepared

The review used each authorised case's index and full event history. The issue list includes explicitly reported physical problems, work items and property-related follow-up matters. Source quotations support each listed item and each record-specific caveat. A room or location appears only when the cited source states it. Locations have not been inferred from repair type.

Recorded outcomes are summaries attributed to the historical case. Questions about property identity, contradictory accounts, dates or missing proof remain separate from the repair list. A missing attachment does not prove that a job failed. A reminder sent after a completion report does not by itself establish a direct contradiction.

The address in each case's index is used as its catalogue label. It is not a verified property identifier, and differing references in the history are not automatically merged or corrected. The `BUILD-` reference is a demo label for the source case, not a property-register ID.

This view uses complete historical records and retrospective summaries. It must not be used as decision-time replay input, training evidence for the held-out evaluation partition or a live work queue.

## What can be built with this data

A property overview can show known reports, linked work items, follow-up concerns and source evidence. The application already has case details, claims, action blockers and parent/child issue links that could supply a live version after property identities have been reconciled.

The data does not establish a complete condition survey, repeated maintenance history for the same property, present-day occupancy or current repair status. The street map uses 25 clearly labelled invented positions around central London, as requested. None is a real location for the synthetic property it represents. No geocoding was attempted. The source data has no verified property coordinates or mapped room layouts. An accurate geographic map would need verified location data. A floor-plan view would also need plans and issue-to-room locations.

For a live property view, introduce a property register with a stable ID, verified display address, original address aliases and a reviewed mapping from each case. Preserve unresolved address conflicts. Keep administratively closed cases, recorded operational actions and verified repairs distinct. Do not count a parent report and its split child issues as separate copies of the same defect.

## Files

- `index.html`: browsable overview with a demo street map. No runtime model calls or geocoding.
- `property-inventory.json`: property metadata, reported issues, recorded outcomes, caveats and evidence references.
- `property-issues.csv`: one row per recorded issue or work item.
- `validation.json`: source, coverage and quotation checks.
- `map-locations.json`: explicit demo coordinates and provenance, separate from source-case facts.
- `map-view.js` and `map-view.css`: street-map display and marker controls.
- `template.html`, `overview.js` and `overview.css`: the shared property panel, view switch, filters, keyboard navigation and responsive layout.
- `review-guidance.json`: reviewed issue states, question categories and proposed next checks. These are historical interpretations for this read-only view, not published operational policies.
- `vendor/leaflet/`: Leaflet 1.9.4, licence and source hashes.
- `interaction-checks-2026-10-10.json`: 17 focused browser checks recorded for the revised interface. The 390-pixel mobile check is not a full accessibility audit.
- `updated-map.jpg`, `updated-list.jpg` and `updated-mobile.jpg`: captures of the revised interface.
- `property-overview.gif`: a 30-second looping walkthrough using captured overview screens, with captions explaining the navigation and evidence states.
- `walkthrough/`: editable animation source, captured screens, a capture manifest, render instructions and validation results.

This output is separate from the running Property Desk application. It creates no cases, changes no policies and sends no communications.

## Map behaviour and external services

Clicking a numbered pin or list entry selects that case in one shared panel. Compact map popups identify the property and demo-location limitation. Search, case-type and evidence-gap filters update both map and list. Map filters fit the visible results; “Fit results” can restore that framing after panning. Switching back from List refreshes and fits the map. Previous/next buttons provide an alternative to finding individual pins.

Evidence-gap categories are reviewed labels tied to the existing caveats: scope, missing documents, chronology, identity, permission, communication and other questions. Dropdown counts refer to the entire 25-case sample; the result count reflects all active filters. These are neither urgency rankings nor automated escalation decisions. All pins use one neutral colour, with the selected pin outlined. Recorded completion is not used as a property-health rating.

Issue states distinguish a reported completion, a plan, a report, an unconfirmed result or a disputed account. Every state includes a supporting source and an explanation. The proposed next question does not send a message or start work. Questions can be edited in `review-guidance.json`; `python3 docs/property-overview/assemble.py` checks labels, tags, quotations and source hashes before rebuilding the embedded inventory. Do not use this retrospective guidance as decision-time replay input.

Leaflet 1.9.4 is stored locally. The street background loads visible tiles from OpenStreetMap over HTTPS and needs internet access. Browser requests contain tile coordinates, not case descriptions or property addresses. No geocoder is called. Normal browser caching and referrer behaviour are preserved; there is no tile prefetch, bulk download or offline-map feature. The tile URL can be changed in `map-locations.json`. If map assets or tiles fail, the property list and recorded evidence remain available.

References: [Leaflet releases](https://leafletjs.com/download.html) and [OpenStreetMap tile policy](https://operations.osmfoundation.org/policies/tiles/). Visible map attribution links to OpenStreetMap copyright information.
