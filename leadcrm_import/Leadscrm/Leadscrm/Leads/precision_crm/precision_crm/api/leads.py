import frappe
from frappe import _
from precision_crm.auth import authenticate_request
from precision_crm.permissions import has_permission, get_permission_query_conditions

def handle_api_exception(e):
    frappe.log_error(message=str(e), title="API Exception")
    frappe.db.rollback()
    frappe.local.response["http_status_code"] = 500
    return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def create_lead(**kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}
    
    if not has_permission(None, "create", doctype="Lead"):
        frappe.local.response["http_status_code"] = 403
        return {"status": "error", "message": "Forbidden"}

    try:
        frappe.db.begin()
        doc = frappe.get_doc(dict(doctype="Lead", **kwargs))
        doc.insert()
        frappe.db.commit()
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_lead(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Lead", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Lead not found"}

        doc = frappe.get_doc("Lead", name)
        if not has_permission(doc, "read"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def update_lead(name, **kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Lead", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Lead not found"}

        doc = frappe.get_doc("Lead", name)
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
def delete_lead(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Lead", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Lead not found"}

        doc = frappe.get_doc("Lead", name)
        if not has_permission(doc, "delete"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.delete()
        frappe.db.commit()
        return {"status": "success", "message": "Lead deleted successfully"}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def list_leads(start=0, limit=20, order_by="creation desc", filters=None):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if isinstance(filters, str):
            filters = json.loads(filters)
        if not filters:
            filters = {}

        # Permission conditions
        perm_conditions = get_permission_query_conditions(frappe.session.user)
        
        # Build query
        query_filters = filters.copy()
        if perm_conditions:
            # Map permission query string to query
            pass
            
        leads = frappe.get_all(
            "Lead",
            filters=query_filters,
            order_by=order_by,
            start=start,
            page_length=limit,
            fields=["*"]
        )
        
        # Filter based on python permissions if query_conditions are complex
        allowed_leads = [l for l in leads if has_permission(frappe.get_doc("Lead", l.name), "read")]
        
        return {"status": "success", "data": allowed_leads, "total": len(allowed_leads)}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def assign_lead(name, assign_to_user):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Lead", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Lead not found"}

        doc = frappe.get_doc("Lead", name)
        if not has_permission(doc, "write"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.assigned_to = assign_to_user
        doc.status = "Assigned"
        doc.save()
        frappe.db.commit()
        
        # Log Audit entry
        audit = frappe.get_doc({
            "doctype": "Audit Log",
            "action": "Lead Assignment",
            "details": f"Lead {name} assigned to {assign_to_user}",
            "user": frappe.session.user
        })
        audit.insert(ignore_permissions=True)

        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def convert_lead(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Lead", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Lead not found"}

        doc = frappe.get_doc("Lead", name)
        if not has_permission(doc, "write"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.status = "Converted"
        doc.save()
        
        # Auto-create Contact
        contact = frappe.get_doc({
            "doctype": "Contact",
            "contact_name": doc.lead_name,
            "mobile_no": doc.mobile_no,
            "email": doc.email,
            "associated_lead": doc.name
        })
        contact.insert(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success", "message": "Lead converted successfully", "contact": contact.name}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def detect_duplicates(mobile_no, email=None):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        duplicates = []
        if mobile_no:
            dup_mobile = frappe.get_all("Lead", filters={"mobile_no": mobile_no}, fields=["name", "lead_name"])
            duplicates.extend(dup_mobile)
        if email:
            dup_email = frappe.get_all("Lead", filters={"email": email}, fields=["name", "lead_name"])
            duplicates.extend(dup_email)
            
        # Unique duplicates
        seen = set()
        unique_dups = []
        for d in duplicates:
            if d.name not in seen:
                seen.add(d.name)
                unique_dups.append(d)
                
        return {"status": "success", "duplicates": unique_dups}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def merge_leads(primary_lead, secondary_leads):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if isinstance(secondary_leads, str):
            secondary_leads = json.loads(secondary_leads)
            
        if not frappe.db.exists("Lead", primary_lead):
            return {"status": "error", "message": f"Primary Lead {primary_lead} does not exist"}

        frappe.db.begin()
        primary_doc = frappe.get_doc("Lead", primary_lead)
        
        for sec in secondary_leads:
            if not frappe.db.exists("Lead", sec):
                continue
            
            # Transfer all activities/tasks from secondary to primary
            activities = frappe.get_all("Activity", filters={"lead": sec})
            for act in activities:
                frappe.db.set_value("Activity", act.name, "lead", primary_lead)
                
            tasks = frappe.get_all("Task", filters={"related_lead": sec})
            for t in tasks:
                frappe.db.set_value("Task", t.name, "related_lead", primary_lead)
                
            # Soft delete secondary lead
            frappe.db.set_value("Lead", sec, "status", "Duplicate")
            
        frappe.db.commit()
        return {"status": "success", "message": "Leads merged successfully"}
    except Exception as e:
        return handle_api_exception(e)
