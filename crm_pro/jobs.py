import logging
import frappe
logger = frappe.logger("crm_pro")
from frappe.utils import now_datetime
from frappe.query_builder.functions import Sum

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
        try:
            # Create an In-app Notification for the recipient
            if rem.recipient:
                frappe.get_doc({
                    "doctype": "CRM Notification",
                    "notification_title": rem.reminder_subject,
                    "message": f"Reminder alert regarding Lead: {rem.lead or 'N/A'}",
                    "for_user": rem.recipient
                }).insert(ignore_permissions=True)
                
            # Mark as sent
            frappe.db.set_value("CRM Reminder", rem.name, "is_sent", 1)
            frappe.db.commit()
        except Exception as e:
            frappe.db.rollback()
            logger.error(f"Failed to process reminder {rem.name}: {str(e)}")


def daily_backup_and_cleanup():
    """
    Simulates database backup and audit log archiving.
    """

    try:
        # Delete notifications older than 30 days in a database-agnostic manner
        from datetime import timedelta
        limit_date = now_datetime() - timedelta(days=30)
        deleted_count = frappe.db.delete("CRM Notification", filters={
            "is_read": 1,
            "creation": ["<", limit_date]
        })
        frappe.db.commit()
        logger.info(f"Daily backup and cleanup completed. Deleted {deleted_count} read notifications.")
    except Exception as e:
        frappe.db.rollback()
        logger.error(f"Daily backup and cleanup job failed: {str(e)}")


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
    
    # Sum revenue using Query Builder (database-agnostic)
    deal = frappe.qb.DocType("CRM Deal")
    total_revenue = (
        frappe.qb.from_(deal)
        .select(Sum(deal.deal_value).as_("rev"))
        .where(deal.deal_status == "Won")
    ).run()[0][0] or 0.0

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
    Includes duplicate detection (Phase 8).
    """
    import requests
    
    token = frappe.get_doc("CRM Settings").get_password("facebook_access_token", raise_exception=False)
    if not token or token == "mock_token":
        # Mock registration for testing / dev sandbox
        mock_email = f"fb_{leadgen_id}@example.com"
        existing = frappe.db.get_value("CRM Lead", {"email": mock_email}, "name")
        if existing:
            frappe.get_doc({
                "doctype": "CRM Activity",
                "activity_type": "Note",
                "lead": existing,
                "notes": f"[Mock] Facebook Lead Ads duplicate submission (Leadgen ID: {leadgen_id}) detected.",
                "activity_date": now_datetime()
            }).insert(ignore_permissions=True)
            frappe.db.commit()
            return
            
        frappe.get_doc({
            "doctype": "CRM Lead",
            "lead_name": f"Facebook Lead {leadgen_id}",
            "email": mock_email,
            "mobile": "+919876543210",
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
        email = lead_fields.get("email")
        mobile = lead_fields.get("phone_number") or lead_fields.get("phone")
        
        # Duplicate detection logic
        existing_lead = None
        if email:
            existing_lead = frappe.db.get_value("CRM Lead", {"email": email}, "name")
        if not existing_lead and mobile:
            existing_lead = frappe.db.get_value("CRM Lead", {"mobile": ["like", f"%{mobile}%"]}, "name")
            
        if existing_lead:
            frappe.get_doc({
                "doctype": "CRM Activity",
                "activity_type": "Note",
                "lead": existing_lead,
                "notes": f"Facebook Lead Ads duplicate submission (Leadgen ID: {leadgen_id}) detected.",
                "activity_date": now_datetime()
            }).insert(ignore_permissions=True)
            
            frappe.get_doc({
                "doctype": "CRM Audit Log",
                "ref_doctype": "CRM Lead",
                "ref_name": existing_lead,
                "action": "Update",
                "user": "System",
                "details": f"Facebook Lead Ads duplicate submission detected (Leadgen ID: {leadgen_id})."
            }).insert(ignore_permissions=True)
            frappe.db.commit()
            return
            
        frappe.get_doc({
            "doctype": "CRM Lead",
            "lead_name": lead_name,
            "email": email,
            "mobile": mobile,
            "source": "Facebook Ads",
            "stage": "LEAD"
        }).insert(ignore_permissions=True)
        
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Failed to fetch Facebook Lead {leadgen_id}: {str(e)}", "Facebook Lead Fetch Error")

