import math
from datetime import datetime, timezone, timedelta


class FieldClimateCommands:
    """Maps API resources to methods."""

    base_url = "https://api.fieldclimate.com/v1"

    @staticmethod
    def clean_time(*times):
        # Server expects t_from and t_to params as unix timestamps since UTC.
        for time in times:
            # I also want to support datetime objects, but timezones make this tricky!
            if isinstance(time, datetime):
                # for naive datetimes, assume and insert UTC.
                if time.utcoffset() is None:
                    time = time.replace(tzinfo=timezone.utc)
                time = time.timestamp()
            yield str(int(time))

    @staticmethod
    def clean_data_group(group):
        # Server expects data_group to be one of these strings:
        valid_groups = ["raw", "hourly", "daily", "monthly"]
        try:
            # I also want to support the older-style group keys: ['0', '1', '2', '3']
            group = valid_groups[int(group)]
        except (IndexError, ValueError, TypeError):
            pass
        assert group in valid_groups, f"data_group argument must be in {valid_groups}"
        return group

    @staticmethod
    def clean_sort(sort):
        valid_sorts = ["asc", "desc"]
        assert sort in valid_sorts, f"sort argument must be in {valid_sorts}"
        return sort

    @staticmethod
    def clean_filter(filter):
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

    @staticmethod
    def clean_format(format):
        valid_formats = ["normal", "optimized"]
        assert format in valid_formats, f"format argument must be in {valid_formats}"
        return format

    @staticmethod
    def clean_time_period(time_period):
        # Server expects a string like Xh, Xd, Xw, Xm, X, where:
        # X = Number, h = hours, d = days, w = weeks, m = months
        # X alone must mean total seconds
        # First, support timedelta, rounding up to nearest full second:
        if isinstance(time_period, timedelta):
            return str(math.ceil(time_period.total_seconds()))
        # Otherwise, enforce the server spec:
        err = "time_period must match server spec: Xh, Xd, Xw, Xm, X"
        try:
            X = int(time_period.rstrip("hdwm"))
        except ValueError:
            raise AssertionError(err)
        assert time_period in [f"{X}h", f"{X}d", f"{X}w", f"{X}m", f"{X}"], err
        return time_period

    def get_user(self):
        """Read user information"""
        route = "/user"
        return self.get(route)

    def put_user(self, data):
        """Update user information"""
        route = "/user"
        return self.put(route, data)

    def delete_user(self):
        """Delete user account"""
        route = "/user"
        return self.delete(route)

    def get_user_stations(self):
        """Read list of stations of a user"""
        route = "/user/stations"
        return self.get(route)

    def get_user_licenses(self):
        """Read user licenses"""
        route = "/user/licenses"
        return self.get(route)

    def get_system_status(self):
        """System running correctly"""
        route = "/system/status"
        return self.get(route)

    def get_system_sensors(self):
        """Supported sensors"""
        route = "/system/sensors"
        return self.get(route)

    def get_system_groups(self):
        """Supported sensor groups"""
        route = "/system/groups"
        return self.get(route)

    def get_system_group_sensors(self):
        """Sensors organized in groups"""
        route = "/system/group/sensors"
        return self.get(route)

    def get_system_types(self):
        """Type of devices"""
        route = "/system/types"
        return self.get(route)

    def get_system_countries(self):
        """Countries for the languages"""
        route = "/system/countries"
        return self.get(route)

    def get_system_timezones(self):
        """Timezones"""
        route = "/system/timezones"
        return self.get(route)

    def get_system_diseases(self):
        """Disease models"""
        route = "/system/diseases"
        return self.get(route)

    def get_station(self, station_id):
        """Read station information"""
        route = f"/station/{station_id}"
        return self.get(route)

    def put_station(self, station_id, data):
        """Update station information"""
        route = f"/station/{station_id}"
        return self.put(route, data)

    def get_station_sensors(self, station_id):
        """Get list of sensors of a station"""
        route = f"/station/{station_id}/sensors"
        return self.get(route)

    def put_station_sensors(self, station_id, data):
        """Update station sensor name"""
        route = f"/station/{station_id}/sensors"
        return self.put(route, data)

    def get_station_nodes(self, station_id):
        """Get list of nodes (wireless devices) connected to a station"""
        route = f"/station/{station_id}/nodes"
        return self.get(route)

    def put_station_nodes(self, station_id, data):
        """Update the name of a node itself"""
        route = f"/station/{station_id}/nodes"
        return self.put(route, data)

    def get_station_serials(self, station_id):
        """List of serials (of a sensor) and their names"""
        route = f"/station/{station_id}/serials"
        return self.get(route)

    def put_station_serials(self, station_id, data):
        """Update sensor with serial the name"""
        route = f"/station/{station_id}/serials"
        return self.put(route, data)

    def post_station_key(self, station_id, station_key, data):
        """Add station to user account"""
        route = f"/station/{station_id}/{station_key}"
        return self.post(route, data)

    def delete_station_key(self, station_id, station_key):
        """Remove station from user account"""
        route = f"/station/{station_id}/{station_key}"
        return self.delete(route)

    def get_stations_in_proximity(self, station_id, radius):
        """Stations in close proximity of specified station"""
        route = f"/station/{station_id}/proximity/{radius}"
        return self.get(route)

    def get_station_events_last(self, station_id, amount, sort):
        """Last station events"""
        sort = self.clean_sort(sort)
        route = f"/station/{station_id}/events/last/{amount}/{sort}"
        return self.get(route)

    def get_station_events(self, station_id, t_from, t_to, sort):
        """Station events from to"""
        t_from, t_to = self.clean_time(t_from, t_to)
        sort = self.clean_sort(sort)
        route = f"/station/{station_id}/events/from/{t_from}/to/{t_to}/{sort}"
        return self.get(route)

    def get_station_history_last(self, station_id, filter, amount, sort):
        """Last station communication history filter"""
        filter = self.clean_filter(filter)
        sort = self.clean_sort(sort)
        route = f"/station/{station_id}/history/{filter}/last/{amount}/{sort}"
        return self.get(route)

    def get_station_history(self, station_id, filter, t_from, t_to, sort):
        """Station communication history from to filter"""
        filter = self.clean_filter(filter)
        t_from, t_to = self.clean_time(t_from, t_to)
        sort = self.clean_sort(sort)
        route = f"/station/{station_id}/history/{filter}/from/{t_from}/to/{t_to}/{sort}"
        return self.get(route)

    def get_station_licenses(self, station_id):
        """Station licenses for disease models or forecast"""
        route = f"/station/{station_id}/licenses"
        return self.get(route)

    def get_data_range(self, station_id):
        """Min and Max date of data availability"""
        route = f"/data/{station_id}"
        return self.get(route)

    def get_data_last(self, format, station_id, data_group, time_period):
        """Reading last data"""
        format = self.clean_format(format)
        data_group = self.clean_data_group(data_group)
        time_period = self.clean_time_period(time_period)
        route = f"/data/{format}/{station_id}/{data_group}/last/{time_period}"
        return self.get(route)

    def get_data(self, format, station_id, data_group, t_from, t_to):
        """Reading data of specific time period"""
        format = self.clean_format(format)
        t_from, t_to = self.clean_time(t_from, t_to)
        data_group = self.clean_data_group(data_group)
        route = f"/data/{format}/{station_id}/{data_group}/from/{t_from}/to/{t_to}"
        return self.get(route)

    def post_data_last(self, format, station_id, data_group, time_period, data):
        """Filtered/Customized reading of last data"""
        format = self.clean_format(format)
        data_group = self.clean_data_group(data_group)
        time_period = self.clean_time_period(time_period)
        route = f"/data/{format}/{station_id}/{data_group}/last/{time_period}"
        return self.post(route, data)

    def post_data(self, format, station_id, data_group, t_from, t_to, data):
        """Filtered/Customized reading of specified time period"""
        format = self.clean_format(format)
        t_from, t_to = self.clean_time(t_from, t_to)
        data_group = self.clean_data_group(data_group)
        route = f"/data/{format}/{station_id}/{data_group}/from/{t_from}/to/{t_to}"
        return self.post(route, data)

    def get_forecast(self, station_id, forecast_option):
        """Forecast data package or image"""
        route = f"/forecast/{station_id}/{forecast_option}"
        return self.get(route)

    def get_disease_last(self, station_id, time_period):
        """Get last Evapotranspiration"""
        time_period = self.clean_time_period(time_period)
        route = f"/disease/{station_id}/last/{time_period}"
        return self.get(route)

    def get_disease(self, station_id, t_from, t_to):
        """Get Evapotranspiration for specified period"""
        t_from, t_to = self.clean_time(t_from, t_to)
        route = f"/disease/{station_id}/from/{t_from}/to/{t_to}"
        return self.get(route)

    def post_disease_last(self, station_id, time_period, data):
        """Get last specified disease model"""
        time_period = self.clean_time_period(time_period)
        route = f"/disease/{station_id}/last/{time_period}"
        return self.post(route, data)

    def post_disease(self, station_id, t_from, t_to, data):
        """Get specified disease model for period"""
        t_from, t_to = self.clean_time(t_from, t_to)
        route = f"/disease/{station_id}/from/{t_from}/to/{t_to}"
        return self.post(route, data)

    def get_chart_last(self, type, station_id, data_group, time_period):
        """Charting last data"""
        data_group = self.clean_data_group(data_group)
        time_period = self.clean_time_period(time_period)
        route = f"/chart/{type}/{station_id}/{data_group}/last/{time_period}"
        return self.get(route)

    def get_chart(self, type, station_id, data_group, t_from, t_to):
        """Charting for period"""
        t_from, t_to = self.clean_time(t_from, t_to)
        data_group = self.clean_data_group(data_group)
        route = f"/chart/{type}/{station_id}/{data_group}/from/{t_from}/to/{t_to}"
        return self.get(route)

    def post_chart_last(self, type, station_id, data_group, time_period, data):
        """Charting customized last data"""
        data_group = self.clean_data_group(data_group)
        time_period = self.clean_time_period(time_period)
        route = f"/chart/{type}/{station_id}/{data_group}/last/{time_period}"
        return self.post(route, data)

    def post_chart(self, type, station_id, data_group, t_from, t_to, data):
        """Charting customized for period"""
        t_from, t_to = self.clean_time(t_from, t_to)
        data_group = self.clean_data_group(data_group)
        route = f"/chart/{type}/{station_id}/{data_group}/from/{t_from}/to/{t_to}"
        return self.post(route, data)

    def get_camera(self, station_id):
        """Read station information"""
        route = f"/camera/{station_id}/photos/info"
        return self.get(route)

    def get_camera_photos_last(self, station_id, amount, camera):
        """Last amount of pictures"""
        route = f"/camera/{station_id}/photos/last/{amount}/{camera}"
        return self.get(route)

    def get_camera_photos(self, station_id, t_from, t_to, camera):
        """Retrieve pictures for specified period"""
        t_from, t_to = self.clean_time(t_from, t_to)
        route = f"/camera/{station_id}/photos/from/{t_from}/to/{t_to}/{camera}"
        return self.get(route)
