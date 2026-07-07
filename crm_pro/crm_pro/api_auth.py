import logging
import frappe
import json
import re
import secrets
import time
from datetime import datetime, timedelta
from werkzeug.wrappers import Response
from frappe import _
from frappe.utils.password import check_password, update_password, passlibctx
from crm_pro.crm_pro.utils.safe_json import safe_json

# Setup logger
logger = frappe.logger("crm_pro")

# Constants
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 1800 # 30 minutes
RATE_LIMIT_PER_MINUTE = 60

# --- Request Context Helper ---
def ensure_request_context():
    has_request = False
    try:
        if getattr(frappe.local, "request", None) and frappe.local.request.path:
            has_request = True
    except RuntimeError:
        pass
        
    if not has_request:
        class DummyRequest:
            def __init__(self):
                self.path = "/api/login"
                self.method = "POST"
                self.host = "localhost"
                self.scheme = "http"
                self.remote_addr = "127.0.0.1"
                self.headers = {}
                self.environ = {}
                self.data = b""
                self.cookies = {}
        frappe.local.request = DummyRequest()
        
    if not getattr(frappe.local, "cookie_manager", None):
        from frappe.auth import CookieManager
        frappe.local.cookie_manager = CookieManager()

# --- Response Helper ---
def json_response(data, status=200):
    return Response(
        json.dumps(data, default=str),
        mimetype="application/json",
        status=status
    )

# --- Rate Limiter ---
def check_rate_limit(action_name, limit=RATE_LIMIT_PER_MINUTE, window=60):
    ip = frappe.local.request_ip or "127.0.0.1"
    cache_key = f"rate_limit:{action_name}:{ip}"
    
    now = time.time()
    timestamps = frappe.cache().get_value(cache_key) or []
    # Clean up old timestamps
    timestamps = [t for t in timestamps if now - t < window]
    
    if len(timestamps) >= limit:
        return False
        
    timestamps.append(now)
    frappe.cache().set_value(cache_key, timestamps, expires_in_sec=window)
    return True

# --- Lockout Helpers ---
def is_account_locked(email):
    lock_key = f"login_lockout:{email}"
    full_lock_key = frappe.cache().make_key(lock_key)
    if hasattr(frappe.local, "cache") and full_lock_key in frappe.local.cache:
        del frappe.local.cache[full_lock_key]
    return bool(frappe.cache().get_value(lock_key))

def get_lockout_remaining(email):
    return LOCKOUT_DURATION_SECONDS

def record_failed_login(email):
    count_key = f"login_failed_count:{email}"
    full_key = frappe.cache().make_key(count_key)
    if hasattr(frappe.local, "cache") and full_key in frappe.local.cache:
        del frappe.local.cache[full_key]
        
    count = frappe.cache().get_value(count_key) or 0
    count += 1
    
    if count >= MAX_FAILED_ATTEMPTS:
        lock_key = f"login_lockout:{email}"
        full_lock_key = frappe.cache().make_key(lock_key)
        if hasattr(frappe.local, "cache") and full_lock_key in frappe.local.cache:
            del frappe.local.cache[full_lock_key]
            
        frappe.cache().set_value(lock_key, 1, expires_in_sec=LOCKOUT_DURATION_SECONDS)
        frappe.cache().delete_value(count_key)
        if hasattr(frappe.local, "cache") and full_key in frappe.local.cache:
            del frappe.local.cache[full_key]
            
        # Log to CRM Audit Log
        log_audit_event("User", email, "Update", f"Account locked due to {MAX_FAILED_ATTEMPTS} failed attempts.")
    else:
        frappe.cache().set_value(count_key, count, expires_in_sec=86400)
        if hasattr(frappe.local, "cache") and full_key in frappe.local.cache:
            del frappe.local.cache[full_key]

def reset_failed_login(email):
    count_key = f"login_failed_count:{email}"
    lock_key = f"login_lockout:{email}"
    frappe.cache().delete_value(count_key)
    frappe.cache().delete_value(lock_key)
    for k in [count_key, lock_key]:
        fk = frappe.cache().make_key(k)
        if hasattr(frappe.local, "cache") and fk in frappe.local.cache:
            del frappe.local.cache[fk]

