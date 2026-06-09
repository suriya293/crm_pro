app_name = "crm_pro"
app_title = "CRM Pro"
app_publisher = "Administrator"
app_description = "CRM Pro production-ready backend app for LeadsCRM using Frappe and PostgreSQL"
app_email = "admin@crm.local"
app_license = "mit"

# DocEvents
doc_events = {
    "CRM Lead": {
        "on_update": "crm_pro.crm_pro.api.lead_on_update",
        "after_insert": "crm_pro.crm_pro.api.lead_after_insert",
        "on_trash": "crm_pro.crm_pro.api.lead_on_trash"
    },
    "CRM Deal": {
        "on_update": "crm_pro.crm_pro.api.deal_on_update",
        "after_insert": "crm_pro.crm_pro.api.deal_after_insert"
    }
}

# Scheduler Events
scheduler_events = {
    "all": [
        "crm_pro.crm_pro.jobs.process_pending_reminders"
    ],
    "daily": [
        "crm_pro.crm_pro.jobs.daily_backup_and_cleanup",
        "crm_pro.crm_pro.jobs.recalculate_dashboard_metrics"
    ],
    "hourly": [
        "crm_pro.crm_pro.jobs.calculate_hourly_analytics"
    ]
}

# Background Jobs queues setup (if custom needed)
# jobs = {
#     "reminder_queue": "crm_pro.crm_pro.jobs.process_pending_reminders"
# }

# Install Hooks
after_install = "crm_pro.crm_pro.install.after_install"

