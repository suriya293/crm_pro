import frappe
from frappe import _
import requests
import json

def get_whatsapp_config():
    # Retrieve configuration from Frappe Settings
    token = frappe.db.get_single_value("System Settings", "whatsapp_access_token") or "mock_whatsapp_access_token"
    phone_id = frappe.db.get_single_value("System Settings", "whatsapp_phone_number_id") or "mock_phone_number_id"
    return token, phone_id

def send_whatsapp_message(to_number, text_content=None, template_name=None, template_language="en", components=None):
    token, phone_id = get_whatsapp_config()
    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number
    }
    
    if template_name:
        payload["type"] = "template"
        payload["template"] = {
            "name": template_name,
            "language": {"code": template_language}
        }
        if components:
            payload["template"]["components"] = components
    else:
        payload["type"] = "text"
        payload["text"] = {"body": text_content}
        
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        res_json = response.json()
        
        # Log to Webhook Log
        webhook_log = frappe.get_doc({
            "doctype": "Webhook Log",
            "webhook_url": url,
            "payload": json.dumps(payload),
            "response": json.dumps(res_json),
            "status": "Success" if response.status_code == 200 else "Failed"
        })
        webhook_log.insert(ignore_permissions=True)
        
        if response.status_code == 200:
            # Sync Message locally
            message_id = res_json.get("messages", [{}])[0].get("id")
            sync_local_message(to_number, text_content or f"Template: {template_name}", "Outbound", message_id)
            return {"status": "success", "message_id": message_id}
        else:
            return {"status": "error", "message": res_json.get("error", {}).get("message")}
    except Exception as e:
        frappe.log_error(message=str(e), title="WhatsApp API Error")
        return {"status": "error", "message": str(e)}

def sync_local_message(phone_number, content, direction, message_id, message_type="Text"):
    # Find or Create Conversation
    conversation_name = frappe.db.get_value("WhatsApp Conversation", {"phone_number": phone_number}, "name")
    if not conversation_name:
        # Check if Lead exists for this phone_number
        lead = frappe.db.get_value("Lead", {"mobile_no": phone_number}, "name")
        conv = frappe.get_doc({
            "doctype": "WhatsApp Conversation",
            "phone_number": phone_number,
            "lead": lead,
            "status": "Open"
        })
        conv.insert(ignore_permissions=True)
        conversation_name = conv.name
        
    # Create Message
    msg = frappe.get_doc({
        "doctype": "WhatsApp Message",
        "conversation": conversation_name,
        "direction": direction,
        "message_type": message_type,
        "content": content,
        "message_id": message_id,
        "timestamp": frappe.utils.now_datetime()
    })
    msg.insert(ignore_permissions=True)
    return msg
