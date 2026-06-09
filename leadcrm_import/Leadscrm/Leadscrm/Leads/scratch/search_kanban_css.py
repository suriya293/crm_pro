import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

found_blocks = []

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "Showing lines" in line and "code.html" in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if not content:
                    continue
                # Search for css selectors
                if "kanban" in content or "column" in content or "card" in content:
                    # Let's search if any lines show the style tag or css selectors
                    lines = content.splitlines()
                    for idx, l in enumerate(lines):
                        if "#kanban-inner-row" in l or ".kanban-column" in l or ".kanban-card" in l or ".kanban-subheader" in l or "kanban-placeholder-card" in l:
                            print(f"Log {line_idx}, Line {idx+1}: {l}")
            except:
                pass
