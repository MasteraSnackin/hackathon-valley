# Storage and local deployment

These views describe source at [2732af6](https://github.com/MasteraSnackin/hackathon-valley/tree/2732af60a920d0f9a88be18a36e078aa22fbfa6d). They use the existing Property Desk palette and Diagram Design's document-wide layout. The HTML is the editable source; its first inline SVG produces the GitHub image. Fonts use the local Inter/system sans-serif stack with no external font request.

## Data storage

![Three physical SQL tables and an application-level case reference](data-storage.svg)

[HTML](data-storage.html) · [SVG](data-storage.svg) · [PNG](data-storage.png) · [Mermaid](data-storage.mmd)

The diagram shows every physical table and column declared in [store.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/store.py#L10-L14). SQLAlchemy `String` becomes VARCHAR, while the `payload` and `value` fields hold JSON serialised into Text. `records.case_id` is nullable and indexed. Its dashed association is service-checked and is not a SQL foreign key. Global records, such as published policies, can have no case ID.

The `cases` and `meta` tables are mutable projections and coordination. Database triggers reject updates and deletes to `records`. This does not establish administrator tamper resistance. The `meta.active_policy` pointer and `cases.payload.parent_case_id` are references inside JSON; they are not drawn as database constraints. Logical record kinds such as claims, decisions, reviews, messages and receipts share `records` rather than separate SQL tables.

## Local deployment

![Browser and one local Python process with two stores and an external Anthropic API](local-deployment.svg)

[HTML](local-deployment.html) · [SVG](local-deployment.svg) · [PNG](local-deployment.png) · [Mermaid](local-deployment.mmd)

The view shows the supported local placement, not a live runtime inspection. Worker threads belong to the one application process. The application uses a SQLite file and the SDK owns a separate local World directory. Both must be retained for recovery. The embedded delivery queue is in memory and timers need the process to run. Anthropic calls leave the machine; simulated contractor, booking and payment actions do not.

The hosted path is deliberately described in prose rather than drawn as an existing deployment. [vercel.json](../../../vercel.json) selects FastAPI, and [pyproject.toml](../../../pyproject.toml) registers `app.workflows:wf`. `native_cloud` uses Vercel World and requires shared PostgreSQL and configured staff API identities. Tenant routes are disabled outside demo mode. Vercel operation, PostgreSQL behaviour and production identity are not verified by these diagrams.

Sources: [runtime](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/workflows.py#L215-L360), [startup and staff identity](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/main.py#L49-L114), [Claude adapter](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/ai.py#L121-L262).

## Validation

Both HTML files pass Diagram Design's self-check. Chromium rendered the SVGs with no text outside the canvas or page-width overflow at the checked desktop size. The resulting images were visually inspected. The HTML and SVG sources contain accessible titles and descriptions, use no external assets and have no scripts. See [render-check.json](render-check.json) for hashes and measurements. The check covers diagram output, not application or cloud execution.
