import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"
out_path = r"c:\Users\YUVEHA\OneDrive\Documents\Leads\scratch\step48.txt"

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('step_index') == 48:
                content = data.get('content', '')
                with open(out_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(content)
        except Exception:
            pass
