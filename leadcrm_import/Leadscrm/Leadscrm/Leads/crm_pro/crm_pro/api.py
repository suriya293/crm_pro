# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
import json

@frappe.whitelist()
def create_lead(lead_name, email=None, mobile=None, **kwargs):
    """
    Creates a new Lead document.
    """
    if not lead_name:
        frappe.throw(_("Lead Name is required"))

    # Instantiate lead
    lead = frappe.new_doc("CRM Lead")
    lead.lead_name = lead_name
    lead.email = email
    lead.mobile = mobile
    
    # Optional fields mapping
    for field in [
        "country_code", "stage", "source", "user", "priority", "segment",
        "alt_mobile_1", "alt_mobile_2", "alt_mobile_3", "age", "gender",
        "address", "state", "city", "country", "pincode", "company_name",
        "designation", "website", "tags", "opportunity_value", "followup_date"
    ]:
        if field in kwargs:
            lead.set(field, kwargs.get(field))

    # Custom fields mapping (expected as JSON array)
    if "custom_fields" in kwargs:
        try:
            cfields = json.loads(kwargs.get("custom_fields"))
            for cf in cfields:
                lead.append("custom_fields", {
                    "field_name": cf.get("name"),
                    "field_value": cf.get("value")
                })
        except Exception:
            pass

    lead.insert()
    return lead.name

@frappe.whitelist()
def update_lead(name, **kwargs):
    """
    Updates an existing Lead document.
    """
    if not name:
        frappe.throw(_("Lead Name/ID is required for update"))
    
    # Try finding doc name by lead_name if name does not exist as doc name
    doc_name = name
    if not frappe.db.exists("CRM Lead", doc_name):
        found = frappe.db.get_value("CRM Lead", {"lead_name": name}, "name")
        if found:
            doc_name = found

    lead = frappe.get_doc("CRM Lead", doc_name)
    
    # Check permissions
    if not frappe.has_permission(lead, "write"):
        frappe.throw(_("Not permitted to write/update Lead"), frappe.PermissionError)

    for field in [
        "lead_name", "email", "mobile", "country_code", "stage", "source", "user", 
        "priority", "segment", "alt_mobile_1", "alt_mobile_2", "alt_mobile_3", "age", 
        "gender", "address", "state", "city", "country", "pincode", "company_name", 
        "designation", "website", "tags", "opportunity_value", "followup_date"
    ]:
        if field in kwargs:
            lead.set(field, kwargs.get(field))

    if "custom_fields" in kwargs:
        lead.set("custom_fields", [])
        try:
            cfields = json.loads(kwargs.get("custom_fields"))
            for cf in cfields:
                lead.append("custom_fields", {
                    "field_name": cf.get("name"),
                    "field_value": cf.get("value")
                })
        except Exception:
            pass

    lead.save()
    return lead.name

@frappe.whitelist()
def delete_lead(name):
    """
    Deletes an existing Lead document.
    """
    if not name:
        frappe.throw(_("Lead Name/ID is required for deletion"))

    # Try finding doc name by lead_name if name does not exist as doc name
    doc_name = name
    if not frappe.db.exists("CRM Lead", doc_name):
        found = frappe.db.get_value("CRM Lead", {"lead_name": name}, "name")
        if found:
            doc_name = found

    lead = frappe.get_doc("CRM Lead", doc_name)
    if not frappe.has_permission(lead, "delete"):
        frappe.throw(_("Not permitted to delete Lead"), frappe.PermissionError)

    # Insert audit log before deletion
    frappe.get_doc({
        "doctype": "CRM Audit Log",
        "ref_doctype": "CRM Lead",
        "ref_name": doc_name,
        "action": "Delete",
        "user": frappe.session.user,
        "details": f"Lead {lead.lead_name} was deleted."
    }).insert(ignore_permissions=True)

    frappe.delete_doc("CRM Lead", doc_name)
    return {"status": "success"}

@frappe.whitelist()
def assign_lead(name, user):
    """
    Assigns a lead to a specific User.
    """
    if not name or not user:
        frappe.throw(_("Lead ID and User ID are required"))

    # Try finding doc name by lead_name if name does not exist as doc name
    doc_name = name
    if not frappe.db.exists("CRM Lead", doc_name):
        found = frappe.db.get_value("CRM Lead", {"lead_name": name}, "name")
        if found:
            doc_name = found

    lead = frappe.get_doc("CRM Lead", doc_name)
    lead.user = user
    lead.save()
    
    # Generate notification
    frappe.get_doc({
        "doctype": "CRM Notification",
        "notification_title": _("New Lead Assignment"),
        "message": f"Lead {lead.lead_name} has been assigned to you.",
        "for_user": user
    }).insert(ignore_permissions=True)

    return {"status": "success"}

@frappe.whitelist()
def get_leads(start=0, limit=20, order_by="creation desc", filters=None):
    """
    Retrieves filtered list of Leads.
    """
    parsed_filters = {}
    if filters:
        try:
            parsed_filters = json.loads(filters)
        except Exception:
            parsed_filters = filters

    leads = frappe.db.get_list("CRM Lead",
        filters=parsed_filters,
        fields=[
            "name", "lead_name", "email", "mobile", "country_code", "stage",
            "source", "user", "priority", "segment", "alt_mobile_1", "creation",
            "modified", "address", "city", "state", "pincode", "company_name", "opportunity_value"
        ],
        order_by=order_by,
        start=start,
        page_length=limit
    )
    return leads

