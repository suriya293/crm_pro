import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series, create_activity
from precision_crm.permissions import has_permission

class FollowUp(Document):
    def autoname(self):
        apply_naming_series(self, "FUP")

    def before_insert(self):
        set_audit_fields(self)
        if not self.outcome:
            self.outcome = "Pending"

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        
        self.validate_followup_date()
        
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this FollowUp record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        if self.is_new() or self.has_value_changed("outcome"):
            create_activity(
                activity_type="Meeting",
                lead=self.lead,
                description=f"FollowUp scheduled for {self.follow_up_date}. Outcome: {self.outcome}",
                performed_by=frappe.session.user
            )
            self.create_reminder()

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this FollowUp record.")

    def validate_followup_date(self):
        if self.follow_up_date:
            today = frappe.utils.today()
            if frappe.utils.getdate(self.follow_up_date) < frappe.utils.getdate(today):
                frappe.throw("Follow-up date must be in the future.")

    def create_reminder(self):
        # Auto-create a task to serve as a reminder
        if self.outcome == "Pending" and self.lead:
            task_name = f"Follow up reminder for Lead {self.lead}"
            if not frappe.db.exists("Task", {"task_name": task_name, "status": "Open"}):
                task = frappe.get_doc({
                    "doctype": "Task",
                    "task_name": task_name,
                    "related_lead": self.lead,
                    "assignee": self.assigned_to or frappe.session.user or "Administrator",
                    "due_date": self.follow_up_date,
                    "status": "Open",
                    "priority": "High"
                })
                task.insert(ignore_permissions=True)
