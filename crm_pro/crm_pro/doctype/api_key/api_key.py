import logging
from ratelimit import limits as ratelimit
import frappe
from frappe.model.document import Document

class APIKey(Document):
    pass
