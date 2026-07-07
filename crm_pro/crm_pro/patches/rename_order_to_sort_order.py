import frappe

def execute():
    doctype = "CRM Pipeline Stage"
    
    # Check if the old column exists
    if frappe.db.has_column(doctype, "order"):
        # Ensure the new sort_order column exists (in case schema update hasn't run yet)
        if not frappe.db.has_column(doctype, "sort_order"):
            frappe.db.commit()
            frappe.db.sql("ALTER TABLE `tabCRM Pipeline Stage` ADD COLUMN `sort_order` INT DEFAULT 0")
            
        # Copy data safely
        frappe.db.sql("UPDATE `tabCRM Pipeline Stage` SET `sort_order` = `order`")
        frappe.db.commit()
        
        # Drop the old column to prevent SQL reserved word issues in future queries
        frappe.db.sql("ALTER TABLE `tabCRM Pipeline Stage` DROP COLUMN `order`")
        frappe.db.commit()
        print("Successfully migrated 'order' to 'sort_order' in database.")
