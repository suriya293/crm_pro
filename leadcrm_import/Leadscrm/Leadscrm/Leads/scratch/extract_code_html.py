import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

print("Searching logs for write_to_file or replace_file_content calls for code.html...")

found_calls = []

with open(log_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        try:
            data = json.loads(line)
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                name = tc.get('name')
                args = tc.get('args', {})
                # Check for write_to_file or replace_file_content on code.html
                target = args.get('TargetFile', '')
                if 'code.html' in target:
                    content_len = len(args.get('CodeContent', '')) or len(args.get('ReplacementContent', ''))
                    print(f"Line {i}: Tool {name}, Target: {target}, Content length: {content_len}")
                    found_calls.append((i, name, args))
        except Exception as e:
            pass

# Let's save the last write_to_file that had a large content
for i, name, args in reversed(found_calls):
    if name == 'write_to_file' and len(args.get('CodeContent', '')) > 20000:
        print(f"Found a large write_to_file at line {i}!")
        with open("scratch/recovered_code_html.html", "w", encoding="utf-8") as out:
            out.write(args['CodeContent'])
        print("Saved to scratch/recovered_code_html.html")
        break
