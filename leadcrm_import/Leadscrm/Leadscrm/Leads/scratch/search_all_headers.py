import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

terms = ["clock-container", "clock", "notifications", "Admin", "fullscreen"]

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx < 150:
            for term in terms:
                if term in line:
                    try:
                        data = json.loads(line)
                        content = data.get('content', '')
                        if content and "code.html" in content:
                            print(f"LogLine {line_idx} contains term '{term}':")
                            # print the lines in content that contain the term
                            for idx, l in enumerate(content.splitlines()):
                                if term in l:
                                    print(f"  {idx+1}: {l}")
                    except Exception as e:
                        pass
print("Finished.")
