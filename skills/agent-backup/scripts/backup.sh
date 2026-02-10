#!/usr/bin/env bash
# agent-backup: Automated workspace backup to GitHub
# Created by Peru (Camila) 🇵🇪 — https://github.com/lokix94/peru-ai
set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
BACKUP_DIR="${BACKUP_DIR:-/tmp/agent-backup}"
REPO_URL="${REPO_URL:-}"
GIT_USER="${GIT_USER:-Agent-Backup}"
GIT_EMAIL="${GIT_EMAIL:-agent@backup.local}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# ─── Helpers ─────────────────────────────────────────────────────
log()  { echo "[backup] $(date '+%H:%M:%S') $*"; }
err()  { echo "[backup] ERROR: $*" >&2; exit 1; }

# ─── Parse credentials from ~/.git-credentials ──────────────────
get_token() {
  if [ -f "$HOME/.git-credentials" ]; then
    head -1 "$HOME/.git-credentials" | sed 's|https://[^:]*:\([^@]*\)@.*|\1|'
  else
    echo ""
  fi
}

get_repo_with_auth() {
  local token
  token=$(get_token)
  if [ -z "$token" ]; then
    echo "$REPO_URL"
  else
    echo "$REPO_URL" | sed "s|https://|https://x:${token}@|"
  fi
}

# ─── Init ────────────────────────────────────────────────────────
do_init() {
  if [ -z "$REPO_URL" ]; then
    err "Set REPO_URL environment variable (e.g., https://github.com/user/repo.git)"
  fi
  log "Initializing backup to $REPO_URL"
  rm -rf "$BACKUP_DIR"
  git clone "$(get_repo_with_auth)" "$BACKUP_DIR" 2>/dev/null || {
    mkdir -p "$BACKUP_DIR"
    cd "$BACKUP_DIR"
    git init
    git remote add origin "$(get_repo_with_auth)"
    git checkout -b main 2>/dev/null || true
  }
  cd "$BACKUP_DIR"
  git config user.name "$GIT_USER"
  git config user.email "$GIT_EMAIL"

  # Create .gitignore
  cat > .gitignore <<'EOF'
# Secrets
*.key
*.pem
*.p12
credentials.json
.env
.env.*
*.secret
*_SECRET*
*_TOKEN*
*_KEY*

# OS
.DS_Store
Thumbs.db

# Temp
*.tmp
*.bak
*.swp
EOF

  log "Initialized. Run 'backup.sh' to perform first backup."
}

