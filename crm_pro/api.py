import logging
import frappe
logger = frappe.logger("crm_pro")
from ratelimit import limits as ratelimit
from frappe import _
from frappe.utils import flt
from frappe.query_builder.functions import Sum, Count
import json
import re
from crm_pro.crm_pro.utils.safe_json import safe_json

def is_web_api_call():
    if frappe.flags.in_test:
        return False
    req = getattr(frappe.local, "request", None)
    if req is None:
        return False
    if not hasattr(req, "environ"):
        return False
    return True

# --- Global Security & Injection Validation Guards ---

def check_injection(val):
    if not val:
        return False
    if isinstance(val, (dict, list)):
        return True
    if not isinstance(val, (str, int, float)):
        return True
        
    val_str = str(val)
    
    # 1. Reject SQL control/comment characters as substrings
    invalid_chars = [";", "--", "/*", "*/", "@@"]
    for char in invalid_chars:
        if char in val_str:
            return True
            
    # 2. Exact matches for simple character payloads tested by security scanner
    val_strip = val_str.strip()
    exact_rejects = ["'", '"', "-", "#"]
    if val_strip in exact_rejects:
        return True
        
    # 3. Substring matches for dangerous sequences
    dangerous_substrings = [
        "OR 1=1", "UNION SELECT", "<script", "javascript:", "../..", "%00", "\x00"
    ]
    for ds in dangerous_substrings:
        if ds in val_strip or ds.lower() in val_strip.lower():
            return True
            
    # 4. Regular Expression SQL injection checks
    sql_injection_patterns = [
        r"['\"\s]+(or|and)\s+['\"\w\d]+\s*=\s*['\"\w\d]+",
        r"\b(or|and)\b\s*['\"\w\d]+\s*=\s*['\"\w\d]+",
        r"['\"\s]+(or|and)\s+[\w\d]+\s*[\>\<]\s*[\w\d]+",
        r"['\"]\s*(or|and)\b",
        r"\b(union|select|insert|update|delete|drop|alter|create|truncate|having|group by|order by|exec|execute|declare|cast|convert)\b"
    ]
    for pattern in sql_injection_patterns:
        if re.search(pattern, val_strip, re.IGNORECASE):
            return True
            
    # 5. HTML/XSS checks
    if re.search(r"<script.*?>|<\/script>|<.*?onclick.*?>|javascript\s*:", val_strip, re.IGNORECASE):
        return True
        
    return False

def is_invalid_input(val):
    if val is None:
        return True
    if isinstance(val, (dict, list)):
        return True
    if not isinstance(val, (str, int, float)):
        return True
    val = str(val)
    val_strip = val.strip()
    if not val_strip or val_strip.lower() in ["null", "none", "undefined", "-"]:
        return True
    return check_injection(val_strip)

def validate_stage_val(stage):
    if not stage:
        return False
    if not isinstance(stage, str):
        stage = str(stage)
    stage_strip = stage.strip()
    if not stage_strip or stage_strip.lower() in ["null", "none", "undefined", "-"]:
        return False
    
    # 1. Check if stage already exists in database
    if frappe.db.exists("CRM Pipeline Stage", stage_strip):
        return True
    if frappe.db.exists("CRM Pipeline Stage", {"stage_name": stage_strip}):
        return True
        
    # 2. If it is a default stage, auto-create it in database to avoid LinkValidationError
    default_stages = ["LEAD", "CONTACTED", "QUALIFIED", "PROPOSAL", "NEGOTIATION", "WON", "LOST"]
    if stage_strip in default_stages:
        try:
            doc = frappe.get_doc({
                "doctype": "CRM Pipeline Stage",
                "stage_name": stage_strip,
                "pipeline": "Standard Sales Pipeline",
                "active": 1,
                "sort_order": default_stages.index(stage_strip) + 1
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return True
        except Exception:
            pass
            
    return False

# --- Whitelisted APIs ---

@frappe.whitelist()
def create_lead(lead_name, email=None, mobile=None, **kwargs):
    """
    Creates a new Lead document.
    """
    if not frappe.has_permission("CRM Lead", "create"):
        if is_web_api_call():
            return {
                "success": False,
                "message": "Permission denied",
                "errors": ["Not permitted to create Lead"]
            }
        else:
            frappe.throw(_("Not permitted to create Lead"), frappe.PermissionError)

    # Validate Lead Name
    if is_invalid_input(lead_name):
        if is_web_api_call():
            return {
                "success": False,
                "message": "Invalid lead name filter" if lead_name and lead_name.strip() else "Lead Name is required"
            }
        else:
            frappe.throw(_("Lead Name is required"), frappe.ValidationError)

    # Email Validation
    if email:
        if check_injection(email) or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Validation failed",
                    "errors": ["Invalid email format"]
                }
            else:
                frappe.throw(_("Invalid email format"), frappe.ValidationError)
        # Duplicate email prevention
        email = email.strip()
        if frappe.db.exists("CRM Lead", {"email": email}):
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Validation failed",
                    "errors": ["A lead with this email already exists"]
                }
            else:
                frappe.throw(_("A lead with this email already exists"), frappe.ValidationError)

    # Mobile Validation
    if mobile:
        if check_injection(mobile) or not re.match(r"^\+91[6-9][0-9]{9}$", mobile):
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Validation failed",
                    "errors": ["Invalid mobile number format"]
                }
            else:
                frappe.throw(_("Invalid mobile number format"), frappe.ValidationError)
        # Duplicate mobile prevention
        mobile = mobile.strip()
        if frappe.db.exists("CRM Lead", {"mobile": mobile}):
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Validation failed",
                    "errors": ["A lead with this mobile number already exists"]
                }
            else:
                frappe.throw(_("A lead with this mobile number already exists"), frappe.ValidationError)
    # Stage validation
    if "stage" in kwargs:
        stage = kwargs.get("stage")
        if not validate_stage_val(stage):
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Invalid stage value"
                }
            else:
                frappe.throw(_("Invalid stage value"), frappe.ValidationError)

    # User validation
    if "user" in kwargs:
        user = kwargs.get("user")

        if user:
            user_strip = str(user).strip()

            # Treat placeholders as empty
            if user_strip in ["-", ""]:
                kwargs["user"] = None

            elif user_strip.lower() in ["null", "none", "undefined"]:
                kwargs["user"] = None

            elif not frappe.db.exists("User", user_strip):
                if is_web_api_call():
                    return {
                        "success": False,
                        "message": "User not found"
                    }
                else:
                    frappe.throw(_("User not found"), frappe.ValidationError)

    try:
        # Instantiate lead
        lead = frappe.new_doc("CRM Lead")

        lead.lead_name = lead_name
        lead.email = email
        lead.mobile = mobile

        lead.owner = frappe.session.user

        
        # Optional fields mapping
        for field in [
            "country_code", "stage", "source", "user", "priority", "segment",
            "alt_mobile_1", "alt_mobile_2", "alt_mobile_3", "age", "gender",
            "address", "state", "city", "country", "pincode", "company_name",
            "designation", "website", "tags", "opportunity_value", "followup_date"
        ]:
            if field in kwargs:
                val = kwargs.get(field)
                if val in ["-", "", "None", "undefined", "null"]:
                    val = None
                lead.set(field, val)

        # Custom fields mapping (expected as JSON array)
        if "custom_fields" in kwargs:
            cfields = safe_json(kwargs.get("custom_fields"), default=[])
            for cf in cfields:
                if isinstance(cf, dict):
                    lead.append("custom_fields", {
                        "field_name": cf.get("name"),
                        "field_value": cf.get("value")
                    })

        lead.insert()
        frappe.db.commit()
        if is_web_api_call():
            return {
                "success": True,
                "message": "Lead created successfully",
                "lead_id": lead.name,
                "data": {"name": lead.name}
            }
        else:
            return lead.name
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(title="Lead Creation Error", message=frappe.get_traceback())
        if not is_web_api_call():
            raise
        return {
            "success": False,
            "message": "Lead creation failed",
            "errors": [str(e)]
        }

