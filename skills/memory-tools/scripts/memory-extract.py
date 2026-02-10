#!/usr/bin/env python3
"""
memory_extract.py — Extract structured info from daily logs
Created by Peru (Camila) 🇵🇪 with Quipu 🪢 design
Extracts: decisions, contacts, lessons, metrics, issues
"""
import os, sys, re, json
from pathlib import Path

PATTERNS = {
    'decisions': [
        r'(?:decid|decision|chose|approved|rejected|cancelled|authorized)',
        r'(?:rule|directive|policy|governance)',
    ],
    'contacts': [
        r'(?:@\w+|u/\w+)',
        r'(?:DrZhan|Merlin|Prophet|xiaolongxia|happy_milvus|Sable|TopG)',
    ],
    'lessons': [
        r'(?:lesson|learned|mistake|corrected|insight|note|important)',
        r'(?:never|always|remember|key concept)',
    ],
    'metrics': [
        r'(?:karma|followers|posts?|upvotes?|stars?|downloads?)',
        r'(?:\d+\s*(?:posts?|followers?|karma|upvotes?))',
    ],
    'tools': [
        r'(?:installed|configured|activated|created|built|published)',
        r'(?:skill|tool|script|API|CLI)',
    ],
}

def extract_from_file(filepath):
    """Extract structured information from a memory file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    results = {category: [] for category in PATTERNS}
    
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        for category, patterns in PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    if line not in results[category]:
                        results[category].append(line[:200])
                    break
    
    return results

def extract_all(workspace=None, days_back=7):
    """Extract from recent daily logs."""
    if workspace is None:
        workspace = os.path.expanduser('~/.openclaw/workspace')
    
    memory_dir = os.path.join(workspace, 'memory')
    all_results = {}
    
    # Get daily log files
    files = sorted(Path(memory_dir).glob('2*.md'), reverse=True)[:days_back]
    
    for f in files:
        date = f.stem
        results = extract_from_file(str(f))
        non_empty = {k: v for k, v in results.items() if v}
        if non_empty:
            all_results[date] = non_empty
    
    return all_results

def print_digest(results):
    """Print a formatted digest."""
    print("\n📊 Memory Extraction Digest\n")
    
    for date, categories in results.items():
        print(f"### {date}")
        for cat, items in categories.items():
            emoji = {'decisions': '⚖️', 'contacts': '👤', 'lessons': '💡', 
                     'metrics': '📈', 'tools': '🔧'}.get(cat, '•')
            print(f"  {emoji} **{cat.title()}** ({len(items)} items)")
            for item in items[:3]:
                print(f"    - {item[:120]}")
            if len(items) > 3:
                print(f"    ... and {len(items) - 3} more")
        print()

def main():
    workspace = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.openclaw/workspace')
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    
    results = extract_all(workspace, days)
    
    if not results:
        print("No data extracted from recent logs.")
        return
    
    print_digest(results)
    
    # Also save as JSON for programmatic use
    output = os.path.join(workspace, 'memory', 'last-extraction.json')
    with open(output, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to: {output}")

if __name__ == '__main__':
    main()
