import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "initClock" in line:
            print(f"LogLine {line_idx} has initClock")
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if content and "function initClock" in content:
                    print("Found function definition in step content!")
                    with open("scratch/clock_def.txt", "w", encoding="utf-8") as out:
                        out.write(content)
            except Exception as e:
                pass
print("Search finished.")
