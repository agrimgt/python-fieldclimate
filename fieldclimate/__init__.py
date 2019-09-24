"""An asynchronous client for the iMetos FieldClimate API."""

__all__ = ["FieldClimateClient"]
__version__ = "1.3"
__author__ = "Agrimanagement, Inc."

from datetime import datetime
from os import getenv

from asks import Session
from Crypto.Hash import HMAC, SHA256

from fieldclimate import clean


class FieldClimateClient(Session):
    """Adapt asks.Session to FieldClimate's API.

    Requires HMAC public and private keys for authentication.

    Usage: See README.rst
    """

    base_location = "https://api.fieldclimate.com/v1"
    public_key = None
    private_key = None

    def __init__(self, public_key=None, private_key=None, **kwargs):
        # Set hmac keys, preferring init args over env vars over subclass's attributes.
        self.public_key = public_key or self.find_public_key() or self.public_key
        self.private_key = private_key or self.find_private_key() or self.private_key
        # Set base_location so asks can build urls for us.
        default_session_kwargs = {"base_location": self.base_location}
        super().__init__(**default_session_kwargs, **kwargs)

    @classmethod
    def find_public_key(cls):
        return getenv("FIELDCLIMATE_PUBLIC_KEY")

    @classmethod
    def find_private_key(cls):
        return getenv("FIELDCLIMATE_PRIVATE_KEY")

    def get_headers(self, method, path):
        # Create HMAC authentication headers as described here:
        # https://api.fieldclimate.com/v1/docs/#authentication-hmac
        date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        if None in [self.public_key, self.private_key]:
            raise TypeError("HMAC headers require public_ and private_key settings.")
        message = method + path + date + self.public_key
        signature = HMAC.new(self.private_key.encode(), message.encode(), SHA256)
        return {
            "Accept": "application/json",
            "Date": date,
            "Authorization": f"hmac {self.public_key}:{signature.hexdigest()}",
        }

    async def request_json(self, method, path, data=None):
        headers = self.get_headers(method, path)
        # Session.request() will generate the full url using base_location and path.
        response = await self.request(method, path=path, data=data, headers=headers)
        return response.json()

    # Full description of all methods: https://api.fieldclimate.com/v1/docs/

    def get_user(self):
        """Read user information"""
        path = "/user"
        return self.request_json("GET", path)

    def put_user(self, data):
        """Update user information"""
        path = "/user"
        return self.request_json("PUT", path, data)

    def delete_user(self):
        """Delete user account"""
        path = "/user"
        return self.request_json("DELETE", path)

    def get_user_stations(self):
        """Read list of stations of a user"""
        path = "/user/stations"
        return self.request_json("GET", path)

    def get_user_licenses(self):
        """Read user licenses"""
        path = "/user/licenses"
        return self.request_json("GET", path)

    def get_system_status(self):
        """System running correctly"""
        path = "/system/status"
        return self.request_json("GET", path)

    def get_system_sensors(self):
        """Supported sensors"""
        path = "/system/sensors"
        return self.request_json("GET", path)

    def get_system_groups(self):
        """Supported sensor groups"""
        path = "/system/groups"
        return self.request_json("GET", path)

    def get_system_group_sensors(self):
        """Sensors organized in groups"""
        path = "/system/group/sensors"
        return self.request_json("GET", path)

    def get_system_types(self):
        """Type of devices"""
        path = "/system/types"
        return self.request_json("GET", path)

    def get_system_countries(self):
        """Countries for the languages"""
        path = "/system/countries"
        return self.request_json("GET", path)

    def get_system_timezones(self):
        """Timezones"""
        path = "/system/timezones"
        return self.request_json("GET", path)

    def get_system_diseases(self):
        """Disease models"""
        path = "/system/diseases"
        return self.request_json("GET", path)

    def get_station(self, station):
        """Read station information"""
        station = clean.station(station)
        path = f"/station/{station}"
        return self.request_json("GET", path)

    def put_station(self, station, data):
        """Update station information"""
        station = clean.station(station)
        path = f"/station/{station}"
        return self.request_json("PUT", path, data)

    def get_station_sensors(self, station):
        """Get list of sensors of a station"""
        station = clean.station(station)
        path = f"/station/{station}/sensors"
        return self.request_json("GET", path)

    def put_station_sensors(self, station, data):
        """Update station sensor name"""
        station = clean.station(station)
        path = f"/station/{station}/sensors"
        return self.request_json("PUT", path, data)

    def get_station_nodes(self, station):
        """Get list of nodes (wireless devices) connected to a station"""
        station = clean.station(station)
        path = f"/station/{station}/nodes"
        return self.request_json("GET", path)

    def put_station_nodes(self, station, data):
        """Update the name of a node itself"""
        station = clean.station(station)
        path = f"/station/{station}/nodes"
        return self.request_json("PUT", path, data)

    def get_station_serials(self, station):
        """List of serials (of a sensor) and their names"""
        station = clean.station(station)
        path = f"/station/{station}/serials"
        return self.request_json("GET", path)

    def put_station_serials(self, station, data):
        """Update sensor with serial the name"""
        station = clean.station(station)
        path = f"/station/{station}/serials"
        return self.request_json("PUT", path, data)

    def post_station_key(self, station, station_key, data):
        """Add station to user account"""
        station = clean.station(station)
        path = f"/station/{station}/{station_key}"
        return self.request_json("POST", path, data)

    def delete_station_key(self, station, station_key):
        """Remove station from user account"""
        station = clean.station(station)
        path = f"/station/{station}/{station_key}"
        return self.request_json("DELETE", path)

    def get_stations_in_proximity(self, station, radius):
        """Stations in close proximity of specified station"""
        station = clean.station(station)
        path = f"/station/{station}/proximity/{radius}"
        return self.request_json("GET", path)

    def get_station_events_last(self, station, amount, sort):
        """Last station events"""
        station = clean.station(station)
        sort = clean.sort(sort)
        path = f"/station/{station}/events/last/{amount}/{sort}"
        return self.request_json("GET", path)

    def get_station_events(self, station, t_from, t_to, sort):
        """Station events from to"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        sort = clean.sort(sort)
        path = f"/station/{station}/events/from/{t_from}/to/{t_to}/{sort}"
        return self.request_json("GET", path)

    def get_station_history_last(self, station, filter, amount, sort):
        """Last station communication history filter"""
        station = clean.station(station)
        filter = clean.filter(filter)
        sort = clean.sort(sort)
        path = f"/station/{station}/history/{filter}/last/{amount}/{sort}"
        return self.request_json("GET", path)

    def get_station_history(self, station, filter, t_from, t_to, sort):
        """Station communication history from to filter"""
        station = clean.station(station)
        filter = clean.filter(filter)
        t_from, t_to = clean.time(t_from, t_to)
        sort = clean.sort(sort)
        path = f"/station/{station}/history/{filter}/from/{t_from}/to/{t_to}/{sort}"
        return self.request_json("GET", path)

    def get_station_licenses(self, station):
        """Station licenses for disease models or forecast"""
        station = clean.station(station)
        path = f"/station/{station}/licenses"
        return self.request_json("GET", path)

    def get_data_range(self, station):
        """Min and Max date of data availability"""
        station = clean.station(station)
        path = f"/data/{station}"
        return self.request_json("GET", path)

    def get_data_last(self, format, station, data_group, time_period):
        """Reading last data"""
        format = clean.format(format)
        station = clean.station(station)
        data_group = clean.data_group(data_group)
        time_period = clean.time_period(time_period)
        path = f"/data/{format}/{station}/{data_group}/last/{time_period}"
        return self.request_json("GET", path)

    def get_data(self, format, station, data_group, t_from, t_to):
        """Reading data of specific time period"""
        format = clean.format(format)
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        data_group = clean.data_group(data_group)
        path = f"/data/{format}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        return self.request_json("GET", path)

    def post_data_last(self, format, station, data_group, time_period, data):
        """Filtered/Customized reading of last data"""
        format = clean.format(format)
        station = clean.station(station)
        data_group = clean.data_group(data_group)
        time_period = clean.time_period(time_period)
        path = f"/data/{format}/{station}/{data_group}/last/{time_period}"
        return self.request_json("POST", path, data)

    def post_data(self, format, station, data_group, t_from, t_to, data):
        """Filtered/Customized reading of specified time period"""
        format = clean.format(format)
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        data_group = clean.data_group(data_group)
        path = f"/data/{format}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        return self.request_json("POST", path, data)

    def get_forecast(self, station, forecast_option):
        """Forecast data package or image"""
        station = clean.station(station)
        path = f"/forecast/{station}/{forecast_option}"
        return self.request_json("GET", path)

    def get_disease_last(self, station, time_period):
        """Get last Evapotranspiration"""
        station = clean.station(station)
        time_period = clean.time_period(time_period)
        path = f"/disease/{station}/last/{time_period}"
        return self.request_json("GET", path)

    def get_disease(self, station, t_from, t_to):
        """Get Evapotranspiration for specified period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        path = f"/disease/{station}/from/{t_from}/to/{t_to}"
        return self.request_json("GET", path)

    def post_disease_last(self, station, time_period, data):
        """Get last specified disease model"""
        station = clean.station(station)
        time_period = clean.time_period(time_period)
        path = f"/disease/{station}/last/{time_period}"
        return self.request_json("POST", path, data)

    def post_disease(self, station, t_from, t_to, data):
        """Get specified disease model for period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        path = f"/disease/{station}/from/{t_from}/to/{t_to}"
        return self.request_json("POST", path, data)

    def get_chart_last(self, type, station, data_group, time_period):
        """Charting last data"""
        station = clean.station(station)
        data_group = clean.data_group(data_group)
        time_period = clean.time_period(time_period)
        path = f"/chart/{type}/{station}/{data_group}/last/{time_period}"
        return self.request_json("GET", path)

    def get_chart(self, type, station, data_group, t_from, t_to):
        """Charting for period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        data_group = clean.data_group(data_group)
        path = f"/chart/{type}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        return self.request_json("GET", path)

    def post_chart_last(self, type, station, data_group, time_period, data):
        """Charting customized last data"""
        station = clean.station(station)
        data_group = clean.data_group(data_group)
        time_period = clean.time_period(time_period)
        path = f"/chart/{type}/{station}/{data_group}/last/{time_period}"
        return self.request_json("POST", path, data)

    def post_chart(self, type, station, data_group, t_from, t_to, data):
        """Charting customized for period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        data_group = clean.data_group(data_group)
        path = f"/chart/{type}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        return self.request_json("POST", path, data)

    def get_camera(self, station):
        """Read station information"""
        station = clean.station(station)
        path = f"/camera/{station}/photos/info"
        return self.request_json("GET", path)

    def get_camera_photos_last(self, station, amount, camera):
        """Last amount of pictures"""
        station = clean.station(station)
        path = f"/camera/{station}/photos/last/{amount}/{camera}"
        return self.request_json("GET", path)

    def get_camera_photos(self, station, t_from, t_to, camera):
        """Retrieve pictures for specified period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        path = f"/camera/{station}/photos/from/{t_from}/to/{t_to}/{camera}"
        return self.request_json("GET", path)
