# Property Desk diagram style

Project-local style for `system-overview.html` and `decision-flow.html`, extracted on 10 October 2026 from the root `DESIGN.md` colour and typography tokens. The existing Property Desk forest-green and warm-neutral style was explicitly selected for this work. This file does not change the application design brief, the installed Diagram Design skill, a global style guide or a saved client profile.

## Tokens

| Diagram role | Value | Property Desk source or adaptation |
| --- | --- | --- |
| Paper | `#F5F6F2` | Background |
| Surface | `#FFFFFF` | Surface |
| Ink | `#192C30` | Text |
| Muted text and connectors | `#647376` | Secondary |
| Border and divider | `#DCE3DF` | Border |
| Focal stroke | `#215848` | Primary |
| Focal fill | `#E7F0E9` | Success background, reused here only for visual emphasis; shape and words convey decision meaning |
| Input and store fill | `#EDF0EC` | Quiet opaque tint derived for the warm-neutral canvas |
| Reserved API link marker | `#355C85` | Information; defined by the skill's three-marker contract but not used for visible connectors |
| Typeface | `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif` | Property Desk body and heading stack, with Arial as an extra offline fallback |
| Canvas | `1280 × 720` | Diagram Design `doc-wide` preset |
| Visible type | `32px` title; `24px` primary names; `20px` names/subtitle; `16px` details, connectors and captions | Larger than the skill's default document type ramp for legibility |
| Grid | `4px` | Coordinates, spacing and type sizes |
| Node radius | `8px` | Diagram Design maximum normal-node radius; start terminator uses a flowchart oval |
| Connector bend | `8px` | Rounded orthogonal routing |

The sources embed all CSS and SVG. They contain no script, image, font import or other network dependency. Fonts are not embedded: Inter is used when available locally, otherwise the declared system fallback renders. Exact line metrics can differ between operating systems; the browser QA records the environment used for review. The all-sans treatment intentionally follows Property Desk typography instead of the Diagram Design default editorial serif.

Each SVG has a diagram-specific accessible title and description, with `role="img"` and matching `aria-labelledby`. Text labels remain present in the exported SVG. Colour reinforces the focal policy check; it never carries the meaning on its own.

## Authoring and export

HTML is the source of truth. SVG files are extracted from the first inline SVG in their matching HTML source, preserving its complete style, title, description and viewBox. No remote font import is added during export because this delivery explicitly requires self-contained offline rendering. Edit the HTML and re-extract the SVG; do not allow the two representations to drift.

## Content and fidelity

The selected visual types are architecture and flowchart. The semantic-pattern reference was read; none of its named patterns exactly describes this single all-requirements decision cycle, so no paired trace or security-boundary pattern is asserted.

`system-overview` has eight components and eight directed connections. It merges tenant and staff into Browser views, groups explicit policy checks with their Case service, and combines literal/live evidence interpretation in one responsibility. Tenant conversation slot extraction is local; the optional live mode concerns evidence interpretation. The interpreter runs before the case transaction. The diagram deliberately omits API endpoint lists, tenant bridge internals, policy drafting/publication detail, retry/recovery mechanics and individual SQL tables. Browser return projections and the interpreter's return value are implicit, not additional arrows. Simulated adapters write their receipt through the service-owned SQL transaction; their box is a responsibility, not a separate process. Native Workflow history remains a distinct store. The after-commit wake and Workflow-to-service fresh cycle are explicit.

`decision-flow` has six nodes and six transitions. It compresses every action-specific requirement into one all-pass decision and represents the full blocker set as a grouped outcome. Those outcomes are alternatives selected from the current checks, not a forced sequence. Clarification is itself a proposed action with its own requirements; placing the word in the blocked-outcome group does not authorise real communication. A revised proposal returns to the same checks; an uncertain result must first be reconciled and does not allow an unguarded scope replacement. The annotation retains uncertain-result handling without adding a separate recovery subgraph. The full policy order, fact statuses, role map, review expiry, stale-response checks and action-idempotency contract remain in the architecture prose.

Both figures describe the implemented local demonstration and code responsibilities. They do not claim real operational delivery, physical repair completion, hosted Vercel validation or live model quality. They are static documentation figures, separate from the existing interactive Archify map, which remains unchanged.