# --- Audit Log Helper ---
def log_audit_event(ref_doctype, ref_name, action, details):
    try:
        frappe.get_doc({
            "doctype": "CRM Audit Log",
            "ref_doctype": ref_doctype,
            "ref_name": ref_name,
            "action": action,
            "user": frappe.session.user or "Guest",
            "details": details
        }).insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        logger.error(f"Failed to write CRM Audit Log: {str(e)}")

# --- Password Policy Validation ---
def validate_password_complexity(password):
    if len(password) < 12:
        return "Password must be at least 12 characters long."
    if not any(c.islower() for c in password):
        return "Password must contain at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number."
    if not any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?/' for c in password):
        return "Password must contain at least one special character."
    return None

def validate_password(password, user=None):
    err = validate_password_complexity(password)
    if err:
        frappe.throw(err, frappe.ValidationError)


def check_password_history(email, new_password):
    profile_name = frappe.db.get_value("CRM User Profile", {"user": email}, "name")
    if not profile_name:
        return None
        
    profile = frappe.get_doc("CRM User Profile", profile_name)
    history_str = profile.password_history or "[]"
    history = safe_json(history_str, default=[])
        
    for pwd_hash in history:
        if passlibctx.verify(new_password, pwd_hash):
            return "Password must not match any of your last 5 passwords."
            
    return None

def save_password_to_history(email, password):
    profile_name = frappe.db.get_value("CRM User Profile", {"user": email}, "name")
    if not profile_name:
        return
        
    profile = frappe.get_doc("CRM User Profile", profile_name)
    history_str = profile.password_history or "[]"
    history = safe_json(history_str, default=[])
        
    new_hash = passlibctx.hash(password)
    history.insert(0, new_hash)
    history = history[:5]
    profile.password_history = json.dumps(history)
    profile.save(ignore_permissions=True)
    frappe.db.commit()

