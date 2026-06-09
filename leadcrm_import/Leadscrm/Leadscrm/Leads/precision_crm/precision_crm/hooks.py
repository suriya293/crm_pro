# precision_crm/hooks.py

app_name = "precision_crm"
app_title = "Precision CRM"
app_publisher = "Administrator"
app_description = "Enterprise-grade CRM built on Frappe Framework"
app_email = "admin@example.com"
app_license = "mit"

# ---------- Scheduler events ----------
scheduler_events = {
    "all": [
        "precision_crm.scheduler.all"
    ],
    "daily": [
        "precision_crm.scheduler.daily"
    ],
    "hourly": [
        "precision_crm.scheduler.hourly"
    ],
    "cron": {
        "*/5 * * * *": [
            "precision_crm.scheduler.five_minute"
        ]
    }
}

# ---------- Permission query conditions ----------
permission_query_conditions = {
    "Lead": "precision_crm.permissions.get_permission_query_conditions",
    "Contact": "precision_crm.permissions.get_permission_query_conditions",
    "Company": "precision_crm.permissions.get_permission_query_conditions",
    "Opportunity": "precision_crm.permissions.get_permission_query_conditions",
    "Deal": "precision_crm.permissions.get_permission_query_conditions",
    "Task": "precision_crm.permissions.get_permission_query_conditions",
    "FollowUp": "precision_crm.permissions.get_permission_query_conditions",
    "Activity": "precision_crm.permissions.get_permission_query_conditions"
}

# ---------- Installation hooks ----------
before_install = "precision_crm.install.before_install"
after_install = "precision_crm.install.after_install"
