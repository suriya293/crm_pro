import json

log_path = r"C:\Users\YUVEHA\.gemini\antigravity-ide\brain\8f53ea80-d75a-4062-a547-db2a3f603faf\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for i in range(15):
        line = f.readline()
        if not line:
            break
        try:
            data = json.loads(line)
            print(f"Step {data.get('step_index')}: Source: {data.get('source')}, Type: {data.get('type')}")
        except Exception as e:
            print("Error parsing line:", e)