# --- Custom Authentication Middleware ---
def check_bearer_token():
    ensure_request_context()
    auth_header = frappe.get_request_header("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        sid = auth_header.split(" ", 1)[1].strip()
        res = frappe.db.sql("select user from tabSessions where sid=%s", (sid,))
        if res:
            username = res[0][0]
            # Save current request parameters before set_user wipes them
            saved_form_dict = frappe.form_dict.copy()
            frappe.set_user(username)
            # Restore the parameters and set sid
            frappe.form_dict.update(saved_form_dict)
            frappe.form_dict.sid = sid
            frappe.local.session.sid = sid
            frappe.local.session.user = username
            from frappe.sessions import Session
            frappe.local.session_obj = Session(user=username, resume=True)
            frappe.local.session = frappe.local.session_obj.data

# --- Werkzeug Router Patching ---
_routes_patched = False

def patch_api_routes():
    global _routes_patched
    if _routes_patched:
        return
    try:
        from frappe.api import API_URL_MAP
        from werkzeug.routing import Rule
        
        # Add rules mapping directly to custom endpoint functions
        API_URL_MAP.add(Rule("/api/register", methods=["POST"], endpoint=register_endpoint))
        API_URL_MAP.add(Rule("/api/login", methods=["POST"], endpoint=login_endpoint))
        API_URL_MAP.add(Rule("/api/logout", methods=["POST"], endpoint=logout_endpoint))
        API_URL_MAP.add(Rule("/api/change-password", methods=["POST"], endpoint=change_password_endpoint))
        API_URL_MAP.add(Rule("/api/forgot-password", methods=["POST"], endpoint=forgot_password_endpoint))
        API_URL_MAP.add(Rule("/api/reset-password", methods=["POST"], endpoint=reset_password_endpoint))
        API_URL_MAP.add(Rule("/api/profile", methods=["GET", "PUT"], endpoint=profile_endpoint))
        API_URL_MAP.add(Rule("/api/profile/upload-avatar", methods=["POST"], endpoint=upload_avatar_endpoint))
        API_URL_MAP.add(Rule("/api/profile/update-mobile", methods=["POST"], endpoint=update_mobile_endpoint))
        API_URL_MAP.add(Rule("/api/profile/update-email", methods=["POST"], endpoint=update_email_endpoint))
        
        _routes_patched = True
    except Exception as e:
        logger.error(f"Error patching routes: {str(e)}")

# --- Endpoints ---

def register_endpoint():
    ensure_request_context()
    if not check_rate_limit("register"):
        return json_response({"success": False, "message": "Too many requests. Try again later."}, 429)
        
    current_roles = frappe.get_roles(frappe.session.user)
    is_crm_admin = "CRM Admin" in current_roles or frappe.session.user == "Administrator"
    if not is_crm_admin:
        return json_response({
            "success": False,
            "message": "Permission denied",
            "errors": ["Only CRM Admin can create users"]
        }, 403)
        
    data = frappe.form_dict

    print("FORM DATA:", frappe.form_dict)
    print("REQUEST DATA:", frappe.request.get_data())
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    mobile_no = data.get("mobile_no")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    
    if not all([first_name, email, password, confirm_password]):
        return json_response({"success": False, "message": "Missing required fields"}, 400)
        
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return json_response({"success": False, "message": "Invalid email format"}, 400)
        
    if password != confirm_password:
        return json_response({"success": False, "message": "Password confirmation does not match"}, 400)
        
    # Complexity Check
    complexity_err = validate_password_complexity(password)
    if complexity_err:
        return json_response({"success": False, "message": complexity_err}, 400)
        
    # Duplicate Checks
    if frappe.db.exists("User", email):
        return json_response({"success": False, "message": "A user with this email already exists"}, 400)
        
    if mobile_no:
        if frappe.db.exists("User", {"mobile_no": mobile_no}) or frappe.db.exists("CRM User Profile", {"phone_number": mobile_no}):
            return json_response({"success": False, "message": "A user with this mobile number already exists"}, 400)
            
    # Create User
    try:
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name or "",
            "mobile_no": mobile_no or "",
            "enabled": 1,
            "send_welcome_email": 0
        })
        # Add default role "Sales Executive"
        user.append("roles", {
            "role": "Sales Executive"
        })
        user.insert(ignore_permissions=True)
        update_password(user.name, password)
        
        # Create CRM User Profile
        profile = frappe.get_doc({
            "doctype": "CRM User Profile",
            "user": user.name,
            "phone_number": mobile_no or "",
            "designation": "Sales Executive"
        })
        profile.insert(ignore_permissions=True)
        frappe.db.commit()
        
        save_password_to_history(user.name, password)
        log_audit_event("User", user.name, "Create", "User registered successfully.")
        
        return json_response({
            "success": True,
            "user_id": user.name,
            "message": "Registration successful"
        }, 200)
    except Exception as e:
        return json_response({"success": False, "message": f"Registration failed: {str(e)}"}, 500)
import frappe

@frappe.whitelist(allow_guest=True)
def login_endpoint():
    ensure_request_context()

    if not check_rate_limit("login"):
        return json_response({"success": False, "message": "Too many requests"}, 429)

    data = frappe.form_dict
    login = (data.get("username") or data.get("email") or "").strip()
    password = data.get("password")
    role = (data.get("role") or "").strip()

    if not login or not password:
        return json_response({"success": False, "message": "Missing credentials"}, 400)



    try:

        user_email = login

        # Username -> Email
        if "@" not in login:

            # First try CRM User Profile
            profile = frappe.db.get_value(
                "CRM User Profile",
                {"username": login},
                "user"
            )

            if profile:
                user_email = profile
            else:
                # Fallback to Frappe User
                if frappe.db.exists("User", login):
                    user_email = login
                else:
                    raise frappe.AuthenticationError

        # Password Check
        check_password(user_email, password)

        # Login
        login_manager = frappe.auth.LoginManager()
        login_manager.user = user_email
        login_manager.post_login()

        user_doc = frappe.get_doc("User", user_email)

        return json_response({
            "success": True,
            "token": frappe.session.sid,
            "user": {
                "email": user_doc.email,
                "first_name": user_doc.first_name,
                "roles": frappe.get_roles(user_email)
            }
        }, 200)

    except frappe.AuthenticationError:
        return json_response({
            "success": False,
            "message": "Invalid credentials"
        }, 401)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Login Endpoint")
        return json_response({
            "success": False,
            "message": f"Login failed: {str(e)}"
        }, 500)





