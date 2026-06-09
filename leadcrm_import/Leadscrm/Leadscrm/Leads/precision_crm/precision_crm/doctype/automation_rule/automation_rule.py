import frappe
from frappe.model.document import Document
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class AutomationRule(Document):
    def autoname(self):
        apply_naming_series(self, "AUTO")

    def before_insert(self):
        set_audit_fields(self)
        if self.is_active is None:
            self.is_active = 1

    def validate(self):
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Automation Rule record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Automation Rule record.")
