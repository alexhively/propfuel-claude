#!/usr/bin/env bash
# Render every built HyperFrames project under <adDir>/src/ to a platform-ready mp4, with a time cap.
#
#   scripts/render.sh "<adDir>" [capSecondsPerRender=600]
#
# For each <adDir>/src/<cut>-<fmt>/: hyperframes check -> hyperframes render (delivery, 30fps)
# -> ffmpeg normalize (H.264 High, yuv420p, 30fps CFR, +faststart, silent AAC 48k stereo)
# -> <adDir>/<slug>_<cut>_<fmt>.mp4
set -euo pipefail
AD="${1:?usage: render.sh <adDir> [capSeconds]}"
CAP="${2:-600}"
HF="npx --yes hyperframes@0.8.150"
SLUG="$(basename "$AD")"

# Budget gate: frames to capture. Over 3,000 total frames, stop and ask before rendering.
total=0
for p in "$AD"/src/*/; do
  d=$(grep -o 'data-composition-id="main"[^>]*data-duration="[0-9.]*"' "$p/index.html" | grep -o 'data-duration="[0-9.]*"' | grep -o '[0-9.]*')
  total=$(python3 -c "print(int($total + float($d) * 30))")
done
echo "budget: $total frames across $(ls -d "$AD"/src/*/ | wc -l | tr -d ' ') project(s), cap ${CAP}s per render"
if [ "$total" -gt 3000 ] && [ "${MOTION_AD_BUDGET_OK:-}" != "1" ]; then
  echo "over the 3,000-frame budget: confirm with the requester, then rerun with MOTION_AD_BUDGET_OK=1"; exit 3
fi

for p in "$AD"/src/*/; do
  name=$(basename "$p")
  echo "== $name"
  (cd "$p" && $HF check) || { echo "check failed for $name: fix before rendering"; exit 4; }
  raw="$AD/.renders/$name.mp4"; mkdir -p "$AD/.renders"
  start=$(date +%s)
  (cd "$p" && $HF render --quality delivery --fps 30 --output "$raw" --quiet) &
  pid=$!
  while kill -0 $pid 2>/dev/null; do
    if [ $(( $(date +%s) - start )) -gt "$CAP" ]; then
      pkill -P $pid 2>/dev/null || true; kill $pid 2>/dev/null || true
      echo "render of $name passed the ${CAP}s cap: killed. Simplify the scene or raise the cap with the requester."; exit 5
    fi
    sleep 2
  done
  wait $pid
  echo "rendered $name in $(( $(date +%s) - start ))s"
  out="$AD/${SLUG}_${name/-/_}.mp4"
  ffmpeg -y -loglevel error -i "$raw" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
    -map 0:v:0 -map 1:a:0 -shortest \
    -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p -r 30 -crf 17 -maxrate 12M -bufsize 24M -g 60 \
    -c:a aac -b:a 128k -movflags +faststart "$out"
  echo "wrote $out"
done
