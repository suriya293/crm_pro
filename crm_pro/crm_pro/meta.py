import logging
import frappe
logger = frappe.logger("crm_pro")
from ratelimit import limits as ratelimit
# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

from frappe import _

def is_web_api_call():
    if frappe.flags.in_test:
        return False
    req = getattr(frappe.local, "request", None)
    if req is None:
        return False
    if not hasattr(req, "environ"):
        return False
    return True
from frappe.utils import now_datetime
import requests
import json
from werkzeug.wrappers import Response
from crm_pro.decorator import require_permission
from crm_pro.ratelimit import ratelimit
from crm_pro.crm_pro.utils.safe_json import safe_json


def verify_meta_signature(request):
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        return False
    
    app_secret = frappe.get_doc("CRM Settings").get_password("facebook_app_secret", raise_exception=False)
    if not app_secret or app_secret in ["mock_secret", ""]:
        # Log a security warning
        frappe.log_error(
            "Meta Webhook signature validation skipped: facebook_app_secret is unconfigured or mock. Set a strong secret for production security.",
            "Meta Webhook Security Warning"
        )
        # Prevent bypass in production (non-developer mode)
        if not frappe.conf.get("developer_mode"):
            return False
        return True
        
    import hmac
    import hashlib
    
    try:
        sha_name, signature_hash = signature.split("=")
        if sha_name != "sha256":
            return False
            
        mac = hmac.new(
            app_secret.encode("utf-8"),
            msg=request.data,
            digestmod=hashlib.sha256
        )
        return hmac.compare_digest(mac.hexdigest(), signature_hash)
    except Exception:
        return False

@require_permission('Authenticated')
@ratelimit(key='user', rate='100/m')
# TODO: add @validate_input(schema) for input validation
@frappe.whitelist(allow_guest=True)
def whatsapp_webhook():
    logger.info('Entering whatsapp_webhook')
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
            # Return raw plain text challenge
            return Response(challenge, mimetype="text/plain")
        else:
            return Response(json.dumps({"success": False, "message": "Invalid verification token"}), mimetype="application/json", status=403)

    elif request.method == "POST":
        if not verify_meta_signature(request):
            return Response(json.dumps({"success": False, "message": "Invalid webhook signature"}), mimetype="application/json", status=403)
            
        # Process webhook payload safely
        data_str = request.data.decode("utf-8") if request.data else "{}"
        payload = safe_json(data_str, default=None)
        if payload is None:
            frappe.log_error("Invalid WhatsApp Webhook JSON payload", "WhatsApp Webhook Payload Error")
            frappe.response["status"] = "failed"
            return
        
        try:
            entry = payload.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            statuses = value.get("statuses", [])
            
            if statuses:
                status_info = statuses[0]
                status = status_info.get("status")
                recipient = status_info.get("recipient_id")
                if status == "failed":
                    errors = status_info.get("errors", [])
                    err_msg = errors[0].get("message") if errors else "Unknown error"
                    frappe.log_error(f"WhatsApp dispatch to {recipient} failed: {err_msg}", "WhatsApp Status Failure")
            
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

                if not lead_name:
                    # Lead creation from WhatsApp (Phase 7 auto-creation)
                    new_lead = frappe.get_doc({
                        "doctype": "CRM Lead",
                        "lead_name": f"WhatsApp Lead {from_number}",
                        "mobile": from_number,
                        "source": "WhatsApp",
                        "stage": "LEAD"
                    })
                    new_lead.insert(ignore_permissions=True)
                    lead_name = new_lead.name

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

@require_permission('Authenticated')
@ratelimit(key='user', rate='100/m')
# TODO: add @validate_input(schema) for input validation
@frappe.whitelist(allow_guest=True)
def facebook_webhook():
    logger.info('Entering facebook_webhook')
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
            # Return raw plain text challenge
            return Response(challenge, mimetype="text/plain")
        else:
            return Response(json.dumps({"success": False, "message": "Invalid verification token"}), mimetype="application/json", status=403)

    elif request.method == "POST":
        if not verify_meta_signature(request):
            return Response(json.dumps({"success": False, "message": "Invalid webhook signature"}), mimetype="application/json", status=403)
            
        data_str = request.data.decode("utf-8") if request.data else "{}"
        payload = safe_json(data_str, default=None)
        if payload is None:
            frappe.log_error("Invalid Facebook Webhook JSON payload", "Facebook Webhook Payload Error")
            frappe.response["status"] = "failed"
            return
        try:
            entry = payload.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            leadgen_id = value.get("leadgen_id")
            
            if leadgen_id:
                # Enqueue background job to fetch leadgen info from Meta Graph API
                frappe.enqueue(
                    "crm_pro.jobs.fetch_and_create_facebook_lead",
                    queue="default",
                    leadgen_id=leadgen_id
                )
        except Exception as e:
            frappe.log_error(f"Error parsing Facebook Webhook: {str(e)}", "Facebook Webhook Error")
            
        frappe.response["status"] = "success"
        return

@frappe.whitelist()
def send_whatsapp_message(lead_id=None, message=None):
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
    if not frappe.has_permission(lead, "write"):
        frappe.throw(_("Not permitted to send messages for this Lead"), frappe.PermissionError)

    if not lead.mobile or lead.mobile == "-":
        frappe.throw(_("Lead does not have a valid mobile number"))
        
    # Get settings
    settings = frappe.get_doc("CRM Settings")
    if not settings.enable_whatsapp_integration:
        frappe.throw(_("WhatsApp integration is disabled in CRM Settings"))
        
    token = settings.get_password("whatsapp_access_token")
    phone_id = settings.whatsapp_phone_number_id
    
    if not token or not phone_id:
        frappe.throw(_("WhatsApp API Token or Phone Number ID is missing in Settings"))

    # Meta request payload
    url = f"https://graph.facebook.com/v16.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    print("LEAD MOBILE =", lead.mobile)
    print("TO =", lead.mobile.replace("+", ""))

    payload = {
        "messaging_product": "whatsapp",
        "to": lead.mobile.replace("+", ""),
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    # In sandbox or local test, we mock requests
    if token == "mock_token":
        response_data = {"messages": [{"id": "mock_msg_123"}]}
    else:
        import time
        max_retries = 3
        backoff_factor = 2
        last_error = None
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=10
                )

                print("STATUS:", response.status_code)
                print("RESPONSE:", response.text)

                response.raise_for_status()

                response_data = response.json()
                break

            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    time.sleep(backoff_factor ** attempt)
                else:
                    frappe.throw(
                        _(f"Meta API Request Failed after {max_retries} attempts: {str(last_error)}")
                    )
            
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
    if is_web_api_call():
        return {
            "success": True,
            "message": "WhatsApp message sent successfully",
            "data": response_data
        }
    return response_data
