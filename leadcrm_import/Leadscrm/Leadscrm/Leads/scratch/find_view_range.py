import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "code.html" in line and "Showing lines" in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if "Showing lines" in content:
                    # check if the range overlaps 800-1130
                    print(f"LogLine {line_idx}: {content[:150]}")
            except Exception as e:
                pass
