import re

for page in ['dashboard.html', 'code.html', 'reports.html']:
    try:
        text = open(page, encoding='utf-8').read()
        
        # We need to find <table> elements that are not already inside an overflow-x-auto div
        # A simple approach: 
        # Replace <table with <div class="overflow-x-auto w-full"><table
        # And replace </table> with </table></div>
        # But wait, this might double wrap if we run it multiple times.
        
        if 'class="overflow-x-auto w-full"><table' not in text:
            # For safe replacement without regex parsing the whole DOM:
            text = text.replace('<table', '<div class="overflow-x-auto w-full">\n<table')
            text = text.replace('</table>', '</table>\n</div>')
            open(page, 'w', encoding='utf-8').write(text)
            print(f'Wrapped tables in {page}')
        else:
            print(f'Tables already wrapped in {page}')
    except Exception as e:
        print(f'Error updating {page}: {e}')
