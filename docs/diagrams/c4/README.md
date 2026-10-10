# Property Desk C4 views

These four views describe the source at [commit 2732af6](https://github.com/MasteraSnackin/hackathon-valley/tree/2732af60a920d0f9a88be18a36e078aa22fbfa6d). They use the C4 progression of [system context, containers, components and code](https://c4model.com/diagrams). The final view follows the [code-level guidance](https://c4model.com/diagrams/code) by expanding a selected decision component into its actual functions and calls.

Property Desk is still being built. The local application has a native Python Workflow coordinator and simulated operational actions. These source maps do not establish hosted Vercel operation, PostgreSQL readiness, model accuracy or real contractor delivery.

| Level | Question | Interactive map | Static preview | Editable source |
| --- | --- | --- | --- | --- |
| C1: context | Who uses Property Desk, and what external system does it call? | [Open](c1-context.html) | [PNG](c1-context.png) | [Archify JSON](c1-context.architecture.json) · [Mermaid](c1-context.mmd) |
| C2: containers | Where do the application and its two stores sit? | [Open](c2-containers.html) | [PNG](c2-containers.png) | [Archify JSON](c2-containers.architecture.json) · [Mermaid](c2-containers.mmd) |
| C3: components | Which Python modules own the work? | [Open](c3-components.html) | [PNG](c3-components.png) | [Archify JSON](c3-components.architecture.json) · [Mermaid](c3-components.mmd) |
| C4: code | Which functions decide whether an action can run? | [Open](c4-code.html) | [PNG](c4-code.png) | [Archify JSON](c4-code.architecture.json) · [Mermaid](c4-code.mmd) |

## Reading the views

C1 groups the application as one system. Tenants report problems and follow up. Staff review evidence, make scoped decisions and publish policies. The external Anthropic API supports tenant intake, reads stored case text and drafts questions. Tenant intake falls back to bounded local parsing if Claude is unavailable; case triage failures require a person. Native Workflow belongs inside Property Desk at this level.

C2 uses logical C4 containers, not Docker containers. The browser client calls the Python application over same-origin HTTP. FastAPI, `Service` and the embedded Workflow queue share one process in the local configuration. SQLAlchemy manages application records in SQLite. Native Workflow keeps its execution history in a separate local World directory. Both stores must survive a local restart. Cloud paths are documented separately because configuration alone does not establish a working deployment.

C3 expands the Python application. It combines `main.py` and `tenant.py` as HTTP routers to keep the view readable. The coordinator has three durable steps: `run_case_cycle`, `triage_case_messages` and `compose_tenant_messages`. Each enters the case service. Before case submission, the tenant router calls Claude for intake and asks the tenant to confirm a summary. The case service owns persistence, calls Claude for case triage and question drafts, and calls the pure policy evaluator for action permission. The policy assistant reads current policy and resolved-review context; saving, previewing and publishing use separate service operations.

C4 is a selected Python call graph. Arrows indicate calls, not an execution sequence. `Service.execute_tx` checks the business-action ID, calls `Service.assess`, and writes a simulated receipt only if the result is `ACT`. `Service.assess` calls `domain.evaluate` with the current case, claims, approvals and policy. The evaluator filters claim scope, validates approval evidence and checks the message-reading state. It returns every blocker alongside the highest-priority outcome. Utility calls such as `scope_of`, `digest` and date parsing are omitted; this is not a complete dependency graph.

The Archify viewer uses its built-in visual roles. The policy evaluator's security colour denotes permission checks; it does not assert a separate network security boundary. The HTML files retain Archify's checked theme and export controls. The PNGs are static captures of the delivered viewer, including its explanatory cards. The Mermaid files retain the same nodes and directed relationships for GitHub editing; their layout is independent of the Archify preview.

## Source evidence

Every map pins the same full commit and carries component-level file and line references. Validation checked those paths and ranges against committed Git blobs with the local repository root. Tracked application code matched that commit during this review. This verifies source identity and link ranges, not production behaviour or public repository access.

| Responsibility | Source |
| --- | --- |
| HTTP routes and runtime startup | [main.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/main.py#L21-L70) |
| Tenant ownership and case bridge | [tenant.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/tenant.py#L189-L224) |
| Three native Workflow steps | [workflows.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/workflows.py#L80-L182) |
| Assessment and action receipt | [service.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/service.py#L540-L558) |
| Pure evaluator and helpers | [domain.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/domain.py#L208-L328) |
| Application store | [store.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/store.py#L10-L75) |
| Claude structured requests | [ai.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/ai.py#L121-L262) |
| Plain-English policy proposals | [policy_assistant.py](https://github.com/MasteraSnackin/hackathon-valley/blob/2732af60a920d0f9a88be18a36e078aa22fbfa6d/app/policy_assistant.py#L277-L397) |

## Checks and editing

All four maps passed nine Archify showcase checks with zero composition errors and zero warnings. Automated browser checks passed at 1440×900, 1600×1000, 1920×1080 and 2048×1320. The delivered screenshots were inspected in both light and dark themes for readable labels, routes, boundaries and fit. Search, focus, source-link navigation and export buttons were not manually exercised in this task.

Each published map includes a `.delivery.json` receipt with source and HTML hashes and a validation summary. The individual validation, browser and handoff records remain local; the published [review summary](../review-summary.json) records their reported outcomes. Receipt paths are normalised to repository-relative paths for publication; the source and HTML hashes are unchanged. These records describe the Archify HTML; they do not validate Mermaid rendering or application execution.

Edit the `.architecture.json` file, validate it with Archify using `--quality showcase --repo-root <repository>`, then deliver it again. Run `visual-check` against that delivered HTML and inspect both themes. Update the corresponding Mermaid source and preview after changing a map. Keep source references pinned to a verified commit.
