import logging
from ratelimit import limits as ratelimit
# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def after_install():
    """
    Called after the app is installed on a site.
    Initializes default setup data.
    """
    create_default_pipeline_and_stages()
    create_default_team()
    create_default_settings()

def create_default_pipeline_and_stages():
    # 1. Create Default Pipeline
    pipeline_name = "Standard Sales Pipeline"
    if not frappe.db.exists("CRM Pipeline", pipeline_name):
        pipeline = frappe.get_doc({
            "doctype": "CRM Pipeline",
            "pipeline_name": pipeline_name,
            "description": "Standard B2B sales pipeline stages."
        }).insert(ignore_permissions=True)
    else:
        pipeline = frappe.get_doc("CRM Pipeline", pipeline_name)

    # 2. Create Default Stages
    default_stages = [
        {"stage_name": "LEAD", "order": 10, "color": "#64748B"},
        {"stage_name": "FOLLOW UP", "order": 20, "color": "#0ea5e9"},
        {"stage_name": "DEMO SCHEDULE", "order": 30, "color": "#8b5cf6"},
        {"stage_name": "DEMO DONE", "order": 40, "color": "#a855f7"},
        {"stage_name": "PROPOSAL SENT", "order": 50, "color": "#f59e0b"},
        {"stage_name": "TRIAL AC", "order": 60, "color": "#ec4899"},
        {"stage_name": "HOT", "order": 70, "color": "#ef4444"},
        {"stage_name": "CALL BACK", "order": 80, "color": "#f97316"},
        {"stage_name": "INVOICE SENT", "order": 90, "color": "#eab308"},
        {"stage_name": "ONBOARDED", "order": 100, "color": "#10b981"},
        {"stage_name": "LOST", "order": 110, "color": "#ef4444"},
        {"stage_name": "RNR", "order": 120, "color": "#94a3b8"},
        {"stage_name": "DUPLICATE", "order": 130, "color": "#cbd5e1"},
        {"stage_name": "DIRECT MEETING", "order": 140, "color": "#06b6d4"},
        {"stage_name": "OTHERS", "order": 150, "color": "#6b7280"}
    ]

    for stage_info in default_stages:
        if not frappe.db.exists("CRM Pipeline Stage", stage_info["stage_name"]):
            frappe.get_doc({
                "doctype": "CRM Pipeline Stage",
                "stage_name": stage_info["stage_name"],
                "pipeline": pipeline.name,
                "sort_order": stage_info["order"],
                "color": stage_info["color"]
            }).insert(ignore_permissions=True)

def create_default_team():
    team_name = "General Sales"
    if not frappe.db.exists("CRM Team", team_name):
        frappe.get_doc({
            "doctype": "CRM Team",
            "team_name": team_name,
            "description": "Primary sales operations team."
        }).insert(ignore_permissions=True)

def create_default_settings():
    # Single doc update
    settings = frappe.get_doc("CRM Settings")
    settings.company_name = "Precision CRM"
    settings.default_pipeline = "Standard Sales Pipeline"
    settings.enable_ai_suggestions = 1
    settings.enable_whatsapp_integration = 0
    settings.save(ignore_permissions=True)
