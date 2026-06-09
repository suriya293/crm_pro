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
                matches = re.findall(r'^(\d+):(?: (.*))?$', content, re.MULTILINE)
                for num_str, val in matches:
                    num = int(num_str)
                    val = val if val is not None else ""
                    if num not in lines_dict:
                        lines_dict[num] = []
                    lines_dict[num].append(val)
        except Exception as e:
            pass

print(f"Total unique line numbers stored: {len(lines_dict)}")
# Let's count how many have non-empty values
non_empty = [k for k, v in lines_dict.items() if any(item.strip() for item in v)]
print(f"Total line numbers with non-empty values: {len(non_empty)}")

# Find ranges of empty line numbers
all_nums = sorted(lines_dict.keys())
empty_ranges = []
start = None
for k in range(1, 2306):
    is_empty = k not in lines_dict or not any(item.strip() for item in lines_dict[k])
    if is_empty:
        if start is None:
            start = k
    else:
        if start is not None:
            empty_ranges.append((start, k - 1))
            start = None
if start is not None:
    empty_ranges.append((start, 2305))

print("Empty/Missing Ranges:")
for r in empty_ranges:
    print(f"  {r[0]} to {r[1]}")
