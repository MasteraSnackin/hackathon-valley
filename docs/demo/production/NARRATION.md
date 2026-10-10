# Property Desk demo narration

The 54-second plan uses a generic British English synthetic voice generated locally with macOS Daniel. It does not clone a person. There is no music.

The final editor checked the real source capture against the spoken claims. This document records source narration preparation, measured WAV durations and the scene plan. Checks of the finished movie are recorded separately in the [delivery report](../delivery-report.json) and [delivery notes](../DELIVERY.md).

| Time | Spoken text | Evidence to show |
|---|---|---|
| 0–8 s | Property Desk turns a maintenance report into a tracked case. A tenant reports a leaking kitchen tap. | Tenant portal: submit and see the saved maintenance request. |
| 8–19 s | Staff see the request and its blockers. Two checks still need review: the person and property, and a verified contact route. | Staff case: person/property and verified contact route reviews remain open; classification has already passed. |
| 19–25 s | Resolving the first check leaves the second open. | Person/property review resolved; verified contact route remains open. |
| 25–37 s | Once both are resolved, the local Vercel Workflow rechecks the case and records a simulated quote request. The action history shows what happened. | Contact route review resolved, native_local run resumes and simulated action receipt appears in Action history. |
| 37–46 s | Staff can propose a policy change. This suggestion remains unsaved and unpublished. | Actual policy assistant shows a proposed change that remains unsaved and unpublished. |
| 46–54 s | The repair is not yet confirmed. This is a local demo. External actions are simulated. | Result: action recorded, repair not yet confirmed; retain visible simulation label. |

The six generated audio segments total 41.193 seconds. Their programme starts include a 0.25-second lead inside each scene; the remaining time gives the viewer room to read the interface. The SRT uses segment boundaries measured from the source WAVs, without invented word timestamps.

The demo records a simulated quote request. It does not confirm a booking, entry permission, contractor contact or completed repair. The policy suggestion remains unsaved and unpublished.

Files: [narration](narration.txt), [captions](narration.srt), [timing and source map](narration-plan.json), [media provenance](media-provenance.json).

The captured application commit is `23cec527a5f3848786b85c965b653982f15a9c57`, using `literal_demo` interpretation and `native_local` Workflow. Claude was not used in this capture. These source records do not claim a continuous listening review.
