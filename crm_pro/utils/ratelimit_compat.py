def ratelimit(*args, **kwargs):
    def decorator(fn):
        return fn
    return decorator
