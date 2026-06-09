import frappe
from frappe import _
import json
from precision_crm.auth import authenticate_request
from precision_crm.permissions import has_permission
from precision_crm.api.leads import handle_api_exception

@frappe.whitelist(allow_guest=True)
def create_task(**kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        frappe.db.begin()
        doc = frappe.get_doc(dict(doctype="Task", **kwargs))
        doc.insert()
        frappe.db.commit()
        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_task(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Task", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Task not found"}

        doc = frappe.get_doc("Task", name)
        if not has_permission(doc, "read"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        return {"status": "success", "data": doc.as_dict()}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def update_task(name, **kwargs):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Task", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Task not found"}

        doc = frappe.get_doc("Task", name)
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
def delete_task(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Task", name):
            frappe.local.response["http_status_code"] = 404
            return {"status": "error", "message": "Task not found"}

        doc = frappe.get_doc("Task", name)
        if not has_permission(doc, "delete"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        frappe.db.begin()
        doc.delete()
        frappe.db.commit()
        return {"status": "success", "message": "Task deleted successfully"}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def list_tasks(start=0, limit=20, order_by="creation desc", filters=None):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if isinstance(filters, str):
            filters = json.loads(filters)
        if not filters:
            filters = {}

        tasks = frappe.get_all(
            "Task",
            filters=filters,
            order_by=order_by,
            start=start,
            page_length=limit,
            fields=["*"]
        )
        
        allowed_tasks = [t for t in tasks if has_permission(frappe.get_doc("Task", t.name), "read")]
        return {"status": "success", "data": allowed_tasks, "total": len(allowed_tasks)}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def assign_task(name, assignee):
    return update_task(name, assignee=assignee)

@frappe.whitelist(allow_guest=True)
def update_task_status(name, status):
    return update_task(name, status=status)

@frappe.whitelist(allow_guest=True)
def task_reminder(name):
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        if not frappe.db.exists("Task", name):
            return {"status": "error", "message": "Task not found"}
            
        doc = frappe.get_doc("Task", name)
        if not has_permission(doc, "read"):
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Forbidden"}

        # Create high-priority Notification for the assignee
        notification = frappe.get_doc({
            "doctype": "Notification",
            "subject": f"Reminder: Task {doc.task_name} is due",
            "message": f"Task {doc.task_name} (Due: {doc.due_date}) needs your attention.",
            "for_user": doc.assignee or doc.owner
        })
        notification.insert(ignore_permissions=True)
        return {"status": "success", "message": "Reminder notification sent"}
    except Exception as e:
        return handle_api_exception(e)
