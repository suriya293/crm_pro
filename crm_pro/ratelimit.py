import frappe
import time
from frappe import _

def ratelimit(key='user', rate='100/m'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                limit_str, window_str = rate.split('/')
                limit = int(limit_str)
                if window_str == 's':
                    window = 1
                elif window_str == 'm':
                    window = 60
                elif window_str == 'h':
                    window = 3600
                else:
                    window = 60
            except Exception:
                limit = 100
                window = 60

            # Determine request identifier
            ip = frappe.local.request_ip or "127.0.0.1"
            user = frappe.session.user or "Guest"

            identifier = user if key == 'user' and user != 'Guest' else ip
            cache_key = f"api_rate_limit:{func.__module__}.{func.__name__}:{identifier}"

            now = time.time()
            timestamps = frappe.cache().get_value(cache_key) or []
            # Clean up old timestamps outside the window
            timestamps = [t for t in timestamps if now - t < window]

            if len(timestamps) >= limit:
                if hasattr(frappe.local, "response"):
                    frappe.local.response["http_status_code"] = 429
                frappe.throw(_("Too many requests. Please try again later."), frappe.ValidationError)

            timestamps.append(now)
            frappe.cache().set_value(cache_key, timestamps, expires_in_sec=window)

            return func(*args, **kwargs)
        return wrapper
    return decorator
