import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if "wizard" in line:
            try:
                data = json.loads(line)
                content = data.get('content', '')
                tool_calls = data.get('tool_calls', [])
                # print summary of where it is
                print(f"LogLine {line_idx}, Step {data.get('step_index')}: type={data.get('type')}, content len={len(content)}, tool_calls len={len(tool_calls)}")
                # check if there's any file writing or replacement in tool calls
                for tc in tool_calls:
                    args = tc.get('args', {})
                    if 'wizard' in str(args):
                        print(f"  Tool {tc.get('name')} args have wizard")
            except:
                pass
