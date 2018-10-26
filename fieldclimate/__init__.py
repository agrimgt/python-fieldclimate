"""A client for the iMetos FieldClimate API."""

__all__ = ["FieldClimateClient"]
__version__ = "1.1"
__author__ = "Agrimanagement, Inc."

from fieldclimate.client import HmacClient
from fieldclimate.utils import *


class FieldClimateClient(HmacClient):
    """Adapt the aiohttp and requests libraries to FieldClimate's API,
    switching between them depending on synchronous/asynchronous usage.

    Requires HMAC public and private keys for authentication.

    Usage: See README.rst

    Full description of all methods: https://api.fieldclimate.com/v1/docs/
    """

    base_url = "https://api.fieldclimate.com/v1"
    settings_prefix = "FIELDCLIMATE"

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

    def get_station(self, station):
        """Read station information"""
        station = clean_station(station)
        route = f"/station/{station}"
        return self.get(route)

    def put_station(self, station, data):
        """Update station information"""
        station = clean_station(station)
        route = f"/station/{station}"
        return self.put(route, data)

    def get_station_sensors(self, station):
        """Get list of sensors of a station"""
        station = clean_station(station)
        route = f"/station/{station}/sensors"
        return self.get(route)

    def put_station_sensors(self, station, data):
        """Update station sensor name"""
        station = clean_station(station)
        route = f"/station/{station}/sensors"
        return self.put(route, data)

    def get_station_nodes(self, station):
        """Get list of nodes (wireless devices) connected to a station"""
        station = clean_station(station)
        route = f"/station/{station}/nodes"
        return self.get(route)

    def put_station_nodes(self, station, data):
        """Update the name of a node itself"""
        station = clean_station(station)
        route = f"/station/{station}/nodes"
        return self.put(route, data)

    def get_station_serials(self, station):
        """List of serials (of a sensor) and their names"""
        station = clean_station(station)
        route = f"/station/{station}/serials"
        return self.get(route)

    def put_station_serials(self, station, data):
        """Update sensor with serial the name"""
        station = clean_station(station)
        route = f"/station/{station}/serials"
        return self.put(route, data)

    def post_station_key(self, station, station_key, data):
        """Add station to user account"""
        station = clean_station(station)
        route = f"/station/{station}/{station_key}"
        return self.post(route, data)

    def delete_station_key(self, station, station_key):
        """Remove station from user account"""
        station = clean_station(station)
        route = f"/station/{station}/{station_key}"
        return self.delete(route)

    def get_stations_in_proximity(self, station, radius):
        """Stations in close proximity of specified station"""
        station = clean_station(station)
        route = f"/station/{station}/proximity/{radius}"
        return self.get(route)

    def get_station_events_last(self, station, amount, sort):
        """Last station events"""
        station = clean_station(station)
        sort = clean_sort(sort)
        route = f"/station/{station}/events/last/{amount}/{sort}"
        return self.get(route)

    def get_station_events(self, station, t_from, t_to, sort):
        """Station events from to"""
        station = clean_station(station)
        t_from, t_to = clean_time(t_from, t_to)
        sort = clean_sort(sort)
        route = f"/station/{station}/events/from/{t_from}/to/{t_to}/{sort}"
        return self.get(route)

    def get_station_history_last(self, station, filter, amount, sort):
        """Last station communication history filter"""
        station = clean_station(station)
        filter = clean_filter(filter)
        sort = clean_sort(sort)
        route = f"/station/{station}/history/{filter}/last/{amount}/{sort}"
        return self.get(route)

    def get_station_history(self, station, filter, t_from, t_to, sort):
        """Station communication history from to filter"""
        station = clean_station(station)
        filter = clean_filter(filter)
        t_from, t_to = clean_time(t_from, t_to)
        sort = clean_sort(sort)
        route = f"/station/{station}/history/{filter}/from/{t_from}/to/{t_to}/{sort}"
        return self.get(route)

    def get_station_licenses(self, station):
        """Station licenses for disease models or forecast"""
        station = clean_station(station)
        route = f"/station/{station}/licenses"
        return self.get(route)

    def get_data_range(self, station):
        """Min and Max date of data availability"""
        station = clean_station(station)
        route = f"/data/{station}"
        return self.get(route)

    def get_data_last(self, format, station, data_group, time_period):
        """Reading last data"""
        format = clean_format(format)
        station = clean_station(station)
        data_group = clean_data_group(data_group)
        time_period = clean_time_period(time_period)
        route = f"/data/{format}/{station}/{data_group}/last/{time_period}"
        return self.get(route)

    def get_data(self, format, station, data_group, t_from, t_to):
        """Reading data of specific time period"""
        format = clean_format(format)
        station = clean_station(station)
        t_from, t_to = clean_time(t_from, t_to)
        data_group = clean_data_group(data_group)
        route = f"/data/{format}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        return self.get(route)

    def post_data_last(self, format, station, data_group, time_period, data):
        """Filtered/Customized reading of last data"""
        format = clean_format(format)
        station = clean_station(station)
        data_group = clean_data_group(data_group)
        time_period = clean_time_period(time_period)
        route = f"/data/{format}/{station}/{data_group}/last/{time_period}"
        return self.post(route, data)

    def post_data(self, format, station, data_group, t_from, t_to, data):
        """Filtered/Customized reading of specified time period"""
        format = clean_format(format)
        station = clean_station(station)
        t_from, t_to = clean_time(t_from, t_to)
        data_group = clean_data_group(data_group)
        route = f"/data/{format}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        return self.post(route, data)

    def get_forecast(self, station, forecast_option):
        """Forecast data package or image"""
        station = clean_station(station)
        route = f"/forecast/{station}/{forecast_option}"
        return self.get(route)

    def get_disease_last(self, station, time_period):
        """Get last Evapotranspiration"""
        station = clean_station(station)
        time_period = clean_time_period(time_period)
        route = f"/disease/{station}/last/{time_period}"
        return self.get(route)

    def get_disease(self, station, t_from, t_to):
        """Get Evapotranspiration for specified period"""
        station = clean_station(station)
        t_from, t_to = clean_time(t_from, t_to)
        route = f"/disease/{station}/from/{t_from}/to/{t_to}"
        return self.get(route)

    def post_disease_last(self, station, time_period, data):
        """Get last specified disease model"""
        station = clean_station(station)
        time_period = clean_time_period(time_period)
        route = f"/disease/{station}/last/{time_period}"
        return self.post(route, data)

    def post_disease(self, station, t_from, t_to, data):
        """Get specified disease model for period"""
        station = clean_station(station)
        t_from, t_to = clean_time(t_from, t_to)
        route = f"/disease/{station}/from/{t_from}/to/{t_to}"
        return self.post(route, data)

    def get_chart_last(self, type, station, data_group, time_period):
        """Charting last data"""
        station = clean_station(station)
        data_group = clean_data_group(data_group)
        time_period = clean_time_period(time_period)
        route = f"/chart/{type}/{station}/{data_group}/last/{time_period}"
        return self.get(route)

    def get_chart(self, type, station, data_group, t_from, t_to):
        """Charting for period"""
        station = clean_station(station)
        t_from, t_to = clean_time(t_from, t_to)
        data_group = clean_data_group(data_group)
        route = f"/chart/{type}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        return self.get(route)

    def post_chart_last(self, type, station, data_group, time_period, data):
        """Charting customized last data"""
        station = clean_station(station)
        data_group = clean_data_group(data_group)
        time_period = clean_time_period(time_period)
        route = f"/chart/{type}/{station}/{data_group}/last/{time_period}"
        return self.post(route, data)

    def post_chart(self, type, station, data_group, t_from, t_to, data):
        """Charting customized for period"""
        station = clean_station(station)
        t_from, t_to = clean_time(t_from, t_to)
        data_group = clean_data_group(data_group)
        route = f"/chart/{type}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        return self.post(route, data)

    def get_camera(self, station):
        """Read station information"""
        station = clean_station(station)
        route = f"/camera/{station}/photos/info"
        return self.get(route)

    def get_camera_photos_last(self, station, amount, camera):
        """Last amount of pictures"""
        station = clean_station(station)
        route = f"/camera/{station}/photos/last/{amount}/{camera}"
        return self.get(route)

    def get_camera_photos(self, station, t_from, t_to, camera):
        """Retrieve pictures for specified period"""
        station = clean_station(station)
        t_from, t_to = clean_time(t_from, t_to)
        route = f"/camera/{station}/photos/from/{t_from}/to/{t_to}/{camera}"
        return self.get(route)
