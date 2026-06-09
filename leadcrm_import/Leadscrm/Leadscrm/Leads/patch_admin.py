import os

files = ['dashboard.html', 'code.html', 'settings.html', 'app.html', 'reports.html']
for f in files:
    try:
        content = open(f, encoding='utf-8').read()
        if 'id="admin-menu"' in content and 'onclick="event.stopPropagation()"' not in content:
            new_content = content.replace('id="admin-menu" class="', 'id="admin-menu" onclick="event.stopPropagation()" class="')
            with open(f, 'w', encoding='utf-8') as out:
                out.write(new_content)
            print(f'Patched {f}')
        else:
            print(f'Skipped {f}')
    except Exception as e:
        print(f'Error {f}: {e}')
