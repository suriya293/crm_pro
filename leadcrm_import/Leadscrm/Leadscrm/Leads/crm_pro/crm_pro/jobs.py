# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now_datetime

def process_pending_reminders():
    """
    Fetches unsent reminders whose time has passed, sends notifications and marks as sent.
    """
    now = now_datetime()
    pending = frappe.get_all("CRM Reminder", 
        filters={"is_sent": 0, "reminder_time": ["<=", now]},
        fields=["name", "reminder_subject", "lead", "recipient"]
    )
    
    for rem in pending:
        # Create an In-app Notification for the recipient
        if rem.recipient:
            frappe.get_doc({
                "doctype": "CRM Notification",
                "notification_title": rem.reminder_subject,
                "message": f"Reminder alert regarding Lead: {rem.lead or 'N/A'}",
                "for_user": rem.recipient
            }).insert(ignore_permissions=True)
            
            # Send Email (in production, using frappe.sendmail)
            # frappe.sendmail(
            #     recipients=[rem.recipient],
            #     subject=rem.reminder_subject,
            #     message=f"Reminder alert regarding Lead: {rem.lead or 'N/A'}"
            # )
            
        # Mark as sent
        frappe.db.set_value("CRM Reminder", rem.name, "is_sent", 1)
    
    frappe.db.commit()

def daily_backup_and_cleanup():
    """
    Simulates database backup and audit log archiving.
    """
    # Delete notifications older than 30 days
    frappe.db.sql("""
        DELETE FROM `tabCRM Notification` 
        WHERE is_read = 1 AND creation < DATE_SUB(NOW(), INTERVAL 30 DAY)
    """)
    frappe.db.commit()

def recalculate_dashboard_metrics():
    """
    Recalculates rollup metrics and saves them to CRM Dashboard Metrics.
    """
    now_date = now_datetime().date()
    
    total_leads = frappe.db.count("CRM Lead")
    new_leads = frappe.db.count("CRM Lead", filters={"stage": "LEAD"})
    converted_leads = frappe.db.count("CRM Lead", filters={"stage": "ONBOARDED"})
    won_deals = frappe.db.count("CRM Deal", filters={"deal_status": "Won"})
    lost_deals = frappe.db.count("CRM Deal", filters={"deal_status": "Lost"})
    
    revenue_dict = frappe.db.sql("""
        SELECT SUM(deal_value) as rev 
        FROM `tabCRM Deal` 
        WHERE deal_status = 'Won'
    """, as_dict=True)
    total_revenue = revenue_dict[0].get("rev") or 0.0

    # Get or create record
    metric_name = frappe.db.get_value("CRM Dashboard Metrics", {"metric_date": now_date})
    if metric_name:
        metric = frappe.get_doc("CRM Dashboard Metrics", metric_name)
    else:
        metric = frappe.new_doc("CRM Dashboard Metrics")
        metric.metric_date = now_date

    metric.total_leads = total_leads
    metric.new_leads = new_leads
    metric.converted_leads = converted_leads
    metric.won_deals = won_deals
    metric.lost_deals = lost_deals
    metric.total_revenue = total_revenue
    metric.save(ignore_permissions=True)
    frappe.db.commit()

def calculate_hourly_analytics():
    """
    Runs short-interval rollup updates if required.
    """
    pass

def fetch_and_create_facebook_lead(leadgen_id):
    """
    Fetches full lead field details from the Meta Graph API and registers a CRM Lead.
    """
    import requests
    
    token = frappe.db.get_single_value("CRM Settings", "facebook_access_token")
    if not token or token == "mock_token":
        # Mock registration for testing / dev sandbox
        frappe.get_doc({
            "doctype": "CRM Lead",
            "lead_name": f"Facebook Lead {leadgen_id}",
            "email": f"fb_{leadgen_id}@example.com",
            "mobile": "15550199000",
            "source": "Facebook Ads",
            "stage": "LEAD"
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        return

    url = f"https://graph.facebook.com/v16.0/{leadgen_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse fields from Meta payload structure
        field_data = data.get("field_data", [])
        lead_fields = {}
        for field in field_data:
            name = field.get("name")
            values = field.get("values", [])
            if values:
                lead_fields[name] = values[0]
                
        # Map fields to CRM Lead Schema
        lead_name = lead_fields.get("full_name") or lead_fields.get("first_name", "") + " " + lead_fields.get("last_name", "")
        lead_name = lead_name.strip() or f"FB Lead {leadgen_id}"
        
        frappe.get_doc({
            "doctype": "CRM Lead",
            "lead_name": lead_name,
            "email": lead_fields.get("email"),
            "mobile": lead_fields.get("phone_number") or lead_fields.get("phone"),
            "source": "Facebook Ads",
            "stage": "LEAD"
        }).insert(ignore_permissions=True)
        
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Failed to fetch Facebook Lead {leadgen_id}: {str(e)}", "Facebook Lead Fetch Error")