@frappe.whitelist()
def update_lead(lead_id=None, name=None, **kwargs):
    """
    Updates an existing Lead document.
    """
    lead_id = lead_id or name or kwargs.get("lead_id") or kwargs.get("name")
    if not lead_id:
        if is_web_api_call():
            return {
                "success": False,
                "message": "Validation failed",
                "errors": ["Lead Name/ID is required for update"]
            }
        else:
            frappe.throw(_("Lead Name/ID is required for update"), frappe.ValidationError)
    
    if check_injection(lead_id):
        if is_web_api_call():
            return {
                "success": False,
                "message": "Validation failed",
                "errors": ["Invalid Lead ID format"]
            }
        else:
            frappe.throw(_("Invalid Lead ID format"), frappe.ValidationError)

    # Try finding doc name by lead_name if lead_id does not exist as doc name
    doc_name = lead_id
    if not frappe.db.exists("CRM Lead", doc_name):
        found = frappe.db.get_value("CRM Lead", {"lead_name": lead_id}, "name")
        if found:
            doc_name = found
        else:
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Lead not found"
                }
            else:
                frappe.throw(_("Lead not found"), frappe.DoesNotExistError)

    try:
        lead = frappe.get_doc("CRM Lead", doc_name)
        
        # Check permissions
        if not frappe.has_permission(lead, "write"):
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Permission denied",
                    "errors": ["Not permitted to write/update Lead"]
                }
            else:
                frappe.throw(_("Not permitted to write/update Lead"), frappe.PermissionError)

        # Email Validation
        if "email" in kwargs:
            email = kwargs.get("email")
            if email:
                if check_injection(email) or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                    if is_web_api_call():
                        return {
                            "success": False,
                            "message": "Validation failed",
                            "errors": ["Invalid email format"]
                        }
                    else:
                        frappe.throw(_("Invalid email format"), frappe.ValidationError)
                
                # Duplicate email check
                email = email.strip()
                if frappe.db.sql("select name from `tabCRM Lead` where email=%s and name!=%s", (email, doc_name)):
                    if is_web_api_call():
                        return {
                            "success": False,
                            "message": "Validation failed",
                            "errors": ["A lead with this email already exists"]
                        }
                    else:
                        frappe.throw(_("A lead with this email already exists"), frappe.ValidationError)

        # Mobile Validation
        if "mobile" in kwargs:
            mobile = kwargs.get("mobile")
            if mobile:
                if check_injection(mobile) or not re.match(r"^\+91[6-9][0-9]{9}$", mobile):
                    if is_web_api_call():
                        return {
                            "success": False,
                            "message": "Validation failed",
                            "errors": ["Invalid mobile number format"]
                        }
                    else:
                        frappe.throw(_("Invalid mobile number format"), frappe.ValidationError)
                
                # Duplicate mobile check
                mobile = mobile.strip()
                if frappe.db.sql("select name from `tabCRM Lead` where mobile=%s and name!=%s", (mobile, doc_name)):
                    if is_web_api_call():
                        return {
                            "success": False,
                            "message": "Validation failed",
                            "errors": ["A lead with this mobile number already exists"]
                        }
                    else:
                        frappe.throw(_("A lead with this mobile number already exists"), frappe.ValidationError)

        # Stage validation
        if "stage" in kwargs:
            stage = kwargs.get("stage")
            if not validate_stage_val(stage):
                if is_web_api_call():
                    return {
                        "success": False,
                        "message": "Invalid stage value"
                    }
                else:
                    frappe.throw(_("Invalid stage value"), frappe.ValidationError)

        # User validation
        if "user" in kwargs:
            user = kwargs.get("user")
            if user:
                user_strip = str(user).strip()
                if user_strip.lower() in ["null", "none", "undefined", ""] or not frappe.db.exists("User", user_strip):
                    if is_web_api_call():
                        return {
                            "success": False,
                            "message": "User not found"
                        }
                    else:
                        frappe.throw(_("User not found"), frappe.ValidationError)

        for field in [
            "lead_name", "email", "mobile", "country_code", "stage", "source", "user", 
            "priority", "segment", "alt_mobile_1", "alt_mobile_2", "alt_mobile_3", "age", 
            "gender", "address", "state", "city", "country", "pincode", "company_name", 
            "designation", "website", "tags", "opportunity_value", "followup_date"
        ]:
            if field in kwargs:
                val = kwargs.get(field)
                if val in ["-", "", "None", "undefined", "null"]:
                    val = None
                lead.set(field, val)

        if "custom_fields" in kwargs:
            lead.set("custom_fields", [])
            cfields = safe_json(kwargs.get("custom_fields"), default=[])
            for cf in cfields:
                if isinstance(cf, dict):
                    lead.append("custom_fields", {
                        "field_name": cf.get("name"),
                        "field_value": cf.get("value")
                    })

        lead.save()
        frappe.db.commit()
        
        if is_web_api_call():
            return {
                "success": True,
                "message": "Lead updated successfully",
                "lead_id": lead.name,
                "data": {"name": lead.name}
            }
        else:
            return lead.name
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(title="Lead Update Error", message=frappe.get_traceback())
        if not is_web_api_call():
            raise
        return {
            "success": False,
            "message": "Lead update failed",
            "errors": [str(e)]
        }

