import frappe
from frappe import _

def validate_email(email):
    if not email:
        return
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        frappe.throw(_("Invalid email address format: {0}").format(email))

def validate_mobile_uniqueness(doctype, mobile_no, docname=None):
    if not mobile_no:
        return
    filters = {"mobile_no": mobile_no}
    if docname:
        filters["name"] = ["!=", docname]
    exists = frappe.db.exists(doctype, filters)
    if exists:
        frappe.throw(_("Mobile number {0} is already registered under {1}").format(mobile_no, exists))

def validate_email_uniqueness(doctype, email, docname=None):
    if not email:
        return
    filters = {"email": email}
    if docname:
        filters["name"] = ["!=", docname]
    exists = frappe.db.exists(doctype, filters)
    if exists:
        frappe.throw(_("Email {0} is already registered under {1}").format(email, exists))

def validate_company(doc):
    if hasattr(doc, "company") and doc.company:
        if not frappe.db.exists("Company", doc.company):
            frappe.throw(_("Company {0} does not exist.").format(doc.company))

def validate_territory(doc):
    if hasattr(doc, "territory") and doc.territory:
        if not frappe.db.exists("Territory", doc.territory):
            frappe.throw(_("Territory {0} does not exist.").format(doc.territory))

def validate_team(doc):
    if hasattr(doc, "team") and doc.team:
        if not frappe.db.exists("Team", doc.team):
            frappe.throw(_("Team {0} does not exist.").format(doc.team))
