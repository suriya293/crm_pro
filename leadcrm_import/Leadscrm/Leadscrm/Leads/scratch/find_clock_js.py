import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "initClock" in line:
            # Let's inspect all fields of the JSON line for "function initClock" or "initClock("
            if "function initClock" in line or "initClock = " in line or "initClock()" in line:
                try:
                    data = json.loads(line)
                    # Let's search inside tools outputs
                    for tc in data.get('tool_calls', []):
                        content = str(tc)
                        if "function initClock" in content:
                            print(f"LogLine {line_idx} has function in tool_calls")
                    content = data.get('content', '')
                    if "function initClock" in content:
                        # Find the function block using regex
                        match = re.search(r'function initClock\(.*?\)\s*\{.*?\}', content, re.DOTALL)
                        if match:
                            print(f"LogLine {line_idx} has function definition:")
                            print(match.group(0))
                except Exception as e:
                    pass
