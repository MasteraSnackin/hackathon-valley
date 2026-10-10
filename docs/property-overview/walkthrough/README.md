# Property overview walkthrough source

A 30-second, silent GIF made from real screenshots of the standalone property overview on 10 October 2026. The six chapters cover the map, Garden filter, case 019, item states, quotations and List view. The thin bar shows the current chapter's playback progress.

The source screenshots are unchanged. Two chapters crop the property panel for readability. These are historical synthetic BUILD records; all map positions are invented. The animation does not show live maintenance actions.

From this directory, with Node.js and FFmpeg installed:

```sh
./render.sh
```

This checks the composition and replaces `../property-overview.gif`. The project pins HyperFrames 0.8.145. Its compiler resolves the animation library and render fonts, so the first run may need network access.

To edit the captions or timing:

```sh
npx --yes hyperframes@0.8.145 preview --background
```

Open the Studio URL printed by that command. The source for each chapter is in `compositions/`; its duration is also set in `index.html`. `capture-manifest.json` records the screenshots and crops. If the interface changes, recapture the relevant screens before updating the walkthrough.

Map imagery in the screenshots is © OpenStreetMap contributors, shown through Leaflet. Its on-screen attribution is retained in the map chapters.
