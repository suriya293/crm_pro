import frappe

def run():
    print("Setting up CRM Pro Roles and Permissions...")
    
    # 1. Create missing roles
    required_roles = [
        "System Manager",
        "CRM Admin",
        "Sales Manager",
        "Sales Executive",
        "Telecaller",
        "Team Lead",
        "Support Agent"
    ]
    for role_name in required_roles:
        if not frappe.db.exists("Role", role_name):
            doc = frappe.new_doc("Role")
            doc.role_name = role_name
            doc.insert(ignore_permissions=True)
            print(f"Role {role_name} created.")
        else:
            print(f"Role {role_name} already exists.")
            
    # 2. Define Permission Matrix
    # Format: { Doctype: [ {role: ..., read: 1, write: 1, create: 1, delete: 1, share: 1, report: 1, export: 1} ] }
    matrix = {
        "CRM Lead": [
            {"role": "Administrator", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "CRM Admin", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "Sales Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "Team Lead", "read": 1, "write": 1, "create": 1, "delete": 0, "share": 1, "report": 1, "export": 1},
            {"role": "Sales Executive", "read": 1, "write": 1, "create": 1, "delete": 0, "share": 1, "report": 1, "export": 0},
            {"role": "Telecaller", "read": 1, "write": 1, "create": 1, "delete": 0, "share": 0, "report": 0, "export": 0},
            {"role": "Support Agent", "read": 1, "write": 0, "create": 0, "delete": 0, "share": 0, "report": 0, "export": 0}
        ],
        "CRM Deal": [
            {"role": "Administrator", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "CRM Admin", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "Sales Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "Team Lead", "read": 1, "write": 1, "create": 1, "delete": 0, "share": 1, "report": 1, "export": 1},
            {"role": "Sales Executive", "read": 1, "write": 1, "create": 1, "delete": 0, "share": 1, "report": 1, "export": 0},
            {"role": "Telecaller", "read": 1, "write": 0, "create": 0, "delete": 0, "share": 0, "report": 0, "export": 0},
            {"role": "Support Agent", "read": 1, "write": 0, "create": 0, "delete": 0, "share": 0, "report": 0, "export": 0}
        ],
        "CRM Task": [
            {"role": "Administrator", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "CRM Admin", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "Sales Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "Team Lead", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 1},
            {"role": "Sales Executive", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 0},
            {"role": "Telecaller", "read": 1, "write": 1, "create": 1, "delete": 0, "share": 0, "report": 0, "export": 0},
            {"role": "Support Agent", "read": 1, "write": 1, "create": 1, "delete": 1, "share": 1, "report": 1, "export": 0}
        ],
        "CRM User Profile": [
            {"role": "Administrator", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "CRM Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Sales Manager", "read": 1, "write": 0, "create": 0, "delete": 0},
            {"role": "Team Lead", "read": 1, "write": 0, "create": 0, "delete": 0},
            {"role": "Sales Executive", "read": 1, "write": 0, "create": 0, "delete": 0},
            {"role": "Telecaller", "read": 1, "write": 0, "create": 0, "delete": 0},
            {"role": "Support Agent", "read": 1, "write": 0, "create": 0, "delete": 0}
        ],
        "CRM Note": [
            {"role": "Administrator", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "CRM Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Sales Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Team Lead", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Sales Executive", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Telecaller", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Support Agent", "read": 1, "write": 1, "create": 1, "delete": 1}
        ],
        "CRM Settings": [
            {"role": "Administrator", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "CRM Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Sales Manager", "read": 1, "write": 0, "create": 0, "delete": 0},
            {"role": "Team Lead", "read": 1, "write": 0, "create": 0, "delete": 0},
            {"role": "Sales Executive", "read": 1, "write": 0, "create": 0, "delete": 0}
        ],
        "CRM Pipeline Stage": [
            {"role": "Administrator", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "CRM Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Sales Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Team Lead", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "Sales Executive", "read": 1, "write": 1, "create": 1, "delete": 1}
        ]
    }
    
    # 3. Apply custom permission matrix
    for doctype, perms in matrix.items():
        # Clear existing custom permissions
        frappe.db.delete("Custom DocPerm", {"parent": doctype})
        
        for p in perms:
            dp = frappe.new_doc("Custom DocPerm")
            dp.parent = doctype
            dp.parenttype = "DocType"
            dp.parentfield = "permissions"
            dp.role = p["role"]
            dp.permlevel = 0
            dp.read = p.get("read", 0)
            dp.write = p.get("write", 0)
            dp.create = p.get("create", 0)
            dp.delete = p.get("delete", 0)
            dp.share = p.get("share", 0)
            dp.report = p.get("report", 0)
            dp.export = p.get("export", 0)
            dp.insert(ignore_permissions=True)
            
        print(f"Permissions configured for {doctype}.")
        
    frappe.db.commit()
    print("Permissions setup completed.")