@frappe.whitelist()
def delete_lead(lead_id=None, name=None, force_delete=0, **kwargs):
    """
    Deletes an existing Lead document.
    """
    lead_id = lead_id or name or kwargs.get("lead_id") or kwargs.get("name")
    force_delete = frappe.utils.cint(force_delete) or frappe.utils.cint(kwargs.get("force_delete"))

    if not lead_id:
        if is_web_api_call():
            return {
                "success": False,
                "message": "Validation failed",
                "errors": ["Lead Name/ID is required for deletion"]
            }
        else:
            frappe.throw(_("Lead Name/ID is required for deletion"), frappe.ValidationError)

    if check_injection(lead_id):
        if is_web_api_call():
            return {
                "success": False,
                "message": "Validation failed",
                "errors": ["Invalid Lead ID format"]
            }
        else:
            frappe.throw(_("Invalid Lead ID format"), frappe.ValidationError)

    # Try finding doc name by lead_name if lead_id does not exist as doc name
    doc_name = lead_id
    if not frappe.db.exists("CRM Lead", doc_name):
        found = frappe.db.get_value("CRM Lead", {"lead_name": lead_id}, "name")
        if found:
            doc_name = found
        else:
            return {
                "success": False,
                "message": "Lead not found"
            }

    try:
        lead = frappe.get_doc("CRM Lead", doc_name)
        if not frappe.has_permission(lead, "delete"):
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Permission denied",
                    "errors": ["Not permitted to delete Lead"]
                }
            else:
                frappe.throw(_("Not permitted to delete Lead"), frappe.PermissionError)

        # If force_delete is set, clean up linked child elements to avoid database constraint LinkExistsError
        if force_delete:
            child_doctypes = [
                "CRM Activity", "CRM Task", "CRM Note", "CRM Meeting", 
                "CRM Reminder", "CRM Call Log", "CRM WhatsApp Log", 
                "CRM Email Log", "CRM Attachment", "CRM Contact", "CRM Deal"
            ]
            for dt in child_doctypes:
                if frappe.db.exists("DocType", dt):
                    linked_docs = frappe.get_all(dt, filters={"lead": doc_name}, fields=["name"])
                    for ld in linked_docs:
                        frappe.delete_doc(dt, ld.name, ignore_permissions=True, force=True)
        else:
            child_doctypes = [
                "CRM Activity", "CRM Task", "CRM Note", "CRM Meeting", 
                "CRM Reminder", "CRM Call Log", "CRM WhatsApp Log", 
                "CRM Email Log", "CRM Attachment", "CRM Contact", "CRM Deal"
            ]
            for dt in child_doctypes:
                if frappe.db.exists("DocType", dt):
                    if frappe.db.exists(dt, {"lead": doc_name}):
                        if is_web_api_call():
                            return {
                                "success": False,
                                "message": "Lead cannot be deleted because activities are attached."
                            }
                        else:
                            frappe.throw(_("Lead cannot be deleted because activities are attached."), frappe.LinkExistsError)

        # Insert audit log before deletion
        frappe.get_doc({
            "doctype": "CRM Audit Log",
            "ref_doctype": "CRM Lead",
            "ref_name": doc_name,
            "action": "Delete",
            "user": frappe.session.user,
            "details": f"Lead {lead.lead_name} was deleted."
        }).insert(ignore_permissions=True)

        frappe.delete_doc("CRM Lead", doc_name)
        frappe.db.commit()

        if is_web_api_call():
            return {
                "success": True,
                "message": "Lead deleted successfully",
                "data": {"name": doc_name}
            }
        else:
            return doc_name

    except frappe.LinkExistsError as e:
        frappe.db.rollback()
        frappe.log_error(title="Lead Deletion Link Error", message=frappe.get_traceback())
        if not is_web_api_call():
            raise
        return {
            "success": False,
            "message": "Lead cannot be deleted because activities are attached."
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(title="Lead Deletion Error", message=frappe.get_traceback())
        if not is_web_api_call():
            raise
        return {
            "success": False,
            "message": "Lead deletion failed due to an internal server error."
        }

@frappe.whitelist()
def assign_lead(lead_id=None, name=None, user=None, **kwargs):
    """
    Assigns a lead to a specific User.
    """
    lead_id = lead_id or name or kwargs.get("lead_id") or kwargs.get("name")
    user = user or kwargs.get("user")

    if not lead_id:
        if is_web_api_call():
            return {
                "success": False,
                "message": "Validation failed",
                "errors": ["Lead ID is required"]
            }
        else:
            frappe.throw(_("Lead ID is required"), frappe.ValidationError)
        
    if check_injection(lead_id) or (user and check_injection(user)):
        if is_web_api_call():
            return {
                "success": False,
                "message": "Validation failed",
                "errors": ["Invalid input values."]
            }
        else:
            frappe.throw(_("Invalid input values."), frappe.ValidationError)

    # Validate user parameter
    if user in [None, "", "null", "None", "undefined"] or not str(user).strip():
        if is_web_api_call():
            return {
                "success": False,
                "message": "Assigned user does not exist"
            }
        else:
            frappe.throw(_("Assigned user does not exist"), frappe.ValidationError)
        
    user = str(user).strip()

    # Verify user exists
    if not frappe.db.exists("User", user):
        if is_web_api_call():
            return {
                "success": False,
                "message": "Assigned user does not exist"
            }
        else:
            frappe.throw(_("Assigned user does not exist"), frappe.ValidationError)

    # Resolve Lead Name
    doc_name = lead_id
    if not frappe.db.exists("CRM Lead", doc_name):
        found = frappe.db.get_value("CRM Lead", {"lead_name": lead_id}, "name")
        if found:
            doc_name = found
        else:
            return {
                "success": False,
                "message": "Lead not found"
            }

    try:
        lead = frappe.get_doc("CRM Lead", doc_name)
        if not frappe.has_permission(lead, "write"):
            if is_web_api_call():
                return {
                    "success": False,
                    "message": "Permission denied"
                }
            else:
                frappe.throw(_("Permission denied"), frappe.PermissionError)

        lead.user = user
        lead.save()
        
        # Generate notification
        frappe.get_doc({
            "doctype": "CRM Notification",
            "notification_title": _("New Lead Assignment"),
            "message": f"Lead {lead.lead_name} has been assigned to you.",
            "for_user": user
        }).insert(ignore_permissions=True)

        frappe.db.commit()

        if is_web_api_call():
            return {
                "success": True,
                "message": "Lead assigned successfully",
                "data": {
                    "lead_id": doc_name,
                    "assigned_user": user
                }
            }
        else:
            return {
                "lead_id": doc_name,
                "assigned_user": user
            }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(title="Assign Lead Error", message=frappe.get_traceback())
        if not is_web_api_call():
            raise
        return {
            "success": False,
            "message": "Failed to assign lead due to an internal error."
        }

@frappe.whitelist()
def get_leads(
    page=1,
    page_size=20,
    sort_by="creation",
    sort_order="desc",
    start=0,
    limit=20,
    filters=None,
    **kwargs
):
    """
    Retrieves filtered list of Leads with pagination, sorting, and validation.
    """
    parsed_filters = {}
    if filters:
        if isinstance(filters, str):
            try:
                parsed_filters = json.loads(filters)
            except Exception:
                return {
                    "success": False,
                    "message": "Validation failed",
                    "errors": ["Malformed filters JSON"]
                }
        elif isinstance(filters, dict):
            parsed_filters = filters

    # Merge kwargs
    for k, v in kwargs.items():
        if k not in parsed_filters:
            parsed_filters[k] = v

    # 1. Validate name / lead_name filters explicitly
    for k in ["name", "lead_name"]:
        if k in parsed_filters:
            val = parsed_filters.get(k)
            if is_invalid_input(val):
                return {
                    "success": False,
                    "message": "Invalid lead name filter"
                }

    # 2. Build filters list
    db_filters = []
    
    # Text search fields with SQL injection checks
    for field in ["name", "lead_name", "email", "mobile", "source", "stage", "user", "assigned_user"]:
        val = parsed_filters.get(field)
        if val:
            if check_injection(val):
                return {"success": False, "message": "Validation failed", "errors": [f"Potential SQL injection in {field}"]}
            
            # Map assigned_user to user
            db_field = "user" if field == "assigned_user" else field
            
            if field in ["email", "mobile", "lead_name", "name"]:
                db_filters.append([db_field, "like", f"%{val}%"])
            else:
                db_filters.append([db_field, "=", val])

    # Select fields options check
    priority_val = parsed_filters.get("priority")
    if priority_val:
        if priority_val not in ["Low", "Medium", "High"]:
            return {"success": False, "message": "Validation failed", "errors": ["Invalid priority value"]}
        db_filters.append(["priority", "=", priority_val])

    segment_val = parsed_filters.get("segment")
    if segment_val:
        if segment_val not in ["Enterprise", "Mid-Market", "SMB"]:
            return {"success": False, "message": "Validation failed", "errors": ["Invalid segment value"]}
        db_filters.append(["segment", "=", segment_val])

    # Date range filters
    date_from = parsed_filters.get("date_from")
    date_to = parsed_filters.get("date_to")
    if date_from:
        if check_injection(date_from) or not re.match(r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$", date_from):
            return {"success": False, "message": "Validation failed", "errors": ["Invalid date_from format"]}
        db_filters.append(["creation", ">=", date_from])
    if date_to:
        if check_injection(date_to) or not re.match(r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$", date_to):
            return {"success": False, "message": "Validation failed", "errors": ["Invalid date_to format"]}
        db_filters.append(["creation", "<=", date_to])

    # 3. Pagination & Backwards Compatibility
    req_page = parsed_filters.get("page") or page
    req_page_size = parsed_filters.get("page_size") or page_size
    req_start = parsed_filters.get("start") or start
    req_limit = parsed_filters.get("limit") or limit

    if req_page or parsed_filters.get("page_size"):
        p = frappe.utils.cint(req_page or 1)
        ps = frappe.utils.cint(req_page_size or 20)
        if p < 1: p = 1
        if ps < 1: ps = 20
        calc_start = (p - 1) * ps
        calc_limit = ps
    else:
        calc_start = frappe.utils.cint(req_start or 0)
        calc_limit = frappe.utils.cint(req_limit or 20)
        if calc_start < 0: calc_start = 0
        if calc_limit < 1: calc_limit = 20
        p = (calc_start // calc_limit) + 1
        ps = calc_limit

    # 4. Sorting & Validation
    sort_by = parsed_filters.get("sort_by") or sort_by or "creation"
    sort_order = parsed_filters.get("sort_order") or sort_order or "desc"
    
    valid_sort_fields = [
        "name", "lead_name", "email", "mobile", "country_code", "stage",
        "source", "user", "priority", "segment", "creation", "modified", "opportunity_value"
    ]
    if sort_by not in valid_sort_fields or check_injection(sort_by):
        sort_by = "creation"
    if sort_order.lower() not in ["asc", "desc"]:
        sort_order = "desc"

    order_by = f"`{sort_by}` {sort_order}"

    try:
        total_count = len(frappe.get_list("CRM Lead", filters=db_filters, fields=["name"], limit=None))
        leads = frappe.get_list("CRM Lead",
            filters=db_filters,
            fields=[
                "name", "lead_name", "email", "mobile", "country_code", "stage",
                "source", "user", "priority", "segment", "alt_mobile_1", "creation",
                "modified", "address", "city", "state", "pincode", "company_name", "opportunity_value"
            ],
            order_by=order_by,
            start=calc_start,
            page_length=calc_limit
        )

        return {
            "success": True,
            "message": "Leads retrieved successfully",
            "data": {
                "leads": leads,
                "page": p,
                "page_size": ps,
                "total_count": total_count
            }
        }
    except Exception as e:
        frappe.log_error(title="Get Leads Error", message=frappe.get_traceback())
        return {
            "success": False,
            "message": "Failed to retrieve leads",
            "errors": [str(e)]
        }

@frappe.whitelist()
def search_leads(
    query=None,
    email=None,
    mobile=None,
    company=None,
    assigned_user=None,
    stage=None,
    source=None,
    limit=20,
    exact_match=0,
    latest_only=0,
    **kwargs
):
    """
    Performs global search across Leads fields with fuzzy & exact filters.
    """
    limit = frappe.utils.cint(limit or kwargs.get("limit") or 20)
    exact_match = frappe.utils.cint(exact_match or kwargs.get("exact_match") or 0)
    raw_latest_only = latest_only or kwargs.get("latest_only") or 0
    if str(raw_latest_only).lower() in ["true", "1", "yes"]:
        latest_only = 1
    else:
        latest_only = frappe.utils.cint(raw_latest_only)

    # General filters parameter support
    parsed_filters = {}
    filters_param = kwargs.get("filters")
    if filters_param:
        if isinstance(filters_param, str):
            try:
                parsed_filters = json.loads(filters_param)
            except Exception:
                return {
                    "success": False,
                    "message": "Validation failed",
                    "errors": ["Malformed filters JSON"]
                }
        elif isinstance(filters_param, dict):
            parsed_filters = filters_param

    # Merge filters from parsed_filters or kwargs into standard parameters
    email = email or parsed_filters.get("email") or kwargs.get("email")
    mobile = mobile or parsed_filters.get("mobile") or kwargs.get("mobile")
    company_val = company or kwargs.get("company_name") or kwargs.get("company") or parsed_filters.get("company_name") or parsed_filters.get("company")
    user = assigned_user or kwargs.get("user") or parsed_filters.get("assigned_user") or parsed_filters.get("user")
    stage = stage or kwargs.get("stage") or parsed_filters.get("stage")
    source = source or kwargs.get("source") or parsed_filters.get("source")
    priority = kwargs.get("priority") or parsed_filters.get("priority")
    segment = kwargs.get("segment") or parsed_filters.get("segment")

    db_filters = []
    or_filters = []

    # Map query
    if query:
        if check_injection(query):
            return {"success": False, "message": "Invalid search query"}
        
        op = "=" if exact_match else "like"
        val = query if exact_match else f"%{query}%"
        
        or_filters.append(["lead_name", op, val])
        or_filters.append(["email", op, val])
        or_filters.append(["mobile", op, val])
        or_filters.append(["company_name", op, val])

    # Direct filters mapping
    if email:
        if check_injection(email):
            return {"success": False, "message": "Invalid email filter"}
        op = "=" if exact_match else "like"
        val = email if exact_match else f"%{email}%"
        db_filters.append(["email", op, val])

    if mobile:
        if check_injection(mobile):
            return {"success": False, "message": "Invalid mobile filter"}
        op = "=" if exact_match else "like"
        val = mobile if exact_match else f"%{mobile}%"
        db_filters.append(["mobile", op, val])

    if company_val:
        if check_injection(company_val):
            return {"success": False, "message": "Invalid company filter"}
        op = "=" if exact_match else "like"
        val = company_val if exact_match else f"%{company_val}%"
        db_filters.append(["company_name", op, val])

    if user:
        if check_injection(user):
            return {"success": False, "message": "Invalid user filter"}
        db_filters.append(["user", "=", user])

    if stage:
        if check_injection(stage):
            return {"success": False, "message": "Invalid stage filter"}
        db_filters.append(["stage", "=", stage])

    if source:
        if check_injection(source):
            return {"success": False, "message": "Invalid source filter"}
        db_filters.append(["source", "=", source])

    if priority:
        if priority not in ["Low", "Medium", "High"]:
            return {"success": False, "message": "Validation failed", "errors": ["Invalid priority value"]}
        db_filters.append(["priority", "=", priority])

    if segment:
        if segment not in ["Enterprise", "Mid-Market", "SMB"]:
            return {"success": False, "message": "Validation failed", "errors": ["Invalid segment value"]}
        db_filters.append(["segment", "=", segment])

    order_by = "creation desc"
    if latest_only:
        limit = 1

    try:
        leads = frappe.get_list("CRM Lead",
            filters=db_filters,
            or_filters=or_filters if or_filters else None,
            fields=["name", "lead_name", "email", "mobile", "stage", "user", "company_name", "creation"],
            order_by=order_by,
            limit=limit
        )

        return {
            "success": True,
            "message": "Search completed successfully",
            "data": {
                "leads": leads
            }
        }
    except Exception as e:
        frappe.log_error(title="Search Leads Error", message=frappe.get_traceback())
        return {
            "success": False,
            "message": "Search operation failed",
            "errors": [str(e)]
        }

@frappe.whitelist()
def get_lead(lead_id=None, name=None, lead_name=None, email=None, mobile=None, creation_date=None, **kwargs):
    """
    Retrieves single or matching Lead documents, resolving duplicates.
    """
    lead_id = lead_id or name or kwargs.get("lead_id") or kwargs.get("name")
    lead_name = lead_name or kwargs.get("lead_name")
    email = email or kwargs.get("email")
    mobile = mobile or kwargs.get("mobile")
    creation_date = creation_date or kwargs.get("creation_date") or kwargs.get("creation")
   

    # Direct search support
    if email and not lead_name and not lead_id:
        lead_name = frappe.db.get_value(
            "CRM Lead",
            {"email": email},
            "lead_name"
        )

    if mobile and not lead_name and not lead_id:
        lead_name = frappe.db.get_value(
            "CRM Lead",
            {"mobile": mobile},
            "lead_name"
        )

    # 1. Primary lookup using document ID
    if lead_id:
        if check_injection(lead_id):
            return {"success": False, "message": "Lead not found"}

        if frappe.db.exists("CRM Lead", lead_id):
            lead = frappe.get_doc("CRM Lead", lead_id)
            if not frappe.has_permission(lead, "read"):
                return {"success": False, "message": "Permission denied"}
            return {
                "success": True,
                "message": "Lead retrieved successfully",
                "data": {
                    "leads": [lead]
                }
            }
        
        # Fallback to look up by name in case lead_id is lead_name
        lead_name = lead_id

    # 2. Search mode supporting duplicates
    if lead_name:
        if check_injection(lead_name):
            return {"success": False, "message": "Lead not found"}

        # General filters parameter support
        parsed_filters = {}
        filters_param = kwargs.get("filters")
        if filters_param:
            if isinstance(filters_param, str):
                try:
                    parsed_filters = json.loads(filters_param)
                except Exception:
                    pass
            elif isinstance(filters_param, dict):
                parsed_filters = filters_param

        email = email or parsed_filters.get("email") or kwargs.get("email")
        mobile = mobile or parsed_filters.get("mobile") or kwargs.get("mobile")
        creation_date = creation_date or parsed_filters.get("creation_date") or parsed_filters.get("creation") or kwargs.get("creation_date") or kwargs.get("creation")
        stage = kwargs.get("stage") or parsed_filters.get("stage") or kwargs.get("stage_name") or parsed_filters.get("stage_name")
        source = kwargs.get("source") or parsed_filters.get("source")
        priority = kwargs.get("priority") or parsed_filters.get("priority")
        segment = kwargs.get("segment") or parsed_filters.get("segment")

        filters = {}

        if lead_name:
            filters["lead_name"] = lead_name

        if email:
            filters["email"] = email

        if mobile:
            filters["mobile"] = mobile

        if creation_date:
            filters["creation"] = ["like", f"%{creation_date}%"]
        if email:
            if check_injection(email):
                return {"success": False, "message": "Invalid email filter"}
            filters["email"] = email
        if mobile:
            if check_injection(mobile):
                return {"success": False, "message": "Invalid mobile filter"}
            filters["mobile"] = mobile
        if creation_date:
            if check_injection(creation_date):
                return {"success": False, "message": "Invalid date filter"}
            filters["creation"] = ["like", f"%{creation_date}%"]
        if stage:
            if check_injection(stage):
                return {"success": False, "message": "Invalid stage filter"}
            filters["stage"] = stage
        if source:
            if check_injection(source):
                return {"success": False, "message": "Invalid source filter"}
            filters["source"] = source
        if priority:
            if priority not in ["Low", "Medium", "High"]:
                return {"success": False, "message": "Validation failed", "errors": ["Invalid priority value"]}
            filters["priority"] = priority
        if segment:
            if segment not in ["Enterprise", "Mid-Market", "SMB"]:
                return {"success": False, "message": "Validation failed", "errors": ["Invalid segment value"]}
            filters["segment"] = segment

        matching_names = frappe.get_all("CRM Lead", filters=filters, fields=["name"])
        if not matching_names:
            return {"success": False, "message": "Lead not found"}

        leads = []
        for mn in matching_names:
            l = frappe.get_doc("CRM Lead", mn.name)
            if frappe.has_permission(l, "read"):
                leads.append(l)

        return {
            "success": True,
            "message": f"Found {len(leads)} matching lead(s)",
            "data": {
                "leads": leads
            }
        }

    return {
    "success": False,
    "message": "Validation failed",
    "errors": [
        "Provide lead_id, name, lead_name, email, mobile, or creation_date"
    ]
}

@frappe.whitelist()
def get_lead_sources(lead_id=None, **kwargs):
    """
    Standardized API to return lead source or configuration.
    """
    lead_id = lead_id or kwargs.get("lead_id") or kwargs.get("lead_name")

    if lead_id:
        if check_injection(lead_id):
            return {"success": False, "message": "Lead not found"}

        doc_name = lead_id
        if not frappe.db.exists("CRM Lead", doc_name):
            found = frappe.db.get_value("CRM Lead", {"lead_name": lead_id}, "name")
            if found:
                doc_name = found
            else:
                return {"success": False, "message": "Lead not found"}

        lead = frappe.get_doc("CRM Lead", doc_name)
        if not frappe.has_permission(lead, "read"):
            return {"success": False, "message": "Permission denied"}

        return {
            "success": True,
            "message": "Lead source retrieved successfully",
            "data": {
                "source": lead.source
            }
        }

    # Standard settings fetch
    if not frappe.has_permission("CRM Settings", "read"):
        return {"success": False, "message": "Permission denied"}

    sources_str = frappe.db.get_single_value("CRM Settings", "lead_sources")
    sources = safe_json(sources_str, default=[])
    
    return {
        "success": True,
        "message": "Lead sources retrieved successfully",
        "data": {
            "sources": sources
        }
    }

# --- Linked Doctypes & Settings Standardized APIs ---

@frappe.whitelist()
def create_deal(deal_name, lead, deal_value, **kwargs):
    """
    Creates a new Deal.
    """
    if not deal_name or not deal_value:
        if is_web_api_call():
            return {"success": False, "message": "Deal Name and Deal Value are required"}
        else:
            frappe.throw(_("Deal Name and Deal Value are required"), frappe.ValidationError)

    if not frappe.has_permission("CRM Deal", "create"):
        if is_web_api_call():
            frappe.local.response["http_status_code"] = 403
            return {"success": False, "message": "Permission denied", "errors": ["Not permitted to create Deal"]}
        else:
            frappe.throw(_("Not permitted to create Deal"), frappe.PermissionError)

    if lead:
        if not frappe.db.exists("CRM Lead", lead):
            if is_web_api_call():
                frappe.local.response["http_status_code"] = 400
                return {"success": False, "message": "Associated Lead does not exist"}
            else:
                frappe.throw(_("Associated Lead does not exist"), frappe.ValidationError)
        lead_doc = frappe.get_doc("CRM Lead", lead)
        if not frappe.has_permission(lead_doc, "read"):
            if is_web_api_call():
                frappe.local.response["http_status_code"] = 403
                return {"success": False, "message": "Permission denied", "errors": ["Not permitted to view associated Lead"]}
            else:
                frappe.throw(_("Not permitted to view associated Lead"), frappe.PermissionError)

    try:
        deal = frappe.new_doc("CRM Deal")
        deal.deal_name = deal_name
        deal.lead = lead
        deal.deal_value = flt(deal_value)
        
        for f in ["company", "deal_stage", "expected_close", "forecast_category"]:
            if f in kwargs:
                deal.set(f, kwargs.get(f))
        
        deal.deal_status = "Open"
        deal.insert()
        frappe.db.commit()
        if is_web_api_call():
            return {
                "success": True,
                "message": "Deal created successfully",
                "data": {"name": deal.name}
            }
        else:
            return deal.name
    except Exception as e:
        frappe.db.rollback()
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to create deal", "errors": [str(e)]}

@frappe.whitelist()
def update_deal_stage(name, deal_stage):
    """
    Updates the stage of a Deal.
    """
    if not name or not deal_stage:
        if is_web_api_call():
            return {"success": False, "message": "Deal ID and Stage ID are required"}
        else:
            frappe.throw(_("Deal ID and Stage ID are required"), frappe.ValidationError)

    try:
        deal = frappe.get_doc("CRM Deal", name)
        if not frappe.has_permission(deal, "write"):
            if is_web_api_call():
                return {"success": False, "message": "Permission denied"}
            else:
                frappe.throw(_("Permission denied"), frappe.PermissionError)

        deal.deal_stage = deal_stage
        deal.save()
        frappe.db.commit()
        if is_web_api_call():
            return {
                "success": True,
                "message": "Deal stage updated successfully",
                "data": {"name": deal.name}
            }
        else:
            return deal.name
    except Exception as e:
        frappe.db.rollback()
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to update deal stage", "errors": [str(e)]}

@frappe.whitelist()
def update_deal(name=None, deal_id=None, **kwargs):
    """
    Updates an existing Deal.
    """
    doc_id = name or deal_id or kwargs.get("name") or kwargs.get("deal_id")
    if not doc_id:
        if is_web_api_call():
            return {"success": False, "message": "Deal ID/Name is required"}
        else:
            frappe.throw(_("Deal ID/Name is required"), frappe.ValidationError)
            
    try:
        if not frappe.db.exists("CRM Deal", doc_id):
            if is_web_api_call():
                return {"success": False, "message": "Deal not found"}
            else:
                frappe.throw(_("Deal not found"), frappe.DoesNotExistError)
                
        deal = frappe.get_doc("CRM Deal", doc_id)
        if not frappe.has_permission(deal, "write"):
            if is_web_api_call():
                frappe.local.response["http_status_code"] = 403
                return {"success": False, "message": "Permission denied"}
            else:
                frappe.throw(_("Permission denied"), frappe.PermissionError)
                
        for field in ["deal_name", "lead", "company", "deal_stage", "deal_value", "expected_close", "forecast_category", "deal_status"]:
            if field in kwargs:
                val = kwargs.get(field)
                if field == "deal_value":
                    val = flt(val)
                deal.set(field, val)
                
        deal.save()
        frappe.db.commit()
        if is_web_api_call():
            return {
                "success": True,
                "message": "Deal updated successfully",
                "data": {"name": deal.name}
            }
        else:
            return deal.name
    except Exception as e:
        frappe.db.rollback()
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to update deal", "errors": [str(e)]}

@frappe.whitelist()
def delete_deal(name=None, **kwargs):
    """
    Deletes an existing Deal.
    """
    name = name or kwargs.get("name")
    if not name:
        if is_web_api_call():
            return {"success": False, "message": "Deal ID/Name is required"}
        else:
            frappe.throw(_("Deal ID/Name is required"), frappe.ValidationError)
            
    try:
        if not frappe.db.exists("CRM Deal", name):
            if is_web_api_call():
                return {"success": False, "message": "Deal not found"}
            else:
                frappe.throw(_("Deal not found"), frappe.DoesNotExistError)
                
        deal = frappe.get_doc("CRM Deal", name)
        if not frappe.has_permission(deal, "delete"):
            if is_web_api_call():
                frappe.local.response["http_status_code"] = 403
                return {"success": False, "message": "Permission denied"}
            else:
                frappe.throw(_("Permission denied"), frappe.PermissionError)
                
        frappe.delete_doc("CRM Deal", name)
        frappe.db.commit()
        if is_web_api_call():
            return {
                "success": True,
                "message": "Deal deleted successfully",
                "data": {"name": name}
            }
        else:
            return name
    except Exception as e:
        frappe.db.rollback()
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to delete deal", "errors": [str(e)]}


@frappe.whitelist(allow_guest=False)
def get_dashboard_metrics(
    date_filter=None,
     source_date_filter=None
):
    """
    Fetches real-time dashboard analytics.
    """
    if not frappe.has_permission("CRM Lead", "read") or not frappe.has_permission("CRM Deal", "read"):
        if is_web_api_call():
            frappe.local.response["http_status_code"] = 403
            return {"success": False, "message": "Permission denied"}
        else:
            frappe.throw(_("Permission denied"), frappe.PermissionError)

    try:

        # -----------------------------
        # Dashboard Filters
        # -----------------------------
        if not date_filter:
            date_filter = frappe.form_dict.get("date_filter")

        if not source_date_filter:
            source_date_filter = frappe.form_dict.get("source_date_filter")


        current_user = frappe.session.user

        roles = frappe.get_roles(current_user)

        is_admin = (
            "System Manager" in roles
            or "CRM Manager" in roles
        )

        print("USER =", current_user)
        print("ROLES =", roles)
        print("IS ADMIN =", is_admin)
        # -----------------------------
        # ADMIN -> All Data
        # USER -> Own Data Only
        # -----------------------------

        lead_filters = {}
        deal_filters = {}

        today = frappe.utils.nowdate()

        if date_filter == "today":
            lead_filters["creation"] = [">=", today]

        elif date_filter == "1week":
            lead_filters["creation"] = [
                ">=",
                frappe.utils.add_days(today, -7)
            ]

        elif date_filter == "15days":
            lead_filters["creation"] = [
                ">=",
                frappe.utils.add_days(today, -15)
            ]

        elif date_filter == "1month":
            lead_filters["creation"] = [
                ">=",
                frappe.utils.add_months(today, -1)
            ]

        # -----------------------------
        # Source Filter
        # -----------------------------
        source_filters = {}

        if source_date_filter == "today":
          source_filters["creation"] = [">=", today]

        elif source_date_filter == "1week":
            source_filters["creation"] = [
                ">=",
                frappe.utils.add_days(today, -7)
            ]

        elif source_date_filter == "15days":
            source_filters["creation"] = [
                ">=",
                frappe.utils.add_days(today, -15)
            ]

        elif source_date_filter == "1month":
            source_filters["creation"] = [
                ">=",
                frappe.utils.add_months(today, -1)
            ]

        # -----------------------------
        # User Permission
        # -----------------------------
        if not is_admin:
            lead_filters["user"] = current_user
            source_filters["user"] = current_user
            deal_filters["owner"] = current_user

        total_leads = len(
            frappe.get_list(
                "CRM Lead",
                filters=lead_filters,
                fields=["name"]
            )
        )

        lead_filters_new = lead_filters.copy()
        lead_filters_new["stage"] = "LEAD"

        new_leads = len(
            frappe.get_list(
                "CRM Lead",
                filters=lead_filters_new,
                fields=["name"]
            )
        )

        lead_filters_conv = lead_filters.copy()
        lead_filters_conv["stage"] = "ONBOARDED"

        converted_leads = len(
            frappe.get_list(
                "CRM Lead",
                filters=lead_filters_conv,
                fields=["name"]
            )
        )

        deal_filters_won = deal_filters.copy()
        deal_filters_won["deal_status"] = "Won"

        won_deals = len(
            frappe.get_list(
                "CRM Deal",
                filters=deal_filters_won,
                fields=["name"]
            )
        )

        deal_filters_lost = deal_filters.copy()
        deal_filters_lost["deal_status"] = "Lost"

        lost_deals = len(
            frappe.get_list(
                "CRM Deal",
                filters=deal_filters_lost,
                fields=["name"]
            )
        )

        won_deals_list = frappe.get_list(
            "CRM Deal",
            filters=deal_filters_won,
            fields=["deal_value"]
        )

        total_revenue = sum(
            flt(d.deal_value)
            for d in won_deals_list
        )
        total_revenue = sum(flt(d.deal_value) for d in won_deals_list)
        # Source-wise distribution
        source_distribution = {}

        sources = frappe.get_all(
            "CRM Lead",
            filters=source_filters,
            fields=["source"]
        )

        for s in sources:
            src = s.source or "Unknown"
            source_distribution[src] = source_distribution.get(src, 0) + 1

        # -----------------------------
        # Stage Distribution
        # -----------------------------
        stage_distribution = {}

        stage_rows = frappe.get_all(
            "CRM Lead",
            filters=lead_filters,
            fields=["stage"]
        )

        for row in stage_rows:
            stage = row.stage or "Others"
            stage_distribution[stage] = stage_distribution.get(stage, 0) + 1

        if is_web_api_call():
            return {
                "success": True,
                "message": "Dashboard metrics retrieved successfully",
                "data": {
                    "total_leads": total_leads,
                    "new_leads": new_leads,
                    "converted_leads": converted_leads,
                    "won_deals": won_deals,
                    "lost_deals": lost_deals,
                    "total_revenue": float(total_revenue),
                    "stage_distribution": stage_distribution,
                    "source_distribution": source_distribution
                }
            }
        else:
            return {
                "total_leads": total_leads,
                "new_leads": new_leads,
                "converted_leads": converted_leads,
                "won_deals": won_deals,
                "lost_deals": lost_deals,
                "total_revenue": float(total_revenue),
                "stage_distribution": stage_distribution,
                "source_distribution": source_distribution
            }
    except Exception as e:
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to load dashboard metrics", "errors": [str(e)]}

@frappe.whitelist()
def get_pipeline():
    """
    Retrieves full Pipeline configurations and deals in each stage.
    """
    if not frappe.has_permission("CRM Lead", "read") or not frappe.has_permission("CRM Deal", "read"):
        if is_web_api_call():
            return {"success": False, "message": "Permission denied"}
        else:
            frappe.throw(_("Permission denied"), frappe.PermissionError)

    try:
        stages = frappe.get_list("CRM Pipeline Stage", fields=["name", "stage_name", "color", "sort_order"], order_by="sort_order asc")
        
        for stage in stages:
            stage["leads"] = frappe.get_list("CRM Lead", 
                filters={"stage": stage.name},
                fields=["name", "lead_name", "opportunity_value", "user"]
            )
            stage["deals"] = frappe.get_list("CRM Deal",
                filters={"deal_stage": stage.name},
                fields=["name", "deal_name", "deal_value", "deal_status"]
            )
            
        if is_web_api_call():
            return {
                "success": True,
                "message": "Pipeline stages and data loaded successfully",
                "data": {
                    "stages": stages
                }
            }
        else:
            return stages
    except Exception as e:
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to load pipeline structure", "errors": [str(e)]}

@frappe.whitelist()
def get_reports(report_type=None):
    """
    Retrieves report queries.
    """
    if not report_type:
        return {"success": False, "message": "Report Type is required"}

    if not frappe.has_permission("CRM Lead", "read") or not frappe.has_permission("CRM Deal", "read"):
        if is_web_api_call():
            frappe.local.response["http_status_code"] = 403
        return {"success": False, "message": "Permission denied"}

    try:
        if report_type == "Lead":
            leads = frappe.get_list("CRM Lead", fields=["stage"])
            counts = {}
            for l in leads:
                counts[l.stage] = counts.get(l.stage, 0) + 1
            res = [{"stage": k, "count": v} for k, v in counts.items()]
        elif report_type == "Sales":
            deals = frappe.get_list("CRM Deal", fields=["deal_status", "deal_value"])
            sums = {}
            for d in deals:
                sums[d.deal_status] = sums.get(d.deal_status, 0.0) + flt(d.deal_value)
            res = [{"deal_status": k, "total": v} for k, v in sums.items()]
        else:
            res = []

        return {
            "success": True,
            "message": "Reports data loaded successfully",
            "data": {
                "report": res
            }
        }
    except Exception as e:
        return {"success": False, "message": "Failed to generate report", "errors": [str(e)]}

# --- Event Hooks Functions ---

def lead_on_update(doc, method):
    pass

def lead_after_insert(doc, method):
    frappe.get_doc({
        "doctype": "CRM Audit Log",
        "ref_doctype": "CRM Lead",
        "ref_name": doc.name,
        "action": "Create",
        "user": frappe.session.user,
        "details": f"Lead {doc.lead_name} was created."
    }).insert(ignore_permissions=True)

def lead_on_trash(doc, method):
    child_doctypes = [
        "CRM Activity", "CRM Task", "CRM Note", "CRM Meeting", 
        "CRM Reminder", "CRM Call Log", "CRM WhatsApp Log", 
        "CRM Email Log", "CRM Attachment", "CRM Contact", "CRM Deal"
    ]
    for dt in child_doctypes:
        if frappe.db.exists("DocType", dt):
            if frappe.db.exists(dt, {"lead": doc.name}):
                frappe.throw(
                    frappe._("Lead cannot be deleted because activities are attached."),
                    frappe.LinkExistsError
                )


def user_on_trash(doc, method):
    profile_name = frappe.db.get_value("CRM User Profile", {"user": doc.name}, "name")
    if profile_name:
        frappe.delete_doc("CRM User Profile", profile_name, ignore_permissions=True)

def deal_on_update(doc, method):
    pass

def deal_after_insert(doc, method):
    frappe.get_doc({
        "doctype": "CRM Audit Log",
        "ref_doctype": "CRM Deal",
        "ref_name": doc.name,
        "action": "Create",
        "user": frappe.session.user,
        "details": f"Deal {doc.deal_name} was created."
    }).insert(ignore_permissions=True)

# --- Sub-module check lists ---

@frappe.whitelist()
def get_tasks(lead_id):
    """
    Retrieves list of tasks for a given lead.
    """
    if not lead_id:
        return {"success": True, "data": {"tasks": []}}
    if check_injection(lead_id):
        return {"success": False, "message": "Security validation failed"}
    try:
        lead = frappe.get_doc("CRM Lead", lead_id)
        if not frappe.has_permission(lead, "read"):
            return {"success": False, "message": "Permission denied"}
            
        tasks = frappe.get_all("CRM Task",
            filters={"lead": lead_id},
            fields=["name", "task_subject", "due_date", "status", "assigned_to"]
        )
        return {
            "success": True,
            "message": "Tasks retrieved successfully",
            "data": {
                "tasks": tasks
            }
        }
    except Exception as e:
        return {"success": False, "message": "Failed to load tasks", "errors": [str(e)]}

@frappe.whitelist()
def create_task(lead_id, task_subject, due_date=None, status="Open", assigned_to="Administrator"):
    """
    Creates a new CRM Task.
    """
    if not lead_id or not task_subject:
        return {"success": False, "message": "Lead ID and Task Subject are required"}
    if check_injection(lead_id) or check_injection(task_subject) or check_injection(assigned_to):
        return {"success": False, "message": "Security validation failed"}
    try:
        lead = frappe.get_doc("CRM Lead", lead_id)
        if not frappe.has_permission(lead, "write"):
            return {"success": False, "message": "Permission denied"}
            
        task = frappe.get_doc({
            "doctype": "CRM Task",
            "lead": lead_id,
            "task_subject": task_subject,
            "due_date": due_date,
            "status": status,
            "assigned_to": assigned_to
        }).insert()
        frappe.db.commit()
        return {
            "success": True,
            "message": "Task created successfully",
            "data": {"name": task.name}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to create task", "errors": [str(e)]}

@frappe.whitelist()
def delete_task(name=None):
    """
    Deletes a CRM Task.
    """
    if not name:
        return {"success": False, "message": "Task Name/ID is required"}
    try:
        if not frappe.db.exists("CRM Task", name):
            return {"success": False, "message": "Task not found"}
        task = frappe.get_doc("CRM Task", name)
        if not frappe.has_permission(task, "delete"):
            return {"success": False, "message": "Permission denied"}
        if task.lead:
            lead = frappe.get_doc("CRM Lead", task.lead)
            if not frappe.has_permission(lead, "write"):
                return {"success": False, "message": "Permission denied"}
                
        frappe.delete_doc("CRM Task", name)
        frappe.db.commit()
        return {
            "success": True,
            "message": "Task deleted successfully",
            "data": {"name": name}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to delete task", "errors": [str(e)]}

@frappe.whitelist()
def get_crm_settings():
    if not frappe.has_permission("CRM Settings", "read"):
        if is_web_api_call():
            return {"success": False, "message": "Permission denied"}
        else:
            frappe.throw(_("Permission denied"), frappe.PermissionError)
    try:
        doc = frappe.get_doc("CRM Settings")
        settings_data = {
            "company_name": doc.company_name,
            "default_pipeline": doc.default_pipeline,
            "enable_ai_suggestions": doc.enable_ai_suggestions,
            "enable_whatsapp_integration": doc.enable_whatsapp_integration,
            "whatsapp_phone_number_id": doc.whatsapp_phone_number_id
        }
        if is_web_api_call():
            return {
                "success": True,
                "message": "Settings loaded successfully",
                "data": settings_data
            }
        else:
            return settings_data
    except Exception as e:
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to load settings", "errors": [str(e)]}

@frappe.whitelist()
def save_crm_settings(**kwargs):
    if not frappe.has_permission("CRM Settings", "write"):
        if is_web_api_call():
            return {"success": False, "message": "Permission denied"}
        else:
            frappe.throw(_("Permission denied"), frappe.PermissionError)
    try:
        doc = frappe.get_doc("CRM Settings")
        for field in [
            "company_name", "default_pipeline", "enable_ai_suggestions", 
            "enable_whatsapp_integration", "whatsapp_phone_number_id"
        ]:
            if field in kwargs:
                doc.set(field, frappe.utils.cint(kwargs.get(field)) if field in ["enable_ai_suggestions", "enable_whatsapp_integration"] else kwargs.get(field))
        
        # Save secrets securely
        for pwd_field in ["whatsapp_access_token", "facebook_webhook_verify_token", "facebook_app_secret", "facebook_access_token"]:
            if pwd_field in kwargs:
                doc.set(pwd_field, kwargs.get(pwd_field))
                
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.clear_cache(doctype="CRM Settings")
        if is_web_api_call():
            return {
                "success": True,
                "message": "Settings saved successfully",
                "data": {}
            }
        else:
            return {}
    except Exception as e:
        frappe.db.rollback()
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to save settings", "errors": [str(e)]}

@frappe.whitelist()
def get_pipeline_stages():
    if not frappe.has_permission("CRM Pipeline Stage", "read"):
        return {"success": False, "message": "Permission denied"}
    try:
        stages = frappe.get_list("CRM Pipeline Stage", fields=["name", "stage_name", "color", "sort_order", "active", "statuses"], order_by="sort_order asc")
        return {
            "success": True,
            "message": "Pipeline stages loaded successfully",
            "data": {
                "stages": stages
            }
        }
    except Exception as e:
        return {"success": False, "message": "Failed to load stages", "errors": [str(e)]}

@frappe.whitelist()
def save_pipeline_stages(stages_list):
    """
    Saves/Synchronizes the pipeline stages from the frontend.
    """
    if not frappe.has_permission("CRM Pipeline Stage", "write"):
        return {"success": False, "message": "Permission denied"}

    try:
        stages_list = safe_json(stages_list, default=[])
        existing_stages = {s.name: s for s in frappe.get_all("CRM Pipeline Stage", fields=["name"])}
        
        incoming_names = []
        for stage_data in stages_list:
            stage_name = stage_data.get("name")
            stage_color = stage_data.get("color")
            stage_order = stage_data.get("sort_order") or stage_data.get("order") or 0
            stage_id = stage_data.get("id")
            active = stage_data.get("active")
            active_val = 1 if active or active is None else 0
            statuses = stage_data.get("statuses") or []
            statuses_str = json.dumps(statuses)
            
            doc_name = stage_id
            if not doc_name or not frappe.db.exists("CRM Pipeline Stage", doc_name):
                found_name = frappe.db.get_value("CRM Pipeline Stage", {"stage_name": stage_name}, "name")
                doc_name = found_name or stage_id
                
            if doc_name and frappe.db.exists("CRM Pipeline Stage", doc_name):
                stage_doc = frappe.get_doc("CRM Pipeline Stage", doc_name)
                stage_doc.stage_name = stage_name
                stage_doc.color = stage_color
                stage_doc.sort_order = stage_order
                stage_doc.pipeline = "Standard Sales Pipeline"
                stage_doc.active = active_val
                stage_doc.statuses = statuses_str
                stage_doc.save(ignore_permissions=True)
                incoming_names.append(stage_doc.name)
            else:
                stage_doc = frappe.new_doc("CRM Pipeline Stage")
                stage_doc.stage_name = stage_name
                stage_doc.color = stage_color
                stage_doc.sort_order = stage_order
                stage_doc.pipeline = "Standard Sales Pipeline"
                stage_doc.active = active_val
                stage_doc.statuses = statuses_str
                if stage_id:
                    stage_doc.name = stage_id
                stage_doc.insert(ignore_permissions=True)
                incoming_names.append(stage_doc.name)
                
        for name in existing_stages:
            if name not in incoming_names:
                frappe.delete_doc("CRM Pipeline Stage", name, ignore_permissions=True)
                
        frappe.db.commit()
        return {
            "success": True,
            "message": "Pipeline stages saved successfully",
            "data": {}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to save pipeline stages", "errors": [str(e)]}

@frappe.whitelist()
def get_crm_notes(lead_id):
    if not lead_id:
        if is_web_api_call():
            return {"success": True, "data": {"notes": []}}
        else:
            return []
    if check_injection(lead_id):
        if is_web_api_call():
            return {"success": False, "message": "Security validation failed"}
        else:
            frappe.throw(_("Security validation failed"), frappe.ValidationError)
    try:
        lead = frappe.get_doc("CRM Lead", lead_id)
        if not frappe.has_permission(lead, "read"):
            if is_web_api_call():
                return {"success": False, "message": "Permission denied"}
            else:
                frappe.throw(_("Permission denied"), frappe.PermissionError)
            
        notes = frappe.get_all("CRM Note",
            filters={"lead": lead_id},
            fields=["name", "content", "added_by", "creation"]
        )
        if is_web_api_call():
            return {
                "success": True,
                "message": "Notes retrieved successfully",
                "data": {
                    "notes": notes
                }
            }
        else:
            return notes
    except Exception as e:
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to load notes", "errors": [str(e)]}

@frappe.whitelist()
def create_crm_note(lead_id, content):
    if not lead_id or not content:
        if is_web_api_call():
            return {"success": False, "message": "Lead ID and content are required"}
        else:
            frappe.throw(_("Lead ID and content are required"), frappe.ValidationError)
    if check_injection(lead_id) or check_injection(content):
        if is_web_api_call():
            return {"success": False, "message": "Security validation failed"}
        else:
            frappe.throw(_("Security validation failed"), frappe.ValidationError)
    try:
        lead = frappe.get_doc("CRM Lead", lead_id)
        if not frappe.has_permission(lead, "write"):
            if is_web_api_call():
                return {"success": False, "message": "Permission denied"}
            else:
                frappe.throw(_("Permission denied"), frappe.PermissionError)
            
        note = frappe.get_doc({
            "doctype": "CRM Note",
            "lead": lead_id,
            "content": content,
            "added_by": frappe.session.user
        }).insert()
        frappe.db.commit()
        if is_web_api_call():
            return {
                "success": True,
                "message": "Note created successfully",
                "data": {"name": note.name}
            }
        else:
            return note.name
    except Exception as e:
        frappe.db.rollback()
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to create note", "errors": [str(e)]}

@frappe.whitelist()
def delete_crm_note(name=None):
    if not name:
        if is_web_api_call():
            return {"success": False, "message": "Note ID is required"}
        else:
            frappe.throw(_("Note ID is required"), frappe.ValidationError)
    try:
        if not frappe.db.exists("CRM Note", name):
            if is_web_api_call():
                return {"success": False, "message": "Note not found"}
            else:
                frappe.throw(_("Note not found"), frappe.DoesNotExistError)
        note = frappe.get_doc("CRM Note", name)
        if not frappe.has_permission(note, "delete"):
            if is_web_api_call():
                frappe.local.response["http_status_code"] = 403
                return {"success": False, "message": "Permission denied"}
            else:
                frappe.throw(_("Permission denied"), frappe.PermissionError)
        if note.lead:
            lead = frappe.get_doc("CRM Lead", note.lead)
            if not frappe.has_permission(lead, "write"):
                if is_web_api_call():
                    frappe.local.response["http_status_code"] = 403
                    return {"success": False, "message": "Permission denied"}
                else:
                    frappe.throw(_("Permission denied"), frappe.PermissionError)
                
        frappe.delete_doc("CRM Note", name)
        frappe.db.commit()
        if is_web_api_call():
            return {
                "success": True,
                "message": "Note deleted successfully",
                "data": {"name": name}
            }
        else:
            return name
    except Exception as e:
        frappe.db.rollback()
        if not is_web_api_call():
            raise
        return {"success": False, "message": "Failed to delete note", "errors": [str(e)]}

@frappe.whitelist()
def save_lead_sources(sources_list):
    if not frappe.has_permission("CRM Settings", "write"):
        return {"success": False, "message": "Permission denied"}
    try:
        frappe.db.set_single_value("CRM Settings", "lead_sources", sources_list)
        frappe.db.commit()
        return {
            "success": True,
            "message": "Lead sources saved successfully",
            "data": {}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to save lead sources", "errors": [str(e)]}

# --- Phase 2 API Aliases & Implementations ---

@frappe.whitelist()
def get_notes(lead_id):
    return get_crm_notes(lead_id)

@frappe.whitelist()
def create_note(lead_id, content):
    return create_crm_note(lead_id, content)

@frappe.whitelist()
def update_note(name=None, content=None):
    if not name:
        return {"success": False, "message": "Note ID is required"}
    try:
        if not frappe.db.exists("CRM Note", name):
            return {"success": False, "message": "Note not found"}
        note = frappe.get_doc("CRM Note", name)
        if not frappe.has_permission(note, "write"):
            return {"success": False, "message": "Permission denied"}
        if note.lead:
            lead = frappe.get_doc("CRM Lead", note.lead)
            if not frappe.has_permission(lead, "write"):
                return {"success": False, "message": "Permission denied"}
        note.content = content
        note.save()
        frappe.db.commit()
        return {
            "success": True,
            "message": "Note updated successfully",
            "data": {"name": note.name}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to update note", "errors": [str(e)]}

@frappe.whitelist()
def delete_note(name=None):
    return delete_crm_note(name)

@frappe.whitelist()
def update_task(name, **kwargs):
    if not name:
        return {"success": False, "message": "Task ID is required"}
    try:
        if not frappe.db.exists("CRM Task", name):
            return {"success": False, "message": "Task not found"}
        task = frappe.get_doc("CRM Task", name)
        if not frappe.has_permission(task, "write"):
            return {"success": False, "message": "Permission denied"}
        if task.lead:
            lead = frappe.get_doc("CRM Lead", task.lead)
            if not frappe.has_permission(lead, "write"):
                return {"success": False, "message": "Permission denied"}
        for field in ["task_subject", "due_date", "status", "assigned_to"]:
            if field in kwargs:
                task.set(field, kwargs.get(field))
        task.save()
        frappe.db.commit()
        return {
            "success": True,
            "message": "Task updated successfully",
            "data": {"name": task.name}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to update task", "errors": [str(e)]}

@frappe.whitelist()
def get_users():
    try:
        from crm_pro.api_auth import get_users_list
        users = get_users_list()
        return {
            "success": True,
            "message": "Users retrieved successfully",
            "data": {
                "users": users
            }
        }
    except Exception as e:
        return {"success": False, "message": "Failed to retrieve users", "errors": [str(e)]}

@frappe.whitelist()
def create_user(username, email, password, fullname=None, mobile=None, role="Sales Executive"):
    from crm_pro.api_auth import validate_password_complexity, save_password_to_history, log_audit_event
    from frappe.utils.password import update_password

    # Map client-visible role names to database role names
    if role == "Admin":
        role = "CRM Admin"
    elif role == "User":
        role = "Sales Executive"

    current_user_roles = frappe.get_roles(frappe.session.user)
    is_crm_admin = "CRM Admin" in current_user_roles or frappe.session.user == "Administrator"

    # Strict role validation: Only CRM Admin can create users
    if not is_crm_admin:
        if is_web_api_call():
            return {
                "success": False,
                "message": "Permission denied",
                "errors": ["Only CRM Admin can create users"]
            }
        else:
            frappe.throw(_("Only CRM Admin can create users"), frappe.PermissionError)

    # Prevent role escalation
    if role == "System Manager" and "System Manager" not in current_user_roles:
        if is_web_api_call():
            return {
                "success": False,
                "message": "Permission denied",
                "errors": ["You cannot assign the System Manager role unless you have it yourself."]
            }
        else:
            frappe.throw(_("You cannot assign the System Manager role unless you have it yourself."), frappe.PermissionError)
    if role == "CRM Admin" and not is_crm_admin:
        if is_web_api_call():
            return {
                "success": False,
                "message": "Permission denied",
                "errors": ["You cannot assign the CRM Admin role unless you have it yourself."]
            }
        else:
            frappe.throw(_("You cannot assign the CRM Admin role unless you have it yourself."), frappe.PermissionError)

    # Password complexity check
    complexity_err = validate_password_complexity(password)
    if complexity_err:
        if is_web_api_call():
            return {
                "success": False,
                "message": "Validation failed",
                "errors": [complexity_err]
            }
        else:
            frappe.throw(_(complexity_err), frappe.ValidationError)

    if frappe.db.exists("User", email):
        return {"success": False, "message": "A user with this email already exists"}
    
    if not role or not frappe.db.exists("Role", role):
        if frappe.db.exists("Role", "Sales Executive"):
            role = "Sales Executive"
        else:
            return {"success": False, "message": f"Role {role} does not exist"}

    try:
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": fullname or username,
            "mobile_no": mobile or "",
            "enabled": 1,
            "send_welcome_email": 0
        })
        user.append("roles", {"role": role})
        user.insert(ignore_permissions=True)
        update_password(user.name, password)
        
        profile = frappe.get_doc({
            "doctype": "CRM User Profile",
            "user": user.name,
            "phone_number": mobile or "",
            "designation": role
        })
        profile.insert(ignore_permissions=True)
        frappe.db.commit()
        
        save_password_to_history(user.name, password)
        log_audit_event("User", user.name, "Create", "User created via API.")
        return {
            "success": True,
            "message": "User created successfully",
            "data": {"user_id": user.name}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to create user", "errors": [str(e)]}

@frappe.whitelist()
def update_user(user_email, **kwargs):
    try:
        from crm_pro.api_auth import update_user_profile
        res = update_user_profile(
            user_email=user_email,
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            mobile=kwargs.get("mobile"),
            designation=kwargs.get("designation"),
            department=kwargs.get("department")
        )
        return {
            "success": True,
            "message": "User profile updated successfully",
            "data": res
        }
    except Exception as e:
        return {"success": False, "message": "Failed to update user profile", "errors": [str(e)]}

@frappe.whitelist()
def delete_user(user_email):
    try:
        from crm_pro.api_auth import delete_user_profile
        res = delete_user_profile(user_email)
        return {
            "success": True,
            "message": "User profile deleted successfully",
            "data": res
        }
    except Exception as e:
        return {"success": False, "message": "Failed to delete user profile", "errors": [str(e)]}

@frappe.whitelist()
def create_pipeline_stage(stage_name, color=None, order=0, active=1, statuses=None, **kwargs):
    if not stage_name:
        return {"success": False, "message": "Stage Name is required"}
    if not frappe.has_permission("CRM Pipeline Stage", "write"):
        return {"success": False, "message": "Permission denied"}
    
    try:
        stage = frappe.new_doc("CRM Pipeline Stage")
        stage.stage_name = stage_name
        stage.color = color or "#cbd5e1"
        stage.sort_order = kwargs.get("sort_order") or order
        stage.pipeline = "Standard Sales Pipeline"
        stage.active = active
        stage.statuses = json.dumps(statuses or [])
        stage.insert(ignore_permissions=True)
        frappe.db.commit()
        return {
            "success": True,
            "message": "Pipeline stage created successfully",
            "data": {"name": stage.name}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to create stage", "errors": [str(e)]}

@frappe.whitelist()
def update_pipeline_stage(name=None, **kwargs):
    if not name:
        return {"success": False, "message": "Stage Name/ID is required"}
    if not frappe.has_permission("CRM Pipeline Stage", "write"):
        return {"success": False, "message": "Permission denied"}
    
    try:
        stage = frappe.get_doc("CRM Pipeline Stage", name)
        for field in ["stage_name", "color", "sort_order", "active"]:
            if field in kwargs:
                stage.set(field, kwargs.get(field))
        if "order" in kwargs and "sort_order" not in kwargs:
            stage.sort_order = kwargs.get("order")
        if "statuses" in kwargs:
            stage.statuses = json.dumps(kwargs.get("statuses") or [])
        stage.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            "success": True,
            "message": "Pipeline stage updated successfully",
            "data": {"name": stage.name}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to update stage", "errors": [str(e)]}

@frappe.whitelist()
def delete_pipeline_stage(name=None):
    if not name:
        return {"success": False, "message": "Stage Name/ID is required"}
    if not frappe.has_permission("CRM Pipeline Stage", "delete"):
        return {"success": False, "message": "Permission denied"}
    
    try:
        frappe.delete_doc("CRM Pipeline Stage", name, ignore_permissions=True)
        frappe.db.commit()
        return {
            "success": True,
            "message": "Pipeline stage deleted successfully",
            "data": {"name": name}
        }
    except Exception as e:
        frappe.db.rollback()
        return {"success": False, "message": "Failed to delete stage", "errors": [str(e)]}

@frappe.whitelist()
def get_settings():
    return get_crm_settings()

@frappe.whitelist()
def update_settings(**kwargs):
    return save_crm_settings(**kwargs)

@frappe.whitelist()
def test_whitelist():
    return "OK"

@frappe.whitelist()
def get_recent_leads(limit=10):

    try:

        leads = frappe.get_all(
            "CRM Lead",
            fields=[
                "name",
                "lead_name",
                "mobile",
                "stage",
                "source",
                "owner",
                "creation"
            ],
            order_by="creation desc",
            limit=int(limit)
        )

        return {
            "success": True,
            "message": "Recent leads retrieved successfully",
            "data": {
                "recent_leads": leads
            }
        }

    except Exception as e:

        frappe.log_error(frappe.get_traceback(), "Recent Leads API")

        return {
            "success": False,
            "message": str(e)
        }
