import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series, create_activity
from precision_crm.permissions import has_permission

class Deal(Document):
    def autoname(self):
        apply_naming_series(self, "DEAL")

    def before_insert(self):
        set_audit_fields(self)
        if not self.stage:
            self.stage = "Prospect"

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        
        if self.amount and float(self.amount) <= 0:
            frappe.throw("Deal value (amount) must be greater than 0.")
            
        self.validate_stage_transitions()
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Deal record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        self.update_pipeline_metrics()
        
        if self.has_value_changed("stage"):
            # Log activity on Opportunity/Lead if possible
            opp = self.opportunity
            lead = frappe.db.get_value("Opportunity", opp, "lead") if opp else None
            create_activity(
                activity_type="Note",
                lead=lead,
                description=f"Deal {self.name} stage updated to {self.stage}",
                performed_by=frappe.session.user
            )

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Deal record.")

    def validate_stage_transitions(self):
        if self.is_new():
            return
        
        old_stage = frappe.db.get_value("Deal", self.name, "stage")
        valid_transitions = {
            "Prospect": ["Negotiation", "Won", "Lost"],
            "Negotiation": ["Won", "Lost"],
            "Won": [],
            "Lost": []
        }
        
        if old_stage and old_stage != self.stage:
            allowed = valid_transitions.get(old_stage, [])
            if self.stage not in allowed:
                frappe.throw(f"Invalid transition from {old_stage} to {self.stage}.")

    def update_pipeline_metrics(self):
        # Update associated Opportunity and Lead status
        if self.stage == "Won" and self.opportunity:
            frappe.db.set_value("Opportunity", self.opportunity, "status", "Won")
            lead = frappe.db.get_value("Opportunity", self.opportunity, "lead")
            if lead:
                frappe.db.set_value("Lead", lead, "status", "Converted")
        elif self.stage == "Lost" and self.opportunity:
            frappe.db.set_value("Opportunity", self.opportunity, "status", "Lost")
