import frappe

def run_checks():
    print("=== BACKEND VALIDATION STARTED ===")
    
    # 1. MariaDB Connection
    try:
        db_res = frappe.db.sql("SELECT VERSION()")[0][0]
        print(f"MariaDB Connection: PASS (Version: {db_res})")
    except Exception as e:
        print(f"MariaDB Connection: FAIL ({str(e)})")

    # Module Def Check
    try:
        exists_crm_pro = frappe.db.exists("Module Def", "CRM Pro")
        print(f"Module Def 'CRM Pro' exists in DB: {exists_crm_pro}")
        if not exists_crm_pro:
            print("Listing some Module Defs in DB:")
            mods = frappe.get_all("Module Def", fields=["name", "app_name"], limit=20)
            print(mods)
    except Exception as e:
        print(f"Module Def Query Fail: {str(e)}")

    # Column Check
    try:
        cols = frappe.db.get_table_columns("CRM Pipeline Stage")
        print("CRM Pipeline Stage Columns:", cols)
    except Exception as e:
        print(f"CRM Pipeline Stage Columns Check Fail: {str(e)}")

    # Role Def Check
    try:
        roles = [r.name for r in frappe.get_all("Role")]
        print("First 20 Roles:", roles[:20])
        print("Sales Executive exists:", "Sales Executive" in roles)
    except Exception as e:
        print(f"Role Def Query Fail: {str(e)}")
        
    # 2. Redis Connection
    try:
        # Check Cache
        redis_cache_ping = frappe.cache().ping()
        print(f"Redis Cache Ping: PASS ({redis_cache_ping})")
    except Exception as e:
        print(f"Redis Cache Ping: FAIL ({str(e)})")
        
    try:
        # Check Queue
        from frappe.utils.background_jobs import get_redis_conn
        conn = get_redis_conn()
        redis_queue_ping = conn.ping()
        print(f"Redis Queue Ping: PASS ({redis_queue_ping})")
    except Exception as e:
        print(f"Redis Queue Ping: FAIL ({str(e)})")

    # 3. Scheduler Status
    try:
        from frappe.utils.scheduler import is_scheduler_inactive
        scheduler_inactive = is_scheduler_inactive()
        print(f"Scheduler Status: PASS (Active: {not scheduler_inactive})")
    except Exception as e:
        print(f"Scheduler Status: FAIL ({str(e)})")
        
    # 4. Installed Apps
    try:
        apps = frappe.get_installed_apps()
        print(f"Installed Apps: PASS ({apps})")
    except Exception as e:
        print(f"Installed Apps: FAIL ({str(e)})")

    # 5. Check API registration and custom endpoints
    try:
        import crm_pro.api_auth as api_auth
        print("crm_pro api_auth module import: PASS")
    except Exception as e:
        print(f"crm_pro api_auth module import: FAIL ({str(e)})")
        
    print("=== BACKEND VALIDATION COMPLETED ===")

if __name__ == "__main__":
    run_checks()
