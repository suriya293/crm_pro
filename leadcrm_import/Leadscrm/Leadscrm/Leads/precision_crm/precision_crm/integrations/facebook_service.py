import frappe
from frappe import _
import requests
import json

def get_facebook_config():
    token = frappe.db.get_single_value("System Settings", "facebook_page_access_token") or "mock_facebook_access_token"
    return token

def fetch_facebook_lead_details(facebook_lead_id):
    token = get_facebook_config()
    url = f"https://graph.facebook.com/v18.0/{facebook_lead_id}"
    params = {
        "access_token": token,
        "fields": "created_time,id,ad_id,ad_name,campaign_id,campaign_name,form_id,field_data"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        res_json = response.json()
        
        # Log to Webhook Log
        webhook_log = frappe.get_doc({
            "doctype": "Webhook Log",
            "webhook_url": url,
            "payload": json.dumps(params),
            "response": json.dumps(res_json),
            "status": "Success" if response.status_code == 200 else "Failed"
        })
        webhook_log.insert(ignore_permissions=True)
        
        if response.status_code == 200:
            return res_json
        return None
    except Exception as e:
        frappe.log_error(message=str(e), title="Facebook API Fetch Error")
        return None

def process_facebook_lead(lead_details):
    lead_id = lead_details.get("id")
    form_id = lead_details.get("form_id")
    campaign_name = lead_details.get("campaign_name") or "Facebook Campaign"
    field_data = lead_details.get("field_data", [])
    
    # Map fields
    email = None
    mobile_no = None
    lead_name = f"FB Lead {lead_id}"
    
    for field in field_data:
        name = field.get("name")
        values = field.get("values", [])
        val = values[0] if values else None
        if not val:
            continue
            
        if name in ["email", "email_address"]:
            email = val
        elif name in ["phone_number", "phone", "mobile"]:
            mobile_no = val
        elif name in ["full_name", "name"]:
            lead_name = val
            
    # Check for campaign, create if missing
    campaign_id = lead_details.get("campaign_id")
    campaign_name_slug = f"FB-{campaign_id}"
    if not frappe.db.exists("Campaign", campaign_name_slug):
        campaign = frappe.get_doc({
            "doctype": "Campaign",
            "campaign_name": campaign_name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        campaign.insert(ignore_permissions=True)
        # Naming series override logic will handle naming
        
    # Check for existing duplicate lead (email or phone)
    duplicate = False
    if email or mobile_no:
        filters = []
        if email:
            filters.append({"email": email})
        if mobile_no:
            filters.append({"mobile_no": mobile_no})
        
        # Check database
        for f in filters:
            exists = frappe.db.exists("Lead", f)
            if exists:
                duplicate = True
                break
                
    # Create FacebookLead log
    fb_lead = frappe.get_doc({
        "doctype": "Facebook Lead",
        "facebook_lead_id": lead_id,
        "form_name": f"Form {form_id}",
        "lead_info": json.dumps(lead_details),
        "sync_status": "Synced" if not duplicate else "Failed"
    })
    fb_lead.insert(ignore_permissions=True)
    
    if not duplicate:
        # Create Lead record
        new_lead = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": lead_name,
            "email": email,
            "mobile_no": mobile_no or f"FB-{lead_id}",
            "lead_source": "Facebook",
            "status": "New"
        })
        new_lead.insert(ignore_permissions=True)
        return new_lead.name
    return None
