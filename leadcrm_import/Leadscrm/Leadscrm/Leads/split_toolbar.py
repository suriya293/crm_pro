import re

content = open('code.html', encoding='utf-8').read()

# The original toolbar starts with:
# <section class="flex flex-row items-center gap-2 px-6 py-3 bg-white border-b border-slate-100 shrink-0 flex-nowrap overflow-x-auto no-scrollbar">

old_toolbar_start = '<section class="flex flex-row items-center gap-2 px-6 py-3 bg-white border-b border-slate-100 shrink-0 flex-nowrap overflow-x-auto no-scrollbar">'
new_toolbar_start = '''<!-- Toolbar -->
    <section class="flex flex-col gap-3 px-6 py-3 bg-white border-b border-slate-100 shrink-0 w-full">
        <!-- Top Row -->
        <div class="flex flex-row items-center gap-2 flex-nowrap overflow-x-auto no-scrollbar w-full">'''

content = content.replace(old_toolbar_start, new_toolbar_start, 1)
content = content.replace('<!-- Divider -->\n        <div class="h-6 w-px bg-slate-200 mx-1 shrink-0"></div>\n\n        <!-- Right actions (push to end) -->\n        <div class="flex items-center gap-2 ml-auto shrink-0">', '</div>\n        \n        <!-- Bottom Row (Right Actions) -->\n        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1 w-full justify-start">', 1)

with open('code.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Toolbar split into two rows!")
