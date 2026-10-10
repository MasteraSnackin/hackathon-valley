# Demo delivery

The finished [Property Desk demo](property-desk-demo.mp4) is **54 seconds**, with generic synthetic British English narration, selectable English captions and six chapters. It is a real recording of the local product. The final file is 5,631,105 bytes, using H.264 at 1280×900, 30fps, with AAC audio.

The request moves through two separate review decisions to a simulated quote-request receipt. Resolving the first check leaves the other blocked. The policy suggestion shown remains unsaved and unpublished, and the repair remains unconfirmed. The [runtime audit](workflow-evidence.json) independently records that sequence.

The recording used application commit `23cec527a5f3848786b85c965b653982f15a9c57`, native_local Vercel Workflow and the local literal interpreter. It does not demonstrate a cloud deployment, live Claude interpretation, contractor contact or a completed physical repair.

## Checks completed

- HyperFrames checks passed with no errors or warnings; all six scene midpoints were inspected.
- The first, middle and last frames of each selected clip and each final scene were inspected. The parent also inspected the final contact sheet and native-size poster.
- Full video and audio decoding passed, independently checked twice.
- Selectable captions were extracted from the final MP4; text and timestamps exactly matched the supplied SRT.
- Duration, 1,620 video frames, codecs, resolution and all six chapter boundaries were verified.
- Final audio measured −16.08 LUFS integrated and −2.01 dBTP. This is a numeric check, not a listening assessment.
- A fresh `npm ci` and check of the packaged editable project passed. Its dependency lockfile is included.

No continuous watch-through or listening review is claimed. [The delivery report](delivery-report.json) binds these checks to the final movie checksum. The raw capture is retained locally; the six selected source clips, narration, fonts, licences and edit map are in the [editable project](project/). Source audio preparation records in `production/` are distinct from the final-film checks here.

[Rebuild instructions](EDITING.md) include the exact render and finishing commands. The original browser recording runs at 25fps; the finished video uses the supported 30fps HyperFrames output cadence, with normal-speed timing. The 100px editorial rail below the untouched 1280×800 UI is added by the edit.

SHA-256: `dc4bb0e905fe0c253d32d665bcd8513e31b6c8d6058baf506e72ca4ad621a80a`
