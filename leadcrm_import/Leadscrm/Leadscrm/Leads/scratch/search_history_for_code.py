import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

def search_obj(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'TargetFile' and 'code.html' in str(v):
                print(f"Found code.html TargetFile reference at: {path}")
                # check if sibling has CodeContent
                if 'CodeContent' in obj:
                    print(f"  CodeContent length: {len(obj['CodeContent'])}")
                    with open(f"scratch/found_code_html_{len(obj['CodeContent'])}.html", "w", encoding="utf-8") as out:
                        out.write(obj['CodeContent'])
                    print(f"  Saved to scratch/found_code_html_{len(obj['CodeContent'])}.html")
            search_obj(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            search_obj(item, f"{path}[{idx}]")

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        try:
            data = json.loads(line)
            search_obj(data, f"Line{line_idx}")
        except Exception as e:
            pass

print("Search completed.")
