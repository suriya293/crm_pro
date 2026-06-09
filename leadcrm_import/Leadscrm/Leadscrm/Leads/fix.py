import re

text = open('code.html', encoding='utf-8').read()
matches = list(re.finditer(r'<header.*?</header>', text, re.DOTALL))

if len(matches) == 4:
    header1 = text[:matches[1].start()]
    
    header2_replacement = '''<header class="flex justify-between items-center w-full px-6 py-4 border-b border-slate-100 bg-white shrink-0">
            <h3 class="text-lg font-bold text-slate-800">Add/Edit Lead</h3>
            <button type="button" onclick="closeModal('add-lead-modal')" class="text-slate-400 hover:text-slate-600 transition-colors">
                <span class="material-symbols-outlined text-[20px]">close</span>
            </button>
        </header>'''
    
    header3_replacement = '''<header class="flex justify-between items-center w-full px-6 py-4 border-b border-slate-100 bg-white shrink-0">
            <h3 class="text-lg font-bold text-slate-800">Import Leads</h3>
            <button type="button" onclick="closeModal('import-modal')" class="text-slate-400 hover:text-slate-600 transition-colors">
                <span class="material-symbols-outlined text-[20px]">close</span>
            </button>
        </header>'''

    header4_replacement = '''<header class="flex justify-between items-center w-full px-6 py-4 border-b border-slate-100 bg-white shrink-0">
            <h3 class="text-lg font-bold text-slate-800">Import History</h3>
            <button type="button" onclick="closeModal('import-history-modal')" class="text-slate-400 hover:text-slate-600 transition-colors">
                <span class="material-symbols-outlined text-[20px]">close</span>
            </button>
        </header>'''
        
    part2 = text[matches[1].end():matches[2].start()]
    part3 = text[matches[2].end():matches[3].start()]
    part4 = text[matches[3].end():]
    
    new_text = header1 + header2_replacement + part2 + header3_replacement + part3 + header4_replacement + part4
    open('code.html', 'w', encoding='utf-8').write(new_text)
    print('Fixed code.html modals')
else:
    print('Error: not 4 headers')
