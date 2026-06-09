import sys
sys.path.append('/home/acer/frappe/frappe-bench/apps/crm_pro')
sys.path.append('/home/acer/frappe/frappe-bench/apps/frappe')

import frappe
frappe.init(site='crm.local')
frappe.connect()

from crm_pro.create_workspaces import run
run()
