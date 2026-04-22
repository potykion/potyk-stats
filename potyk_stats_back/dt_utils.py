import datetime


def parse_dt(dt_str: str) -> datetime.datetime:
    """
    >>> parse_dt('2026-04-21T23:30')
    datetime.datetime(2026, 4, 21, 23, 30)
    """
    return datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
