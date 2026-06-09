import frappe
from frappe import _
import json
from precision_crm.auth import authenticate_request
from precision_crm.permissions import has_permission
from precision_crm.api.leads import handle_api_exception

@frappe.whitelist(allow_guest=True)
def create_opportunity(**kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        frappe.db.begin()
        doc = frappe.get_doc(dict(doctype="Opportunity", **kwargs))
        doc.insert()
        frappe.db.commit()
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_opportunity(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Opportunity", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Opportunity not found"}

        doc = frappe.get_doc("Opportunity", name)
        if not has_permission(doc, "read"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def update_opportunity(name, **kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Opportunity", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Opportunity not found"}

        doc = frappe.get_doc("Opportunity", name)
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
def delete_opportunity(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Opportunity", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Opportunity not found"}

        doc = frappe.get_doc("Opportunity", name)
        if not has_permission(doc, "delete"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.delete()
        frappe.db.commit()
        return {"status": "success", "message": "Opportunity deleted successfully"}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def list_opportunities(start=0, limit=20, order_by="creation desc", filters=None):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if isinstance(filters, str):
            filters = json.loads(filters)
        if not filters:
            filters = {}

        opportunities = frappe.get_all(
            "Opportunity",
            filters=filters,
            order_by=order_by,
            start=start,
            page_length=limit,
            fields=["*"]
        )
        
        allowed_opps = [o for o in opportunities if has_permission(frappe.get_doc("Opportunity", o.name), "read")]
        return {"status": "success", "data": allowed_opps, "total": len(allowed_opps)}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def move_stage(name, status):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Opportunity", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Opportunity not found"}

        doc = frappe.get_doc("Opportunity", name)
        if not has_permission(doc, "write"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.status = status
        doc.save()
        frappe.db.commit()
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def mark_won(name):
    return move_stage(name, "Won")

@frappe.whitelist(allow_guest=True)
def mark_lost(name):
    return move_stage(name, "Lost")
