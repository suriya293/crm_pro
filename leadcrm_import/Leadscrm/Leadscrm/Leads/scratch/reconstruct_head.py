import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

lines_dict = {}

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        try:
            data = json.loads(line)
            content = data.get('content', '')
            if 'code.html' in content:
                matches = re.findall(r'^(\d+): (.*)$', content, re.MULTILINE)
                for num_str, val in matches:
                    num = int(num_str)
                    if num <= 300:
                        if num not in lines_dict:
                            lines_dict[num] = []
                        lines_dict[num].append((line_idx, val))
        except Exception as e:
            pass

# Let's rebuild the head by picking the earliest snapshot of each line
reconstructed = {}
for num, versions in lines_dict.items():
    # Sort by log line index (earliest first, to get original code before corruption)
    versions.sort()
    # Find the first version that doesn't look like parts of other files (e.g. reconstruct_code.py, read_logs.py, etc.)
    # In this case, we'll just pick the one from the lowest log index that isn't empty if possible.
    val = versions[0][1]
    for l_idx, v in versions:
        # If the log line index is very low (e.g. before step 150 where the corruption occurred), it's likely original
        if l_idx < 100:
            val = v
            break
    reconstructed[num] = val

with open("scratch/reconstructed_head.txt", "w", encoding="utf-8") as out:
    for k in sorted(reconstructed.keys()):
        out.write(f"{k}: {reconstructed[k]}\n")

print("Done! Reconstructed head written to scratch/reconstructed_head.txt")
