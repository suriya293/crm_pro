import frappe
from frappe import _

@frappe.whitelist()
def assign_lead_round_robin(lead_name):
    # Find all active users with role "Sales Agent"
    agents = frappe.get_all(
        "User",
        filters={"enabled": 1},
        fields=["name"]
    )
    
    # Filter users who have the role "Sales Agent"
    sales_agents = []
    for agent in agents:
        if "Sales Agent" in frappe.get_roles(agent.name):
            sales_agents.append(agent.name)
            
    if not sales_agents:
        return
        
    # Get last assigned agent from cache
    last_assigned = frappe.cache().get_value("last_lead_agent_index") or 0
    
    # Assign Lead
    next_index = (int(last_assigned) + 1) % len(sales_agents)
    assigned_agent = sales_agents[next_index]
    
    frappe.db.set_value("Lead", lead_name, "assigned_to", assigned_agent)
    frappe.db.set_value("Lead", lead_name, "status", "Assigned")
    
    frappe.cache().set_value("last_lead_agent_index", next_index)
    
    # Create notification
    notification = frappe.get_doc({
        "doctype": "Notification",
        "subject": "New Round Robin Lead Assigned",
        "message": f"Lead {lead_name} has been assigned to you via Round Robin.",
        "for_user": assigned_agent
    })
    notification.insert(ignore_permissions=True)

@frappe.whitelist()
def detect_stale_leads():
    # Fetch Leads created more than 24 hours ago that are still "New" or "Assigned"
    stale_limit = frappe.utils.add_days(frappe.utils.now_datetime(), -1)
    stale_leads = frappe.get_all(
        "Lead",
        filters={
            "status": ["in", ["New", "Assigned"]],
            "creation": ["<", stale_limit]
        },
        fields=["name", "assigned_to", "team"]
    )
    
    for lead in stale_leads:
        escalate_lead(lead.name)

def escalate_lead(lead_name):
    lead_doc = frappe.get_doc("Lead", lead_name)
    
    # Find Team Leader or Sales Manager to escalate to
    escalate_to = None
    if lead_doc.team:
        escalate_to = frappe.db.get_value("Team", lead_doc.team, "leader")
        
    if not escalate_to:
        # Fallback to Sales Manager
        escalate_to = frappe.db.get_value("User", {"enabled": 1}, "name") # Or default CRM Manager
        
    if escalate_to:
        frappe.db.set_value("Lead", lead_name, "assigned_to", escalate_to)
        frappe.db.set_value("Lead", lead_name, "status", "Attempted Contact") # Escalated status
        
        # Log to Audit Log
        audit = frappe.get_doc({
            "doctype": "Audit Log",
            "action": "Lead Escalation",
            "details": f"Lead {lead_name} escalated to {escalate_to} due to inactivity",
            "user": "System"
        })
        audit.insert(ignore_permissions=True)
        
        # Create Escalation Notification
        notification = frappe.get_doc({
            "doctype": "Notification",
            "subject": "Escalated Lead Assignment",
            "message": f"Lead {lead_name} has been escalated to you due to inactivity.",
            "for_user": escalate_to
        })
        notification.insert(ignore_permissions=True)

@frappe.whitelist()
def trigger_reminders():
    trigger_followup_reminders()
    trigger_task_reminders()
    trigger_opportunity_reminders()
    trigger_invoice_reminders()

def trigger_followup_reminders():
    # Follow-ups scheduled for today which are still Pending
    today = frappe.utils.today()
    pending_followups = frappe.get_all(
        "FollowUp",
        filters={
            "follow_up_date": today,
            "outcome": "Pending"
        },
        fields=["name", "lead", "assigned_to", "owner"]
    )
    
    for f in pending_followups:
        target_user = f.assigned_to or f.owner
        notification = frappe.get_doc({
            "doctype": "Notification",
            "subject": f"Pending Follow-up Today",
            "message": f"Follow-up {f.name} for Lead {f.lead} is scheduled today.",
            "for_user": target_user
        })
        notification.insert(ignore_permissions=True)

def trigger_task_reminders():
    # Tasks due today or overdue
    today = frappe.utils.today()
    due_tasks = frappe.get_all(
        "Task",
        filters={
            "due_date": ["<=", today],
            "status": ["in", ["Open", "In Progress"]]
        },
        fields=["name", "task_name", "assignee", "owner"]
    )
    
    for t in due_tasks:
        target_user = t.assignee or t.owner
        notification = frappe.get_doc({
            "doctype": "Notification",
            "subject": f"Task Due: {t.task_name}",
            "message": f"Task {t.task_name} (ID: {t.name}) is due or overdue.",
            "for_user": target_user
        })
        notification.insert(ignore_permissions=True)

def trigger_opportunity_reminders():
    # Opportunities with no activity for more than 7 days
    limit_date = frappe.utils.add_days(frappe.utils.now_datetime(), -7)
    opps = frappe.get_all(
        "Opportunity",
        filters={
            "status": ["in", ["Open", "Discovery", "Qualification", "Proposal Sent", "Negotiation"]],
            "modified": ["<", limit_date]
        },
        fields=["name", "opportunity_name", "assigned_to", "owner"]
    )
    
    for opp in opps:
        target_user = opp.assigned_to or opp.owner
        notification = frappe.get_doc({
            "doctype": "Notification",
            "subject": f"Stale Opportunity Reminder",
            "message": f"Opportunity {opp.opportunity_name} (ID: {opp.name}) has had no updates for 7 days.",
            "for_user": target_user
        })
        notification.insert(ignore_permissions=True)

def trigger_invoice_reminders():
    # Unpaid invoices overdue by posting date
    today = frappe.utils.today()
    overdue_invoices = frappe.get_all(
        "Invoice",
        filters={
            "posting_date": ["<", today],
            "status": "Unpaid"
        },
        fields=["name", "customer", "grand_total", "assigned_to", "owner"]
    )
    
    for inv in overdue_invoices:
        target_user = inv.assigned_to or inv.owner
        notification = frappe.get_doc({
            "doctype": "Notification",
            "subject": f"Overdue Invoice Alert: {inv.name}",
            "message": f"Invoice {inv.name} for Customer {inv.customer} (Grand Total: {inv.grand_total}) is unpaid.",
            "for_user": target_user
        })
        notification.insert(ignore_permissions=True)
