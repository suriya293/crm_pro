import logging
import frappe
import json

def run():
    print("=== STARTING CRM DATABASE AND DOCTYPE AUDIT ===")
    
    doctypes_to_check = [
        "CRM Lead", "CRM Deal", "CRM Contact", "CRM Company", "CRM Task",
        "CRM Reminder", "CRM Pipeline", "CRM Pipeline Stage", "CRM Meeting",
        "CRM Activity", "CRM Audit Log", "CRM WhatsApp Log", "CRM Dashboard Metrics",
        "CRM Settings", "CRM Notification", "CRM Team", "CRM User Profile",
        "CRM Sales Target", "CRM Email Log", "CRM Call Log", "CRM Attachment",
        "CRM Custom Field", "CRM Lead Snapshot", "CRM Contact Email",
        "CRM Contact Phone", "CRM Role Configuration", "CRM Note"
    ]
    
    report = {
        "doctypes": {},
        "database_tables": {},
        "integrity_checks": {},
        "overall_status": "PASS"
    }
    
    # 1. Check if DocTypes exist in Frappe meta
    for dt in doctypes_to_check:
        exists = frappe.db.exists("DocType", dt)
        report["doctypes"][dt] = "Exists" if exists else "MISSING"
        if not exists:
            report["overall_status"] = "FAIL"
            
    # 2. Check if DB tables exist
    for dt in doctypes_to_check:
        if report["doctypes"][dt] == "Exists":
            try:
                meta = frappe.get_meta(dt)
                if meta.issingle:
                    report["database_tables"][dt] = "Exists (Single)"
                else:
                    try:
                        frappe.db.sql(f"select 1 from `tab{dt}` limit 1")
                        report["database_tables"][dt] = "Exists"
                    except Exception as e:
                        report["database_tables"][dt] = f"TABLE MISSING: {str(e)}"
                        report["overall_status"] = "FAIL"
            except Exception as e:
                report["database_tables"][dt] = f"Error: {str(e)}"
                report["overall_status"] = "FAIL"
        else:
            report["database_tables"][dt] = "DocType Missing"
            
    # 3. Check Pipeline Stages Integrity
    pipeline_exists = frappe.db.exists("CRM Pipeline", "Standard Sales Pipeline")
    report["integrity_checks"]["default_pipeline"] = "Standard Sales Pipeline Exists" if pipeline_exists else "Standard Sales Pipeline MISSING"
    
    stages = frappe.get_all("CRM Pipeline Stage", fields=["stage_name", "pipeline"])
    report["integrity_checks"]["stages_count"] = len(stages)
    if len(stages) == 0:
        report["overall_status"] = "FAIL"
        report["integrity_checks"]["stages_status"] = "NO STAGES IN DATABASE"
    else:
        report["integrity_checks"]["stages_status"] = f"{len(stages)} stages verified"

    # 4. Check Settings Integrity
    settings = frappe.get_doc("CRM Settings")
    report["integrity_checks"]["settings"] = {
        "company_name": settings.company_name,
        "default_pipeline": settings.default_pipeline,
        "enable_ai_suggestions": settings.enable_ai_suggestions,
        "enable_whatsapp_integration": settings.enable_whatsapp_integration
    }
    
    # Write report to a log file
    report_file_path = "/mnt/c/Users/acer/Documents/Leadscrm/Leadscrm/Leads/database_audit_report.json"
    with open(report_file_path, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"=== AUDIT COMPLETE. REPORT WRITTEN TO {report_file_path} ===")

    # 5. Extract additional details for reports, dashboards, etc.
    print("=== EXTRACTING REPORTS AND DASHBOARDS DETAILS ===")
    details = {}
    for dt in ["Report", "Dashboard", "Dashboard Chart", "Number Card", "Workspace"]:
        try:
            if dt == "Report":
                details[dt] = frappe.get_all(dt, fields=["name", "report_name", "ref_doctype", "report_type", "module"])
            elif dt == "Dashboard":
                details[dt] = frappe.get_all(dt, fields=["name", "dashboard_name", "module"])
            elif dt == "Dashboard Chart":
                details[dt] = frappe.get_all(dt, fields=["name", "chart_name", "chart_type", "module"])
            elif dt == "Number Card":
                details[dt] = frappe.get_all(dt, fields=["name", "label", "module"])
            elif dt == "Workspace":
                details[dt] = frappe.get_all(dt, fields=["name", "label", "module", "parent_page"])
        except Exception as e:
            print(f"Error querying {dt}: {str(e)}")
            details[dt] = []

    details_file_path = "/mnt/c/Users/acer/Documents/Leadscrm/Leadscrm/Leads/db_details_output.json"
    with open(details_file_path, "w") as f:
        json.dump(details, f, indent=4)
    print(f"=== DETAILS COMPLETE. WRITTEN TO {details_file_path} ===")

if __name__ == "__main__":
    try:
        frappe.init(site="crm.local", sites_path="/home/acer/frappe/frappe-bench/sites")
        frappe.connect()
    except Exception as e:
        print(f"Frappe Init Exception: {e}")
    run()

