import re
text = open('code.html', encoding='utf-8').read()
js_blocks = re.findall(r'<script>([\s\S]*?)</script>', text)
for js in js_blocks:
    if 'addEventListener(\'click\'' in js or 'addEventListener("click"' in js:
        print(js)
