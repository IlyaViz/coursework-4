import statistics
from fastapi import HTTPException
from ..external_api.cached_region_lat_lon_converter import CachedRegionLatLonConverter
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke


class WeatherAggregator():
    def __init__(self, weather_API_classes: tuple, region: str, days: int) -> None:
        coordinates = CachedRegionLatLonConverter.convert(region)

        if coordinates is None:
            raise HTTPException(404, "Region doesn't exist")

        self.weather_APIs = []

        for weather_API_class in weather_API_classes:
            weather_API = weather_API_class(coordinates)
            
            if weather_API.update_data(days):
                self.weather_APIs.append(weather_API)

    def get_aggregated_current(self) -> dict | None:
        current_data = [weather_API.get_current() for weather_API in self.weather_APIs]

        return self.aggregate_data(current_data)

    def get_aggregated_hour_forecast(self, day: int, hour: int) -> dict | None:
        hour_forecast_data = [weather_API.get_hour_forecast(day, hour) for weather_API in self.weather_APIs if weather_API.get_hour_forecast(day, hour) is not None]

        return self.aggregate_data(hour_forecast_data)

    def get_aggregated_day_forecast(self, day: int) -> dict | None:
        day_forecast_data = [weather_API.get_day_forecast(day) for weather_API in self.weather_APIs if weather_API.get_day_forecast(day) is not None]

        return self.aggregate_data(day_forecast_data)

    def aggregate_data(self, data: list) -> dict | None:
        if not data:
            return None

        result = {}

        for key in data[0]:
            values = []

            for d in data:
                values.append(d[key])
            
            result[key] = self.get_min_max_mean(values)

        result["resources"] = len(data)

        return result

    def get_min_max_mean(self, values: list) -> dict | list:
        if (isinstance(values[0], str) or isinstance(values[0], list)):
            return values

        min_value = min(values)
        max_value = max(values)
        mean = round(statistics.mean(values), 1)

        return {"min": min_value, "max": max_value, "mean": mean}