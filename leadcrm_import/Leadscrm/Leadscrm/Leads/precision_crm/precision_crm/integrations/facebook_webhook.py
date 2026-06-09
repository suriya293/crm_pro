import frappe
from frappe import _
import json
from precision_crm.integrations.facebook_service import fetch_facebook_lead_details, process_facebook_lead

@frappe.whitelist(allow_guest=True)
def handle_facebook_webhook():
    request = frappe.local.request
    
    # Verification GET Request
    if request.method == "GET":
        params = frappe.local.request.args
        hub_mode = params.get("hub.mode")
        hub_verify_token = params.get("hub.verify_token")
        hub_challenge = params.get("hub.challenge")
        
        expected_token = frappe.db.get_single_value("System Settings", "facebook_verify_token") or "precision_fb_token"
        
        if hub_mode == "subscribe" and hub_verify_token == expected_token:
            frappe.local.response["type"] = "binary"
            frappe.local.response["filename"] = "challenge"
            frappe.local.response["filecontent"] = str(hub_challenge).encode("utf-8")
            return
        else:
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Verification token mismatch"}

    # Ingestion POST Request
    elif request.method == "POST":
        payload_data = frappe.request.get_data()
        if not payload_data:
            return {"status": "success", "message": "No payload"}
            
        try:
            payload = json.loads(payload_data.decode("utf-8"))
        except Exception:
            payload = {}
            
        # Log to Webhook Log
        webhook_log = frappe.get_doc({
            "doctype": "Webhook Log",
            "webhook_url": "/api/method/precision_crm.precision_crm.integrations.facebook_webhook.handle_facebook_webhook",
            "payload": json.dumps(payload),
            "status": "Success"
        })
        webhook_log.insert(ignore_permissions=True)
        
        # Extract lead ad changes
        entry = payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        
        leadgen_id = value.get("leadgen_id")
        
        if leadgen_id:
            # Fetch full lead payload details
            lead_details = fetch_facebook_lead_details(leadgen_id)
            if lead_details:
                # Ingest Lead Ads details
                process_facebook_lead(lead_details)
                
        return {"status": "success"}
