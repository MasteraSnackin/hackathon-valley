# Demo production record

The final video is a recording of the local Property Desk application with a generic synthetic British English narrator. It uses a fictional tenant and address. External actions are simulated; a quote-request receipt does not prove that a contractor was contacted or that a physical repair was completed.

## Edit

The sequence follows one request: tenant intake, two independent checks, the first check resolved while another remains open, the remaining check resolved, a locally executed Vercel Workflow recheck, and a simulated quote-request receipt. It then shows an unsaved, unpublished policy suggestion and returns to the case result.

The application footage retains its 1280×800 viewport. The 1280×900 movie adds a 100px explanatory rail below the recording. The rail is editorial text, not part of the product. There are no reconstructed screens or pitch slides. The pointer overlay follows recorded UI actions. Cuts remove waiting; the source-to-programme map records selected intervals.

The production target is 54 seconds, with narration starting a quarter of a second into each scene. The actual final MP4 duration and checksum are recorded in the delivery report. Captions are selectable and are also supplied separately as an SRT file.

## Rebuild

The editable HyperFrames project is packaged under `project/`. It pins HyperFrames 0.8.145 and contains the selected footage, six scene compositions, narration files, fonts and licences. It does not require the private application database or a running Property Desk server.

From the repository root, run:

```sh
cd docs/demo/project
npm ci
npm run check
npm run render -- --quality delivery --fps 30 --workers 2 --output ../property-desk-demo-render.mp4
cd ..
python3 finish_video.py --render property-desk-demo-render.mp4 --captions property-desk-demo.srt --output property-desk-demo-rebuilt.mp4
```

Node.js, npm, Python 3, FFmpeg and a compatible Chromium installation are required. `npm ci` installs the exact dependency graph recorded in `project/package-lock.json`; the first install needs package-registry access. Keep a different output name for rebuilds to preserve the delivered movie. The finishing script refuses to overwrite an existing output.

The finishing script performs a measured two-pass narration level adjustment, embeds selectable subtitles and adds chapter metadata. Raw recordings are preserved locally and are not needed to reproduce the selected edit. The source hashes identify the recording used to create each extract.

## Verification boundary

Metadata validation, full-stream decoding and sampled rendered frames are technical checks. They do not establish a continuous human watch-through or a listening review. The delivery report states which checks were actually completed and binds them to the final video checksum.

## Captured application version

The footage was recorded from commit `23cec527a5f3848786b85c965b653982f15a9c57`, using native_local Vercel Workflow and the local literal interpreter. It does not demonstrate live Claude interpretation or later application changes. The source media records under `production/` describe narration creation; the final delivery report records the rendered movie and its validation.
