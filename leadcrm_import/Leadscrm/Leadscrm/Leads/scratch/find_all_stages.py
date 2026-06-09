import json
import re

log_path = r"C:\Users\YUVEHA\OneDrive\Documents\Leads\scratch\css_dump_21.txt"

# Let's search inside css_dump_21.txt first as it was a direct dump of code.html from step 21
# Wait, css_dump_21.txt might be truncated, let's also search transcript.jsonl
log_path_2 = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

stages = []

with open(log_path_2, 'r', encoding='utf-8') as f:
    for line in f:
        # Search for pattern <!-- X. YYY --> or stage comments
        matches = re.findall(r'<!--\s*\d+\.\s*([^>]+?)-->', line)
        for m in matches:
            val = m.strip()
            if val not in stages:
                stages.append(val)

print("Found stage comments in logs:")
for s in sorted(stages):
    print("  ", s)
