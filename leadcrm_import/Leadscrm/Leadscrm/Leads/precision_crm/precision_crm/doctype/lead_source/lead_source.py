import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class LeadSource(Document):
    def autoname(self):
        apply_naming_series(self, "SRC")

    def before_insert(self):
        set_audit_fields(self)

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Lead Source record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Lead Source record.")
