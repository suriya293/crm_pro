import os

files_to_check = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.txt') or f.endswith('.html') or f.endswith('.js') or f.endswith('.py'):
            files_to_check.append(os.path.join(root, f))

print(f"Checking {len(files_to_check)} files for 'kanban-column'...")

for p in files_to_check:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'kanban-column' in content:
                count = content.count('kanban-column')
                print(f"File: {p}, occurrences: {count}, size: {len(content)} bytes")
    except Exception as e:
        pass
