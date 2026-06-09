import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx < 100:
            if "code.html" in line and "<header" in line:
                try:
                    data = json.loads(line)
                    content = data.get('content', '')
                    if content:
                        print(f"LogLine {line_idx} contains header:")
                        # print lines containing <header
                        lines = content.splitlines()
                        for idx, l in enumerate(lines):
                            if "<header" in l or "clock" in l or "clock-container" in l or "schedule" in l:
                                print(f"  {idx+1}: {l}")
                except Exception as e:
                    pass
print("Finished.")
