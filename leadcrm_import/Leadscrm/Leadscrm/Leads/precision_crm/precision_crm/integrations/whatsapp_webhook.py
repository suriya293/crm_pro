import frappe
from frappe import _
import json
from precision_crm.integrations.whatsapp_service import sync_local_message
from precision_crm.utils import create_activity

@frappe.whitelist(allow_guest=True)
def handle_whatsapp_webhook():
    request = frappe.local.request
    
    # Verification flow (GET)
    if request.method == "GET":
        params = frappe.local.request.args
        hub_mode = params.get("hub.mode")
        hub_verify_token = params.get("hub.verify_token")
        hub_challenge = params.get("hub.challenge")
        
        expected_token = frappe.db.get_single_value("System Settings", "whatsapp_verify_token") or "precision_verify_token"
        
        if hub_mode == "subscribe" and hub_verify_token == expected_token:
            # Return challenge as raw text response
            frappe.local.response["type"] = "binary"
            frappe.local.response["filename"] = "challenge"
            frappe.local.response["filecontent"] = str(hub_challenge).encode("utf-8")
            return
        else:
            frappe.local.response["http_status_code"] = 403
            return {"status": "error", "message": "Verification token mismatch"}

    # Ingestion flow (POST)
    elif request.method == "POST":
        payload_data = frappe.request.get_data()
        if not payload_data:
            return {"status": "success", "message": "No payload"}
            
        try:
            payload = json.loads(payload_data.decode("utf-8"))
        except Exception:
            payload = {}
            
        # Log payload in Webhook Log
        webhook_log = frappe.get_doc({
            "doctype": "Webhook Log",
            "webhook_url": "/api/method/precision_crm.precision_crm.integrations.whatsapp_webhook.handle_whatsapp_webhook",
            "payload": json.dumps(payload),
            "status": "Success"
        })
        webhook_log.insert(ignore_permissions=True)
        
        # Parse message payload
        entry = payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        
        messages = value.get("messages", [])
        statuses = value.get("statuses", [])
        
        # Sync inbound messages
        for msg in messages:
            from_number = msg.get("from")
            msg_id = msg.get("id")
            msg_type = msg.get("type", "text").capitalize()
            
            content = ""
            if msg_type.lower() == "text":
                content = msg.get("text", {}).get("body", "")
            elif msg_type.lower() == "image":
                content = "[Image Message]"
            elif msg_type.lower() == "document":
                content = "[Document Message]"
            else:
                content = f"[{msg_type} Message]"
                
            # Sync local record
            local_msg = sync_local_message(from_number, content, "Inbound", msg_id, msg_type)
            
            # Check/create Lead if missing
            lead_name = frappe.db.get_value("Lead", {"mobile_no": from_number}, "name")
            if not lead_name:
                contact_name = value.get("contacts", [{}])[0].get("profile", {}).get("name") or f"WhatsApp Lead {from_number}"
                lead = frappe.get_doc({
                    "doctype": "Lead",
                    "lead_name": contact_name,
                    "mobile_no": from_number,
                    "lead_source": "WhatsApp",
                    "status": "New"
                })
                lead.insert(ignore_permissions=True)
                lead_name = lead.name
                
                # Update WhatsApp Conversation linked Lead
                frappe.db.set_value("WhatsApp Conversation", local_msg.conversation, "lead", lead_name)
                
            # Log Activity
            create_activity(
                activity_type="Email", # Map WhatsApp to communication type
                lead=lead_name,
                description=f"Received WhatsApp message: {content}",
                performed_by="System"
            )
            
        # Sync message delivery/read status updates
        for status_update in statuses:
            msg_id = status_update.get("id")
            status = status_update.get("status")
            whatsapp_msg_name = frappe.db.get_value("WhatsApp Message", {"message_id": msg_id}, "name")
            if whatsapp_msg_name:
                # Update status in local message log
                frappe.db.set_value("WhatsApp Message", whatsapp_msg_name, "content", f"{frappe.db.get_value('WhatsApp Message', whatsapp_msg_name, 'content')} ({status})")
                
        return {"status": "success"}
