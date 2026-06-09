import re

content = open('code.html', encoding='utf-8').read()
old_str = """<button onclick="alert('View Lead feature coming soon')" class="text-slate-500 hover:text-slate-700 transition-colors" title="View">
                        <span class="material-symbols-outlined text-[18px]">visibility</span>
                    </button>"""
new_str = """<button onclick="window.location.href='view_lead.html?name=' + encodeURIComponent('${lead.name.replace(/'/g, "\\'")}')" class="text-slate-500 hover:text-slate-700 transition-colors" title="View">
                        <span class="material-symbols-outlined text-[18px]">visibility</span>
                    </button>"""

if old_str in content:
    with open('code.html', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_str, new_str))
    print("code.html patched successfully!")
else:
    print("Could not find the exact string to replace in code.html")

