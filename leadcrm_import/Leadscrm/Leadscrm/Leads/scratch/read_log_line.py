import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx == 474:
            data = json.loads(line)
            content = data.get('content', '')
            print("Content:")
            # print first 2000 chars of content
            print(content[:2000])
            with open("scratch/log_line_474.txt", "w", encoding="utf-8") as out:
                out.write(content)
            break
