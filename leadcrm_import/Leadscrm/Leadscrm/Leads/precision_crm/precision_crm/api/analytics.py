import frappe
from frappe import _
from precision_crm.auth import authenticate_request
from precision_crm.permissions import has_permission
from precision_crm.api.leads import handle_api_exception

@frappe.whitelist(allow_guest=True)
def get_dashboard_summary():
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        # Lead stats
        leads = frappe.get_all("Lead", fields=["status"])
        lead_summary = {}
        for l in leads:
            lead_summary[l.status] = lead_summary.get(l.status, 0) + 1
            
        # Deal stats
        deals = frappe.get_all("Deal", fields=["stage", "amount"])
        deal_summary = {}
        pipeline_value = 0.0
        for d in deals:
            deal_summary[d.stage] = deal_summary.get(d.stage, 0) + 1
            pipeline_value += float(d.amount or 0.0)
            
        # Tasks stats
        pending_tasks = frappe.db.count("Task", {"status": ["in", ["Open", "In Progress"]]})
        
        # Converted leads stats
        total_leads = len(leads)
        converted_leads = lead_summary.get("Converted", 0)
        conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0.0

        return {
            "status": "success",
            "data": {
                "lead_summary": lead_summary,
                "deal_summary": deal_summary,
                "pipeline_value": pipeline_value,
                "pending_tasks": pending_tasks,
                "conversion_rate": conversion_rate
            }
        }
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_lead_funnel():
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        # Funnel stages: New -> Assigned -> Contacted -> Converted
        stages = ["New", "Assigned", "Attempted Contact", "Contacted", "Interested", "Qualified", "Converted"]
        funnel = {}
        for stage in stages:
            funnel[stage] = frappe.db.count("Lead", {"status": stage})
            
        return {"status": "success", "data": funnel}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_agent_performance():
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        agents = frappe.get_all("User", filters={"enabled": 1}, fields=["name"])
        performance = []
        
        for agent in agents:
            # Check if user has CRM roles
            roles = frappe.get_roles(agent.name)
            if "Sales Agent" not in roles and "Sales Manager" not in roles:
                continue
                
            lead_count = frappe.db.count("Lead", {"assigned_to": agent.name})
            converted_count = frappe.db.count("Lead", {"assigned_to": agent.name, "status": "Converted"})
            
            # Weighted Deal Revenue Won by this Agent
            deals = frappe.get_all("Deal", filters={"assigned_to": agent.name, "stage": "Won"}, fields=["amount"])
            revenue_won = sum(float(d.amount or 0.0) for d in deals)
            
            performance.append({
                "agent": agent.name,
                "leads_assigned": lead_count,
                "leads_converted": converted_count,
                "revenue_won": revenue_won,
                "conversion_rate": (converted_count / lead_count * 100) if lead_count > 0 else 0.0
            })
            
        return {"status": "success", "data": performance}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_campaign_roi():
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        campaigns = frappe.get_all("Campaign", fields=["name", "campaign_name", "budget"])
        roi_report = []
        
        for camp in campaigns:
            # Lead conversion count driven by this campaign
            leads = frappe.get_all("Lead", filters={"lead_source": camp.campaign_name})
            total_leads = len(leads)
            
            # Opportunity value linked to this campaign
            opps = frappe.get_all("Opportunity", filters={"opportunity_name": ["like", f"%{camp.campaign_name}%"]}, fields=["value", "status"])
            revenue_won = sum(float(o.value or 0.0) for o in opps if o.status == "Won")
            
            budget = float(camp.budget or 0.0)
            roi = ((revenue_won - budget) / budget * 100) if budget > 0 else 0.0
            
            roi_report.append({
                "campaign": camp.campaign_name,
                "budget": budget,
                "leads_generated": total_leads,
                "revenue_won": revenue_won,
                "roi_percentage": roi
            })
            
        return {"status": "success", "data": roi_report}
    except Exception as e:
        return handle_api_exception(e)

@frappe.whitelist(allow_guest=True)
def get_whatsapp_analytics():
    if not authenticate_request():
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Unauthorized"}

    try:
        inbound_count = frappe.db.count("WhatsApp Message", {"direction": "Inbound"})
        outbound_count = frappe.db.count("WhatsApp Message", {"direction": "Outbound"})
        
        # WhatsApp Conversations Status
        open_convs = frappe.db.count("WhatsApp Conversation", {"status": "Open"})
        closed_convs = frappe.db.count("WhatsApp Conversation", {"status": "Closed"})
        
        return {
            "status": "success",
            "data": {
                "inbound_messages": inbound_count,
                "outbound_messages": outbound_count,
                "open_conversations": open_convs,
                "closed_conversations": closed_convs
            }
        }
    except Exception as e:
        return handle_api_exception(e)
