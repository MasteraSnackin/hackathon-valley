# BUILD replay boundary

The development partition contains exactly the 25 IDs fixed in `app/build_data.py` and `handoff/BUILD_MANIFEST.json`. The read-only manifest records source revision `9bcdca585955dfb930005ed742572606e68f5688` and SHA-256 hashes for 58 supplied files. The source loader rejects IDs outside that partition, traversal paths, altered histories, invalid event counts and mismatched hashes.

Each imported snapshot consists only of selected chronological history events `001..N`. It excludes the file's total-event header, index page, later events, later description amendments and all attachment bytes. Catalogue titles and whole-case complexity labels are presentation metadata, not decision input. An amendment within the selected history prefix is visible as a dated historical event; the loader does not replace earlier sources with the latest description.

## BUILD 008 exclusion

The supplied `data/build/008/attachments/attachment-02-estimate.pdf` is available and was inspected read-only through text extraction of its complete one-page content. Alongside the estimate dated 3 April 2025, its observation section refers to what a later case overview records about whether a tap needed replacement. That observation is retrospective and must not appear in a decision snapshot at the estimate's issue time.

The implemented choice is **exclude the complete attachment from all replay inputs**. The original PDF is preserved; no edited derivative is used. All other attachment bytes are also excluded by this first prototype. A history message may mention an attachment, but that mention supplies no claim that the contents were seen, read, verified or complete. Missing usable material remains an evidence requirement where the proposed action needs it.

This conservative exclusion limits replay coverage. The app accepts pasted evidence text with exact quoted claims and source labels, but it does not yet supply historical availability-aware binary attachment extraction or object storage. A later implementation must establish when each document version became available and separate contemporaneous document material from retrospective observations before using it in replay.

## Interpretation and scoring

Replay sends each selected chronological prefix (never attachments, later events or index summaries) to Claude through the Anthropic API, using a clean isolated database. Claude triages it and may draft tenant questions, which stay in the simulated thread; no external communication is sent and no adapter executes. Generated source assertions stay distinct from verified facts. The replay report shows outcomes and blockers; it does not treat eventual historical closure as an acceptable-outcome label or an accuracy score.

All 50 original cases informed an earlier generic audit before this split. The other partition is reserved from this implementation onward, rather than previously unseen. The source loader and replay command address only the BUILD partition. A later evaluator should freeze code/policy/labels and test the reserved partition separately.

## Shared runtime exposure during UI verification

The existing default `var/property.db` had records labelled as reserved evaluation data, introduced outside this implementation subtask. The dashboard automatically selected one of those records during the first browser check and displayed its stored history. The verification server was stopped immediately after that was recognised. No source folder from the reserved partition was opened, and no implementation or test decision was based on that displayed history. The existing database was preserved without cleanup.

Subsequent browser verification used a fresh separate application database and native workflow directory containing fictional demonstration material only. Automated tests use isolated temporary storage, and CLI replay uses its own temporary BUILD-only database. The shared default database and the accidentally displayed case cannot be described as an untouched evaluation environment. This exposure must remain disclosed in any later evaluation report.
