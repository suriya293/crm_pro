import os

files = [f for f in os.listdir('recovery') if f.endswith('.txt')]
for fname in files:
    path = os.path.join('recovery', fname)
    print(f"=== lines with hover in {fname} ===")
    with open(path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if 'hover' in line.lower():
                print(f"{idx+1}: {line.strip()}")
