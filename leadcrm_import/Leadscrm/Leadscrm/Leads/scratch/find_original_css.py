import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "KANBAN LAYOUT - Visible Scrollbars" in line:
            # Let's decode the json to get the exact clean text
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if content:
                    print(f"LogLine {line_idx} has content length {len(content)}")
                    # Write to a txt file to inspect
                    with open(f"scratch/css_dump_{line_idx}.txt", "w", encoding="utf-8") as out:
                        out.write(content)
                    print(f"Saved to scratch/css_dump_{line_idx}.txt")
            except Exception as e:
                print("Error loading line:", e)
