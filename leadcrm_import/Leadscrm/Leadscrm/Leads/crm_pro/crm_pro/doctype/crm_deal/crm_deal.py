# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CRMDeal(Document):
    def validate(self):
        if self.deal_value < 0:
            frappe.throw("Deal Value cannot be negative.")

    def on_update(self):
        # Insert audit log on save
        frappe.get_doc({
            "doctype": "CRM Audit Log",
            "ref_doctype": "CRM Deal",
            "ref_name": self.name,
            "action": "Update",
            "user": frappe.session.user,
            "details": f"Deal {self.deal_name} updated status to {self.deal_status} and stage to {self.deal_stage}"
        }).insert(ignore_permissions=True)
