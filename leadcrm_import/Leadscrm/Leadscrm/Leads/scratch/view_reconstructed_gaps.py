import re

with open('scratch/code_html_reconstructed_full.html', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

gaps = []
start = None

for idx, line in enumerate(lines):
    line_num = idx + 1
    # Check if the line is empty or just whitespace
    if not line.strip():
        if start is None:
            start = line_num
    else:
        if start is not None:
            gaps.append((start, line_num - 1))
            start = None

if start is not None:
    gaps.append((start, len(lines)))

print(f"Total lines: {len(lines)}")
print("Missing line ranges (1-indexed):")
for s, e in gaps:
    print(f"  {s} to {e} ({e - s + 1} lines)")
