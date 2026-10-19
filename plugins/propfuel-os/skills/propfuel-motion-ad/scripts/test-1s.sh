#!/usr/bin/env bash
# 1-second test of the hardest beat, before building the whole ad. Required whenever a beat uses an effect
# (stack, sketch, brush, filter, orb, words) or anything new.
#
#   scripts/test-1s.sh <spec.json> <cut>:<sceneIndex>[@secondsIntoBeat] [outDir]
#
# Builds a 1080x1080, 30 fps, 1-second project holding only that beat (no captions), playing the second that
# starts <secondsIntoBeat> after the beat starts (default 0.3), runs `hyperframes check`, renders it, and writes
#   <outDir>/test_<cut>_s<i>.mp4          the playable preview (30 frames)
#   <outDir>/test_<cut>_s<i>_keys.jpg     timestamp-labelled keyframes at 0 / 0.25 / 0.5 / 0.75 / 0.97 s
#   <outDir>/test_<cut>_s<i>_frames.jpg   all 30 frames, left to right, top to bottom
# Then show the requester the mp4 + sheets and wait for a yes on texture and motion before expanding the effect.
set -euo pipefail
SPEC="${1:?usage: test-1s.sh <spec.json> <cut>:<sceneIndex>[@sec] [outDir]}"
WHICH="${2:?usage: test-1s.sh <spec.json> <cut>:<sceneIndex>[@sec] [outDir]}"
SLUG=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['slug'])" "$SPEC")
OUT="${3:-$HOME/Desktop/PropFuel/03 Video/PropFuel Motion Ads/_fx-tests/$SLUG}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
HF="npx --yes hyperframes@0.8.150"
CUT="${WHICH%%:*}"; REST="${WHICH#*:}"; I="${REST%%@*}"
NAME="test-${CUT}-s${I}-1x1"; BASE="test_${CUT}_s${I}"
mkdir -p "$OUT"
node "$HERE/engine/build.mjs" "$SPEC" "$OUT" --test "$WHICH" --formats 1x1
P="$OUT/src/$NAME"
(cd "$P" && $HF check) || { echo "check failed for $NAME: fix before rendering"; exit 4; }
start=$(date +%s)
(cd "$P" && $HF render --quality delivery --fps 30 --output "$OUT/$BASE.mp4" --quiet)
echo "rendered $NAME in $(( $(date +%s) - start ))s"
(cd "$P" && rm -rf snapshots && $HF snapshot --at 0,0.25,0.5,0.75,0.97 --no-end --describe false >/dev/null)
cp "$P/snapshots/contact-sheet.jpg" "$OUT/${BASE}_keys.jpg"
ffmpeg -y -loglevel error -i "$OUT/$BASE.mp4" -vf "scale=216:-1,tile=6x5:padding=4:color=0x222222" -frames:v 1 "$OUT/${BASE}_frames.jpg"
echo "1s test: $OUT/$BASE.mp4  sheets: ${BASE}_keys.jpg, ${BASE}_frames.jpg. Look, then wait for feedback."
