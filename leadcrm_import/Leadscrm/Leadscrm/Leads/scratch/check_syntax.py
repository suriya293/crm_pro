import os
import ast
import sys

doctypes_dir = r"C:\Users\acer\Downloads\Leadscrm\Leadscrm\Leads\precision_crm\precision_crm\doctype"
api_dir = r"C:\Users\acer\Downloads\Leadscrm\Leadscrm\Leads\precision_crm\precision_crm\api"
integrations_dir = r"C:\Users\acer\Downloads\Leadscrm\Leadscrm\Leads\precision_crm\precision_crm\integrations"
errors = []

for folder_path in [doctypes_dir, api_dir, integrations_dir]:
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    py_path = os.path.join(root, file)
                    try:
                        with open(py_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        ast.parse(content, filename=py_path)
                        print(f"Syntax OK: {py_path}")
                    except Exception as e:
                        errors.append((py_path, str(e)))

# Also check top-level files
for file in ["validators.py", "utils.py", "permissions.py", "auth.py", "automation.py", "scheduler.py"]:

    py_path = os.path.join(r"C:\Users\acer\Downloads\Leadscrm\Leadscrm\Leads\precision_crm\precision_crm", file)
    if os.path.exists(py_path):
        try:
            with open(py_path, "r", encoding="utf-8") as f:
                content = f.read()
            ast.parse(content, filename=py_path)
            print(f"Syntax OK: {py_path}")
        except Exception as e:
            errors.append((py_path, str(e)))

if errors:
    print("\nSyntax errors found:")
    for path, err in errors:
        print(f"{path}: {err}")
    sys.exit(1)
else:
    print("\nAll Python files parsed successfully (Syntax OK)!")

