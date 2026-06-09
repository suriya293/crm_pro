import re

content = open('code.html', encoding='utf-8').read()
match = re.search(r'id="admin-menu"[^>]*', content)
if match:
    print(match.group(0))

new_content = re.sub(r'id="admin-menu"([^>]*class=")', r'id="admin-menu" onclick="event.stopPropagation()"\1', content)
if new_content != content:
    with open('code.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Patched code.html")
else:
    print("No change made to code.html")
