---
name: memory-tools
description: Memory management utilities for AI agents. Index, search, deduplicate, and curate memory files. Use when managing agent memory, finding past decisions, cleaning up duplicates, generating memory summaries, or extracting key information from daily logs. Works with file-based memory systems (MEMORY.md + daily logs).
---

# Memory Tools

Utilities for managing and improving agent memory. Pure file-based, no external dependencies.

## Scripts

### 1. Memory Index — `scripts/memory-index.sh`
Generates a searchable index of all memory files with key topics, dates, and line counts.

```bash
bash scripts/memory-index.sh [workspace_path]
```
Output: `memory/INDEX.md` — a table of contents for all memory files.

### 2. Memory Health — `scripts/memory-health.sh`  
Analyzes MEMORY.md for potential issues: duplicates, outdated info, oversized sections.

```bash
bash scripts/memory-health.sh [memory_file]
```
Output: Report of issues found with line numbers and suggestions.

### 3. Daily Digest — `scripts/daily-digest.sh`
Extracts key decisions, contacts, and lessons from daily log files.

```bash
bash scripts/daily-digest.sh [memory_dir] [days_back]
```
Output: Condensed digest of recent activity.
