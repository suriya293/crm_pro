import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx == 484:
            data = json.loads(line)
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                args = tc.get('args', {})
                for k, v in args.items():
                    if "initClock" in str(v):
                        print(f"Key: {k}")
                        print(str(v)[:1500])
                        with open("scratch/clock_js_484.txt", "w", encoding="utf-8") as out:
                            out.write(str(v))
                        print("Saved to scratch/clock_js_484.txt")
            break
