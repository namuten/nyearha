#!/bin/bash
# Blue/source/gen.py -> MusicXML -> MuseScore 4 -> out/ (mscz, pdf, png 150dpi, mpos, mp3 192k)
# 사용: bash Blue/source/build.sh   (MuseScore 4, ffmpeg 필요)
set -euo pipefail
S="$(cd "$(dirname "$0")" && pwd)"
MS="${MSCORE:-/Applications/MuseScore 4.app/Contents/MacOS/mscore}"
OUT="$S/out"
rm -rf "$OUT"; mkdir -p "$OUT"
python3 -I "$S/gen.py" "$OUT" >/dev/null
for x in "$OUT"/*.musicxml; do
  n=$(basename "$x" .musicxml)
  "$MS" -o "$OUT/$n.mscz" "$x" >/dev/null 2>&1
  "$MS" -o "$OUT/$n.pdf" "$OUT/$n.mscz" >/dev/null 2>&1
  "$MS" -r 150 -o "$OUT/$n.png" "$OUT/$n.mscz" >/dev/null 2>&1
  "$MS" -o "$OUT/$n.mpos" "$OUT/$n.mscz" >/dev/null 2>&1
  "$MS" -o "$OUT/$n.wav" "$OUT/$n.mscz" >/dev/null 2>&1
  ffmpeg -hide_banner -loglevel error -y -i "$OUT/$n.wav" -codec:a libmp3lame -b:a 192k "$OUT/$n.mp3"
  rm "$OUT/$n.wav"
  echo "built $n"
done
