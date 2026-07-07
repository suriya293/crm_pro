import logging
from ratelimit import limits as ratelimit
import frappe
import json
import os

def run():
    print("=== INITIALIZING CRM REPORTS, DASHBOARDS, AND WORKSPACES ===")
    
    # 1. Seed Custom Reports (Phase 5)
    reports = [
        {
            "report_name": "Lead Summary",
            "ref_doctype": "CRM Lead",
            "report_type": "Query Report",
            "query": "SELECT name, lead_name, email, mobile, source, stage, creation FROM `tabCRM Lead`"
        },
        {
            "report_name": "Lead Source Analysis",
            "ref_doctype": "CRM Lead",
            "report_type": "Query Report",
            "query": "SELECT source as \"Source:Data:120\", COUNT(name) as \"Count:Int:80\", SUM(opportunity_value) as \"Total Value:Currency:120\" FROM `tabCRM Lead` GROUP BY source"
        },
        {
            "report_name": "Lead Conversion",
            "ref_doctype": "CRM Lead",
            "report_type": "Query Report",
            "query": "SELECT stage as \"Stage:Data:120\", COUNT(name) as \"Count:Int:80\", SUM(opportunity_value) as \"Total Value:Currency:120\" FROM `tabCRM Lead` GROUP BY stage"
        },
        {
            "report_name": "Deal Pipeline",
            "ref_doctype": "CRM Deal",
            "report_type": "Query Report",
            "query": "SELECT name, deal_name, lead, deal_value, deal_status, deal_stage, expected_close FROM `tabCRM Deal`"
        },
        {
            "report_name": "Revenue Forecast",
            "ref_doctype": "CRM Deal",
            "report_type": "Query Report",
            "query": "SELECT expected_close as \"Expected Close:Date:120\", SUM(deal_value) as \"Forecast Value:Currency:120\", COUNT(name) as \"Deal Count:Int:80\" FROM `tabCRM Deal` WHERE deal_status = 'Open' GROUP BY expected_close"
        },
        {
            "report_name": "Task Performance",
            "ref_doctype": "CRM Task",
            "report_type": "Query Report",
            "query": "SELECT assigned_to as \"Assignee:Link/User:150\", status as \"Status:Data:100\", COUNT(name) as \"Count:Int:80\" FROM `tabCRM Task` GROUP BY assigned_to, status"
        },
        {
            "report_name": "Activity Timeline",
            "ref_doctype": "CRM Activity",
            "report_type": "Query Report",
            "query": "SELECT name, activity_type, lead, notes, activity_date FROM `tabCRM Activity` ORDER BY activity_date DESC"
        }
    ]

    for rep in reports:
        if not frappe.db.exists("Report", rep["report_name"]):
            doc = frappe.get_doc({
                "doctype": "Report",
                "report_name": rep["report_name"],
                "ref_doctype": rep["ref_doctype"],
                "report_type": rep["report_type"],
                "module": "CRM Pro",
                "is_standard": "No",
                "query": rep["query"]
            })
            doc.insert(ignore_permissions=True)
            print(f"Report {rep['report_name']} seeded.")
        else:
            doc = frappe.get_doc("Report", rep["report_name"])
            doc.query = rep["query"]
            doc.save(ignore_permissions=True)
            print(f"Report {rep['report_name']} updated.")

    # 2. Seed Number Cards (Phase 4)
    number_cards = [
        {"card_name": "Total Leads", "document_type": "CRM Lead", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[]"},
        {"card_name": "New Leads", "document_type": "CRM Lead", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Lead\",\"stage\",\"=\",\"LEAD\"]]" },
        {"card_name": "Qualified Leads", "document_type": "CRM Lead", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Lead\",\"stage\",\"=\",\"ONBOARDED\"]]" },
        {"card_name": "Lost Leads", "document_type": "CRM Lead", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Lead\",\"stage\",\"=\",\"LOST\"]]" },
        {"card_name": "Total Deals", "document_type": "CRM Deal", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[]"},
        {"card_name": "Won Deals", "document_type": "CRM Deal", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Deal\",\"deal_status\",\"=\",\"Won\"]]" },
        {"card_name": "Lost Deals", "document_type": "CRM Deal", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Deal\",\"deal_status\",\"=\",\"Lost\"]]" },
        {"card_name": "Revenue", "document_type": "CRM Deal", "function": "Sum", "aggregate_function_based_on": "deal_value", "filters_config": "[[\"CRM Deal\",\"deal_status\",\"=\",\"Won\"]]" },
        {"card_name": "Open Tasks", "document_type": "CRM Task", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Task\",\"status\",\"=\",\"Open\"]]" },
        {"card_name": "Completed Tasks", "document_type": "CRM Task", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Task\",\"status\",\"=\",\"Completed\"]]" }
    ]

    for nc in number_cards:
        if not frappe.db.exists("Number Card", nc["card_name"]):
            doc = frappe.get_doc({
                "doctype": "Number Card",
                "name": nc["card_name"],
                "label": nc["card_name"],
                "document_type": nc["document_type"],
                "function": nc["function"],
                "aggregate_function_based_on": nc["aggregate_function_based_on"],
                "is_standard": 1,
                "module": "CRM Pro",
                "filters_config": nc["filters_config"]
            })
            doc.insert(ignore_permissions=True)
            print(f"Number Card {nc['card_name']} seeded.")

    # 3. Seed Dashboard Charts (Phase 4)
    charts = [
        {"chart_name": "Lead Funnel", "document_type": "CRM Lead", "chart_type": "Group By", "group_by_type": "Count", "group_by_based_on": "stage", "type": "Donut", "filters_json": "{}"},
        {"chart_name": "Lead Sources", "document_type": "CRM Lead", "chart_type": "Group By", "group_by_type": "Count", "group_by_based_on": "source", "type": "Pie", "filters_json": "{}"},
        {"chart_name": "Deal Funnel", "document_type": "CRM Deal", "chart_type": "Group By", "group_by_type": "Count", "group_by_based_on": "deal_stage", "type": "Bar", "filters_json": "{}"},
        {"chart_name": "Task Status", "document_type": "CRM Task", "chart_type": "Group By", "group_by_type": "Count", "group_by_based_on": "status", "type": "Pie", "filters_json": "{}"}
    ]

    for c in charts:
        if not frappe.db.exists("Dashboard Chart", c["chart_name"]):
            doc = frappe.get_doc({
                "doctype": "Dashboard Chart",
                "chart_name": c["chart_name"],
                "document_type": c["document_type"],
                "chart_type": c["chart_type"],
                "group_by_type": c["group_by_type"],
                "group_by_based_on": c["group_by_based_on"],
                "type": c["type"],
                "filters_json": c["filters_json"],
                "is_standard": 1,
                "module": "CRM Pro"
            })
            doc.insert(ignore_permissions=True)
            print(f"Dashboard Chart {c['chart_name']} seeded.")

    # 4. Seed Dashboard (Phase 4)
    db_name = "CRM Pro Dashboard"
    if not frappe.db.exists("Dashboard", db_name):
        doc = frappe.get_doc({
            "doctype": "Dashboard",
            "dashboard_name": db_name,
            "is_standard": 1,
            "module": "CRM Pro",
            "charts": [
                {"chart": "Lead Funnel", "width": "Half"},
                {"chart": "Lead Sources", "width": "Half"},
                {"chart": "Deal Funnel", "width": "Half"},
                {"chart": "Task Status", "width": "Half"}
            ],
            "cards": [
                {"card": "Total Leads", "width": "Quarter"},
                {"card": "Revenue", "width": "Quarter"},
                {"card": "Total Deals", "width": "Quarter"},
                {"card": "Open Tasks", "width": "Quarter"}
            ]
        })
        doc.insert(ignore_permissions=True)
        print(f"Dashboard {db_name} seeded.")

    # 5. Define layouts for Workspaces (Phase 3)
    def make_content(title, cards=[], charts=[], shortcuts=[]):
        blocks = [
            {"id": "header1", "type": "header", "data": {"text": title}}
        ]
        # Add Number Cards
        if cards:
            blocks.append({
                "id": "cards_block",
                "type": "number_card",
                "data": {
                    "number_cards": [{"card": card} for card in cards]
                }
            })
        # Add Charts
        if charts:
            blocks.append({
                "id": "charts_block",
                "type": "chart",
                "data": {
                    "charts": [{"chart": ch} for ch in charts]
                }
            })
        # Add Shortcuts
        for i, s in enumerate(shortcuts):
            blocks.append({
                "id": f"shortcut_{i}",
                "type": "shortcut",
                "data": {
                    "shortcut_name": s["label"],
                    "link_to": s["link_to"],
                    "type": s.get("type", "DocType")
                }
            })
        return "\n" + json.dumps(blocks, indent=1) + "\n"

    workspaces_def = [
        {
            "name": "CRM Pro",
            "label": "CRM Pro",
            "title": "CRM Pro",
            "icon": "briefcase",
            "sequence_id": 1.0,
            "parent_page": "",
            "number_cards": ["Total Leads", "Revenue"],
            "charts": ["Lead Funnel", "Deal Funnel"],
            "shortcuts": [
                {"label": "CRM Lead", "link_to": "CRM Lead"},
                {"label": "CRM Deal", "link_to": "CRM Deal"},
                {"label": "CRM Contact", "link_to": "CRM Contact"},
                {"label": "CRM Company", "link_to": "CRM Company"},
                {"label": "CRM Task", "link_to": "CRM Task"},
                {"label": "CRM Settings", "link_to": "CRM Settings"}
            ],
            "links": [
                {"link_to": "CRM Lead", "link_type": "DocType", "label": "CRM Lead"},
                {"link_to": "CRM Deal", "link_type": "DocType", "label": "CRM Deal"},
                {"link_to": "CRM Contact", "link_type": "DocType", "label": "CRM Contact"},
                {"link_to": "CRM Company", "link_type": "DocType", "label": "CRM Company"},
                {"link_to": "CRM Task", "link_type": "DocType", "label": "CRM Task"},
                {"link_to": "CRM Settings", "link_type": "DocType", "label": "CRM Settings"}
            ]
        },
        {
            "name": "Leads Workspace",
            "label": "Leads Workspace",
            "title": "Leads Workspace",
            "icon": "people",
            "sequence_id": 2.0,
            "parent_page": "CRM Pro",
            "number_cards": ["Total Leads", "New Leads", "Qualified Leads", "Lost Leads"],
            "charts": ["Lead Funnel", "Lead Sources"],
            "shortcuts": [
                {"label": "CRM Lead", "link_to": "CRM Lead"}
            ],
            "links": [
                {"link_to": "CRM Lead", "link_type": "DocType", "label": "Leads List"},
                {"link_to": "Lead Summary", "link_type": "Report", "label": "Lead Summary", "is_query_report": 1},
                {"link_to": "Lead Source Analysis", "link_type": "Report", "label": "Lead Source Analysis", "is_query_report": 1},
                {"link_to": "Lead Conversion", "link_type": "Report", "label": "Lead Conversion", "is_query_report": 1}
            ]
        },
        {
            "name": "Deals Workspace",
            "label": "Deals Workspace",
            "title": "Deals Workspace",
            "icon": "package",
            "sequence_id": 3.0,
            "parent_page": "CRM Pro",
            "number_cards": ["Total Deals", "Won Deals", "Lost Deals", "Revenue"],
            "charts": ["Deal Funnel"],
            "shortcuts": [
                {"label": "CRM Deal", "link_to": "CRM Deal"}
            ],
            "links": [
                {"link_to": "CRM Deal", "link_type": "DocType", "label": "Deals List"},
                {"link_to": "Deal Pipeline", "link_type": "Report", "label": "Deal Pipeline", "is_query_report": 1},
                {"link_to": "Revenue Forecast", "link_type": "Report", "label": "Revenue Forecast", "is_query_report": 1}
            ]
        },
        {
            "name": "Reports Workspace",
            "label": "Reports Workspace",
            "title": "Reports Workspace",
            "icon": "graph",
            "sequence_id": 4.0,
            "parent_page": "CRM Pro",
            "number_cards": [],
            "charts": [],
            "shortcuts": [],
            "links": [
                {"link_to": "Lead Summary", "link_type": "Report", "label": "Lead Summary", "is_query_report": 1},
                {"link_to": "Lead Source Analysis", "link_type": "Report", "label": "Lead Source Analysis", "is_query_report": 1},
                {"link_to": "Lead Conversion", "link_type": "Report", "label": "Lead Conversion", "is_query_report": 1},
                {"link_to": "Deal Pipeline", "link_type": "Report", "label": "Deal Pipeline", "is_query_report": 1},
                {"link_to": "Revenue Forecast", "link_type": "Report", "label": "Revenue Forecast", "is_query_report": 1},
                {"link_to": "Task Performance", "link_type": "Report", "label": "Task Performance", "is_query_report": 1},
                {"link_to": "Activity Timeline", "link_type": "Report", "label": "Activity Timeline", "is_query_report": 1}
            ]
        },
        {
            "name": "Dashboard Workspace",
            "label": "Dashboard Workspace",
            "title": "Dashboard Workspace",
            "icon": "dashboard",
            "sequence_id": 5.0,
            "parent_page": "CRM Pro",
            "number_cards": ["Total Leads", "Revenue", "Total Deals", "Open Tasks"],
            "charts": ["Lead Funnel", "Deal Funnel", "Task Status"],
            "shortcuts": [
                {"label": "CRM Pro Dashboard", "link_to": "CRM Pro Dashboard", "type": "Dashboard"}
            ],
            "links": []
        }
    ]

    for ws in workspaces_def:
        name = ws["name"]
        
        # Build block content structure
        content_json = make_content(
            ws["title"],
            cards=ws["number_cards"],
            charts=ws["charts"],
            shortcuts=ws["shortcuts"]
        )

        ws_doc_dict = {
            "doctype": "Workspace",
            "name": name,
            "label": ws["label"],
            "title": ws["title"],
            "icon": ws["icon"],
            "public": 1,
            "module": "CRM Pro",
            "is_hidden": 0,
            "sequence_id": ws["sequence_id"],
            "parent_page": ws["parent_page"],
            "content": content_json,
            "number_cards": [{"number_card_name": card, "label": card} for card in ws["number_cards"]],
            "charts": [{"chart_name": chart, "label": chart} for chart in ws["charts"]],
            "shortcuts": [{"label": sc["label"], "link_to": sc["link_to"], "type": sc.get("type", "DocType")} for sc in ws["shortcuts"]],
            "links": ws["links"]
        }

        if frappe.db.exists("Workspace", name):
            doc = frappe.get_doc("Workspace", name)
            doc.parent_page = ws["parent_page"]
            doc.sequence_id = ws["sequence_id"]
            doc.title = ws["title"]
            doc.label = ws["label"]
            doc.icon = ws["icon"]
            doc.content = content_json
            doc.set("number_cards", ws_doc_dict["number_cards"])
            doc.set("charts", ws_doc_dict["charts"])
            doc.set("shortcuts", ws_doc_dict["shortcuts"])
            doc.set("links", ws_doc_dict["links"])
            doc.save(ignore_permissions=True)
            print(f"Workspace {name} updated in DB.")
        else:
            doc = frappe.get_doc(ws_doc_dict)
            doc.insert(ignore_permissions=True)
            print(f"Workspace {name} created in DB.")

    frappe.db.commit()
    print("=== WORKSPACE DATABASE IMPORT COMPLETE ===")

    # 6. Export Workspaces to JSON Fixtures (disk write)
    base_fixture_path = "/mnt/c/Users/acer/Documents/Leadscrm/Leadscrm/Leads/crm_pro/crm_pro/workspace"
    for ws in workspaces_def:
        ws_name = ws["name"]
        ws_doc = frappe.get_doc("Workspace", ws_name)
        
        # Serialize fields matching fixture formatting
        serialized = ws_doc.as_dict(no_nulls=True)
        # Exclude runtime fields
        for field in ["_user_tags", "_comments", "_assign", "_liked_by"]:
            serialized.pop(field, None)
            
        folder_name = ws_name.lower().replace(" ", "_")
        target_dir = os.path.join(base_fixture_path, folder_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        file_path = os.path.join(target_dir, f"{folder_name}.json")
        with open(file_path, "w") as f:
            json.dump(serialized, f, indent=1, default=str)
        print(f"Fixture exported to: {file_path}")

    print("=== ALL SEEDING AND EXPORTS COMPLETED ===")

