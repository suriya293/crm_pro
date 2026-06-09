# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CRMLead(Document):
    def validate(self):
        # Name Validation (at least 3 characters)
        if len(self.lead_name or "") < 3:
            frappe.throw("Lead Name must be at least 3 characters long.")
        
        # Format mobile & email fields
        if self.mobile:
            self.mobile = self.mobile.strip()
        if self.email:
            self.email = self.email.strip().lower()

        # Enforce unique active mobile check
        if self.mobile and self.mobile != "-":
            duplicates = frappe.db.get_all("CRM Lead", 
                filters={"mobile": self.mobile, "name": ["!=", self.name]},
                fields=["name", "lead_name"]
            )
            if duplicates:
                frappe.throw(f"A lead with this mobile number already exists: {duplicates[0].lead_name}")

        # Enforce unique active email check
        if self.email and self.email != "-":
            duplicates = frappe.db.get_all("CRM Lead",
                filters={"email": self.email, "name": ["!=", self.name]},
                fields=["name", "lead_name"]
            )
            if duplicates:
                frappe.throw(f"A lead with this email address already exists: {duplicates[0].lead_name}")

    def on_update(self):
        # Insert audit log on save
        frappe.get_doc({
            "doctype": "CRM Audit Log",
            "ref_doctype": "CRM Lead",
            "ref_name": self.name,
            "action": "Update",
            "user": frappe.session.user,
            "details": f"Lead {self.lead_name} updated status to {self.stage}"
        }).insert(ignore_permissions=True)
