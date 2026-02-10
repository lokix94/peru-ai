#!/usr/bin/env bash
# edge-tts-voice: Quick speech generation
# Created by Peru (Camila) 🇵🇪
set -euo pipefail

TEXT="${1:?Usage: speak.sh \"text\" [voice] [output_file]}"
VOICE="${2:-en-US-AriaNeural}"
OUTPUT="${3:-/tmp/tts_output.mp3}"

# Check if edge-tts is installed
if ! command -v edge-tts &> /dev/null; then
  echo "[tts] Installing edge-tts..."
  pip3 install edge-tts -q
fi

# Handle long texts by splitting
TEXT_LEN=${#TEXT}
if [ "$TEXT_LEN" -gt 5000 ]; then
  echo "[tts] Long text ($TEXT_LEN chars) — splitting into chunks..."
  TMPDIR=$(mktemp -d)
  CHUNK_SIZE=4000
  CONCAT_LIST=""
  i=0

  while [ "$i" -lt "$TEXT_LEN" ]; do
    CHUNK="${TEXT:$i:$CHUNK_SIZE}"
    CHUNK_FILE="$TMPDIR/chunk_${i}.mp3"
    edge-tts --voice "$VOICE" --text "$CHUNK" --write-media "$CHUNK_FILE" 2>/dev/null
    CONCAT_LIST="$CONCAT_LIST|$CHUNK_FILE"
    i=$((i + CHUNK_SIZE))
  done

  # Remove leading pipe
  CONCAT_LIST="${CONCAT_LIST:1}"

  # Concatenate with ffmpeg if available
  if command -v ffmpeg &> /dev/null; then
    # Build ffmpeg concat
    LIST_FILE="$TMPDIR/list.txt"
    for f in "$TMPDIR"/chunk_*.mp3; do
      echo "file '$f'" >> "$LIST_FILE"
    done
    ffmpeg -f concat -safe 0 -i "$LIST_FILE" -c copy "$OUTPUT" -y 2>/dev/null
  else
    # Fallback: just use the first chunk
    cp "$TMPDIR/chunk_0.mp3" "$OUTPUT"
    echo "[tts] Warning: ffmpeg not found, only first chunk saved"
  fi
  rm -rf "$TMPDIR"
else
  edge-tts --voice "$VOICE" --text "$TEXT" --write-media "$OUTPUT" 2>/dev/null
fi

SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
echo "[tts] ✅ Generated: $OUTPUT ($SIZE) — voice: $VOICE"
