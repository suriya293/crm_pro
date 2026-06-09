import re

for page in ['code.html', 'settings.html', 'app.html', 'reports.html']:
    try:
        text = open(page, encoding='utf-8').read()
        target = 'f"{dd}-{mm}-{yyyy} {hh}:{min}:{ss}"'
        if target in text:
            new_text = text.replace(target, '`${dd}-${mm}-${yyyy} ${hh}:${min}:${ss}`')
            open(page, 'w', encoding='utf-8').write(new_text)
            print(f'Fixed clock script in {page}')
        elif "f'{dd}-{mm}-{yyyy} {hh}:{min}:{ss}'" in text:
            new_text = text.replace("f'{dd}-{mm}-{yyyy} {hh}:{min}:{ss}'", '`${dd}-${mm}-${yyyy} ${hh}:${min}:${ss}`')
            open(page, 'w', encoding='utf-8').write(new_text)
            print(f'Fixed clock script in {page}')
        else:
            print(f'Clock f-string not found in {page}')
    except Exception as e:
        print(f'Error updating {page}: {e}')
