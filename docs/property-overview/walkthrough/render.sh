#!/bin/sh
set -eu
cd "$(dirname "$0")"
npx --yes hyperframes@0.8.145 check --at 0,2,3.95,4,6,7.95,8,10,12.95,13,16,18.95,19,22,25.95,26,28,29.95 --strict
npx --yes hyperframes@0.8.145 render --format gif --gif-loop 0 --fps 12 --quality delivery --output ../property-overview.gif
