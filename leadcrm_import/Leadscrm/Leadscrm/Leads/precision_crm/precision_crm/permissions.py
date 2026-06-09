import frappe
from frappe import _

def has_permission(doc, ptype="read", user=None):
    if not user:
        user = frappe.session.user
    if user == "Administrator" or "System Manager" in frappe.get_roles(user) or "CRM Admin" in frappe.get_roles(user):
        return True
    
    # Check roles
    roles = frappe.get_roles(user)
    
    # Viewer role has only read access
    if "Viewer" in roles and ptype != "read":
        return False
        
    # Check Sales Agent ownership restrictions
    if "Sales Agent" in roles:
        # Check if record belongs to owner or is assigned to them
        if hasattr(doc, "owner") and doc.owner == user:
            return True
        if hasattr(doc, "assigned_to") and doc.assigned_to == user:
            return True
        return False

    # Check Team Leader team restrictions
    if "Team Leader" in roles:
        # Check if doc has team
        if hasattr(doc, "team") and doc.team:
            # Check if leader belongs to the team or is lead of the team
            leader_team = frappe.db.get_value("Team", {"leader": user}, "name")
            if leader_team and doc.team == leader_team:
                return True
        return False
        
    return True

def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user
    if user == "Administrator" or "System Manager" in frappe.get_roles(user) or "CRM Admin" in frappe.get_roles(user):
        return ""
        
    roles = frappe.get_roles(user)
    conditions = []
    
    if "Sales Agent" in roles:
        conditions.append(f"(`owner` = {frappe.db.escape(user)} OR `assigned_to` = {frappe.db.escape(user)})")
        
    if "Team Leader" in roles:
        leader_teams = frappe.get_all("Team", filters={"leader": user}, fields=["name"])
        if leader_teams:
            team_names = [t.name for t in leader_teams]
            conditions.append(f"`team` in ({', '.join(frappe.db.escape(t) for t in team_names)})")

    if conditions:
        return " OR ".join(conditions)
    return ""
