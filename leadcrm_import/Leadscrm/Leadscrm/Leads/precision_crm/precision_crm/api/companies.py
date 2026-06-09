import frappe
from frappe import _
import json
from precision_crm.auth import authenticate_request
from precision_crm.permissions import has_permission
from precision_crm.api.leads import handle_api_exception

@frappe.whitelist(allow_guest=True)
def create_company(**kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        frappe.db.begin()
        doc = frappe.get_doc(dict(doctype="Company", **kwargs))
        doc.insert()
        frappe.db.commit()
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_company(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Company", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Company not found"}

        doc = frappe.get_doc("Company", name)
        if not has_permission(doc, "read"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def update_company(name, **kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Company", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Company not found"}

        doc = frappe.get_doc("Company", name)
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
def delete_company(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Company", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Company not found"}

        doc = frappe.get_doc("Company", name)
        if not has_permission(doc, "delete"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.delete()
        frappe.db.commit()
        return {"status": "success", "message": "Company deleted successfully"}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def list_companies(start=0, limit=20, order_by="creation desc", filters=None):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if isinstance(filters, str):
            filters = json.loads(filters)
        if not filters:
            filters = {}

        companies = frappe.get_all(
            "Company",
            filters=filters,
            order_by=order_by,
            start=start,
            page_length=limit,
            fields=["*"]
        )
        
        allowed_companies = [c for c in companies if has_permission(frappe.get_doc("Company", c.name), "read")]
        return {"status": "success", "data": allowed_companies, "total": len(allowed_companies)}
    except Exception as e:
        return handle_api_exception(e)
