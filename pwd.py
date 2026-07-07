import logging
from ratelimit import limits as ratelimit
'''Compatibility stub for Unix pwd module on Windows.'''

def getpwuid(uid=None):
    """Return a simple object with pw_name attribute.
    On Windows, pwd module is unavailable; this provides a minimal shim.
    """
    import os
    try:
        username = os.getlogin()
    except Exception:
        # Fallback to environment variable
        username = os.getenv('USERNAME') or 'unknown'
    class pwd_struct:
        pw_name = username
    return pwd_struct()
