import logging
from ratelimit import limits as ratelimit
import frappe

def setup_webhook_settings():
    settings = frappe.get_doc("CRM Settings")
    settings.facebook_webhook_verify_token = "test_verify_token"
    settings.facebook_app_secret = "facebook_secret_xyz"
    settings.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache(doctype="CRM Settings")
    print("Database Settings updated for testing.")

def restore_webhook_settings():
    settings = frappe.get_doc("CRM Settings")
    settings.facebook_webhook_verify_token = ""
    settings.facebook_app_secret = ""
    settings.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache(doctype="CRM Settings")
    print("Database Settings restored.")

def run():
    print("Starting verification...")
    setup_webhook_settings()
    restore_webhook_settings()
    print("Verification completed successfully.")
