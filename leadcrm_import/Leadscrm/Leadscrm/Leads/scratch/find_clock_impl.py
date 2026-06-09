import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "function initClock" in line:
            print(f"LogLine {line_idx} has function initClock")
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if content:
                    match = re.search(r'function initClock\(.*?\)\s*\{.*?\}', content, re.DOTALL)
                    if match:
                        print("FOUND:")
                        print(match.group(0))
                        break
            except Exception as e:
                pass
