import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class Activity(Document):
    def autoname(self):
        apply_naming_series(self, "ACT")

    def before_insert(self):
        set_audit_fields(self)
        if not self.timestamp:
            self.timestamp = frappe.utils.now_datetime()

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        self.validate_linked_document()
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Activity record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        pass

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Activity record.")

    def validate_linked_document(self):
        if self.lead:
            if not frappe.db.exists("Lead", self.lead):
                frappe.throw(f"Linked Lead {self.lead} does not exist.")

    @staticmethod
    def get_timeline(lead_id):
        return frappe.get_all(
            "Activity",
            filters={"lead": lead_id},
            fields=["name", "activity_type", "description", "timestamp", "performed_by"],
            order_by="timestamp desc"
        )
