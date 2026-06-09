import glob
import re

for filepath in glob.glob('*.html') + glob.glob('*.js'):
    try:
        content = open(filepath, encoding='utf-8').read()
        fb_matches = re.findall(r'(?i)facebook|fb_', content)
        wa_matches = re.findall(r'(?i)whatsapp|wa_', content)
        if fb_matches or wa_matches:
            print(f"{filepath}: {len(fb_matches)} FB matches, {len(wa_matches)} WA matches")
            # print matching lines
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if any(x in line.lower() for x in ['facebook', 'fb_', 'whatsapp', 'wa_']):
                    print(f"  Line {i+1}: {line.strip()[:100]}")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
