"""An asynchronous client for the iMetos FieldClimate API."""

__all__ = ["FieldClimateClient"]
__version__ = "1.2"
__author__ = "Agrimanagement, Inc."

from datetime import datetime
from functools import partialmethod
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
        headers = {
            "Accept": "application/json",  # we always want json back.
            "Date": date,
            "Authorization": f"hmac {self.public_key}:{signature.hexdigest()}",
        }
        return headers

    async def request(self, method, **kwargs):
        # Inject our headers, allowing them to be overridden by kwargs.
        headers = self.get_headers(method, kwargs["path"])
        kwargs["headers"] = {**headers, **kwargs.get("headers", {})}
        # Session.request() will generate the full url using kwargs["path"].
        return await super().request(method, **kwargs)

    # Re-create the http methods Session provides, using our new request method:

    get = partialmethod(request, "GET")
    head = partialmethod(request, "HEAD")
    post = partialmethod(request, "POST")
    put = partialmethod(request, "PUT")
    delete = partialmethod(request, "DELETE")
    options = partialmethod(request, "OPTIONS")

    # Full description of all methods: https://api.fieldclimate.com/v1/docs/

    async def get_user(self):
        """Read user information"""
        route = "/user"
        response = await self.get(path=route)
        return response.json()

    async def put_user(self, data):
        """Update user information"""
        route = "/user"
        response = await self.put(path=route, data=data)
        return response.json()

    async def delete_user(self):
        """Delete user account"""
        route = "/user"
        response = await self.delete(path=route)
        return response.json()

    async def get_user_stations(self):
        """Read list of stations of a user"""
        route = "/user/stations"
        response = await self.get(path=route)
        return response.json()

    async def get_user_licenses(self):
        """Read user licenses"""
        route = "/user/licenses"
        response = await self.get(path=route)
        return response.json()

    async def get_system_status(self):
        """System running correctly"""
        route = "/system/status"
        response = await self.get(path=route)
        return response.json()

    async def get_system_sensors(self):
        """Supported sensors"""
        route = "/system/sensors"
        response = await self.get(path=route)
        return response.json()

    async def get_system_groups(self):
        """Supported sensor groups"""
        route = "/system/groups"
        response = await self.get(path=route)
        return response.json()

    async def get_system_group_sensors(self):
        """Sensors organized in groups"""
        route = "/system/group/sensors"
        response = await self.get(path=route)
        return response.json()

    async def get_system_types(self):
        """Type of devices"""
        route = "/system/types"
        response = await self.get(path=route)
        return response.json()

    async def get_system_countries(self):
        """Countries for the languages"""
        route = "/system/countries"
        response = await self.get(path=route)
        return response.json()

    async def get_system_timezones(self):
        """Timezones"""
        route = "/system/timezones"
        response = await self.get(path=route)
        return response.json()

    async def get_system_diseases(self):
        """Disease models"""
        route = "/system/diseases"
        response = await self.get(path=route)
        return response.json()

    async def get_station(self, station):
        """Read station information"""
        station = clean.station(station)
        route = f"/station/{station}"
        response = await self.get(path=route)
        return response.json()

    async def put_station(self, station, data):
        """Update station information"""
        station = clean.station(station)
        route = f"/station/{station}"
        response = await self.put(path=route, data=data)
        return response.json()

    async def get_station_sensors(self, station):
        """Get list of sensors of a station"""
        station = clean.station(station)
        route = f"/station/{station}/sensors"
        response = await self.get(path=route)
        return response.json()

    async def put_station_sensors(self, station, data):
        """Update station sensor name"""
        station = clean.station(station)
        route = f"/station/{station}/sensors"
        response = await self.put(path=route, data=data)
        return response.json()

    async def get_station_nodes(self, station):
        """Get list of nodes (wireless devices) connected to a station"""
        station = clean.station(station)
        route = f"/station/{station}/nodes"
        response = await self.get(path=route)
        return response.json()

    async def put_station_nodes(self, station, data):
        """Update the name of a node itself"""
        station = clean.station(station)
        route = f"/station/{station}/nodes"
        response = await self.put(path=route, data=data)
        return response.json()

    async def get_station_serials(self, station):
        """List of serials (of a sensor) and their names"""
        station = clean.station(station)
        route = f"/station/{station}/serials"
        response = await self.get(path=route)
        return response.json()

    async def put_station_serials(self, station, data):
        """Update sensor with serial the name"""
        station = clean.station(station)
        route = f"/station/{station}/serials"
        response = await self.put(path=route, data=data)
        return response.json()

    async def post_station_key(self, station, station_key, data):
        """Add station to user account"""
        station = clean.station(station)
        route = f"/station/{station}/{station_key}"
        response = await self.post(path=route, data=data)
        return response.json()

    async def delete_station_key(self, station, station_key):
        """Remove station from user account"""
        station = clean.station(station)
        route = f"/station/{station}/{station_key}"
        response = await self.delete(path=route)
        return response.json()

    async def get_stations_in_proximity(self, station, radius):
        """Stations in close proximity of specified station"""
        station = clean.station(station)
        route = f"/station/{station}/proximity/{radius}"
        response = await self.get(path=route)
        return response.json()

    async def get_station_events_last(self, station, amount, sort):
        """Last station events"""
        station = clean.station(station)
        sort = clean.sort(sort)
        route = f"/station/{station}/events/last/{amount}/{sort}"
        response = await self.get(path=route)
        return response.json()

    async def get_station_events(self, station, t_from, t_to, sort):
        """Station events from to"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        sort = clean.sort(sort)
        route = f"/station/{station}/events/from/{t_from}/to/{t_to}/{sort}"
        response = await self.get(path=route)
        return response.json()

    async def get_station_history_last(self, station, filter, amount, sort):
        """Last station communication history filter"""
        station = clean.station(station)
        filter = clean.filter(filter)
        sort = clean.sort(sort)
        route = f"/station/{station}/history/{filter}/last/{amount}/{sort}"
        response = await self.get(path=route)
        return response.json()

    async def get_station_history(self, station, filter, t_from, t_to, sort):
        """Station communication history from to filter"""
        station = clean.station(station)
        filter = clean.filter(filter)
        t_from, t_to = clean.time(t_from, t_to)
        sort = clean.sort(sort)
        route = f"/station/{station}/history/{filter}/from/{t_from}/to/{t_to}/{sort}"
        response = await self.get(path=route)
        return response.json()

    async def get_station_licenses(self, station):
        """Station licenses for disease models or forecast"""
        station = clean.station(station)
        route = f"/station/{station}/licenses"
        response = await self.get(path=route)
        return response.json()

    async def get_data_range(self, station):
        """Min and Max date of data availability"""
        station = clean.station(station)
        route = f"/data/{station}"
        response = await self.get(path=route)
        return response.json()

    async def get_data_last(self, format, station, data_group, time_period):
        """Reading last data"""
        format = clean.format(format)
        station = clean.station(station)
        data_group = clean.data_group(data_group)
        time_period = clean.time_period(time_period)
        route = f"/data/{format}/{station}/{data_group}/last/{time_period}"
        response = await self.get(path=route)
        return response.json()

    async def get_data(self, format, station, data_group, t_from, t_to):
        """Reading data of specific time period"""
        format = clean.format(format)
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        data_group = clean.data_group(data_group)
        route = f"/data/{format}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        response = await self.get(path=route)
        return response.json()

    async def post_data_last(self, format, station, data_group, time_period, data):
        """Filtered/Customized reading of last data"""
        format = clean.format(format)
        station = clean.station(station)
        data_group = clean.data_group(data_group)
        time_period = clean.time_period(time_period)
        route = f"/data/{format}/{station}/{data_group}/last/{time_period}"
        response = await self.post(path=route, data=data)
        return response.json()

    async def post_data(self, format, station, data_group, t_from, t_to, data):
        """Filtered/Customized reading of specified time period"""
        format = clean.format(format)
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        data_group = clean.data_group(data_group)
        route = f"/data/{format}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        response = await self.post(path=route, data=data)
        return response.json()

    async def get_forecast(self, station, forecast_option):
        """Forecast data package or image"""
        station = clean.station(station)
        route = f"/forecast/{station}/{forecast_option}"
        response = await self.get(path=route)
        return response.json()

    async def get_disease_last(self, station, time_period):
        """Get last Evapotranspiration"""
        station = clean.station(station)
        time_period = clean.time_period(time_period)
        route = f"/disease/{station}/last/{time_period}"
        response = await self.get(path=route)
        return response.json()

    async def get_disease(self, station, t_from, t_to):
        """Get Evapotranspiration for specified period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        route = f"/disease/{station}/from/{t_from}/to/{t_to}"
        response = await self.get(path=route)
        return response.json()

    async def post_disease_last(self, station, time_period, data):
        """Get last specified disease model"""
        station = clean.station(station)
        time_period = clean.time_period(time_period)
        route = f"/disease/{station}/last/{time_period}"
        response = await self.post(path=route, data=data)
        return response.json()

    async def post_disease(self, station, t_from, t_to, data):
        """Get specified disease model for period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        route = f"/disease/{station}/from/{t_from}/to/{t_to}"
        response = await self.post(path=route, data=data)
        return response.json()

    async def get_chart_last(self, type, station, data_group, time_period):
        """Charting last data"""
        station = clean.station(station)
        data_group = clean.data_group(data_group)
        time_period = clean.time_period(time_period)
        route = f"/chart/{type}/{station}/{data_group}/last/{time_period}"
        response = await self.get(path=route)
        return response.json()

    async def get_chart(self, type, station, data_group, t_from, t_to):
        """Charting for period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        data_group = clean.data_group(data_group)
        route = f"/chart/{type}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        response = await self.get(path=route)
        return response.json()

    async def post_chart_last(self, type, station, data_group, time_period, data):
        """Charting customized last data"""
        station = clean.station(station)
        data_group = clean.data_group(data_group)
        time_period = clean.time_period(time_period)
        route = f"/chart/{type}/{station}/{data_group}/last/{time_period}"
        response = await self.post(path=route, data=data)
        return response.json()

    async def post_chart(self, type, station, data_group, t_from, t_to, data):
        """Charting customized for period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        data_group = clean.data_group(data_group)
        route = f"/chart/{type}/{station}/{data_group}/from/{t_from}/to/{t_to}"
        response = await self.post(path=route, data=data)
        return response.json()

    async def get_camera(self, station):
        """Read station information"""
        station = clean.station(station)
        route = f"/camera/{station}/photos/info"
        response = await self.get(path=route)
        return response.json()

    async def get_camera_photos_last(self, station, amount, camera):
        """Last amount of pictures"""
        station = clean.station(station)
        route = f"/camera/{station}/photos/last/{amount}/{camera}"
        response = await self.get(path=route)
        return response.json()

    async def get_camera_photos(self, station, t_from, t_to, camera):
        """Retrieve pictures for specified period"""
        station = clean.station(station)
        t_from, t_to = clean.time(t_from, t_to)
        route = f"/camera/{station}/photos/from/{t_from}/to/{t_to}/{camera}"
        response = await self.get(path=route)
        return response.json()
