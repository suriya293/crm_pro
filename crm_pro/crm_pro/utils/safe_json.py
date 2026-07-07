import json

def safe_json(val, default=None):
    """
    Safely parses a JSON string, dictionary, or list.
    Protects against None, empty string, invalid JSON, and placeholder strings.
    """
    if val is None:
        return default if default is not None else {}
    if isinstance(val, (dict, list)):
        return val
    if not isinstance(val, str):
        return default if default is not None else {}
        
    val = val.strip()
    if not val or val.lower() in ["none", "undefined", "null", "<filters>", "<stages_list>", ""]:
        return default if default is not None else {}
        
    try:
        return json.loads(val)
    except Exception:
        return default if default is not None else {}
