import os
import sys

# Add project path for rbac_audit module
sys.path.append('/mnt/c/Users/acer/Downloads/Leadscrm/Leadscrm/Leads')

# Ensure working directory is bench root
os.chdir('/home/acer/frappe/frappe-bench')

# Set FRAPPE_SITE_PATH for site lookup
os.environ['FRAPPE_SITE_PATH'] = os.path.join(os.getcwd(), 'sites')

import frappe
import rbac_audit

frappe.init(site='crm.local')
frappe.connect()

rbac_audit.run()

frappe.destroy()
