import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "function initClock" in line or "initClock = function" in line:
            # Let's load json and print any matched js function in 'content' or other fields
            try:
                data = json.loads(line)
                for k, v in data.items():
                    if isinstance(v, str) and "function initClock" in v:
                        print(f"Log {line_idx}, field {k}:")
                        # Extract the function
                        match = re.search(r'function initClock\(.*?\)\s*\{.*?\}', v, re.DOTALL)
                        if match:
                            print(match.group(0))
                        else:
                            # Print around it
                            idx = v.find("function initClock")
                            print(v[idx:idx+500])
            except Exception as e:
                pass
