status = "ON"

def get_status():
    return status

def set_status(s: str):
    global status
    s = s.upper()
    if s in ["ON", "OFF"]:
        status = s
        return True
    return False
