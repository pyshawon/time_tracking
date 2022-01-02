from datetime import datetime, time


def date_diff(dt2, dt1):
    """
    Function for Diff between two dates.
    """
    timedelta = dt2 - dt1
    seconds = timedelta.days * 24 * 3600 + timedelta.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return "{} days, {} hours, {} minutes, {} seconds".format(days, hours, minutes, seconds)
