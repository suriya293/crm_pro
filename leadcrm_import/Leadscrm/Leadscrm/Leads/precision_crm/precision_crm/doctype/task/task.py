import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series, create_activity
from precision_crm.permissions import has_permission

class Task(Document):
    def autoname(self):
        apply_naming_series(self, "TASK")

    def before_insert(self):
        set_audit_fields(self)
        if not self.status:
            self.status = "Open"
        if not self.priority:
            self.priority = "Medium"

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        
        self.validate_due_date()
        self.validate_status_transitions()
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Task record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        if self.has_value_changed("status"):
            create_activity(
                activity_type="Task",
                lead=self.related_lead,
                description=f"Task {self.name} status updated to {self.status}",
                performed_by=frappe.session.user
            )

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Task record.")

    def validate_due_date(self):
        if self.due_date and self.is_new():
            today = frappe.utils.today()
            if frappe.utils.getdate(self.due_date) < frappe.utils.getdate(today):
                frappe.throw("Due date cannot be in the past.")

    def validate_status_transitions(self):
        if self.is_new():
            return
        old_status = frappe.db.get_value("Task", self.name, "status")
        valid_transitions = {
            "Open": ["In Progress", "Completed", "Cancelled"],
            "In Progress": ["Completed", "Open", "Cancelled"],
            "Completed": [],
            "Cancelled": []
        }
        if old_status and old_status != self.status:
            allowed = valid_transitions.get(old_status, [])
            if self.status not in allowed:
                frappe.throw(f"Invalid transition from {old_status} to {self.status}.")
