import logging

app_name = "crm_pro"
app_title = "CRM Pro"
app_publisher = "Administrator"
app_description = "CRM Pro production-ready backend app for LeadsCRM using Frappe and PostgreSQL"
app_email = "admin@crm.local"
app_license = "mit"

# DocEvents
doc_events = {
    "CRM Lead": {
        "on_update": "crm_pro.api.lead_on_update",
        "after_insert": "crm_pro.api.lead_after_insert",
        "on_trash": "crm_pro.api.lead_on_trash"
    },
    "CRM Deal": {
        "on_update": "crm_pro.api.deal_on_update",
        "after_insert": "crm_pro.api.deal_after_insert"
    },
    "User": {
        "validate": "crm_pro.utils.mobile_validator.validate_user_mobile",
        "on_trash": "crm_pro.api.user_on_trash"
    },
    "CRM User Profile": {
        "validate": "crm_pro.utils.mobile_validator.validate_profile_mobile"
    }
}

# Scheduler Events
scheduler_events = {
    "all": [
        "crm_pro.jobs.process_pending_reminders"
    ],
    "daily": [
        "crm_pro.jobs.daily_backup_and_cleanup",
        "crm_pro.jobs.recalculate_dashboard_metrics"
    ],
    "hourly": [
        "crm_pro.jobs.calculate_hourly_analytics"
    ]
}

# Install Hooks
validate_password = "crm_pro.api_auth.validate_password"

after_install = "crm_pro.install.after_install"

before_request = [
    "crm_pro.api_auth.check_bearer_token",
]

after_request = [
    "crm_pro.api_auth.after_request"
]

workspaces = [
    {
        "name": "crm_pro",
        "label": "CRM Pro",
        "icon": "octicon octicon-briefcase",
        "module": "CRM Pro"
    }
]
