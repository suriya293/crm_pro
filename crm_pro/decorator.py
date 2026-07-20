import frappe
from frappe import _

from functools import wraps

def require_permission(permission_name, *args, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if permission_name == 'Authenticated':
                if frappe.session.user == 'Guest':
                    if hasattr(frappe.local, "response"):
                        frappe.local.response["http_status_code"] = 401
                    frappe.throw(_("Authentication required"), frappe.PermissionError)
            return func(*args, **kwargs)
        return wrapper
    return decorator
