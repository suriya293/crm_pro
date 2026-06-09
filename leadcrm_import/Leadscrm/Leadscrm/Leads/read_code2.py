import re
text = open('code.html', encoding='utf-8').read()
js_blocks = re.findall(r'<script>([\s\S]*?)</script>', text)
with open('js_output.txt', 'w', encoding='utf-8') as f:
    for js in js_blocks:
        if 'addEventListener(\'click\'' in js or 'addEventListener("click"' in js:
            f.write(js)
            f.write('\n\n--- \n\n')
