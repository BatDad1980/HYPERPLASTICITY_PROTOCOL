"""Inspect datasets."""
import json
import os

for fname in os.listdir('datasets/hf_local'):
    path = os.path.join('datasets/hf_local', fname)
    lines = open(path, 'r', encoding='utf-8').readlines()
    sample = json.loads(lines[0])
    print(f"{fname}: {len(lines)} samples | Keys: {list(sample.keys())}")
    text = str(sample.get('text', sample.get('response', '')))[:200]
    print(f"  Preview: {text}\n")
