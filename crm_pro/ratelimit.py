def ratelimit(*args, **kwargs):
    def decorator(func):
        return func
    return decorator
