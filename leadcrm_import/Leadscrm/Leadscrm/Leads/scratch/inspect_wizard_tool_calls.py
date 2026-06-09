import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

targets = [510, 630, 744, 748]

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx in targets:
            print(f"=== LogLine {line_idx} ===")
            data = json.loads(line)
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                print(f"Tool: {tc.get('name')}")
                args = tc.get('args', {})
                # Save code/text content if it exists
                for k, v in args.items():
                    if isinstance(v, str) and len(v) > 200:
                        filename = f"scratch/recovered_wizard_{line_idx}_{k}.txt"
                        with open(filename, "w", encoding="utf-8") as out:
                            out.write(v)
                        print(f"  Saved argument {k} to {filename} (length={len(v)})")
                    else:
                        print(f"  Arg {k}: {v}")
