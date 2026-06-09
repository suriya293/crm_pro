# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import now_datetime
import requests
import json

@frappe.whitelist(allow_guest=True)
def whatsapp_webhook():
    """
    Webhook handler for Meta WhatsApp Cloud API.
    Supports GET verification challenge and POST messages payloads.
    """
    request = frappe.request

    if request.method == "GET":
        # Verification
        params = frappe.form_dict
        verify_token = frappe.db.get_single_value("CRM Settings", "facebook_webhook_verify_token")
        
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            # Frappe returns plain text challenge
            frappe.response["type"] = "text"
            frappe.response["result"] = challenge
            return
        else:
            frappe.throw(_("Invalid verification token"), frappe.PermissionError)

    elif request.method == "POST":
        # Process webhook payload
        payload = json.loads(request.data.decode("utf-8"))
        
        try:
            entry = payload.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if messages:
                msg = messages[0]
                from_number = msg.get("from") # e.g. "15550268680"
                text_body = msg.get("text", {}).get("body", "")
                
                # Match lead by mobile number (either mobile, alt_mobile_1, 2, or 3)
                lead_name = frappe.db.get_value("CRM Lead", {
                    "mobile": ["like", f"%{from_number}%"]
                }, "name")
                
                if not lead_name:
                    # check alt mobile
                    lead_name = frappe.db.get_value("CRM Lead", {
                        "alt_mobile_1": ["like", f"%{from_number}%"]
                    }, "name")

                if lead_name:
                    # 1. Log WhatsApp entry
                    log_doc = frappe.get_doc({
                        "doctype": "CRM WhatsApp Log",
                        "lead": lead_name,
                        "phone_number": from_number,
                        "message": text_body,
                        "direction": "Inbound"
                    }).insert(ignore_permissions=True)
                    
                    # 2. Log Activity
                    frappe.get_doc({
                        "doctype": "CRM Activity",
                        "activity_type": "WhatsApp",
                        "lead": lead_name,
                        "notes": f"Inbound WhatsApp message: {text_body}",
                        "activity_date": now_datetime()
                    }).insert(ignore_permissions=True)
                    
                    frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Error parsing WhatsApp Webhook: {str(e)}", "WhatsApp Webhook Error")
            
        frappe.response["status"] = "success"
        return

@frappe.whitelist(allow_guest=True)
def facebook_webhook():
    """
    Webhook handler for Facebook Lead Ads.
    Supports GET verification challenge and POST lead gen updates.
    """
    request = frappe.request

    if request.method == "GET":
        # Verification
        params = frappe.form_dict
        verify_token = frappe.db.get_single_value("CRM Settings", "facebook_webhook_verify_token")
        
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            frappe.response["type"] = "text"
            frappe.response["result"] = challenge
            return
        else:
            frappe.throw(_("Invalid verification token"), frappe.PermissionError)

    elif request.method == "POST":
        payload = json.loads(request.data.decode("utf-8"))
        try:
            entry = payload.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            leadgen_id = value.get("leadgen_id")
            
            if leadgen_id:
                # Enqueue background job to fetch leadgen info from Meta Graph API
                frappe.enqueue(
                    "crm_pro.crm_pro.jobs.fetch_and_create_facebook_lead",
                    queue="default",
                    leadgen_id=leadgen_id
                )
        except Exception as e:
            frappe.log_error(f"Error parsing Facebook Webhook: {str(e)}", "Facebook Webhook Error")
            
        frappe.response["status"] = "success"
        return

@frappe.whitelist()
def send_whatsapp_message(lead_id, message):
    """
    Sends outbound WhatsApp message using Meta Cloud API.
    """
    if not lead_id or not message:
        frappe.throw(_("Lead ID and message text are required"))
        
    doc_name = lead_id
    if not frappe.db.exists("CRM Lead", doc_name):
        found = frappe.db.get_value("CRM Lead", {"lead_name": lead_id}, "name")
        if found:
            doc_name = found

    lead = frappe.get_doc("CRM Lead", doc_name)
    if not lead.mobile or lead.mobile == "-":
        frappe.throw(_("Lead does not have a valid mobile number"))
        
    # Get settings
    settings = frappe.get_doc("CRM Settings")
    if not settings.enable_whatsapp_integration:
        frappe.throw(_("WhatsApp integration is disabled in CRM Settings"))
        
    token = settings.whatsapp_access_token
    phone_id = settings.whatsapp_phone_number_id
    
    if not token or not phone_id:
        frappe.throw(_("WhatsApp API Token or Phone Number ID is missing in Settings"))

    # Meta request payload
    url = f"https://graph.facebook.com/v16.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": lead.mobile.replace("+", ""),
        "type": "text",
        "text": {"body": message}
    }
    
    # In sandbox or local test, we mock requests
    if token == "mock_token":
        response_data = {"messages": [{"id": "mock_msg_123"}]}
    else:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            response_data = response.json()
        except Exception as e:
            frappe.throw(_(f"Meta API Request Failed: {str(e)}"))
            
    # Log outbound WhatsApp message
    frappe.get_doc({
        "doctype": "CRM WhatsApp Log",
        "lead": doc_name,
        "phone_number": lead.mobile,
        "message": message,
        "direction": "Outbound"
    }).insert(ignore_permissions=True)
    
    # Log Activity
    frappe.get_doc({
        "doctype": "CRM Activity",
        "activity_type": "WhatsApp",
        "lead": doc_name,
        "notes": f"Outbound WhatsApp message: {message}",
        "activity_date": now_datetime()
    }).insert(ignore_permissions=True)
    
    frappe.db.commit()
    return response_data
