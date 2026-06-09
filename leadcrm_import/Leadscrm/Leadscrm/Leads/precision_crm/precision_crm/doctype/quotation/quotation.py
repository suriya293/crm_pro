import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class Quotation(Document):
    def autoname(self):
        apply_naming_series(self, "QUO")

    def before_insert(self):
        set_audit_fields(self)
        if not self.status:
            self.status = "Draft"

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        self.validate_valid_till()
        
        if self.total_amount and float(self.total_amount) < 0:
            frappe.throw("Total Amount cannot be negative.")
            
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Quotation record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Quotation record.")

    def validate_valid_till(self):
        if self.valid_till and self.is_new():
            today = frappe.utils.today()
            if frappe.utils.getdate(self.valid_till) < frappe.utils.getdate(today):
                frappe.throw("Valid Till date cannot be in the past.")
