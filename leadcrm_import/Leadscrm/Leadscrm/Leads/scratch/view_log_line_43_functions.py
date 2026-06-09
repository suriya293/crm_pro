import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx == 43:
            data = json.loads(line)
            content = data.get('content', '')
            matches = re.findall(r'^(\d+):(?: (.*))?$', content, re.MULTILINE)
            print(f"Parsed {len(matches)} matches from LogLine 43.")
            
            with open("scratch/recovered_lines_1500_1800.txt", "w", encoding="utf-8") as out:
                for num_str, val in matches:
                    val = val if val is not None else ""
                    out.write(f"{num_str}: {val}\n")
            print("Saved to scratch/recovered_lines_1500_1800.txt")
            break
