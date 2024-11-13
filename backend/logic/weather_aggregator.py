import statistics
from fastapi import HTTPException
from ..external_api.cached_region_lat_lon_converter import CachedRegionLatLonConverter
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from ..enums.shared_result_key_enum import SharedResultKeyEnum as srke
from ..external_api.weather_api_base import WeatherAPIBase


class WeatherAggregator():
    def __init__(self, weather_API_classes: tuple[WeatherAPIBase], region: str, days: int) -> None:
        coordinates = CachedRegionLatLonConverter.convert(region)

        if coordinates is None:
            raise HTTPException(404, "Region doesn't exist")

        self._weather_APIs = []

        for weather_API_class in weather_API_classes:
            weather_API = weather_API_class(coordinates)
            
            if weather_API.update_data(days):
                self._weather_APIs.append(weather_API)

    def get_aggregated_current(self) -> dict[hrke] | None:
        current_data = [weather_API.get_current() for weather_API in self._weather_APIs]

        return self._aggregate_data(current_data)

    def get_aggregated_hour_forecast(self, day: int, hour: int) -> dict[hrke] | None:
        hour_forecast_data = [weather_API.get_hour_forecast(day, hour) for weather_API in self._weather_APIs if weather_API.get_hour_forecast(day, hour) is not None]

        return self._aggregate_data(hour_forecast_data)

    def get_aggregated_day_forecast(self, day: int) -> dict[drke] | None:
        day_forecast_data = [weather_API.get_day_forecast(day) for weather_API in self._weather_APIs if weather_API.get_day_forecast(day) is not None]

        return self._aggregate_data(day_forecast_data)

    def _aggregate_data(self, data: list[dict[hrke | drke]]) -> dict[hrke | drke] | None:
        if not data:
            return None

        result = {}

        for key in data[0]:
            values = []

            for d in data:
                values.append(d[key])
            
            result[key] = self._get_min_max_mean(values)

        result["resources"] = len(data)

        return result

    def _get_min_max_mean(self, values: list[int | str | list]) -> dict[srke] | list[str | list]:
        if (isinstance(values[0], str) or isinstance(values[0], list)):
            return values

        min_value = min(values)
        max_value = max(values)
        mean = round(statistics.mean(values), 1)

        return {srke.MIN: min_value, srke.MAX: max_value, srke.MEAN: mean}