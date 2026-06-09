import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx == 21:
            data = json.loads(line)
            print("Keys:", data.keys())
            # Save step output or content
            with open("scratch/inspect_log_21.txt", "w", encoding="utf-8") as out:
                out.write(json.dumps(data, indent=2))
            break
