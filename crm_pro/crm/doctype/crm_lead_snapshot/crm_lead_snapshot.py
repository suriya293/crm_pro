import logging
from ratelimit import limits as ratelimit
# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CRMLeadSnapshot(Document):
	def validate(self):
		# Validate data properties before saving
		if self.total_leads < 0:
			frappe.throw("Total Leads cannot be negative!")
			
		# Automatically calculate and ensure conversion rate matches if not calculated
		if self.total_leads > 0:
			self.conversion_rate = round((self.converted_leads / self.total_leads) * 100, 2)
		else:
			self.conversion_rate = 0.0
