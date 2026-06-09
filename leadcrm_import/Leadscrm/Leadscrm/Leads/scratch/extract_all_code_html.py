import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

lines_dict = {}

def extract_from_text(text, log_idx):
    # Find patterns like "123: some code" at the start of a line
    # The text might have CRLF or LF newlines.
    matches = re.findall(r'^(\d+):(?: (.*))?$', text, re.MULTILINE)
    for num_str, val in matches:
        num = int(num_str)
        val = val if val is not None else ""
        if num not in lines_dict:
            lines_dict[num] = []
        lines_dict[num].append((log_idx, val))

def scan_val(val, log_idx):
    if isinstance(val, str):
        if "code.html" in val or "Showing lines" in val or "Material Symbols" in val or "kanban" in val:
            extract_from_text(val, log_idx)
    elif isinstance(val, dict):
        for k, v in val.items():
            scan_val(v, log_idx)
    elif isinstance(val, list):
        for item in val:
            scan_val(item, log_idx)

with open(log_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        try:
            data = json.loads(line)
            scan_val(data, line_idx)
        except Exception as e:
            pass

print(f"Total unique line numbers: {len(lines_dict)}")

# For each line, let's pick the version from the lowest log index that has content
clean_lines = {}
for num, versions in lines_dict.items():
    versions.sort() # earliest first
    # Find first non-empty
    best_val = ""
    for log_idx, val in versions:
        # Ignore lines that contain python code or log script output
        if "reconstruct_code.py" in val or "lines_dict" in val:
            continue
        if val.strip():
            best_val = val
            break
    if not best_val and versions:
        best_val = versions[0][1]
    clean_lines[num] = best_val

# Check density
missing_lines = []
for k in range(1, 2306):
    if k not in clean_lines or not clean_lines[k].strip():
        missing_lines.append(k)

print(f"Missing lines count: {len(missing_lines)}")

# Save reconstructed file
reconstructed_content = []
for k in range(1, 2306):
    reconstructed_content.append(clean_lines.get(k, ""))

with open("scratch/code_html_reconstructed_full.html", "w", encoding="utf-8", newline="\r\n") as out:
    out.write("\n".join(reconstructed_content))

print("Reconstructed full file saved to scratch/code_html_reconstructed_full.html")
