#!/usr/bin/env bash
# Pre-render keyframe contact sheet: required before the final render (step 7). Fast: no video is encoded.
#
#   scripts/keyframes.sh "<adDir>"
#
# For each built project in <adDir>/src/<cut>-<fmt>/ it snapshots the start (0s), every beat and caption change
# (just before and just after each boundary), the middle of each beat and the final hold, and writes
# <adDir>/qa/keyframes/<cut>-<fmt>_keyframes_<n>.jpg (12 frames per sheet) with every frame labelled by its timestamp.
# LOOK at each sheet for cropped text, overlaps and anything that vanishes mid-transition, then STOP: show the
# sheets and wait for the requester's feedback before running render.sh.
set -euo pipefail
AD="${1:?usage: keyframes.sh <adDir>}"
HF="npx --yes hyperframes@0.8.150"
mkdir -p "$AD/qa/keyframes"
for p in "$AD"/src/*/; do
  name=$(basename "$p")
  case "$name" in test-*) continue ;; esac
  at=$(python3 - "$p/index.html" <<'PY'
import re, sys
h = open(sys.argv[1]).read()
dur = float(re.search(r'data-composition-id="main"[^>]*data-duration="([\d.]+)"', h).group(1))
ts = {0.0, round(dur - 0.1, 2)}
for s, d in re.findall(r'class="clip[^"]*"[^>]*data-start="([\d.]+)" data-duration="([\d.]+)"', h):
    s, d = float(s), float(d)
    for t in (s - 0.15, s + 0.15, s + d / 2, s + d - 0.15):
        if 0 <= t < dur: ts.add(round(t, 2))
keep = []
for t in sorted(ts):
    if not keep or t - keep[-1] >= 0.1: keep.append(t)
print(",".join(str(t) for t in keep))
PY
)
  echo "== $name @ $at"
  (cd "$p" && rm -rf snapshots && $HF snapshot --at "$at" --no-end --describe false >/dev/null)
  # snapshot writes contact-sheet.jpg, or contact-sheet-1..n.jpg past 12 frames
  k=0; for sheet in "$p"/snapshots/contact-sheet*.jpg; do k=$((k + 1)); cp "$sheet" "$AD/qa/keyframes/${name}_keyframes_${k}.jpg"; done
done
echo "Keyframe sheets in $AD/qa/keyframes/ : check them, then show the requester and WAIT for feedback before render.sh."
