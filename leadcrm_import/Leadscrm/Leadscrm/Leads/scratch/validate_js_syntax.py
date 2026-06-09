import os
import re
import subprocess

html_dir = r"c:\Users\YUVEHA\OneDrive\Documents\Leads"
temp_js = os.path.join(html_dir, "scratch", "temp_syntax_check.js")

html_files = [f for f in os.listdir(html_dir) if f.endswith(".html")]

print(f"Checking syntax for {len(html_files)} html files...")

for f_name in html_files:
    if f_name == "code.html":
        print(f"Skipping {f_name} (needs to be rebuilt)")
        continue
        
    f_path = os.path.join(html_dir, f_name)
    with open(f_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    scripts = re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.DOTALL)
    
    for idx, script in enumerate(scripts):
        if "tailwind.config" in script or len(script.strip()) < 50:
            continue
            
        with open(temp_js, "w", encoding="utf-8") as js_out:
            js_out.write(script)
            
        res = subprocess.run(["node", "--check", temp_js], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[ERROR] Syntax Error in {f_name} script block {idx+1}:")
            print(res.stderr)
        else:
            print(f"[OK] {f_name} script block {idx+1} syntax is valid.")

if os.path.exists(temp_js):
    os.remove(temp_js)
