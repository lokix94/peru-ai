---
name: agent-backup
description: Backup agent workspace files to a GitHub repository. Use when the user or agent wants to back up identity files, memory, skills, or any workspace content to Git. Handles init, commit, push, restore, and scheduled backups. Works with GitHub Personal Access Tokens.
---

# Agent Backup

Automate workspace backups to a GitHub repository.

## Quick Start

Run the backup script to push all critical files:

```bash
bash scripts/backup.sh
```

## Setup (First Time)

1. Ensure Git credentials exist at `~/.git-credentials` with a GitHub PAT
2. Set environment variables or edit `scripts/backup.sh`:
   - `REPO_URL` — GitHub repo URL (e.g., `https://github.com/user/repo.git`)
   - `BACKUP_DIR` — Local staging directory (default: `/tmp/agent-backup`)
   - `WORKSPACE` — Workspace root (default: `~/.openclaw/workspace`)

3. Run: `bash scripts/backup.sh --init` to initialize

## Commands

| Command | Description |
|---------|-------------|
| `bash scripts/backup.sh` | Full backup (commit + push) |
| `bash scripts/backup.sh --init` | First-time setup |
| `bash scripts/backup.sh --status` | Show backup status |
| `bash scripts/backup.sh --diff` | Show changes since last backup |
| `bash scripts/backup.sh --restore` | Restore from remote |

## What Gets Backed Up

By default, the script backs up:
- `*.md` files in workspace root (SOUL, IDENTITY, MEMORY, AGENTS, etc.)
- `memory/` directory (daily logs, notes)
- `skills/` directory (custom skills)
- Any additional paths listed in `scripts/backup-include.txt`

To exclude files, add patterns to `scripts/backup-exclude.txt`.

## Scheduling Backups

Use OpenClaw cron to schedule automatic backups:

```
Schedule a cron job to run `bash ~/.openclaw/workspace/skills/agent-backup/scripts/backup.sh`
every 6 hours with payload kind "agentTurn".
```

## Security Notes

- Never commit credentials, API keys, or `.env` files
- The script auto-generates a `.gitignore` with common secret patterns
- Review `scripts/backup-exclude.txt` before first push
