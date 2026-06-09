import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

found_lines = []

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "code.html" in line or "Showing lines" in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if not content:
                    continue
                # Search for comments like <!-- \d+. or material symbols
                lines = content.splitlines()
                for idx, l in enumerate(lines):
                    if "<!--" in l or "material-symbols-outlined" in l or "kanban-column" in l:
                        found_lines.append((line_idx, idx+1, l))
            except:
                pass

# Filter and display occurrences of column definitions
for log_idx, line_num, text in found_lines:
    if any(f"<!-- {i}." in text for i in range(1, 14)):
        print(f"Log {log_idx}, Line {line_num}: {text}")
    elif "kanban-column" in text:
        print(f"Log {log_idx}, Line {line_num}: {text}")
