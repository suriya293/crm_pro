import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series, create_activity
from precision_crm.permissions import has_permission

class Opportunity(Document):
    def autoname(self):
        apply_naming_series(self, "OPP")

    def before_insert(self):
        set_audit_fields(self)
        if not self.status:
            self.status = "Open"
        if not self.probability:
            self.probability = 0

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        
        if self.value and float(self.value) <= 0:
            frappe.throw("Expected value (value) must be greater than 0.")
            
        self.validate_stage_transitions()
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Opportunity record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        # Create activity record on change
        if self.has_value_changed("status"):
            create_activity(
                activity_type="Note",
                lead=self.lead,
                description=f"Opportunity {self.name} status updated to {self.status}",
                performed_by=frappe.session.user
            )

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Opportunity record.")

    def validate_stage_transitions(self):
        if self.is_new():
            return
        
        old_status = frappe.db.get_value("Opportunity", self.name, "status")
        valid_transitions = {
            "Open": ["Discovery", "Qualification", "On Hold", "Lost"],
            "Discovery": ["Qualification", "Proposal Sent", "On Hold", "Lost"],
            "Qualification": ["Proposal Sent", "Negotiation", "On Hold", "Lost"],
            "Proposal Sent": ["Negotiation", "Won", "Lost", "On Hold"],
            "Negotiation": ["Won", "Lost", "On Hold"],
            "On Hold": ["Open", "Discovery", "Qualification", "Proposal Sent", "Negotiation", "Lost"],
            "Won": [],
            "Lost": []
        }
        
        if old_status and old_status != self.status:
            allowed = valid_transitions.get(old_status, [])
            if self.status not in allowed:
                frappe.throw(f"Invalid transition from {old_status} to {self.status}.")
                
            # If changed to Won, check if we should auto-create Activity or log it
            if self.status == "Won":
                create_activity(
                    activity_type="Note",
                    lead=self.lead,
                    description=f"Opportunity {self.name} won!",
                    performed_by=frappe.session.user
                )
