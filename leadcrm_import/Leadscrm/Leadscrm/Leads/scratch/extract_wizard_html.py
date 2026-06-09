import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "wizard-step-1" in line or "wizard-step" in line or "lead-modal" in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                if content and "Showing lines" in content and "code.html" in content:
                    # Let's see the line numbers range
                    print(f"LogLine {line_idx} has wizard HTML:")
                    lines = content.splitlines()
                    for idx, l in enumerate(lines):
                        if "wizard-step" in l or "lead-modal" in l or "wizard-" in l:
                            print(f"  Line {idx+1}: {l}")
            except:
                pass
