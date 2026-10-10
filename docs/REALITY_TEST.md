# Reality Test preparation and execution

This runner prepares the submitted Property Desk system for newly released cases.
It is **not an official results set**, and the included example is wholly fictional.
No reserved evaluation cases are included, read or loaded automatically.

## What it actually runs

`python -m app.reality_test` starts each case in a separate Python process with its
own SQLite database and native local Vercel Workflow directory. It uses the same
FastAPI intake/evidence endpoints, application service, Claude triage and native
Vercel Workflow coordinator as the product. The in-process HTTP client runs the
real application lifespan; it does not need a running web server.

There is no manual execution fallback. Contractor contact, messages, bookings and
other operational adapters remain **simulated**, as in the submitted prototype.
A policy assessment, native workflow start, simulated receipt, human wait and
confirmed physical repair are distinct outcomes. A model failure is recorded as
a failure, never replaced with an invented decision.

Each report is processed before the next evidence item becomes visible. The runner
waits for the current application revision and all committed events to reach a
native checkpoint, with no pending triage/message work and a persisted native wait
or terminal run. Separate issues created by the agent are included and checked too.
It stops at a stable decision or information/human wait; it does not invent a human
approval, advance a timer or claim a repair is finished.

## Install and validate without calling any API

From the repository root, use Python 3.12 and the locked dependencies described in
the main README (`uv sync --frozen`). Then:

```sh
PROPERTY_LOCAL_ENV=off uv run --frozen python -m app.reality_test \
  --manifest examples/reality-test/manifest.json \
  --config config/reality-test.example.json \
  --validate-only
```

This reads and validates the manifest, input schema, paths and configuration. It
checks credential **presence**, never values, and reports the source commit and
hashes and installed package versions. It creates no result directory, starts no
Workflow and calls no model. Missing required packages are reported explicitly.
Without explicitly exported Anthropic credentials it correctly reports
`ready_to_attempt: false` and returns exit code 1. `.env.local` is deliberately not
loaded by the runner. This is validation, not evidence of a successful model run.

## Input contract and the organiser release

The organiser's release format is not known to this implementation. The runner
accepts this versioned JSON contract; a mechanical adapter is required if their
release differs. Validate that adapter before the freeze where possible. Do not
edit agent code, prompts, policy or answers after the freeze to fit the test cases.

A manifest must have:

```json
{
  "schema_version": 1,
  "dataset_kind": "organiser_release",
  "cases": [
    {"id": "release-001", "input_file": "release-001.json"}
  ]
}
```

The manifest lists every released case. Case IDs must be unique even ignoring
letter case, start with a letter or digit, and contain only letters, digits,
hyphens or underscores (maximum 80 characters). Input files must be relative paths
inside the manifest directory. Path traversal and symlinks escaping that directory
are rejected. A malformed case is preserved as a failed output while other valid
cases continue; malformed or duplicate manifest IDs are rejected before execution.

Each case file follows the fictional example at
[`examples/reality-test/fictional-tap.json`](../examples/reality-test/fictional-tap.json):

| Field | Meaning |
|---|---|
| `schema_version` | Exactly `1`. |
| `title` | A neutral case title, 3–160 characters. |
| `property_ref` | The supplied property reference; an unverified identifier does not establish identity or permission. |
| `as_of` | The decision cutoff, with an explicit timezone. |
| `report_available_at` | When the initial report was available, at or before the cutoff. |
| `report` | Exact input report text, 3–30,000 characters. |
| `evidence` | Zero or more `{source_label, text, available_at}` records in availability order; each at or before the cutoff. |

Supply only information available at that decision point. Preserve originals and
record any text extraction/conversion separately. Do not include expected answers,
future messages, retrospective outcome summaries, synthetic permission claims or
manual triage labels. Unknown schema fields are rejected. The timestamp validator
cannot discover a hidden retrospective answer embedded in otherwise valid text;
input preparation still needs a chronological check against the release format.

`DEMO-FLAT-1` is rejected because the demonstration directory would otherwise inject
preverified fictional identity and contact permissions. The runner submits all
sources as untrusted assertions, with no human responses. It does not ingest binary
PDFs, images or audio; a reviewed, provenance-preserving text adapter is required.

Only the `development_fixture` manifest kind is used for the shipped example.
Official mode rejects a development manifest. Relabelling a fictional example does
not make it an official case.

## Configuration and freeze

Copy [`config/reality-test.example.json`](../config/reality-test.example.json) to a
local run configuration under `var/` before editing it. This keeps run-specific
settings separate from committed source files.

| Setting | Default / rule |
|---|---|
| `mode` | `preparation`; all outputs prominently say they are not official results. |
| `expected_commit` | Required 40-character frozen Git commit in `official` mode. |
| `model` | `claude-opus-5`, matching the current product default; verify account availability before the freeze. |
| `triage_effort`, `draft_effort` | `medium` / `low`, explicitly applied to the worker environment. |
| `model_timeout_seconds` | 30 seconds per SDK request; the product SDK may retry twice. |
| `case_timeout_seconds` | 150 seconds total per isolated case, including startup and all evidence. |
| `batch_timeout_seconds` | 1,500 seconds for the batch, leaving headroom within a 30-minute test window. |
| `workers` | Four independent workers; reduce if API rate limits require it. |
| `poll_seconds` | 0.25 seconds between state checks. |
| `require_model_credentials` | `true`; cannot be disabled in official mode. Missing credentials produce explicit failed outputs. |
| `policy_settings`, `policy_rules` | Empty means the committed application defaults. Any supplied policy is validated, previewed and published in the empty isolated store before intake. |

