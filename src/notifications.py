global _notification
_notification = ""

def set_notification(text):
    global _notification
    _notification = text

def display_notification():
    global _notification
    print("\033[94m" + _notification + "\033[0m")
    _notification = ""