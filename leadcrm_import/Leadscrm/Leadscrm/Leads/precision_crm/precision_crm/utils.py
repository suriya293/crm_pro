import frappe
from frappe import _
from frappe.model.naming import make_autoname

def set_audit_fields(doc):
    user = frappe.session.user or "Administrator"
    now = frappe.utils.now_datetime()
    
    if not doc.owner:
        doc.owner = user
    if not doc.created_by:
        doc.created_by = user
    
    doc.modified_by = user
    doc.modified = now
    
    if doc.is_new():
        doc.creation = now

def apply_naming_series(doc, prefix):
    if not doc.naming_series:
        doc.naming_series = f"{prefix}-.YYYY.-#####"
    doc.name = make_autoname(doc.naming_series)

def create_activity(activity_type, lead=None, description=None, performed_by=None):
    activity = frappe.get_doc({
        "doctype": "Activity",
        "activity_type": activity_type,
        "lead": lead,
        "description": description,
        "performed_by": performed_by or frappe.session.user or "Administrator",
        "timestamp": frappe.utils.now_datetime()
    })
    activity.insert(ignore_permissions=True)
    return activity
