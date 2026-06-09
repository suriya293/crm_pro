import frappe
from precision_crm.automation import detect_stale_leads, trigger_reminders

def all():
    pass

def daily():
    # Trigger CRM reminders once a day
    trigger_reminders()

def hourly():
    # Detect stale leads hourly
    detect_stale_leads()

def five_minute():
    pass
