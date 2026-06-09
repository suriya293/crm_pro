import frappe
from frappe.model.document import Document
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class Notification(Document):
    def autoname(self):
        apply_naming_series(self, "NOTIF")

    def before_insert(self):
        set_audit_fields(self)
        if self.is_read is None:
            self.is_read = 0

    def validate(self):
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Notification record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Notification record.")
