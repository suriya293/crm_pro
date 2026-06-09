import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "wizard-" in line or "wizard_step" in line or "wizard-step" in line:
            if "div" in line or "button" in line or "input" in line:
                try:
                    data = json.loads(line)
                    content = data.get('content', '')
                    if content and len(content) > 1000:
                        print(f"LogLine {line_idx} has wizard HTML, length {len(content)}")
                        with open(f"scratch/wizard_html_{line_idx}.txt", "w", encoding="utf-8") as out:
                            out.write(content)
                        print(f"Saved scratch/wizard_html_{line_idx}.txt")
                except Exception as e:
                    pass

print("Finished.")
