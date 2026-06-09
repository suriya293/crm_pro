import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx == 27:
            data = json.loads(line)
            content = data.get('content', '')
            # Find all line number patterns e.g. "1801: function addCustomFieldRow(fieldName ="
            matches = re.findall(r'^(\d+):(?: (.*))?$', content, re.MULTILINE)
            print(f"Parsed {len(matches)} matches from LogLine 27.")
            
            # Save them
            with open("scratch/recovered_lines_1800_2305.txt", "w", encoding="utf-8") as out:
                for num_str, val in matches:
                    val = val if val is not None else ""
                    out.write(f"{num_str}: {val}\n")
            print("Saved to scratch/recovered_lines_1800_2305.txt")
            break