def logout_endpoint():
    ensure_request_context()
    if frappe.session.user == "Guest":
        return json_response({"success": False, "message": "Authentication required"}, 401)
        
    try:
        email = frappe.session.user
        frappe.local.login_manager.logout()
        log_audit_event("User", email, "Update", "User logged out successfully.")
        return json_response({"success": True, "message": "Logged out successfully"}, 200)
    except Exception as e:
        return json_response({"success": False, "message": f"Logout failed: {str(e)}"}, 500)


def change_password_endpoint():
    ensure_request_context()
    if frappe.session.user == "Guest":
        return json_response({"success": False, "message": "Authentication required"}, 401)
        
    data = frappe.form_dict
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    
    if not old_password or not new_password:
        return json_response({"success": False, "message": "Missing password fields"}, 400)
        
    email = frappe.session.user
    
    try:
        # Verify old password
        check_password(email, old_password)
    except frappe.AuthenticationError:
        return json_response({"success": False, "message": "Current password is incorrect"}, 400)
        
    # Complexity Check
    complexity_err = validate_password_complexity(new_password)
    if complexity_err:
        return json_response({"success": False, "message": complexity_err}, 400)
        
    # History Check
    history_err = check_password_history(email, new_password)
    if history_err:
        return json_response({"success": False, "message": history_err}, 400)
        
    try:
        update_password(email, new_password)
        save_password_to_history(email, new_password)
        log_audit_event("User", email, "Update", "Password changed successfully.")
        return json_response({"success": True, "message": "Password changed successfully"}, 200)
    except Exception as e:
        return json_response({"success": False, "message": f"Failed to change password: {str(e)}"}, 500)


def forgot_password_endpoint():
    ensure_request_context()
    data = frappe.form_dict
    email = data.get("email")
    
    if not email:
        return json_response({"success": False, "message": "Missing email"}, 400)
        
    if not frappe.db.exists("User", email):
        return json_response({"success": True, "message": "If the email exists, a reset code has been sent."}, 200)
        
    try:
        token = secrets.token_hex(16)
        
        # Use Redis for reset token storing (highly secure and self-expiring!)
        frappe.cache().set_value(f"pwd_reset_token:{token}", email, expires_in_sec=3600)
        
        # Return success with token (in dev/test environments)
        log_audit_event("User", email, "Update", "Password reset request initiated.")
        resp = {
            "success": True,
            "message": "If the email exists, a reset code has been sent."
        }
        if frappe.conf.get("developer_mode") or frappe.flags.in_test:
            resp["token"] = token
        return json_response(resp, 200)
    except Exception as e:
        return json_response({"success": False, "message": f"Forgot password failed: {str(e)}"}, 500)


def reset_password_endpoint():
    ensure_request_context()
    data = frappe.form_dict
    token = data.get("token")
    new_password = data.get("new_password")
    
    if not token or not new_password:
        return json_response({"success": False, "message": "Missing token or password"}, 400)
        
    email = frappe.cache().get_value(f"pwd_reset_token:{token}")
    if not email:
        return json_response({"success": False, "message": "Invalid or expired reset token"}, 400)
        
    # Complexity Check
    complexity_err = validate_password_complexity(new_password)
    if complexity_err:
        return json_response({"success": False, "message": complexity_err}, 400)
        
    # History Check
    history_err = check_password_history(email, new_password)
    if history_err:
        return json_response({"success": False, "message": history_err}, 400)
        
    try:
        update_password(email, new_password)
        save_password_to_history(email, new_password)
        frappe.cache().delete_value(f"pwd_reset_token:{token}")
        log_audit_event("User", email, "Update", "Password reset successfully completed.")
        return json_response({"success": True, "message": "Password reset successfully"}, 200)
    except Exception as e:
        return json_response({"success": False, "message": f"Password reset failed: {str(e)}"}, 500)


