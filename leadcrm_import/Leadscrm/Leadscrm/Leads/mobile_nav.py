import re

files = ['dashboard.html', 'code.html', 'settings.html', 'app.html', 'reports.html']

for page in files:
    try:
        text = open(page, encoding='utf-8').read()
        
        # 1. Update Sidebar classes
        if 'id="main-sidebar"' not in text:
            text = re.sub(
                r'<aside class="hidden md:flex flex-col (.*?)">',
                r'<aside id="main-sidebar" class="fixed md:static inset-y-0 left-0 z-50 transform -translate-x-full md:translate-x-0 transition-transform duration-300 ease-in-out flex flex-col \1">',
                text, count=1
            )
            # Inject overlay
            text = re.sub(
                r'(<body.*?>\s*(?:<div id="vanta-bg".*?></div>)?)',
                r'\1\n  <div id="sidebar-overlay" class="fixed inset-0 bg-slate-900/50 z-40 hidden md:hidden" onclick="toggleSidebar()"></div>',
                text, count=1
            )
            
        # 2. Update Header Hamburger and Hide items
        if 'toggleSidebar()' not in text.split('</header>')[0]:
            # Add hamburger before title
            text = re.sub(
                r'(<div class="flex items-center">\s*<h2)',
                r'<div class="flex items-center gap-2 md:gap-0">\n              <button onclick="toggleSidebar()" class="md:hidden p-2 -ml-2 rounded-xl text-[#0D9488] hover:bg-teal-50 transition-colors"><span class="material-symbols-outlined text-[24px]">menu</span></button>\n              <h2',
                text, count=1
            )
            # Hide clock
            text = text.replace(
                '<div id="clock-container" class="flex items-center',
                '<div id="clock-container" class="hidden md:flex items-center'
            )
            # Clean up old class string if present and add hidden md:flex to buttons
            text = re.sub(
                r'class="p-2 rounded-full hover:bg-slate-100 transition-colors flex items-center justify-center text-slate-500" (title="Tips".*?>)',
                r'class="hidden md:flex p-2 rounded-full hover:bg-slate-100 transition-colors items-center justify-center text-slate-500" \1', text
            )
            text = re.sub(
                r'class="p-2 rounded-full hover:bg-slate-100 transition-colors flex items-center justify-center text-slate-500" (title="Toggle Fullscreen".*?>)',
                r'class="hidden md:flex p-2 rounded-full hover:bg-slate-100 transition-colors items-center justify-center text-slate-500" \1', text
            )
            
        # 3. Add JS function
        if 'function toggleSidebar()' not in text:
            js = '''
window.toggleSidebar = function() {
    const sidebar = document.getElementById('main-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    if (sidebar) sidebar.classList.toggle('-translate-x-full');
    if (overlay) overlay.classList.toggle('hidden');
};
'''
            text = text.replace('</head>', f'<script>{js}</script>\n</head>')

        open(page, 'w', encoding='utf-8').write(text)
        print(f'Updated {page} header & sidebar')
    except Exception as e:
        print(f'Error on {page}: {e}')
