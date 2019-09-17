from datetime import datetime, timedelta, timezone
from unittest import TestCase

from fieldclimate import clean


class MethodUtilsTestCase(TestCase):
    def test_clean_time(self):
        tz = timezone(timedelta(hours=5))  # (5 hours east of utc)
        a, b, c, d = clean.time(
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
        self.assertEqual(clean.data_group("raw"), "raw")
        self.assertEqual(clean.data_group("hourly"), "hourly")
        self.assertEqual(clean.data_group("daily"), "daily")
        self.assertEqual(clean.data_group("monthly"), "monthly")
        self.assertEqual(clean.data_group("0"), "raw")
        self.assertEqual(clean.data_group("1"), "hourly")
        self.assertEqual(clean.data_group("2"), "daily")
        self.assertEqual(clean.data_group("3"), "monthly")
        self.assertEqual(clean.data_group(0), "raw")
        self.assertEqual(clean.data_group(1), "hourly")
        self.assertEqual(clean.data_group(2), "daily")
        self.assertEqual(clean.data_group(3), "monthly")
        with self.assertRaises(AssertionError):
            clean.data_group("other")

    def test_clean_sort(self):
        self.assertEqual(clean.sort("asc"), "asc")
        self.assertEqual(clean.sort("desc"), "desc")
        with self.assertRaises(AssertionError):
            clean.sort("other")

    def test_clean_filter(self):
        self.assertEqual(clean.filter("unknown"), "unknown")
        self.assertEqual(clean.filter("success"), "success")
        self.assertEqual(clean.filter("resync"), "resync")
        self.assertEqual(clean.filter("registration"), "registration")
        self.assertEqual(clean.filter("no_data"), "no_data")
        self.assertEqual(clean.filter("xml_error"), "xml_error")
        self.assertEqual(clean.filter("fw_update"), "fw_update")
        self.assertEqual(clean.filter("apn_update"), "apn_update")
        with self.assertRaises(AssertionError):
            clean.filter("other")

    def test_clean_format(self):
        self.assertEqual(clean.format("normal"), "normal")
        self.assertEqual(clean.format("optimized"), "optimized")
        with self.assertRaises(AssertionError):
            clean.format("other")

    def test_clean_time_period(self):
        self.assertEqual(clean.time_period("4h"), "4h")
        self.assertEqual(clean.time_period("4d"), "4d")
        self.assertEqual(clean.time_period("4w"), "4w")
        self.assertEqual(clean.time_period("4m"), "4m")
        self.assertEqual(clean.time_period("4"), "4")
        self.assertEqual(clean.time_period(4), "4")
        self.assertEqual(clean.time_period(4.0), "4")
        self.assertEqual(clean.time_period(timedelta(seconds=4)), "4")
        self.assertEqual(clean.time_period(timedelta(minutes=4)), "240")
        self.assertEqual(clean.time_period(timedelta(hours=4)), "14400")
        self.assertEqual(clean.time_period(timedelta(days=4)), "345600")
        with self.assertRaises(AssertionError):
            clean.time_period("other")

    def test_clean_station(self):
        self.assertEqual(clean.station("01234567"), "01234567")
        self.assertEqual(clean.station({"name": {"original": "01234567"}}), "01234567")
