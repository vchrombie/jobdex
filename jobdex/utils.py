# utils.py

from datetime import datetime


def is_today(date_str, date_format):
    """Check if the given date string corresponds to today's date."""
    today = datetime.now().date()
    date = datetime.strptime(date_str, date_format).date()
    return date == today