# ─── Sync files ──────────────────────────────────────────────────
sync_files() {
  local include_file="$SKILL_DIR/scripts/backup-include.txt"
  local exclude_file="$SKILL_DIR/scripts/backup-exclude.txt"

  # Default files to backup
  log "Syncing workspace files..."

  # Copy markdown files from workspace root
  for f in "$WORKSPACE"/*.md; do
    [ -f "$f" ] && cp "$f" "$BACKUP_DIR/" 2>/dev/null || true
  done

  # Copy memory directory
  if [ -d "$WORKSPACE/memory" ]; then
    mkdir -p "$BACKUP_DIR/memory"
    cp -r "$WORKSPACE/memory/"* "$BACKUP_DIR/memory/" 2>/dev/null || true
  fi

  # Copy skills directory
  if [ -d "$WORKSPACE/skills" ]; then
    mkdir -p "$BACKUP_DIR/skills"
    cp -r "$WORKSPACE/skills/"* "$BACKUP_DIR/skills/" 2>/dev/null || true
  fi

  # Copy additional paths from include file
  if [ -f "$include_file" ]; then
    while IFS= read -r path; do
      [ -z "$path" ] || [[ "$path" == \#* ]] && continue
      local src="$WORKSPACE/$path"
      if [ -e "$src" ]; then
        local dest="$BACKUP_DIR/$path"
        mkdir -p "$(dirname "$dest")"
        cp -r "$src" "$dest"
      fi
    done < "$include_file"
  fi

  # Remove excluded patterns
  if [ -f "$exclude_file" ]; then
    while IFS= read -r pattern; do
      [ -z "$pattern" ] || [[ "$pattern" == \#* ]] && continue
      find "$BACKUP_DIR" -name "$pattern" -not -path '*/.git/*' -delete 2>/dev/null || true
    done < "$exclude_file"
  fi
}

# ─── Backup (commit + push) ─────────────────────────────────────
do_backup() {
  if [ ! -d "$BACKUP_DIR/.git" ]; then
    err "Not initialized. Run: backup.sh --init"
  fi

  sync_files
  cd "$BACKUP_DIR"

  git add -A
  local changes
  changes=$(git diff --cached --stat)

  if [ -z "$changes" ]; then
    log "No changes to backup."
    exit 0
  fi

  local file_count
  file_count=$(git diff --cached --numstat | wc -l)
  local timestamp
  timestamp=$(date '+%Y-%m-%d %H:%M UTC')
  git commit -m "🔄 Backup $timestamp ($file_count files changed)"

  log "Pushing to remote..."
  git push origin main 2>&1 || git push -u origin main 2>&1
  log "✅ Backup complete! $file_count files updated."
}

# ─── Status ──────────────────────────────────────────────────────
do_status() {
  if [ ! -d "$BACKUP_DIR/.git" ]; then
    echo "Status: NOT INITIALIZED"
    echo "Run: backup.sh --init"
    return
  fi
  cd "$BACKUP_DIR"
  local last_commit
  last_commit=$(git log -1 --format='%ci - %s' 2>/dev/null || echo "No commits yet")
  local file_count
  file_count=$(find . -not -path './.git/*' -type f | wc -l)
  echo "Status: ACTIVE"
  echo "Directory: $BACKUP_DIR"
  echo "Files tracked: $file_count"
  echo "Last backup: $last_commit"
  echo "Remote: $(git remote get-url origin 2>/dev/null | sed 's/x:[^@]*@/***@/' || echo 'none')"
}

# ─── Diff ────────────────────────────────────────────────────────
do_diff() {
  if [ ! -d "$BACKUP_DIR/.git" ]; then
    err "Not initialized."
  fi
  sync_files
  cd "$BACKUP_DIR"
  git add -A
  git diff --cached --stat
}

# ─── Restore ─────────────────────────────────────────────────────
do_restore() {
  if [ -z "$REPO_URL" ]; then
    err "Set REPO_URL to restore from."
  fi
  log "⚠️  This will overwrite local workspace files. Press Ctrl+C to cancel..."
  sleep 3
  rm -rf "$BACKUP_DIR"
  git clone "$(get_repo_with_auth)" "$BACKUP_DIR"
  cd "$BACKUP_DIR"

  # Restore markdown files
  for f in *.md; do
    [ -f "$f" ] && cp "$f" "$WORKSPACE/"
  done

  # Restore memory
  [ -d "memory" ] && mkdir -p "$WORKSPACE/memory" && cp -r memory/* "$WORKSPACE/memory/"

  # Restore skills
  [ -d "skills" ] && mkdir -p "$WORKSPACE/skills" && cp -r skills/* "$WORKSPACE/skills/"

  log "✅ Restore complete!"
}

# ─── Main ────────────────────────────────────────────────────────
case "${1:-}" in
  --init)    do_init ;;
  --status)  do_status ;;
  --diff)    do_diff ;;
  --restore) do_restore ;;
  --help|-h)
    echo "Usage: backup.sh [--init|--status|--diff|--restore|--help]"
    echo "  (no args)  Run full backup (commit + push)"
    echo "  --init     First-time setup"
    echo "  --status   Show backup status"
    echo "  --diff     Show pending changes"
    echo "  --restore  Restore from remote"
    ;;
  *)         do_backup ;;
esac
