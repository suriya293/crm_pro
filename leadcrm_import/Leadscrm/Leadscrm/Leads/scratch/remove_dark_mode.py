import os
import re

html_dir = r"c:\Users\YUVEHA\OneDrive\Documents\Leads"

html_files = [f for f in os.listdir(html_dir) if f.endswith(".html")]

print(f"Removing dark mode references from {len(html_files)} files...")

for f_name in html_files:
    f_path = os.path.join(html_dir, f_name)
    with open(f_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_len = len(content)

    # 1. Remove darkMode: "class", or darkMode: 'class', (with optional spaces and trailing commas)
    content = re.sub(r"darkMode\s*:\s*[\"']class[\"']\s*,?", "", content)
    
    # 2. Remove initDarkMode() call or function references
    content = content.replace("initDarkMode();", "")
    content = content.replace("initDarkMode()", "")
    
    # 3. Remove initDarkMode function definition if any
    content = re.sub(r"function initDarkMode\(\)\s*\{.*?\}", "", content, flags=re.DOTALL)
    
    # 4. Remove toggleDarkMode function definition if any
    content = re.sub(r"function toggleDarkMode\(\)\s*\{.*?\}", "", content, flags=re.DOTALL)
    
    # 5. Remove HTML class="dark" if any (e.g. from html tag)
    content = re.sub(r'<html\s+class="dark"\s+lang="en">', '<html class="light" lang="en">', content)

    # 6. Remove any dark:... classes from tailwind classes
    # e.g. dark:hover:bg-slate-700, dark:text-slate-350, dark:bg-slate-800, etc.
    # We find class="..." or class='...' and strip any classes starting with dark:
    def strip_dark_classes(match):
        class_attr = match.group(0)
        # Find the inner quote content
        quote_char = class_attr[6] # either " or '
        inner_content = class_attr[7:-1]
        
        # Split by spaces and remove any class containing "dark:"
        classes = inner_content.split()
        cleaned_classes = [c for c in classes if not c.startswith("dark:")]
        
        return f'class={quote_char}{" ".join(cleaned_classes)}{quote_char}'

    content = re.sub(r'class=["\'](.*?)["\']', strip_dark_classes, content)

    # Write back if changed
    if len(content) != original_len or True:
        with open(f_path, "w", encoding="utf-8", newline="\r\n") as f:
            f.write(content)
        print(f"Processed {f_name}")

print("Dark mode removal finished successfully!")
