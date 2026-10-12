#!/usr/bin/env bash
# Frame QA for every exported mp4 in <adDir>: spec probe + contact sheet + poster frame + safe-zone overlay.
#
#   scripts/qa.sh "<adDir>"
#
# Writes <adDir>/qa/<file>_contact.jpg (one frame per second, in order),
# <adDir>/qa/<file>_poster.jpg (frame 0: the thumbnail), <adDir>/qa/<file>_safezone.jpg (the same sheet with
# the safe box drawn), and <adDir>/qa/specs.txt. Then LOOK at every sheet; the script does not judge.
set -euo pipefail
AD="${1:?usage: qa.sh <adDir>}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$AD/qa"
: > "$AD/qa/specs.txt"
for f in "$AD"/*.mp4; do
  b=$(basename "$f" .mp4)
  fmt=$(echo "$b" | grep -oE '(9x16|4x5|1x1|16x9)$')
  read -r W H DUR FPS VC PIX AC < <(ffprobe -v error -show_entries stream=width,height,codec_name,pix_fmt,r_frame_rate:format=duration -of json "$f" |
    python3 -c 'import json,sys;d=json.load(sys.stdin);v=[s for s in d["streams"] if "width" in s][0];a=[s for s in d["streams"] if "width" not in s];print(v["width"],v["height"],round(float(d["format"]["duration"]),2),v["r_frame_rate"],v["codec_name"],v["pix_fmt"],a[0]["codec_name"] if a else "none")')
  size=$(du -h "$f" | cut -f1)
  echo "$b: ${W}x${H} ${DUR}s ${FPS}fps ${VC} ${PIX} audio=${AC} ${size}" | tee -a "$AD/qa/specs.txt"
  # contact sheet: 1 fps (tile k = second k-1), 5 columns, read left to right. (No drawtext: Homebrew ffmpeg lacks freetype.)
  cols=5; n=$(python3 -c "import math;print(math.ceil($DUR))"); rows=$(( (n + cols - 1) / cols ))
  ffmpeg -y -loglevel error -i "$f" -vf "fps=1,scale=360:-1,tile=${cols}x${rows}:padding=6:color=0x222222" -frames:v 1 "$AD/qa/${b}_contact.jpg"
  ffmpeg -y -loglevel error -i "$f" -vf "select=eq(n\,0)" -frames:v 1 "$AD/qa/${b}_poster.jpg"
  # safe-zone sheet: the same 1 fps frames with the format's safe box drawn in red; no word, number or logo may cross it
  read -r T B L R < <(python3 -c "import json;s=json.load(open('$HERE/engine/formats.json'))['$fmt']['safe'];print(s['top'],s['bottom'],s['left'],s['right'])")
  ffmpeg -y -loglevel error -i "$f" -vf "fps=1,drawbox=x=$L:y=$T:w=iw-$L-$R:h=ih-$T-$B:color=red@0.9:t=6,scale=360:-1,tile=${cols}x${rows}:padding=6:color=0x222222" -frames:v 1 "$AD/qa/${b}_safezone.jpg"
done
echo "QA sheets in $AD/qa/ : open each contact sheet and run the checklist in SKILL.md 'Frame QA'."
