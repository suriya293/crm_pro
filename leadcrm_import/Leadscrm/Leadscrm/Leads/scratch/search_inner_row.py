import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "kanban-inner-row" in line or "#kanban-inner-row" in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if content:
                    lines = content.splitlines()
                    for idx, l in enumerate(lines):
                        if "kanban-inner-row" in l or "#kanban-inner-row" in l:
                            print(f"LogLine {line_idx}, Line {idx+1}: {l}")
            except:
                pass
