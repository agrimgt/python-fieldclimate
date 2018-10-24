"""Functions for accepting python data types when formatting API method urls."""

__all__ = [
    "clean_time",
    "clean_data_group",
    "clean_sort",
    "clean_filter",
    "clean_format",
    "clean_time_period",
]

import math

from datetime import datetime, timezone, timedelta
from numbers import Real
from typing import Union


def clean_time(*times: Union[str, int, datetime]) -> str:
    # Server expects t_from and t_to params as unix timestamps since UTC.
    for time in times:
        # I also want to support datetime objects, but timezones make this tricky!
        if isinstance(time, datetime):
            # for naive datetimes, assume and insert UTC.
            if time.utcoffset() is None:
                time = time.replace(tzinfo=timezone.utc)
            time = time.timestamp()
        yield str(int(time))


def clean_data_group(group) -> str:
    # Server expects data_group to be one of these strings:
    valid_groups = ["raw", "hourly", "daily", "monthly"]
    try:
        # I also want to support the older-style group keys: ['0', '1', '2', '3']
        group = valid_groups[int(group)]
    except (IndexError, ValueError, TypeError):
        pass
    assert group in valid_groups, f"data_group argument must be in {valid_groups}"
    return group


def clean_sort(sort) -> str:
    valid_sorts = ["asc", "desc"]
    assert sort in valid_sorts, f"sort argument must be in {valid_sorts}"
    return sort


def clean_filter(filter: str) -> str:
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
    assert filter in valid_filters, f"filter argument must be in {valid_filters}"
    return filter


def clean_format(format: str) -> str:
    valid_formats = ["normal", "optimized"]
    assert format in valid_formats, f"format argument must be in {valid_formats}"
    return format


def clean_time_period(time_period: Union[str, Real, timedelta]) -> str:
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
    assert time_period in [f"{X}h", f"{X}d", f"{X}w", f"{X}m", f"{X}"], err
    return time_period
