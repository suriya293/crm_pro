import re
import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address


class CRMLead(Document):
    def validate(self):
        if not self.lead_name or len(self.lead_name.strip()) < 3:
            frappe.throw("Lead Name must be at least 3 characters long.")

        if not self.mobile:
            frappe.throw("Mobile Number is required")

        from crm_pro.utils.mobile_validator import validate_mobile
        validate_mobile(self.mobile)

        for field in ["alt_mobile_1", "alt_mobile_2", "alt_mobile_3"]:
            val = self.get(field)
            if val:
                validate_mobile(val)
        if self.email:
            self.email = self.email.strip().lower()

            if not validate_email_address(self.email, throw=False):
                frappe.throw("Invalid Email Address")

        if self.mobile:
            duplicates = frappe.db.get_all(
                "CRM Lead",
                filters={"mobile": self.mobile, "name": ["!=", self.name]},
                fields=["name", "lead_name"],
                limit=1
            )

            if duplicates:
                frappe.throw(
                    f"A lead with this mobile number already exists: {duplicates[0].lead_name}"
                )

        if self.email:
            duplicates = frappe.db.get_all(
                "CRM Lead",
                filters={"email": self.email, "name": ["!=", self.name]},
                fields=["name", "lead_name"],
                limit=1
            )

            if duplicates:
                frappe.throw(
                    f"A lead with this email address already exists: {duplicates[0].lead_name}"
                )

    def on_update(self):

        current_user = frappe.session.user or "Administrator"

        try:
            frappe.get_doc({
                "doctype": "CRM Audit Log",
                "ref_doctype": "CRM Lead",
                "ref_name": self.name,
                "action": "Update",
                "user": current_user,
                "details": f"Lead {self.lead_name} updated status to {self.stage}"
            }).insert(ignore_permissions=True)

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "CRM Lead Audit Log Failure"
            )
