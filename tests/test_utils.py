from datetime import datetime, timezone, timedelta
from unittest import TestCase

from fieldclimate.utils import (
    clean_time,
    clean_data_group,
    clean_sort,
    clean_filter,
    clean_format,
    clean_time_period,
    clean_station,
)


class MethodUtilsTestCase(TestCase):
    def test_clean_time(self):
        tz = timezone(timedelta(hours=5))  # (5 hours east of utc)
        a, b, c, d = clean_time(
            datetime(2018, 10, 1, 0, 0),
            datetime(2018, 10, 1, 5, 0, tzinfo=tz),
            1538352000,
            "1538352000",
        )
        self.assertEqual(a, "1538352000")
        self.assertEqual(b, "1538352000")
        self.assertEqual(c, "1538352000")
        self.assertEqual(d, "1538352000")

    def test_clean_data_group(self):
        self.assertEqual(clean_data_group("raw"), "raw")
        self.assertEqual(clean_data_group("hourly"), "hourly")
        self.assertEqual(clean_data_group("daily"), "daily")
        self.assertEqual(clean_data_group("monthly"), "monthly")
        self.assertEqual(clean_data_group("0"), "raw")
        self.assertEqual(clean_data_group("1"), "hourly")
        self.assertEqual(clean_data_group("2"), "daily")
        self.assertEqual(clean_data_group("3"), "monthly")
        self.assertEqual(clean_data_group(0), "raw")
        self.assertEqual(clean_data_group(1), "hourly")
        self.assertEqual(clean_data_group(2), "daily")
        self.assertEqual(clean_data_group(3), "monthly")
        with self.assertRaises(AssertionError):
            clean_data_group("other")

    def test_clean_sort(self):
        self.assertEqual(clean_sort("asc"), "asc")
        self.assertEqual(clean_sort("desc"), "desc")
        with self.assertRaises(AssertionError):
            clean_sort("other")

    def test_clean_filter(self):
        self.assertEqual(clean_filter("unknown"), "unknown")
        self.assertEqual(clean_filter("success"), "success")
        self.assertEqual(clean_filter("resync"), "resync")
        self.assertEqual(clean_filter("registration"), "registration")
        self.assertEqual(clean_filter("no_data"), "no_data")
        self.assertEqual(clean_filter("xml_error"), "xml_error")
        self.assertEqual(clean_filter("fw_update"), "fw_update")
        self.assertEqual(clean_filter("apn_update"), "apn_update")
        with self.assertRaises(AssertionError):
            clean_filter("other")

    def test_clean_format(self):
        self.assertEqual(clean_format("normal"), "normal")
        self.assertEqual(clean_format("optimized"), "optimized")
        with self.assertRaises(AssertionError):
            clean_format("other")

    def test_clean_time_period(self):
        self.assertEqual(clean_time_period("4h"), "4h")
        self.assertEqual(clean_time_period("4d"), "4d")
        self.assertEqual(clean_time_period("4w"), "4w")
        self.assertEqual(clean_time_period("4m"), "4m")
        self.assertEqual(clean_time_period("4"), "4")
        self.assertEqual(clean_time_period(4), "4")
        self.assertEqual(clean_time_period(4.0), "4")
        self.assertEqual(clean_time_period(timedelta(seconds=4)), "4")
        self.assertEqual(clean_time_period(timedelta(minutes=4)), "240")
        self.assertEqual(clean_time_period(timedelta(hours=4)), "14400")
        self.assertEqual(clean_time_period(timedelta(days=4)), "345600")
        with self.assertRaises(AssertionError):
            clean_time_period("other")

    def test_clean_station(self):
        self.assertEqual(clean_station("01234567"), "01234567")
        self.assertEqual(clean_station({"name": {"original": "01234567"}}), "01234567")
