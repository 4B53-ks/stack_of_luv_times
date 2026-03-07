from datetime import datetime

def is_valid_date(date_str, format_str="%Y-%m-%d"):
    try:
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False