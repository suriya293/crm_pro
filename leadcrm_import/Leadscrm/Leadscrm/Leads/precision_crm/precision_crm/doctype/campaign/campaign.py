import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class Campaign(Document):
    def autoname(self):
        apply_naming_series(self, "CAMP")

    def before_insert(self):
        set_audit_fields(self)
        if not self.status:
            self.status = "Draft"

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        self.validate_dates()
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Campaign record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Campaign record.")

    def validate_dates(self):
        if self.start_date and self.end_date:
            if frappe.utils.getdate(self.end_date) < frappe.utils.getdate(self.start_date):
                frappe.throw("End date cannot be before start date.")
