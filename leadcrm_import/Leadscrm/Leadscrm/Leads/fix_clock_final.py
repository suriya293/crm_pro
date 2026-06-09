import re

valid_clock_script = """<!-- Injected Live Clock Script -->
<script>
document.addEventListener('DOMContentLoaded', () => {
    const clock = document.getElementById('live-clock');
    if (!clock) return;
    const update = () => {
        const now = new Date();
        const dd = String(now.getDate()).padStart(2, '0');
        const mm = String(now.getMonth()+1).padStart(2, '0');
        const yyyy = now.getFullYear();
        const hh = String(now.getHours()).padStart(2, '0');
        const min = String(now.getMinutes()).padStart(2, '0');
        const ss = String(now.getSeconds()).padStart(2, '0');
        clock.textContent = `${dd}-${mm}-${yyyy} ${hh}:${min}:${ss}`;
    };
    update();
    setInterval(update, 1000);
});
</script>
</body>"""

for page in ['code.html', 'settings.html', 'app.html', 'reports.html']:
    try:
        text = open(page, encoding='utf-8').read()
        
        # Strip out the old broken injected script
        if '<!-- Injected Live Clock Script -->' in text:
            # use regex to remove everything from the comment to </body>
            new_text = re.sub(r'<!-- Injected Live Clock Script -->.*?</body>', valid_clock_script, text, flags=re.DOTALL)
            open(page, 'w', encoding='utf-8').write(new_text)
            print(f'Fixed clock script in {page}')
        else:
            print(f'No injected script found in {page}, inserting it')
            new_text = text.replace('</body>', valid_clock_script)
            open(page, 'w', encoding='utf-8').write(new_text)
    except Exception as e:
        print(f'Error updating {page}: {e}')
