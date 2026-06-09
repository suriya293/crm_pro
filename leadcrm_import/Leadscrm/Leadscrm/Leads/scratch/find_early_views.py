import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        try:
            data = json.loads(line)
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                if tc.get('name') == 'view_file' and 'code.html' in tc.get('args', {}).get('AbsolutePath', ''):
                    print(f"LogLine {line_idx}, Step {data.get('step_index')}: args={tc.get('args')}")
        except:
            pass
