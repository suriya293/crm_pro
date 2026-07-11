def require_permission(*args, **kwargs):
    def decorator(func):
        return func
    return decorator
