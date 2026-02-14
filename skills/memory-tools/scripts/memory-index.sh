#!/usr/bin/env bash
# memory-index: Generate searchable index of all memory files
# Created by Peru (Camila) 🇵🇪
set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
OUTPUT="$MEMORY_DIR/INDEX.md"

log() { echo "[index] $*"; }

if [ ! -d "$MEMORY_DIR" ]; then
  echo "Error: Memory directory not found: $MEMORY_DIR"
  exit 1
fi

log "Indexing memory files in $MEMORY_DIR..."

cat > "$OUTPUT" <<'HEADER'
# 📇 Memory Index
*Auto-generated — do not edit manually*

HEADER

# Index MEMORY.md
MAIN="$WORKSPACE/MEMORY.md"
if [ -f "$MAIN" ]; then
  LINES=$(wc -l < "$MAIN")
  SECTIONS=$(grep -c '^## ' "$MAIN" 2>/dev/null || echo 0)
  SIZE=$(ls -lh "$MAIN" | awk '{print $5}')
  echo "## MEMORY.md (Main)" >> "$OUTPUT"
  echo "- **Lines:** $LINES | **Sections:** $SECTIONS | **Size:** $SIZE" >> "$OUTPUT"
  echo "- **Topics:**" >> "$OUTPUT"
  grep '^## ' "$MAIN" | sed 's/^## /  - /' >> "$OUTPUT"
  echo "" >> "$OUTPUT"
fi

# Index daily logs
echo "## Daily Logs" >> "$OUTPUT"
echo "" >> "$OUTPUT"
echo "| Date | Lines | Size | Key Topics |" >> "$OUTPUT"
echo "|------|-------|------|------------|" >> "$OUTPUT"

for f in "$MEMORY_DIR"/2*.md; do
  [ -f "$f" ] || continue
  FNAME=$(basename "$f")
  DATE="${FNAME%.md}"
  LINES=$(wc -l < "$f")
  SIZE=$(ls -lh "$f" | awk '{print $5}')
  # Extract ## headers as topics
  TOPICS=$(grep "^## " "$f" 2>/dev/null | sed "s/^## //" | paste -sd", " -)
  [ -z "$TOPICS" ] && TOPICS="(no sections)"
  echo "| $DATE | $LINES | $SIZE | $TOPICS |" >> "$OUTPUT"
done

echo "" >> "$OUTPUT"

# Index other memory files
echo "## Reference Files" >> "$OUTPUT"
echo "" >> "$OUTPUT"

for f in "$MEMORY_DIR"/*.md; do
  [ -f "$f" ] || continue
  FNAME=$(basename "$f")
  # Skip daily logs and INDEX itself
  [[ "$FNAME" == 2*.md ]] && continue
  [[ "$FNAME" == "INDEX.md" ]] && continue
  
  LINES=$(wc -l < "$f")
  SIZE=$(ls -lh "$f" | awk '{print $5}')
  FIRST_LINE=$(head -1 "$f" | sed 's/^# //')
  echo "- **$FNAME** ($LINES lines, $SIZE): $FIRST_LINE" >> "$OUTPUT"
done

# Stats summary
echo "" >> "$OUTPUT"
TOTAL_FILES=$(find "$MEMORY_DIR" -name "*.md" -not -name "INDEX.md" | wc -l)
TOTAL_LINES=$(cat "$MEMORY_DIR"/*.md 2>/dev/null | wc -l)
echo "---" >> "$OUTPUT"
echo "*Total: $TOTAL_FILES files, $TOTAL_LINES lines | Generated: $(date -u '+%Y-%m-%d %H:%M UTC')*" >> "$OUTPUT"

log "✅ Index generated: $OUTPUT ($TOTAL_FILES files, $TOTAL_LINES lines)"
