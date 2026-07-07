import logging
from ratelimit import limits as ratelimit
'''Compatibility stub for Unix pwd module on Windows.'''

def getpwuid(uid=None):
    """Return a simple object with pw_name attribute.
    Provides minimal compatibility for code expecting pwd.getpwuid().
    """
    import os
    try:
        username = os.getlogin()
    except Exception:
        username = os.getenv('USERNAME') or 'unknown'
    class pwd_struct:
        pw_name = username
    return pwd_struct()

def getpwnam(name):
    """Return a simple object with pw_name attribute for a given username.
    """
    class pwd_struct:
        pw_name = name
    return pwd_struct()
