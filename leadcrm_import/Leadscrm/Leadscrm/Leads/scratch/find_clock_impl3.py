import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx == 532:
            data = json.loads(line)
            # check content
            content = data.get('content', '')
            if content:
                print("LogLine 532 Content:")
                print(content[:2500])
            # check tool outputs
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                args = tc.get('args', {})
                for k, v in args.items():
                    if "initClock" in str(v):
                        print(f"Arg {k}:")
                        print(str(v)[:1500])
            break
