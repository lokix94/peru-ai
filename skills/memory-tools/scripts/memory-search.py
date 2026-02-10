#!/usr/bin/env python3
"""
memory_search.py — TF-IDF-lite search across agent memory files
Created by Peru (Camila) 🇵🇪 with Quipu 🪢 design
No external dependencies — Python stdlib only.
"""
import os, sys, re, json, math
from collections import Counter
from pathlib import Path

def tokenize(text):
    """Simple word tokenizer."""
    return re.findall(r'[a-záéíóúñü]+', text.lower())

def compute_tf(tokens):
    """Term frequency: count / total."""
    total = len(tokens) if tokens else 1
    counts = Counter(tokens)
    return {t: c / total for t, c in counts.items()}

def build_index(workspace):
    """Index all memory files."""
    memory_dir = os.path.join(workspace, 'memory')
    docs = {}
    
    # Index MEMORY.md
    main = os.path.join(workspace, 'MEMORY.md')
    if os.path.exists(main):
        with open(main, 'r') as f:
            docs['MEMORY.md'] = f.read()
    
    # Index memory/*.md
    if os.path.isdir(memory_dir):
        for fname in sorted(os.listdir(memory_dir)):
            if fname.endswith('.md') and fname != 'INDEX.md':
                fpath = os.path.join(memory_dir, fname)
                with open(fpath, 'r') as f:
                    docs[f'memory/{fname}'] = f.read()
    
    return docs

def search(query, workspace=None, top_k=5):
    """Search memory files using TF-IDF-lite ranking."""
    if workspace is None:
        workspace = os.path.expanduser('~/.openclaw/workspace')
    
    docs = build_index(workspace)
    if not docs:
        print("No memory files found.")
        return []
    
    query_tokens = tokenize(query)
    if not query_tokens:
        print("Empty query.")
        return []
    
    # Compute IDF
    N = len(docs)
    df = Counter()
    doc_tokens = {}
    for name, content in docs.items():
        tokens = tokenize(content)
        doc_tokens[name] = tokens
        unique = set(tokens)
        for t in unique:
            df[t] += 1
    
    idf = {t: math.log(N / (1 + df[t])) + 1 for t in df}
    
    # Score each document
    results = []
    for name, tokens in doc_tokens.items():
        tf = compute_tf(tokens)
        score = 0.0
        matched_terms = []
        for qt in query_tokens:
            if qt in tf:
                score += tf[qt] * idf.get(qt, 1.0)
                matched_terms.append(qt)
        
        # Recency boost for daily logs (newer = higher)
        if re.match(r'memory/\d{4}-\d{2}-\d{2}\.md', name):
            date_str = name.split('/')[-1].replace('.md', '')
            try:
                from datetime import datetime
                days_ago = (datetime.now() - datetime.strptime(date_str, '%Y-%m-%d')).days
                recency_boost = max(0.1, 1.0 - (days_ago * 0.05))
                score *= recency_boost
            except:
                pass
        
        # MEMORY.md gets a small curation boost
        if name == 'MEMORY.md':
            score *= 1.2
        
        if score > 0:
            # Find matching context lines
            content = docs[name]
            context_lines = []
            for line in content.split('\n'):
                line_lower = line.lower()
                if any(qt in line_lower for qt in query_tokens):
                    stripped = line.strip()
                    if stripped and len(stripped) > 10:
                        context_lines.append(stripped[:150])
            
            results.append({
                'file': name,
                'score': round(score, 4),
                'matched': matched_terms,
                'context': context_lines[:3]
            })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

def main():
    if len(sys.argv) < 2:
        print("Usage: memory_search.py <query> [workspace] [top_k]")
        print("Example: memory_search.py 'moltbook karma strategy'")
        sys.exit(1)
    
    query = sys.argv[1]
    workspace = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/.openclaw/workspace')
    top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    results = search(query, workspace, top_k)
    
    if not results:
        print(f"No results for: {query}")
        return
    
    print(f"\n🔍 Search: \"{query}\" ({len(results)} results)\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['score']:.3f}] {r['file']}")
        print(f"   Matched: {', '.join(r['matched'])}")
        for ctx in r['context']:
            print(f"   > {ctx}")
        print()

if __name__ == '__main__':
    main()
