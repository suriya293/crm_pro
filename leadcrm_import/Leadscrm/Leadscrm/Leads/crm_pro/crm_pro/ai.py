# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe import _

@frappe.whitelist()
def get_lead_score(lead_id):
    """
    Computes a lead quality score (0 to 100) based on source, completeness, and activities.
    """
    if not lead_id:
        frappe.throw(_("Lead ID is required"))
        
    lead = frappe.get_doc("CRM Lead", lead_id)
    score = 30 # Base score
    
    # completeness
    if lead.email: score += 10
    if lead.mobile: score += 10
    if lead.company_name: score += 10
    
    # Source scoring
    source_boost = {
        "Direct Sales": 20,
        "Referral": 25,
        "Google Ads": 15,
        "Webinar": 15
    }
    score += source_boost.get(lead.source, 5)
    
    # Activities check
    activity_count = frappe.db.count("CRM Activity", filters={"lead": lead_id})
    score += min(activity_count * 5, 20)
    
    # Limit score to 100
    score = min(score, 100)
    
    return {"lead_id": lead_id, "score": score}

@frappe.whitelist()
def generate_email_draft(lead_id, subject_template="Introduction"):
    """
    Generates a personalized introduction or follow-up email draft for a lead.
    """
    if not lead_id:
        frappe.throw(_("Lead ID is required"))

    lead = frappe.get_doc("CRM Lead", lead_id)
    lead_name = lead.lead_name or "there"
    company_name = lead.company_name or "your company"
    
    draft = f"Subject: Following up on our conversation - {subject_template}\n\n"
    draft += f"Hi {lead_name},\n\n"
    draft += f"I hope you are doing well. I wanted to follow up on our previous discussion regarding how we can support {company_name}.\n\n"
    draft += "Please let me know if you have a few minutes for a brief call next week to discuss this further.\n\n"
    draft += "Best regards,\nCRM Pro Sales Team"
    
    return {"lead_id": lead_id, "email_draft": draft}

@frappe.whitelist()
def generate_lead_summary(lead_id):
    """
    Summarizes the lead's history, attributes, and next actions.
    """
    if not lead_id:
        frappe.throw(_("Lead ID is required"))
        
    lead = frappe.get_doc("CRM Lead", lead_id)
    
    # Activities summary
    activities = frappe.get_all("CRM Activity", 
        filters={"lead": lead_id},
        fields=["activity_type", "notes", "activity_date"],
        order_by="activity_date desc"
    )
    
    summary = f"Summary for {lead.lead_name} ({lead.company_name or 'Independent'}):\n"
    summary += f"- Stage: {lead.stage}\n"
    summary += f"- Total activities recorded: {len(activities)}\n"
    
    if activities:
        summary += f"- Last activity ({activities[0].activity_type}): {activities[0].notes or 'No notes'}\n"
    else:
        summary += "- No activity recorded yet. Consider setting a reminder.\n"
        
    return {"lead_id": lead_id, "summary": summary}

@frappe.whitelist()
def predict_deal_success(deal_id):
    """
    Predicts the probability (0.0 to 1.0) of winning a deal.
    """
    if not deal_id:
        frappe.throw(_("Deal ID is required"))
        
    deal = frappe.get_doc("CRM Deal", deal_id)
    probability = 0.4 # Base probability
    
    # Stage booster
    stage_boost = {
        "Proposal Sent": 0.2,
        "Trial Ac": 0.3,
        "Invoice Sent": 0.4,
        "Demo Done": 0.25,
        "Lost": -0.4,
        "Won": 0.6
    }
    
    probability += stage_boost.get(deal.deal_stage, 0.0)
    
    # Forecast Category booster
    category_boost = {
        "Commit": 0.3,
        "Best Case": 0.15,
        "Pipeline": 0.05,
        "Closed": 0.6
    }
    
    probability += category_boost.get(deal.forecast_category, 0.0)
    
    # Constraints between 0.0 and 1.0
    probability = max(0.0, min(1.0, probability))
    
    return {"deal_id": deal_id, "success_probability": round(probability, 2)}