@frappe.whitelist()
def search_leads(query):
    """
    Performs global search across Leads fields.
    """
    if not query:
        return []
    
    leads = frappe.db.sql("""
        SELECT name, lead_name, email, mobile, stage, user, company_name 
        FROM `tabCRM Lead`
        WHERE lead_name LIKE %s 
           OR email LIKE %s 
           OR mobile LIKE %s 
           OR company_name LIKE %s
        ORDER BY creation DESC
        LIMIT 20
    """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"), as_dict=True)
    
    return leads

@frappe.whitelist()
def create_deal(deal_name, lead, deal_value, **kwargs):
    """
    Creates a new Deal.
    """
    if not deal_name or not deal_value:
        frappe.throw(_("Deal Name and Deal Value are required"))

    deal = frappe.new_doc("CRM Deal")
    deal.deal_name = deal_name
    deal.lead = lead
    deal.deal_value = flt(deal_value)
    
    if "company" in kwargs:
        deal.company = kwargs.get("company")
    if "deal_stage" in kwargs:
        deal.deal_stage = kwargs.get("deal_stage")
    if "expected_close" in kwargs:
        deal.expected_close = kwargs.get("expected_close")
    if "forecast_category" in kwargs:
        deal.forecast_category = kwargs.get("forecast_category")
    
    deal.deal_status = "Open"
    deal.insert()
    return deal.name

@frappe.whitelist()
def update_deal_stage(name, deal_stage):
    """
    Updates the stage of a Deal.
    """
    if not name or not deal_stage:
        frappe.throw(_("Deal ID and Stage ID are required"))

    deal = frappe.get_doc("CRM Deal", name)
    deal.deal_stage = deal_stage
    deal.save()
    return deal.name

@frappe.whitelist()
def get_dashboard_metrics():
    """
    Fetches real-time dashboard analytics.
    """
    # Count totals
    total_leads = frappe.db.count("CRM Lead")
    new_leads = frappe.db.count("CRM Lead", filters={"stage": "LEAD"})
    converted_leads = frappe.db.count("CRM Lead", filters={"stage": "ONBOARDED"})
    
    # Deals
    won_deals = frappe.db.count("CRM Deal", filters={"deal_status": "Won"})
    lost_deals = frappe.db.count("CRM Deal", filters={"deal_status": "Lost"})
    
    # Sum revenue
    revenue_dict = frappe.db.sql("""
        SELECT SUM(deal_value) as rev 
        FROM `tabCRM Deal` 
        WHERE deal_status = 'Won'
    """, as_dict=True)
    total_revenue = revenue_dict[0].get("rev") or 0.0

    return {
        "total_leads": total_leads,
        "new_leads": new_leads,
        "converted_leads": converted_leads,
        "won_deals": won_deals,
        "lost_deals": lost_deals,
        "total_revenue": float(total_revenue)
    }

@frappe.whitelist()
def get_pipeline():
    """
    Retrieves full Pipeline configurations and deals in each stage.
    """
    stages = frappe.get_all("CRM Pipeline Stage", fields=["name", "stage_name", "color", "order"], order_by="order asc")
    
    for stage in stages:
        stage["leads"] = frappe.get_all("CRM Lead", 
            filters={"stage": stage.name},
            fields=["name", "lead_name", "opportunity_value", "user"]
        )
        stage["deals"] = frappe.get_all("CRM Deal",
            filters={"deal_stage": stage.name},
            fields=["name", "deal_name", "deal_value", "deal_status"]
        )
        
    return stages

@frappe.whitelist()
def get_reports(report_type):
    """
    Retrieves report queries.
    """
    if report_type == "Lead":
        return frappe.db.sql("""
            SELECT stage, COUNT(name) as count 
            FROM `tabCRM Lead` 
            GROUP BY stage
        """, as_dict=True)
    elif report_type == "Sales":
        return frappe.db.sql("""
            SELECT deal_status, SUM(deal_value) as total 
            FROM `tabCRM Deal` 
            GROUP BY deal_status
        """, as_dict=True)
    else:
        return []

# DocType hook methods (invoked via hooks.py)
def lead_on_update(doc, method):
    # Triggers on Lead Save/Update
    pass

def lead_after_insert(doc, method):
    # Logs Audit trail
    frappe.get_doc({
        "doctype": "CRM Audit Log",
        "ref_doctype": "CRM Lead",
        "ref_name": doc.name,
        "action": "Create",
        "user": frappe.session.user,
        "details": f"Lead {doc.lead_name} was created."
    }).insert(ignore_permissions=True)

def lead_on_trash(doc, method):
    pass

def deal_on_update(doc, method):
    pass

def deal_after_insert(doc, method):
    frappe.get_doc({
        "doctype": "CRM Audit Log",
        "ref_doctype": "CRM Deal",
        "ref_name": doc.name,
        "action": "Create",
        "user": frappe.session.user,
        "details": f"Deal {doc.deal_name} was created."
    }).insert(ignore_permissions=True)
