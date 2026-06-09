import os

html_path = r"c:\Users\YUVEHA\OneDrive\Documents\Leads\code.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# find the script tag that contains "let leadsData"
idx = content.find("<script>\n// --- State")
if idx == -1:
    idx = content.find("let leadsData = []")
    # find the script tag before it
    idx = content.rfind("<script>", 0, idx)

if idx != -1:
    js_content = content[idx:]
    with open(r"c:\Users\YUVEHA\OneDrive\Documents\Leads\scratch\current_js.txt", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("JS extracted.")
else:
    print("Failed to find JS.")