def profile_endpoint():
    ensure_request_context()
    if frappe.session.user == "Guest":
        return json_response({"success": False, "message": "Authentication required"}, 401)
        
    email = frappe.session.user
    
    # Check request method safely
    req_method = "GET"
    if frappe.request and getattr(frappe.request, "method", None):
        req_method = frappe.request.method
        
    if req_method == "GET":
        try:
            user_doc = frappe.get_doc("User", email)
            profile_name = frappe.db.get_value("CRM User Profile", {"user": email}, "name")
            profile_doc = frappe.get_doc("CRM User Profile", profile_name) if profile_name else None
            
            return json_response({
                "success": True,
                "profile": {
                    "name": f"{user_doc.first_name} {user_doc.last_name or ''}".strip(),
                    "email": user_doc.email,
                    "mobile": user_doc.mobile_no or (profile_doc.phone_number if profile_doc else ""),
                    "avatar": user_doc.user_image or (profile_doc.profile_picture if profile_doc else ""),
                    "department": profile_doc.department if profile_doc else "",
                    "designation": profile_doc.designation if profile_doc else ""
                }
            }, 200)
        except Exception as e:
            return json_response({"success": False, "message": f"Failed to retrieve profile: {str(e)}"}, 500)
            
    elif req_method == "PUT":
        data = frappe.form_dict
        name = data.get("name")
        mobile = data.get("mobile")
        avatar = data.get("avatar")
        department = data.get("department")
        designation = data.get("designation")
        
        try:
            user_doc = frappe.get_doc("User", email)
            profile_name = frappe.db.get_value("CRM User Profile", {"user": email}, "name")
            if not profile_name:
                # Autocreate profile if missing
                profile_doc = frappe.get_doc({"doctype": "CRM User Profile", "user": email})
                profile_doc.insert(ignore_permissions=True)
            else:
                profile_doc = frappe.get_doc("CRM User Profile", profile_name)
                
            if name:
                names = name.split(" ", 1)
                user_doc.first_name = names[0]
                user_doc.last_name = names[1] if len(names) > 1 else ""
            if mobile:
                # Duplicate check
                if frappe.db.sql("select name from tabUser where mobile_no=%s and name!=%s", (mobile, email)):
                    return json_response({"success": False, "message": "Mobile number already in use"}, 400)
                user_doc.mobile_no = mobile
                profile_doc.phone_number = mobile
            if avatar:
                user_doc.user_image = avatar
                profile_doc.profile_picture = avatar
            if department:
                profile_doc.department = department
            if designation and designation != profile_doc.designation:
                allowed_roles = ["CRM Admin", "System Manager"]
                is_admin = any(role in frappe.get_roles(frappe.session.user) for role in allowed_roles)
                if not is_admin:
                    return json_response({"success": False, "message": "Not permitted to change user designation"}, 403)
                profile_doc.designation = designation

                
            user_doc.save(ignore_permissions=True)
            profile_doc.save(ignore_permissions=True)
            frappe.db.commit()
            
            log_audit_event("User", email, "Update", "Profile updated successfully.")
            return json_response({"success": True, "message": "Profile updated successfully"}, 200)
        except Exception as e:
            return json_response({"success": False, "message": f"Failed to update profile: {str(e)}"}, 500)


def upload_avatar_endpoint():
    ensure_request_context()
    if frappe.session.user == "Guest":
        return json_response({"success": False, "message": "Authentication required"}, 401)
        
    data = frappe.form_dict
    file_url = data.get("file_url")
    
    if not file_url:
        return json_response({"success": False, "message": "Missing file_url"}, 400)
        
    email = frappe.session.user
    
    try:
        user_doc = frappe.get_doc("User", email)
        profile_name = frappe.db.get_value("CRM User Profile", {"user": email}, "name")
        
        user_doc.user_image = file_url
        user_doc.save(ignore_permissions=True)
        
        if profile_name:
            frappe.db.set_value("CRM User Profile", profile_name, "profile_picture", file_url)
            
        frappe.db.commit()
        log_audit_event("User", email, "Update", "Profile avatar uploaded successfully.")
        return json_response({"success": True, "message": "Avatar updated successfully", "avatar": file_url}, 200)
    except Exception as e:
        return json_response({"success": False, "message": f"Failed to upload avatar: {str(e)}"}, 500)


