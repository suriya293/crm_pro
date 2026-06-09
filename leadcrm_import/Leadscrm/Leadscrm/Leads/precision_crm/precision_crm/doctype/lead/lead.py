import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_email, validate_email_uniqueness, validate_mobile_uniqueness
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class Lead(Document):
    def autoname(self):
        apply_naming_series(self, "LEAD")

    def before_insert(self):
        set_audit_fields(self)

    def validate(self):
        validate_email(self.email)
        validate_email_uniqueness("Lead", self.email, self.name)
        validate_mobile_uniqueness("Lead", self.mobile_no, self.name)
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Lead record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Lead record.")
