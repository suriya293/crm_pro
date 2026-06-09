import frappe
from frappe.model.document import Document
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class AuditLog(Document):
    def autoname(self):
        apply_naming_series(self, "AUD")

    def before_insert(self):
        set_audit_fields(self)
        if not self.timestamp:
            self.timestamp = frappe.utils.now_datetime()
        if not self.user:
            self.user = frappe.session.user

    def validate(self):
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Audit Log record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Audit Log record.")