def update_mobile_endpoint():
    ensure_request_context()
    if frappe.session.user == "Guest":
        return json_response({"success": False, "message": "Authentication required"}, 401)
        
    data = frappe.form_dict
    mobile = data.get("mobile")
    
    if not mobile:
        return json_response({"success": False, "message": "Missing mobile number"}, 400)
        
    email = frappe.session.user
    
    # Duplicate check
    if frappe.db.sql("select name from tabUser where mobile_no=%s and name!=%s", (mobile, email)):
        return json_response({"success": False, "message": "Mobile number already in use"}, 400)
        
    try:
        user_doc = frappe.get_doc("User", email)
        profile_name = frappe.db.get_value("CRM User Profile", {"user": email}, "name")
        
        user_doc.mobile_no = mobile
        user_doc.save(ignore_permissions=True)
        
        if profile_name:
            profile_doc = frappe.get_doc("CRM User Profile", profile_name)
            profile_doc.phone_number = mobile
            profile_doc.save(ignore_permissions=True)
            
        frappe.db.commit()
        log_audit_event("User", email, "Update", "Mobile number updated successfully.")
        return json_response({"success": True, "message": "Mobile number updated successfully"}, 200)
    except Exception as e:
        return json_response({"success": False, "message": f"Failed to update mobile: {str(e)}"}, 500)


def update_email_endpoint():
    ensure_request_context()
    if frappe.session.user == "Guest":
        return json_response({"success": False, "message": "Authentication required"}, 401)
        
    data = frappe.form_dict
    new_email = data.get("new_email")
    
    if not new_email:
        return json_response({"success": False, "message": "Missing new email"}, 400)
        
    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
        return json_response({"success": False, "message": "Invalid email format"}, 400)
        
    email = frappe.session.user
    
    if frappe.db.exists("User", new_email):
        return json_response({"success": False, "message": "Email already in use"}, 400)
        
    try:
        frappe.rename_doc("User", email, new_email, force=True)
        user_doc = frappe.get_doc("User", new_email)
        user_doc.email = new_email
        user_doc.save(ignore_permissions=True)
        
        profile_name = frappe.db.get_value("CRM User Profile", {"user": new_email}, "name")
        if profile_name:
            frappe.db.set_value("CRM User Profile", profile_name, "user", new_email)
            
        frappe.db.commit()
        
        frappe.set_user(new_email)
        frappe.local.session.user = new_email
        
        log_audit_event("User", new_email, "Update", f"Email address changed from {email} to {new_email}.")
        return json_response({"success": True, "message": "Email address updated successfully"}, 200)
    except Exception as e:
        return json_response({"success": False, "message": f"Failed to update email: {str(e)}"}, 500)


@frappe.whitelist()
def get_users_list():
    """
    Returns list of all active CRM Users.
    """
    if not frappe.has_permission("CRM User Profile", "read"):
        frappe.throw(_("Not permitted to view CRM Users"), frappe.PermissionError)

    profiles = frappe.get_all("CRM User Profile", fields=["user", "phone_number", "designation", "department", "profile_picture"])
    user_details = {p.user: p for p in profiles}
    
    users = frappe.get_all("User", 
        filters={"enabled": 1, "user_type": "System User"},
        fields=["name", "first_name", "last_name", "mobile_no", "email"]
    )
    
    results = []
    for u in users:
        p = user_details.get(u.name)
        raw_designation = p.designation if p else ""
        if raw_designation in ["CRM Admin", "System Manager", "Administrator", "Admin"]:
            designation = "Admin"
        else:
            designation = "User"
        results.append({
            "email": u.email or u.name,
            "first_name": u.first_name or "",
            "last_name": u.last_name or "",
            "mobile": u.mobile_no or (p.phone_number if p else ""),
            "designation": designation,
            "department": p.department if p else "",
            "avatar": (p.profile_picture if p else "") or ""
        })
        
    return results

