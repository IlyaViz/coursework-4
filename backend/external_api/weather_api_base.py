from abc import ABC, abstractmethod
from .cached_region_lat_lon_converter import CachedRegionLatLonConverter


class WeatherAPIBase(ABC):
    def __init__(self, region: str) -> None:
        self.pos = CachedRegionLatLonConverter.convert(region)
        self.data = {}

    @abstractmethod
    def update_data(self, days: int) -> bool:
        pass

    @abstractmethod
    def get_current(self) -> dict:
        pass

    @abstractmethod
    def get_hour_forecast(self, day: int, hour: int) -> dict | None:
        pass

    @abstractmethod
    def get_day_forecast(self, day: int) -> dict | None:
        pass
    