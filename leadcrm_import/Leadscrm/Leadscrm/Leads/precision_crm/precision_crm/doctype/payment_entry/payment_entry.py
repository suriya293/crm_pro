import frappe
from frappe.model.document import Document
from precision_crm.validators import validate_company, validate_territory, validate_team
from precision_crm.utils import set_audit_fields, apply_naming_series
from precision_crm.permissions import has_permission

class PaymentEntry(Document):
    def autoname(self):
        apply_naming_series(self, "PAY")

    def before_insert(self):
        set_audit_fields(self)
        if not self.status:
            self.status = "Draft"
        if not self.payment_date:
            self.payment_date = frappe.utils.today()

    def validate(self):
        validate_company(self)
        validate_territory(self)
        validate_team(self)
        
        if self.amount and float(self.amount) <= 0:
            frappe.throw("Amount must be greater than 0.")
            
        if not has_permission(self, "write"):
            frappe.throw("You do not have permission to write to this Payment Entry record.")

    def before_save(self):
        set_audit_fields(self)

    def on_update(self):
        self.update_invoice_status()

    def on_trash(self):
        if not has_permission(self, "delete"):
            frappe.throw("You do not have permission to delete this Payment Entry record.")

    def update_invoice_status(self):
        if self.status == "Confirmed" and self.invoice:
            frappe.db.set_value("Invoice", self.invoice, "status", "Paid")
