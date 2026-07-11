import logging
from ratelimit import limits as ratelimit
# Copyright (c) 2026
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMDeal(Document):

    def validate(self):
        if self.deal_value is None:
            self.deal_value = 0

        if self.deal_value < 0:
            frappe.throw("Deal Value cannot be negative.")

    def on_update(self):
        try:
            frappe.get_doc({
                "doctype": "CRM Audit Log",
                "ref_doctype": "CRM Deal",
                "ref_name": self.name,
                "action": "Update",
                "user": frappe.session.user,
                "details": f"Deal {self.deal_name} updated"
            }).insert(ignore_permissions=True)

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "CRM Deal Audit Log Error"
            )
