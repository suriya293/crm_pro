import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

lines_dict = {}

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            content = data.get('content', '')
            if 'Showing lines' in content and 'code.html' in content:
                # Find all line number matches
                matches = re.findall(r'^(\d+): (.*)$', content, re.MULTILINE)
                for num_str, val in matches:
                    num = int(num_str)
                    if 140 <= num <= 220:
                        if num not in lines_dict:
                            lines_dict[num] = []
                        lines_dict[num].append(val)
        except Exception as e:
            pass

print("Lines found:")
for num in sorted(lines_dict.keys()):
    # Get the earliest version
    val = lines_dict[num][0]
    print(f"{num}: {val}")
