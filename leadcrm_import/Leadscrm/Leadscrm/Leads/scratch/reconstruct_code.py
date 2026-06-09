import json
import re

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

lines_dict = {}

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            # Check the content of the step output
            content = data.get('content', '')
            if not content:
                # Also check tool_calls output / results
                tool_ops = data.get('tool_calls', [])
                for op in tool_ops:
                    # check if it is a view_file output
                    pass
            
            # Let's inspect content and look for code.html line markers
            if 'Showing lines' in content and 'code.html' in content:
                matches = re.findall(r'^(\d+):(?: (.*))?$', content, re.MULTILINE)
                for num_str, val in matches:
                    num = int(num_str)
                    lines_dict[num] = val if val is not None else ""
        except Exception as e:
            pass

# Sort lines and reconstruct file
sorted_keys = sorted(lines_dict.keys())
print(f"Reconstructed {len(sorted_keys)} lines.")

if len(sorted_keys) > 0:
    min_k, max_k = sorted_keys[0], sorted_keys[-1]
    print(f"Range: {min_k} to {max_k}")
    
    reconstructed_content = []
    for k in range(1, max_k + 1):
        if k in lines_dict:
            reconstructed_content.append(lines_dict[k])
        else:
            print(f"Missing line {k}!")
            reconstructed_content.append("")
            
    # Write output to code.html
    # Note: Use CRLF line endings as it is a Windows environment
    with open(r"c:\Users\YUVEHA\OneDrive\Documents\Leads\code.html", 'w', encoding='utf-8', newline='\r\n') as out_f:
        out_f.write("\n".join(reconstructed_content))
    print("code.html successfully reconstructed!")
else:
    print("No lines found to reconstruct.")
