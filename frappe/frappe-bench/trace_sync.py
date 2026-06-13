import frappe
import sys

frappe.init(site="crm.local", sites_path="/home/acer/frappe/frappe-bench/sites")
frappe.connect()

import frappe.modules.import_file as import_file
import frappe.model.sync
orig_import_file_by_path = import_file.import_file_by_path

def patched_import_file_by_path(path, force=False, pre_import=None, ignore_version=False, reset_permissions=False):
    print("IMPORTING:", path)
    sys.stdout.flush()
    try:
        res = orig_import_file_by_path(path, force, pre_import, ignore_version, reset_permissions)
        return res
    except Exception as e:
        print("FAILED ON:", path, file=sys.stderr)
        raise

import_file.import_file_by_path = patched_import_file_by_path

def run():
    try:
        frappe.model.sync.sync_for("crm_pro", force=True)
        print("SUCCESSFULLY SYNCED ALL")
    except Exception as e:
        import traceback
        traceback.print_exc()
