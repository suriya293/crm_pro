import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class Product(Document):
    def autoname(self):
        apply_naming_series(self, "PROD")

    def before_insert(self):
        set_audit_fields(self)
        if self.is_active is None:
            self.is_active = 1

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Product record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Product record.")
