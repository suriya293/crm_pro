import frappe
from frappe import _
import hmac
import hashlib
import json
import base64
import time

def get_secret():
    return frappe.local.conf.get("encryption_key") or frappe.local.conf.db_password or "precision_crm_secret_key"

def base64url_encode(input_bytes):
    return base64.urlsafe_b64encode(input_bytes).replace(b'=', b'').decode('utf-8')

def base64url_decode(input_str):
    input_str += '=' * (4 - len(input_str) % 4)
    return base64.urlsafe_b64decode(input_str.encode('utf-8'))

def generate_jwt(payload, expires_in=3600):
    secret = get_secret()
    header = {"alg": "HS256", "typ": "JWT"}
    payload["exp"] = int(time.time()) + expires_in
    
    header_b64 = base64url_encode(json.dumps(header).encode('utf-8'))
    payload_b64 = base64url_encode(json.dumps(payload).encode('utf-8'))
    
    signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(secret.encode('utf-8'), signature_input, hashlib.sha256).digest()
    signature_b64 = base64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_jwt(token):
    secret = get_secret()
    parts = token.split('.')
    if len(parts) != 3:
        return None
    header_b64, payload_b64, signature_b64 = parts
    
    signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    expected_signature = hmac.new(secret.encode('utf-8'), signature_input, hashlib.sha256).digest()
    expected_signature_b64 = base64url_encode(expected_signature)
    
    if not hmac.compare_digest(signature_b64, expected_signature_b64):
        return None
        
    try:
        payload = json.loads(base64url_decode(payload_b64).decode('utf-8'))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None

@frappe.whitelist(allow_guest=True)
def login(username, password):
    try:
        # Authenticate using Frappe's native authentication
        from frappe.auth import LoginManager
        login_manager = LoginManager()
        login_manager.authenticate(username, password)
        login_manager.post_login()
        
        user = login_manager.user
        roles = frappe.get_roles(user)
        
        # Generate Access and Refresh Tokens
        access_token = generate_jwt({"user": user, "roles": roles, "type": "access"}, expires_in=3600) # 1 hour
        refresh_token = generate_jwt({"user": user, "type": "refresh"}, expires_in=86400 * 7) # 7 days
        
        # Store refresh token in cache for rotation check
        frappe.cache().set_value(f"refresh_token:{user}", refresh_token, expires_in_sec=86400 * 7)
        
        return {
            "status": "success",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
            "roles": roles
        }
    except frappe.AuthenticationError:
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Invalid username or password"}

@frappe.whitelist(allow_guest=True)
def refresh_token(token):
    payload = verify_jwt(token)
    if not payload or payload.get("type") != "refresh":
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Invalid or expired refresh token"}
        
    user = payload.get("user")
    stored_token = frappe.cache().get_value(f"refresh_token:{user}")
    
    # Refresh token rotation validation
    if not stored_token or stored_token != token:
        # Reuse detected - invalidate the token entirely for security
        frappe.cache().delete_value(f"refresh_token:{user}")
        frappe.local.response["http_status_code"] = 401
        return {"status": "error", "message": "Invalid or reused refresh token"}
        
    roles = frappe.get_roles(user)
    
    new_access_token = generate_jwt({"user": user, "roles": roles, "type": "access"}, expires_in=3600)
    new_refresh_token = generate_jwt({"user": user, "type": "refresh"}, expires_in=86400 * 7)
    
    frappe.cache().set_value(f"refresh_token:{user}", new_refresh_token, expires_in_sec=86400 * 7)
    
    return {
        "status": "success",
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }

@frappe.whitelist()
def logout():
    user = frappe.session.user
    frappe.cache().delete_value(f"refresh_token:{user}")
    return {"status": "success", "message": "Logged out successfully"}

@frappe.whitelist(allow_guest=True)
def password_reset(email):
    if not frappe.db.exists("User", email):
        return {"status": "error", "message": "User not found"}
        
    from frappe.core.doctype.user.user import get_reset_link
    user_doc = frappe.get_doc("User", email)
    reset_link = get_reset_link(user_doc)
    
    # Log reset action
    audit_log = frappe.get_doc({
        "doctype": "Audit Log",
        "action": "Password Reset Request",
        "details": f"Password reset link generated for {email}",
        "user": email
    })
    audit_log.insert(ignore_permissions=True)
    
    return {"status": "success", "message": "Password reset link generated", "reset_link": reset_link}

def validate_token_request():
    auth_header = frappe.get_request_header("Authorization")
    if not auth_header:
        return None
        
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
        
    token = parts[1]
    payload = verify_jwt(token)
    if payload and payload.get("type") == "access":
        return payload
    return None

def validate_api_key_request():
    api_key = frappe.get_request_header("X-API-Key")
    api_secret = frappe.get_request_header("X-API-Secret")
    if api_key and api_secret:
        user = frappe.db.get_value("User", {"api_key": api_key}, "name")
        if user:
            # Verify API Secret
            user_secret = frappe.utils.password.get_decrypted_password("User", user, fieldname="api_secret")
            if user_secret == api_secret:
                return {"user": user, "roles": frappe.get_roles(user)}
    return None

def authenticate_request():
    # Attempt JWT Auth
    jwt_payload = validate_token_request()
    if jwt_payload:
        frappe.set_user(jwt_payload.get("user"))
        return True
        
    # Attempt API Key Auth
    api_payload = validate_api_key_request()
    if api_payload:
        frappe.set_user(api_payload.get("user"))
        return True
        
    return False

def check_role(allowed_roles):
    current_roles = frappe.get_roles(frappe.session.user)
    for role in allowed_roles:
        if role in current_roles:
            return True
    return False
