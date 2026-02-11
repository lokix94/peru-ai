#!/usr/bin/env python3
"""
memory_audit.py — Detect duplicates, stale data, and inconsistencies in memory
Created by Peru (Camila) 🇵🇪 with Quipu 🪢 design
"""
import os, sys, re
from collections import defaultdict
from pathlib import Path

def find_numbers(text):
    """Extract numbers with context for comparison."""
    patterns = [
        (r'(\d+)\s*(?:posts?|publicaciones)', 'posts'),
        (r'(\d+)\s*(?:karma)', 'karma'),
        (r'(\d+)\s*(?:followers?|seguidores)', 'followers'),
        (r'(\d+)\s*(?:following|siguiendo)', 'following'),
        (r'(\d+)\s*(?:upvotes?)', 'upvotes'),
        (r'(\d+)\s*(?:comments?)', 'comments'),
        (r'(\d+)\s*(?:files?|archivos)', 'files'),
    ]
    findings = {}
    for pattern, label in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            findings[label] = [int(m) for m in matches]
    return findings

def find_duplicates(lines):
    """Find lines that appear multiple times."""
    seen = defaultdict(list)
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped and len(stripped) > 20 and not stripped.startswith('#'):
            key = stripped.lower()
            seen[key].append(i)
    return {k: v for k, v in seen.items() if len(v) > 1}

def check_stale_metrics(workspace):
    """Compare metrics between MEMORY.md and latest daily log."""
    issues = []
    
    main_file = os.path.join(workspace, 'MEMORY.md')
    if not os.path.exists(main_file):
        return issues
    
    with open(main_file, 'r') as f:
        main_content = f.read()
    main_numbers = find_numbers(main_content)
    
    # Find latest daily log
    memory_dir = os.path.join(workspace, 'memory')
    daily_logs = sorted(Path(memory_dir).glob('2*.md'), reverse=True)
    if not daily_logs:
        return issues
    
    with open(str(daily_logs[0]), 'r') as f:
        latest_content = f.read()
    latest_numbers = find_numbers(latest_content)
    latest_date = daily_logs[0].stem
    
    for metric, main_vals in main_numbers.items():
        if metric in latest_numbers:
            latest_val = max(latest_numbers[metric])
            main_val = max(main_vals)
            if main_val != latest_val:
                issues.append({
                    'type': 'stale_metric',
                    'metric': metric,
                    'memory_md_value': main_val,
                    'latest_log_value': latest_val,
                    'latest_log': latest_date,
                    'severity': 'warning' if abs(main_val - latest_val) > 2 else 'info'
                })
    
    return issues

def check_duplicate_lines(workspace):
    """Check MEMORY.md for duplicate lines."""
    main_file = os.path.join(workspace, 'MEMORY.md')
    if not os.path.exists(main_file):
        return []
    
    with open(main_file, 'r') as f:
        lines = f.readlines()
    
    dupes = find_duplicates(lines)
    issues = []
    for text, line_nums in dupes.items():
        issues.append({
            'type': 'duplicate',
            'text': text[:100],
            'lines': line_nums,
            'severity': 'warning'
        })
    return issues

def check_missing_sections(workspace):
    """Check if daily logs have content not reflected in MEMORY.md."""
    issues = []
    main_file = os.path.join(workspace, 'MEMORY.md')
    if not os.path.exists(main_file):
        return issues
    
    with open(main_file, 'r') as f:
        main_lower = f.read().lower()
    
    memory_dir = os.path.join(workspace, 'memory')
    daily_logs = sorted(Path(memory_dir).glob('2*.md'), reverse=True)[:3]
    
    important_markers = ['lesson', 'decision', 'directive', 'rule', 'important', 'never', 'always']
    
    for log_file in daily_logs:
        with open(str(log_file), 'r') as f:
            for i, line in enumerate(f, 1):
                stripped = line.strip().lower()
                if any(m in stripped for m in important_markers):
                    # Check if key content is in MEMORY.md
                    words = re.findall(r'\w{5,}', stripped)
                    key_words = [w for w in words if w not in ('important', 'lesson', 'decision', 'always', 'never')]
                    if key_words and not any(w in main_lower for w in key_words[:3]):
                        issues.append({
                            'type': 'not_in_memory',
                            'source': f'{log_file.name}:{i}',
                            'text': line.strip()[:120],
                            'severity': 'info'
                        })
    
    return issues

def audit(workspace=None):
    """Run full memory audit."""
    if workspace is None:
        workspace = os.path.expanduser('~/.openclaw/workspace')
    
    print("\n🔍 Memory Audit Report\n")
    all_issues = []
    
    # Check stale metrics
    stale = check_stale_metrics(workspace)
    all_issues.extend(stale)
    
    # Check duplicates
    dupes = check_duplicate_lines(workspace)
    all_issues.extend(dupes)
    
    # Check missing items
    missing = check_missing_sections(workspace)
    all_issues.extend(missing)
    
    if not all_issues:
        print("✅ No issues found. Memory is healthy!")
        return
    
    warnings = [i for i in all_issues if i['severity'] == 'warning']
    infos = [i for i in all_issues if i['severity'] == 'info']
    
    if warnings:
        print(f"⚠️  Warnings ({len(warnings)}):\n")
        for issue in warnings:
            if issue['type'] == 'stale_metric':
                print(f"  📊 Stale metric: {issue['metric']}")
                print(f"     MEMORY.md says: {issue['memory_md_value']}")
                print(f"     {issue['latest_log']} says: {issue['latest_log_value']}")
                print()
            elif issue['type'] == 'duplicate':
                print(f"  📋 Duplicate on lines {issue['lines']}:")
                print(f"     {issue['text']}")
                print()
    
    if infos:
        print(f"ℹ️  Info ({len(infos)}):\n")
        for issue in infos[:5]:
            if issue['type'] == 'not_in_memory':
                print(f"  📝 {issue['source']}: {issue['text']}")
                print()
    
    print(f"---\nTotal: {len(warnings)} warnings, {len(infos)} info items")

if __name__ == '__main__':
    workspace = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.openclaw/workspace')
    audit(workspace)
