import frappe
from frappe import _
import json
from precision_crm.auth import authenticate_request
from precision_crm.permissions import has_permission
from precision_crm.api.leads import handle_api_exception

@frappe.whitelist(allow_guest=True)
def create_deal(**kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        frappe.db.begin()
        doc = frappe.get_doc(dict(doctype="Deal", **kwargs))
        doc.insert()
        frappe.db.commit()
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_deal(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Deal", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Deal not found"}

        doc = frappe.get_doc("Deal", name)
        if not has_permission(doc, "read"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def update_deal(name, **kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Deal", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Deal not found"}

        doc = frappe.get_doc("Deal", name)
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
def delete_deal(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Deal", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Deal not found"}

        doc = frappe.get_doc("Deal", name)
        if not has_permission(doc, "delete"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.delete()
        frappe.db.commit()
        return {"status": "success", "message": "Deal deleted successfully"}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def list_deals(start=0, limit=20, order_by="creation desc", filters=None):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if isinstance(filters, str):
            filters = json.loads(filters)
        if not filters:
            filters = {}

        deals = frappe.get_all(
            "Deal",
            filters=filters,
            order_by=order_by,
            start=start,
            page_length=limit,
            fields=["*"]
        )
        
        allowed_deals = [d for d in deals if has_permission(frappe.get_doc("Deal", d.name), "read")]
        return {"status": "success", "data": allowed_deals, "total": len(allowed_deals)}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def pipeline_view():
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        deals = frappe.get_all("Deal", fields=["name", "deal_name", "amount", "stage", "expected_close_date"])
        pipeline = {
            "Prospect": [],
            "Negotiation": [],
            "Won": [],
            "Lost": []
        }
        for d in deals:
            # Check permission
            doc = frappe.get_doc("Deal", d.name)
            if has_permission(doc, "read"):
                stage = d.stage or "Prospect"
                if stage in pipeline:
                    pipeline[stage].append(d)
                    
        return {"status": "success", "data": pipeline}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def deal_forecast():
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        deals = frappe.get_all("Deal", fields=["name", "amount", "stage"])
        total_forecast = 0.0
        stage_weights = {
            "Prospect": 0.1,
            "Negotiation": 0.5,
            "Won": 1.0,
            "Lost": 0.0
        }
        for d in deals:
            doc = frappe.get_doc("Deal", d.name)
            if has_permission(doc, "read"):
                amount = float(d.amount or 0.0)
                weight = stage_weights.get(d.stage, 0.0)
                total_forecast += amount * weight
                
        return {"status": "success", "forecasted_revenue": total_forecast}
    except Exception as e:
        return handle_api_exception(e)
