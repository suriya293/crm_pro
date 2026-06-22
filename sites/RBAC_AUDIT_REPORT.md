# RBAC Audit Report

## Permission Matrix

| DocType | Administrator | Sales Manager | Sales User | Marketing User | Support User |
|---|---|---|---|---|---|
| CRM Lead | R1 W1 C1 D1 S1 Rp1 E1 | R1 W1 C1 D1 S1 Rp1 E1 | - | - | - |
| CRM Deal | R1 W1 C1 D1 S1 Rp1 E1 | R1 W1 C1 D1 S1 Rp1 E1 | - | - | - |
| CRM Contact | - | - | - | - | - |
| CRM Task | R1 W1 C1 D1 S1 Rp1 E1 | R1 W1 C1 D1 S1 Rp1 E1 | - | - | - |
| CRM Note | R1 W1 C1 D1 S0 Rp0 E0 | R1 W1 C1 D1 S0 Rp0 E0 | - | - | - |
| CRM Settings | R1 W1 C1 D1 S0 Rp0 E0 | R1 W0 C0 D0 S0 Rp0 E0 | - | - | - |
| CRM Pipeline | - | - | - | - | - |
| CRM Company | - | - | - | - | - |

## APIs Missing Authorization Checks

All @frappe.whitelist endpoints have a permission decorator.

## All @frappe.whitelist Endpoints (for reference)