@frappe.whitelist()
def update_user_profile(user_email, first_name=None, last_name=None, mobile=None, designation=None, department=None):
    if not user_email:
        return {
            "success": False,
            "message": "Validation failed",
            "errors": ["User email is required"]
        }

    if not frappe.db.exists("User", user_email):
        return {
            "success": False,
            "message": "Validation failed",
            "errors": ["User not found"]
        }

    current_roles = frappe.get_roles(frappe.session.user)
    is_crm_admin = "CRM Admin" in current_roles or frappe.session.user == "Administrator"

    # Only CRM Admin can edit other users
    if not is_crm_admin and frappe.session.user != user_email:
        return {
            "success": False,
            "message": "Permission denied",
            "errors": ["Only CRM Admin can update other users"]
        }

    # Normal users cannot change designation/roles
    if designation is not None and not is_crm_admin:
        return {
            "success": False,
            "message": "Permission denied",
            "errors": ["Only CRM Admin can change designation"]
        }
        
    user_doc = frappe.get_doc("User", user_email)
    if first_name is not None:
        user_doc.first_name = first_name
    if last_name is not None:
        user_doc.last_name = last_name
    if mobile is not None:
        user_doc.mobile_no = mobile
    user_doc.save(ignore_permissions=True)
    
    profile_name = frappe.db.get_value("CRM User Profile", {"user": user_email}, "name")
    if not profile_name:
        profile_doc = frappe.new_doc("CRM User Profile")
        profile_doc.user = user_email
    else:
        profile_doc = frappe.get_doc("CRM User Profile", profile_name)
        
    if mobile is not None:
        profile_doc.phone_number = mobile
    if designation is not None:
        if designation == "Admin":
            designation = "CRM Admin"
        elif designation == "User":
            designation = "Sales Executive"
        profile_doc.designation = designation
    if department is not None:
        profile_doc.department = department
        
    profile_doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {
        "success": True,
        "status": "success",
        "message": "Profile updated successfully"
    }

@frappe.whitelist()
def delete_user_profile(user_email):
    current_roles = frappe.get_roles(frappe.session.user)
    is_crm_admin = "CRM Admin" in current_roles or frappe.session.user == "Administrator"

    if not is_crm_admin:
        return {
            "success": False,
            "message": "Permission denied",
            "errors": ["Only CRM Admin can delete users"]
        }

    if not user_email:
        return {
            "success": False,
            "message": "Validation failed",
            "errors": ["User email is required"]
        }

    if not frappe.db.exists("User", user_email):
        return {
            "success": False,
            "message": "Validation failed",
            "errors": ["User not found"]
        }

    admin_email = frappe.db.get_value("User", "Administrator", "email")
    if user_email == "Administrator" or (admin_email and user_email == admin_email):
        return {
            "success": False,
            "message": "Permission denied",
            "errors": ["Administrator account can never be deleted"]
        }

    profile_name = frappe.db.get_value(
        "CRM User Profile",
        {"user": user_email},
        "name"
    )

    if profile_name:
        frappe.delete_doc(
            "CRM User Profile",
            profile_name,
            ignore_permissions=True
        )

    frappe.delete_doc(
        "User",
        user_email,
        ignore_permissions=True
    )

    frappe.db.commit()

    return {
        "success": True,
        "status": "success",
        "deleted_user": user_email,
        "message": "User profile deleted successfully"
    }

