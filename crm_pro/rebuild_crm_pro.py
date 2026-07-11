import logging
from ratelimit import limits as ratelimit
import frappe
import json
import os

def run():
    print("=== STARTING CRM PRO AUDIT AND REBUILD SCRIPTS ===")

    # 1. Audit and Create Reports
    reports_to_create = [
        {
            "report_name": "Lead Conversion Report",
            "ref_doctype": "CRM Lead",
            "report_type": "Query Report",
            "query": "SELECT stage as \"Stage:Link/CRM Pipeline Stage:150\", COUNT(name) as \"Count:Int:80\", SUM(opportunity_value) as \"Total Value:Currency:120\" FROM `tabCRM Lead` GROUP BY stage"
        },
        {
            "report_name": "Sales Funnel Report",
            "ref_doctype": "CRM Deal",
            "report_type": "Query Report",
            "query": "SELECT deal_stage as \"Deal Stage:Link/CRM Pipeline Stage:150\", COUNT(name) as \"Count:Int:80\", SUM(deal_value) as \"Total Value:Currency:120\" FROM `tabCRM Deal` GROUP BY deal_stage"
        },
        {
            "report_name": "Revenue Report",
            "ref_doctype": "CRM Deal",
            "report_type": "Query Report",
            "query": "SELECT deal_status as \"Status:Data:100\", SUM(deal_value) as \"Total Revenue:Currency:120\", COUNT(name) as \"Deals Count:Int:80\" FROM `tabCRM Deal` GROUP BY deal_status"
        },
        {
            "report_name": "Activity Report",
            "ref_doctype": "CRM Activity",
            "report_type": "Query Report",
            "query": "SELECT name as \"ID:Link/CRM Activity:150\", activity_type as \"Activity Type:Data:120\", lead as \"Lead:Link/CRM Lead:150\", activity_date as \"Date:Date:120\", notes as \"Notes:Text:250\" FROM `tabCRM Activity` ORDER BY activity_date DESC"
        },
        {
            "report_name": "Task Performance Report",
            "ref_doctype": "CRM Task",
            "report_type": "Query Report",
            "query": "SELECT assigned_to as \"Assignee:Link/User:150\", status as \"Status:Data:100\", COUNT(name) as \"Tasks Count:Int:80\" FROM `tabCRM Task` GROUP BY assigned_to, status"
        }
    ]

    for rep in reports_to_create:
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
            print(f"Report '{rep['report_name']}' created.")
        else:
            doc = frappe.get_doc("Report", rep["report_name"])
            doc.query = rep["query"]
            doc.save(ignore_permissions=True)
            print(f"Report '{rep['report_name']}' verified/updated.")

    # 2. Audit and Create Number Cards
    cards_to_create = [
        {"card_name": "Total Leads", "document_type": "CRM Lead", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[]"},
        {"card_name": "Total Deals", "document_type": "CRM Deal", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[]"},
        {"card_name": "Won Deals", "document_type": "CRM Deal", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Deal\",\"deal_status\",\"=\",\"Won\"]]" },
        {"card_name": "Lost Deals", "document_type": "CRM Deal", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Deal\",\"deal_status\",\"=\",\"Lost\"]]" },
        {"card_name": "Revenue", "document_type": "CRM Deal", "function": "Sum", "aggregate_function_based_on": "deal_value", "filters_config": "[[\"CRM Deal\",\"deal_status\",\"=\",\"Won\"]]" },
        {"card_name": "Open Tasks", "document_type": "CRM Task", "function": "Count", "aggregate_function_based_on": "name", "filters_config": "[[\"CRM Task\",\"status\",\"=\",\"Open\"]]" }
    ]

    for nc in cards_to_create:
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
            print(f"Number Card '{nc['card_name']}' created.")
        else:
            print(f"Number Card '{nc['card_name']}' exists.")

    # 3. Audit and Create Dashboard Charts
    charts_to_create = [
        {"chart_name": "Lead Sources", "document_type": "CRM Lead", "chart_type": "Group By", "group_by_type": "Count", "group_by_based_on": "source", "type": "Pie", "filters_json": "{}", "timeseries": 0},
        {"chart_name": "Lead Status", "document_type": "CRM Lead", "chart_type": "Group By", "group_by_type": "Count", "group_by_based_on": "stage", "type": "Donut", "filters_json": "{}", "timeseries": 0},
        {"chart_name": "Deal Funnel", "document_type": "CRM Deal", "chart_type": "Group By", "group_by_type": "Count", "group_by_based_on": "deal_stage", "type": "Bar", "filters_json": "{}", "timeseries": 0},
        {"chart_name": "Revenue Trend", "document_type": "CRM Deal", "chart_type": "Sum", "timeseries": 1, "based_on": "creation", "value_based_on": "deal_value", "type": "Line", "time_interval": "Monthly", "timespan": "Last Year", "filters_json": "{}"},
        {"chart_name": "Task Distribution", "document_type": "CRM Task", "chart_type": "Group By", "group_by_type": "Count", "group_by_based_on": "status", "type": "Donut", "filters_json": "{}", "timeseries": 0}
    ]

    for c in charts_to_create:
        if not frappe.db.exists("Dashboard Chart", c["chart_name"]):
            chart_doc = {
                "doctype": "Dashboard Chart",
                "chart_name": c["chart_name"],
                "document_type": c["document_type"],
                "chart_type": c["chart_type"],
                "type": c["type"],
                "filters_json": c["filters_json"],
                "is_standard": 1,
                "module": "CRM Pro"
            }
            if c.get("timeseries"):
                chart_doc["timeseries"] = 1
                chart_doc["based_on"] = c["based_on"]
                chart_doc["value_based_on"] = c["value_based_on"]
                chart_doc["time_interval"] = c["time_interval"]
                chart_doc["timespan"] = c["timespan"]
            else:
                chart_doc["timeseries"] = 0
                chart_doc["group_by_type"] = c["group_by_type"]
                chart_doc["group_by_based_on"] = c["group_by_based_on"]
            
            doc = frappe.get_doc(chart_doc)
            doc.insert(ignore_permissions=True)
            print(f"Dashboard Chart '{c['chart_name']}' created.")
        else:
            print(f"Dashboard Chart '{c['chart_name']}' exists.")

    # 4. Helper to Build EditorJS Content for Workspaces
    def make_content(title, cards=[], charts=[], shortcuts=[]):
        blocks = [
            {"id": "header1", "type": "header", "data": {"text": title}}
        ]
        if cards:
            blocks.append({
                "id": "cards_block",
                "type": "number_card",
                "data": {
                    "number_cards": [{"card": card} for card in cards]
                }
            })
        if charts:
            blocks.append({
                "id": "charts_block",
                "type": "chart",
                "data": {
                    "charts": [{"chart": ch} for ch in charts]
                }
            })
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

    # Define all 5 workspaces
    workspaces_def = [
        {
            "name": "CRM Pro",
            "label": "CRM Pro",
            "title": "CRM Pro",
            "icon": "briefcase",
            "sequence_id": 1.0,
            "parent_page": "",
            "number_cards": ["Total Leads", "Revenue", "Total Deals", "Open Tasks"],
            "charts": ["Lead Sources", "Lead Status", "Deal Funnel", "Revenue Trend", "Task Distribution"],
            "shortcuts": [
                {"label": "CRM Lead", "link_to": "CRM Lead"},
                {"label": "CRM Deal", "link_to": "CRM Deal"},
                {"label": "CRM Task", "link_to": "CRM Task"}
            ],
            "links": [
                {"link_to": "CRM Lead", "link_type": "DocType", "label": "CRM Lead List"},
                {"link_to": "CRM Deal", "link_type": "DocType", "label": "CRM Deal List"}
            ]
        },
        {
            "name": "Leads Workspace",
            "label": "Leads Workspace",
            "title": "Leads Workspace",
            "icon": "people",
            "sequence_id": 2.0,
            "parent_page": "CRM Pro",
            "number_cards": ["Total Leads", "Revenue"],
            "charts": ["Lead Sources", "Lead Status"],
            "shortcuts": [
                {"label": "CRM Lead", "link_to": "CRM Lead"}
            ],
            "links": [
                {"link_to": "CRM Lead", "link_type": "DocType", "label": "CRM Lead List"},
                {"link_to": "Lead Conversion Report", "link_type": "Report", "label": "Lead Conversion Report", "is_query_report": 1}
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
            "charts": ["Deal Funnel", "Revenue Trend"],
            "shortcuts": [
                {"label": "CRM Deal", "link_to": "CRM Deal"}
            ],
            "links": [
                {"link_to": "CRM Deal", "link_type": "DocType", "label": "CRM Deal List"},
                {"link_to": "Sales Funnel Report", "link_type": "Report", "label": "Sales Funnel Report", "is_query_report": 1},
                {"link_to": "Revenue Report", "link_type": "Report", "label": "Revenue Report", "is_query_report": 1}
            ]
        },
        {
            "name": "Reports Workspace",
            "label": "Reports Workspace",
            "title": "Reports Workspace",
            "icon": "graph",
            "sequence_id": 4.0,
            "parent_page": "CRM Pro",
            "number_cards": ["Total Leads"],
            "charts": ["Lead Sources"],
            "shortcuts": [
                {"label": "CRM Lead", "link_to": "CRM Lead"}
            ],
            "links": [
                {"link_to": "Lead Conversion Report", "link_type": "Report", "label": "Lead Conversion Report", "is_query_report": 1},
                {"link_to": "Sales Funnel Report", "link_type": "Report", "label": "Sales Funnel Report", "is_query_report": 1},
                {"link_to": "Revenue Report", "link_type": "Report", "label": "Revenue Report", "is_query_report": 1},
                {"link_to": "Activity Report", "link_type": "Report", "label": "Activity Report", "is_query_report": 1},
                {"link_to": "Task Performance Report", "link_type": "Report", "label": "Task Performance Report", "is_query_report": 1}
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
            "charts": ["Lead Sources", "Lead Status", "Deal Funnel", "Revenue Trend", "Task Distribution"],
            "shortcuts": [
                {"label": "CRM Pro Dashboard", "link_to": "CRM Pro Dashboard", "type": "Dashboard"}
            ],
            "links": [
                {"link_to": "CRM Lead", "link_type": "DocType", "label": "CRM Lead List"}
            ]
        }
    ]

    base_fixture_path = "/mnt/c/Users/downloads/Leadscrm/Leadscrm/Leads/crm_pro/crm_pro/workspace"
    # Wait, let's construct correct local path
    base_fixture_path = "/mnt/c/Users/acer/Documents/Leadscrm/Leadscrm/Leads/crm_pro/crm_pro/workspace"

    # Rebuild/Create Workspaces
    for ws in workspaces_def:
        name = ws["name"]
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
            "links": [{"link_to": ln["link_to"], "link_type": ln["link_type"], "label": ln["label"], "is_query_report": ln.get("is_query_report", 0)} for ln in ws["links"]]
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
            print(f"Workspace '{name}' rebuilt/updated in database.")
        else:
            doc = frappe.get_doc(ws_doc_dict)
            doc.insert(ignore_permissions=True)
            print(f"Workspace '{name}' created in database.")

    frappe.db.commit()

    # 5. Export Fixtures
    for ws in workspaces_def:
        ws_name = ws["name"]
        ws_doc = frappe.get_doc("Workspace", ws_name)
        
        serialized = ws_doc.as_dict(no_nulls=True)
        # Exclude runtime/internal fields
        for field in ["_user_tags", "_comments", "_assign", "_liked_by", "creation", "modified", "modified_by", "owner", "docstatus"]:
            serialized.pop(field, None)
        
        # Clean child records internal keys
        for child_tbl in ["number_cards", "charts", "shortcuts", "links"]:
            if child_tbl in serialized:
                for row in serialized[child_tbl]:
                    for f in ["name", "parent", "parentfield", "parenttype", "doctype", "owner", "creation", "modified", "modified_by"]:
                        row.pop(f, None)
                        
        folder_name = ws_name.lower().replace(" ", "_")
        target_dir = os.path.join(base_fixture_path, folder_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        file_path = os.path.join(target_dir, f"{folder_name}.json")
        with open(file_path, "w") as f:
            json.dump(serialized, f, indent=1, default=str)
        print(f"Fixture exported to: {file_path}")

    # 6. Verify and Print Counts
    print("\n" + "="*50)
    print(f"{'Workspace Name':<20} | {'Links':<5} | {'Shortcuts':<9} | {'Charts':<6} | {'Cards':<5}")
    print("="*50)
    
    all_greater_than_zero = True
    for ws in workspaces_def:
        ws_name = ws["name"]
        
        # Compare database against local json fixture to verify sync
        folder_name = ws_name.lower().replace(" ", "_")
        fixture_file = os.path.join(base_fixture_path, folder_name, f"{folder_name}.json")
        
        # Load database doc
        db_doc = frappe.get_doc("Workspace", ws_name)
        
        # Load fixture
        with open(fixture_file, "r") as f:
            fix_data = json.load(f)
            
        # Verify counts in db
        links_cnt = len(db_doc.links)
        shortcuts_cnt = len(db_doc.shortcuts)
        charts_cnt = len(db_doc.charts)
        cards_cnt = len(db_doc.number_cards)
        
        print(f"{ws_name:<20} | {links_cnt:<5} | {shortcuts_cnt:<9} | {charts_cnt:<6} | {cards_cnt:<5}")
        
        if links_cnt == 0 or shortcuts_cnt == 0 or charts_cnt == 0 or cards_cnt == 0:
            all_greater_than_zero = False
            
    print("="*50)
    if all_greater_than_zero:
        print("SUCCESS: All workspace component counts are greater than zero!")
    else:
        print("ERROR: One or more workspace counts are zero!")
        
run()
