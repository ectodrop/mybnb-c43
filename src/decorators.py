import notifications

def error_notif(default=None):
    def _error_notif(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs) 
            except Exception as e:
                notifications.set_notification(str(e))
                return default
        return wrapper
    return _error_notif