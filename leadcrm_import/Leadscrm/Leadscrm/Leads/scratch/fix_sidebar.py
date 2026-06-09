import os
import re

files = [r"c:\Users\YUVEHA\OneDrive\Documents\Leads\code.html", r"c:\Users\YUVEHA\OneDrive\Documents\Leads\settings.html", r"c:\Users\YUVEHA\OneDrive\Documents\Leads\listview.html"]

for fpath in files:
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # We want to find the <aside> block and replace text-white with text-slate-700
        # and bg-white/10 with hover:bg-slate-50
        def fix_aside(match):
            aside_html = match.group(0)
            aside_html = aside_html.replace("text-white", "text-slate-800")
            aside_html = aside_html.replace("bg-white/20", "bg-slate-100")
            aside_html = aside_html.replace("bg-white/10", "bg-transparent")
            aside_html = aside_html.replace("border-white/20", "border-slate-200")
            aside_html = aside_html.replace("border-white/30", "border-slate-200")
            aside_html = aside_html.replace("hover:border-white", "hover:border-slate-300")
            return aside_html

        content = re.sub(r'<aside.*?</aside>', fix_aside, content, flags=re.DOTALL)
        
        # Also clean up the main body background
        content = content.replace("bg-background", "bg-slate-50")
        content = content.replace("text-on-surface", "text-slate-800")
        
        with open(fpath, "w", encoding="utf-8", newline="\r\n") as f:
            f.write(content)
        print(f"Fixed sidebar in {fpath}")
