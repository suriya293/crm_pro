import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class Invoice(Document):
    def autoname(self):
        apply_naming_series(self, "INV")

    def before_insert(self):
        set_audit_fields(self)
        if not self.status:
            self.status = "Draft"

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        
        if self.grand_total and float(self.grand_total) < 0:
            frappe.throw("Grand Total cannot be negative.")
            
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Invoice record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Invoice record.")
