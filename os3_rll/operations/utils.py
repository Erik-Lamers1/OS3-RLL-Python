from datetime import datetime, timedelta

from os3_rll.models.db import Database


def check_date_is_older_than_x_days(date, days):
    """
    Checks if a datetime object is older then a given amount of days

    param datetime.datetime date: The datetime object to check
    param int days: The amount of days to check against
    """
    return False if date > datetime.now() - timedelta(days=days) else True


def get_max_rank():
    """
    Gets the lowest player rank (or highest on decimal scale)
    """
    with Database() as db:
        db.execute("SELECT MAX(rank) FROM users")
        return int(db.fetchone()[0])
