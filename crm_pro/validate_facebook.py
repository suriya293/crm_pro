import logging
from ratelimit import limits as ratelimit
import frappe
from crm_pro.meta import verify_meta_signature
from crm_pro.jobs import fetch_and_create_facebook_lead
import hmac
import hashlib

def run():
    print("=== STARTING FACEBOOK WEBHOOK VALIDATION CHECK ===")
    
    # 1. Verify GET Challenge simulation
    verify_token = frappe.db.get_single_value("CRM Settings", "facebook_webhook_verify_token")
    if not verify_token:
        # Set dummy token for test
        frappe.db.set_single_value("CRM Settings", "facebook_webhook_verify_token", "mock_verify_token")
        verify_token = "mock_verify_token"
        
    print(f"Verified webhook verify token: {verify_token}")

    # 2. Verify POST webhook signature parsing
    # Set app secret
    frappe.db.set_single_value("CRM Settings", "facebook_app_secret", "secret_key")
    frappe.clear_cache(doctype="CRM Settings")
    
    class MockRequest:
        def __init__(self, headers, data):
            self.headers = headers
            self.data = data
            
    payload = b'{"entry": [{"changes": [{"value": {"leadgen_id": "lead_12345"}}]}]}'
    
    # Generate correct signature
    mac = hmac.new(b"secret_key", msg=payload, digestmod=hashlib.sha256)
    signature = f"sha256={mac.hexdigest()}"
    
    mock_req = MockRequest({"X-Hub-Signature-256": signature}, payload)
    sig_check = verify_meta_signature(mock_req)
    
    print(f"Signature Check passed: {sig_check}")
    assert sig_check == True, "Webhook signature validation failed."

    # 3. Verify Lead Ingestion Flow
    # Clear existing fb test leads
    frappe.db.delete("CRM Lead", {"source": "Facebook Ads"})
    frappe.db.commit()
    
    print("Simulating lead ingestion for leadgen_id: lead_12345")
    fetch_and_create_facebook_lead("lead_12345")
    
    # Verify lead created
    lead_name = frappe.db.get_value("CRM Lead", {"source": "Facebook Ads", "lead_name": "Facebook Lead lead_12345"}, "name")
    if lead_name:
        print(f"Success! Lead created: {lead_name}")
    else:
        raise Exception("Lead creation failed.")
        
    # Clean up settings
    frappe.db.set_single_value("CRM Settings", "facebook_app_secret", "")
    frappe.db.set_single_value("CRM Settings", "facebook_webhook_verify_token", "")
    frappe.db.commit()
    
    print("=== FACEBOOK WEBHOOK VALIDATION SUCCESSFUL ===")
