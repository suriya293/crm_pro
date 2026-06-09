import re

for page in ['dashboard.html', 'code.html', 'settings.html', 'app.html', 'reports.html']:
    text = open(page, encoding='utf-8').read()
    match = re.search(r'<div id="admin-menu"[^>]*>(.*?)</div>\s*</div>', text, re.DOTALL)
    if match:
        print(f'{page} admin-menu found:')
        print(match.group(1).strip()[:100] + '...')
    else:
        print(f'{page} admin-menu NOT found.')
