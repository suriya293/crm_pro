import json

log_path = r"C:\Users\YUVEHA\\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

targets = [27, 158, 315]

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx in targets:
            print(f"=== LogLine {line_idx} ===")
            data = json.loads(line)
            # check content
            content = data.get('content', '')
            if content:
                print("Content preview:")
                # print first 500 chars
                print(content[:500])
            # check tool outputs
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                args = tc.get('args', {})
                print(f"Tool: {tc.get('name')}, Args keys: {list(args.keys())}")
                for k, v in args.items():
                    if "initClock" in str(v):
                        # print first 300 chars of value
                        print(f"  Arg {k}: {str(v)[:300]}")