Before the freeze, settle the model and policy configuration, test the adapters,
commit the implementation and record the exact frozen commit and configuration
hash. Official mode checks that the running commit matches `expected_commit` and
that application/configuration sources, dependency declarations, `uv.lock` and
`requirements.lock`
are clean. It records their SHA-256 hashes and checks again after the batch. Never
edit these sources during execution. Policy content and policy version are also
recorded per case. The runner records configuration bytes and their hash; operators
must preserve their pre-freeze approved configuration rather than tune it on the
released cases.

No credentials go in JSON or Git. Export the authorised `ANTHROPIC_API_KEY` or
`ANTHROPIC_AUTH_TOKEN` in your own terminal. An exported credential is used only by
the existing Anthropic integration. Never paste it into an answer or log.

## Run a preparation batch

With authorised model credentials available, this calls the real configured model
on the fictional example and may incur API charges:

```sh
PROPERTY_LOCAL_ENV=off uv run --frozen python -m app.reality_test \
  --manifest examples/reality-test/manifest.json \
  --config config/reality-test.example.json \
  --output var/reality-preparation-001
```

The output directory must not exist. Each repeat needs a new run directory; failed
attempts are retained. For credential-free runner tests, use the test command below,
which injects a deterministic model double only inside a test process. No fake-model
option is available in the production CLI.

## Execute the released cases

Prepare `var/reality-official.json` with `mode: "official"`, the frozen
`expected_commit`, and the approved settings. Validate the release manifest first:

```sh
PROPERTY_LOCAL_ENV=off uv run --frozen python -m app.reality_test \
  --manifest /absolute/path/to/released-inputs/manifest.json \
  --config var/reality-official.json \
  --validate-only
```

Then run once into a new directory:

```sh
PROPERTY_LOCAL_ENV=off uv run --frozen python -m app.reality_test \
  --manifest /absolute/path/to/released-inputs/manifest.json \
  --config var/reality-official.json \
  --output var/reality-official-001
```

The runner enforces hard subprocess timeouts. Cases starting after the batch budget
are marked `not_run_batch_deadline`; timed-out processes are stopped and retain
their last committed evidence. Four workers and a 25-minute budget are bounds, not
a guarantee of throughput. Long histories, API retries and rate limits can exhaust
the budget. No case is silently skipped and a waiting human is not auto-approved.

Exit code 0 means every case settled without a recorded model failure and the
source hashes were unchanged. It **does not mean the answers were correct**.
Exit code 1 means a partial/failed batch or a validation-only run not ready to
attempt. Exit code 2 means an invalid invocation or failed batch preflight.

## Files to review and submit

```text
var/reality-official-001/
  provenance.json             # running commit, source/config/manifest hashes
  manifest.json
  config.json                 # credential-free run configuration
  summary.json                # every case, including failed/not-run cases
  ANSWERS/
    release-001/
      ANSWER.md               # actual state, next step, actions, waits/failures
      REASONING.md            # recorded policy reasons and concise model rationale
      input.json              # exact submitted input bytes
      provenance.json        # per-case input hash and batch provenance
      evidence.json           # application timeline and native execution records
      checkpoint-000.json     # snapshot after the report
      checkpoint-001.json     # snapshot after the next source, if any
      result.json
      runtime-status.json
      worker.log
  runtime/                    # isolated SQLite/native SDK state; keep local
```

For the submission, copy this run's `ANSWERS/` to the repository root and include
its `summary.json`, `provenance.json`, manifest and credential-free configuration
in a clearly named evidence directory. Review logs/source inputs for accidental
personal data or credentials before publishing, while preserving an unmodified
local original and documenting any necessary redaction. Do not publish `runtime/`
automatically. Do not silently drop failed cases or manually improve their answers.
Commit results separately from the frozen implementation and record both hashes.
This runner does not submit the form, publish results or alter repository access.

`REASONING.md` quotes the system's recorded policy reasons and concise route
rationale. It does not request or expose hidden chain-of-thought. `evidence.json`
preserves the corresponding source IDs, claim IDs, decisions, reviews and real
native Workflow records so the summary can be checked.

## Verification and limitations

```sh
PROPERTY_LOCAL_ENV=off uv run --frozen python -m pytest tests/test_reality_test.py -q
```

The tests use wholly fictional inputs. The native smoke exercises the actual
application endpoints and native SDK with a controlled, offline AI double. It
tests execution, chronological input isolation, output provenance and failure
handling. It does not measure Claude accuracy or prove hosted/cloud execution.

The runner uses real wall-clock time for workflow deadlines. Source timestamps
establish input ordering/cutoffs; they do not rewind the application's clock or
simulate days of waiting. Initial report receipt time in the application is the
run time, while the original availability timestamp remains in `input.json`.
The model's existing bounded context and source truncation behaviour is unchanged.
Identity, contact routes and authority that cannot be verified by this product stay
blocked; this runner does not manufacture the external directory/policy integrations
that a deployed property manager would need.