@frappe.whitelist()
def get_login_activities():
    """
    Returns login/logout activity logs for the current user from CRM Audit Log.
    """
    user_email = frappe.session.user
    if not user_email or user_email == "Guest":
        return []
        
    logs = frappe.get_all("CRM Audit Log",
        filters={"ref_doctype": "User", "user": user_email},
        fields=["creation", "details"],
        order_by="creation desc"
    )
    
    login_events = []
    logout_events = []
    
    for l in logs:
        timestamp = int(frappe.utils.get_datetime(l.creation).timestamp() * 1000)
        if "logged in" in l.details:
            login_events.append({"time": timestamp, "details": l.details})
        elif "logged out" in l.details:
            logout_events.append({"time": timestamp, "details": l.details})
            
    login_events.sort(key=lambda x: x["time"])
    logout_events.sort(key=lambda x: x["time"])
    
    paired = []
    for login in login_events:
        logout_time = None
        duration_str = "--"
        matched_logout = None
        for logout in logout_events:
            if logout["time"] > login["time"]:
                logout_time = logout["time"]
                diff_sec = (logout_time - login["time"]) // 1000
                hours = diff_sec // 3600
                mins = (diff_sec % 3600) // 60
                duration_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
                matched_logout = logout
                break
        if matched_logout:
            logout_events.remove(matched_logout)
                
        paired.append({
            "username": user_email,
            "loginAt": login["time"],
            "logoutAt": logout_time,
            "duration": duration_str,
            "ip": "127.0.0.1"
        })
        
    paired.reverse()
    return paired


def global_security_check():
    from crm_pro.api import check_injection
    for k, v in frappe.form_dict.items():
        if v and isinstance(v, str):
            if check_injection(v):
                frappe.local.response["http_status_code"] = 400
                frappe.throw(_("Security validation failed: invalid input for parameter {0}").format(k), frappe.ValidationError)

import frappe
from frappe import _

@frappe.whitelist()
def get_profile():
    user = frappe.session.user

    if user == "Guest":
        return {"success": False, "message": "Not logged in"}

    doc = frappe.get_doc("User", user)

    return {
        "success": True,
        "username": doc.first_name or doc.full_name,
        "email": doc.email,
        "roles": frappe.get_roles(user)
    }


@frappe.whitelist()
def update_profile(username=None, email=None):
    user = frappe.session.user   # 👈 VERY IMPORTANT

    if user == "Guest":
        return {"success": False, "message": "Not logged in"}

    doc = frappe.get_doc("User", user)

    if username:
        doc.first_name = username   # name change

    if email:
        doc.email = email           # email change

    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return {"success": True, "message": "Profile updated successfully"}


@frappe.whitelist()
def change_password(old_password, new_password):
    user = frappe.session.user

    if not frappe.check_password(user, old_password):
        frappe.throw("Old password incorrect")

    from frappe.utils.password import update_password
    update_password(user, new_password)

    return {"success": True, "message": "Password updated"}


@frappe.whitelist(allow_guest=True)
def signup_endpoint():
    import frappe
    from frappe.utils.password import update_password

    data = frappe.form_dict


    print("FORM DATA =", frappe.form_dict)
    frappe.errprint(frappe.form_dict)


    username = (data.get("first_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    phone = (data.get("contact") or "").strip()
    password = data.get("password")
    role = (data.get("role") or "User").strip()

    if not username or not email or not password:
        return {
            "success": False,
            "message": "Missing required fields"
        }

    # Duplicate Email
    if frappe.db.exists("User", email):
        return {
            "success": False,
            "message": "Email already registered"
        }

    # Duplicate Phone
    if frappe.db.exists("CRM User Profile", {"phone_number": phone}):
        return {
            "success": False,
            "message": "Phone number already exists"
        }

    try:

        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": username,
            "enabled": 1,
            "send_welcome_email": 0
        })

        user.insert(ignore_permissions=True)

        print("USER CREATED")

        update_password(email, password)

        if role.lower() == "admin":
            user.add_roles("Admin")

        elif role.lower() == "user":
            user.add_roles("User")

        print(email)

        frappe.get_doc({
            "doctype": "CRM User Profile",
            "user": email,
            "username": username,
            "phone_number": phone
        }).insert(ignore_permissions=True)

        print("PROFILE CREATED")
        print(phone)

        frappe.db.commit()

        return {
            "success": True,
            "message": "Account created successfully"
        }

    except Exception as e:

        frappe.db.rollback()

        print(frappe.get_traceback())

        frappe.log_error(
            frappe.get_traceback(),
            "Signup Endpoint"
        )

        return {
            "success": False,
            "message": str(e)
        }
