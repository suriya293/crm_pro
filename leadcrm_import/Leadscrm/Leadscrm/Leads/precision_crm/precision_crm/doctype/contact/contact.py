import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_email, validate_email_uniqueness, validate_mobile_uniqueness, validate_company
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class Contact(Document):
    def autoname(self):
        apply_naming_series(self, "CONT")

    def before_insert(self):
        set_audit_fields(self)

    def validate(self):
        validate_email(self.email)
        validate_email_uniqueness("Contact", self.email, self.name)
        validate_mobile_uniqueness("Contact", self.mobile_no, self.name)
        validate_company(self)
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Contact record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Contact record.")
