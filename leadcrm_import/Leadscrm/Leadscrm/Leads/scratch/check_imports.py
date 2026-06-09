import os
import sys
import importlib

sys.path.insert(0, r"C:\Users\acer\Downloads\Leadscrm\Leadscrm\Leads\precision_crm")

doctypes_dir = r"C:\Users\acer\Downloads\Leadscrm\Leadscrm\Leads\precision_crm\precision_crm\doctype"
errors = []

for folder in os.listdir(doctypes_dir):
    py_path = os.path.join(doctypes_dir, folder, f"{folder}.py")
    if os.path.exists(py_path):
        module_name = f"precision_crm.doctype.{folder}.{folder}"
        try:
            importlib.import_module(module_name)
            print(f"Successfully imported {module_name}")
        except Exception as e:
            errors.append((module_name, str(e)))

if errors:
    print("\nErrors encountered:")
    for mod, err in errors:
        print(f"Failed to import {mod}: {err}")
    sys.exit(1)
else:
    print("\nAll controllers imported successfully!")
