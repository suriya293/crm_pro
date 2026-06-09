import re
import glob

files = ['dashboard.html', 'settings.html', 'reports.html', 'app.html', 'stage.html']
for filename in files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Remove Three.js script
        content = re.sub(r'<script[^>]+three\.(?:min|r134\.min)\.js[^>]*></script>', '', content, flags=re.IGNORECASE)
        
        # Remove Vanta.js script
        content = re.sub(r'<script[^>]+vanta\.clouds(?:2)?\.min\.js[^>]*></script>', '', content, flags=re.IGNORECASE)
        
        # Remove initialization script
        content = re.sub(r'<script>\s*document\.addEventListener\([\'"]DOMContentLoaded[\'"].*?VANTA\.CLOUDS.*?</script>', '', content, flags=re.IGNORECASE|re.DOTALL)
        
        content = re.sub(r'<script>\s*VANTA\.CLOUDS\(.*?</script>', '', content, flags=re.IGNORECASE|re.DOTALL)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Processed {filename}')
    except Exception as e:
        print(f'Error processing {filename}: {e}')
