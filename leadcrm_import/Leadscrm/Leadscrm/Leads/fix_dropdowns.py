import re

old_js = """    // Admin Dropdown Toggle
    function toggleAdminMenu(event) {
        event.stopPropagation();
        const menu = document.getElementById('admin-menu');
        if (menu) menu.classList.toggle('hidden');
    }
    document.addEventListener('click', () => {
        const menu = document.getElementById('admin-menu');
        if (menu) menu.classList.add('hidden');
    });"""

new_js = """    // Admin Dropdown Toggle
    function toggleAdminMenu(event) {
        event.stopPropagation();
        const menu = document.getElementById('admin-menu');
        if (menu) menu.classList.toggle('hidden');
    }
    document.addEventListener('click', (e) => {
        const menu = document.getElementById('admin-menu');
        if (menu && !menu.contains(e.target)) {
            menu.classList.add('hidden');
        }
    });"""

for page in ['dashboard.html', 'code.html', 'settings.html', 'app.html', 'reports.html']:
    try:
        text = open(page, encoding='utf-8').read()
        if old_js in text:
            new_text = text.replace(old_js, new_js)
            open(page, 'w', encoding='utf-8').write(new_text)
            print(f'Fixed dropdown JS in {page}')
        else:
            print(f'Could not find old JS block in {page}')
    except Exception as e:
        print(f'Error updating {page}: {e}')

