import re
text = open('dashboard.html', encoding='utf-8').read()
match = re.search(r'<div id="admin-menu"[^>]*>(.*?)</div>\s*</div>\s*</header>', text, re.DOTALL)
if match:
    print('admin-menu block:', match.group(1).strip())
