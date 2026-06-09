import re

with open("scratch/css_dump_21.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Match lines of the form: "  12:         /* KANBAN LAYOUT - Visible Scrollbars */"
# and extract the actual content.
lines = content.splitlines()
clean_lines = []

for line in lines:
    m = re.match(r'^\s*(\d+):\s?(.*)$', line)
    if m:
        line_num = int(m.group(1))
        line_val = m.group(2)
        clean_lines.append((line_num, line_val))

# Sort by line number
clean_lines.sort()

# Print the range we got
if clean_lines:
    print(f"Cleaned lines from {clean_lines[0][0]} to {clean_lines[-1][0]}")
    with open("scratch/clean_head_reconstructed.html", "w", encoding="utf-8") as out:
        for num, val in clean_lines:
            out.write(val + "\n")
    print("Wrote clean head to scratch/clean_head_reconstructed.html")
else:
    print("No matching lines found.")
