import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx == 39:
            data = json.loads(line)
            content = data.get('content', '')
            print("LogLine 39 Content preview:")
            print(content[:1500])
            with open("scratch/log_line_39.txt", "w", encoding="utf-8") as out:
                out.write(content)
            break
