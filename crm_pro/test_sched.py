import logging
from ratelimit import limits as ratelimit
import frappe
from frappe.utils.scheduler import is_scheduler_disabled

def run():
    print("=== SCHEDULER REPAIR ===")
    val = frappe.db.get_single_value("System Settings", "enable_scheduler")
    print("Current enable_scheduler in System Settings:", val)
    print("is_scheduler_disabled() before:", is_scheduler_disabled())
    
    # Enable it
    frappe.db.set_single_value("System Settings", "enable_scheduler", 1)
    frappe.db.commit()
    frappe.clear_cache(doctype="System Settings")
    
    print("is_scheduler_disabled() after:", is_scheduler_disabled())
