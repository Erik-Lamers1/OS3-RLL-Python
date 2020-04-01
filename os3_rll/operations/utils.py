from datetime import datetime, timedelta


def check_date_is_older_than_x_days(date, days):
    """
    Checks if a datetime object is older then a given amount of days

    param datetime.datetime date: The datetime object to check
    param int days: The amount of days to check against
    """
    return False if date < datetime.now() - timedelta(days=days) else True
