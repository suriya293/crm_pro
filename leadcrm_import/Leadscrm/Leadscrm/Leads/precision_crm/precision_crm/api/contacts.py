import frappe
from frappe import _
import json
from precision_crm.auth import authenticate_request
from precision_crm.permissions import has_permission
from precision_crm.api.leads import handle_api_exception

@frappe.whitelist(allow_guest=True)
def create_contact(**kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        frappe.db.begin()
        doc = frappe.get_doc(dict(doctype="Contact", **kwargs))
        doc.insert()
        frappe.db.commit()
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_contact(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Contact", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Contact not found"}

        doc = frappe.get_doc("Contact", name)
        if not has_permission(doc, "read"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def update_contact(name, **kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Contact", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Contact not found"}

        doc = frappe.get_doc("Contact", name)
        if not has_permission(doc, "write"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.update(kwargs)
        doc.save()
        frappe.db.commit()
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def delete_contact(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Contact", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Contact not found"}

        doc = frappe.get_doc("Contact", name)
        if not has_permission(doc, "delete"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.delete()
        frappe.db.commit()
        return {"status": "success", "message": "Contact deleted successfully"}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def list_contacts(start=0, limit=20, order_by="creation desc", filters=None):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if isinstance(filters, str):
            filters = json.loads(filters)
        if not filters:
            filters = {}

        contacts = frappe.get_all(
            "Contact",
            filters=filters,
            order_by=order_by,
            start=start,
            page_length=limit,
            fields=["*"]
        )
        
        allowed_contacts = [c for c in contacts if has_permission(frappe.get_doc("Contact", c.name), "read")]
        return {"status": "success", "data": allowed_contacts, "total": len(allowed_contacts)}
    except Exception as e:
        return handle_api_exception(e)
