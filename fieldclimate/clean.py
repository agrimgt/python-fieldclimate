"""Clean functions validate arguments and transform them into strings
that the API server expects. Will raise AssertionError if invalid."""

__all__ = ["time", "data_group", "sort", "filter", "format", "time_period", "station"]

import math
from datetime import datetime, timedelta, timezone
from numbers import Real
from typing import Union


def time(*times: Union[str, int, datetime]) -> str:
    # Server expects t_from and t_to params as unix timestamps since UTC.
    for time in times:
        # I also want to support datetime objects, but timezones make this tricky!
        if isinstance(time, datetime):
            # for naive datetimes, assume and insert UTC.
            if time.utcoffset() is None:
                time = time.replace(tzinfo=timezone.utc)
            time = time.timestamp()
        yield str(int(time))


def data_group(group: Union[str, int]) -> str:
    # Server expects data_group to be one of these strings:
    valid_groups = ["raw", "hourly", "daily", "monthly"]
    try:
        # I also want to support the older-style group keys: ['0', '1', '2', '3']
        group = valid_groups[int(group)]
    except (IndexError, ValueError, TypeError):
        pass
    if group not in valid_groups:
        raise AssertionError(f"data_group argument must be in {valid_groups}")
    return group


def sort(sort: str) -> str:
    valid_sorts = ["asc", "desc"]
    if sort not in valid_sorts:
        raise AssertionError(f"sort argument must be in {valid_sorts}")
    return sort


def filter(filter: str) -> str:
    valid_filters = [
        "unknown",
        "success",
        "resync",
        "registration",
        "no_data",
        "xml_error",
        "fw_update",
        "apn_update",
    ]
    if filter not in valid_filters:
        raise AssertionError(f"filter argument must be in {valid_filters}")
    return filter


def format(format: str) -> str:
    valid_formats = ["normal", "optimized"]
    if format not in valid_formats:
        raise AssertionError(f"format argument must be in {valid_formats}")
    return format


def time_period(time_period: Union[str, Real, timedelta]) -> str:
    # Server expects a string like Xh, Xd, Xw, Xm, X, where:
    # X = Number, h = hours, d = days, w = weeks, m = months
    # X alone must mean total seconds
    # First, support timedelta, rounding up to nearest full second:
    if isinstance(time_period, timedelta):
        return str(math.ceil(time_period.total_seconds()))
    if isinstance(time_period, Real):
        return str(int(time_period))
    # Otherwise, enforce the server spec:
    err = "time_period must match server spec: Xh, Xd, Xw, Xm, X"
    try:
        X = int(time_period.rstrip("hdwm"))
    except ValueError:
        raise AssertionError(err)
    if time_period not in [f"{X}h", f"{X}d", f"{X}w", f"{X}m", f"{X}"]:
        raise AssertionError(err)
    return time_period


def station(station: Union[str, dict]) -> str:
    # Server expects 'station_id', an 8-digit serial code.
    # Dicts returned by get_user_stations() store that code like this:
    # {'name': {'original': 'STATION_ID'}, ...}
    # So lets try and extract that ID in case station is a dict.
    try:
        return station["name"]["original"]
    except (TypeError, KeyError):
        pass
    return station
