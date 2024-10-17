import math
from ..external_api.weather_api_base import WeatherAPIBase
from ..enums.result_key_enum import ResultKeyEnum as rke


class WeatherAggregator():
    def __init__(self, weather_API_classes: tuple[WeatherAPIBase], region: str, days: int) -> None:
        self.weather_APIs = []

        for weather_API_class in weather_API_classes:
            weather_API = weather_API_class(region)
            
            if weather_API.update_data(days):
                self.weather_APIs.append(weather_API)

    def get_aggregated_current(self) -> dict | None:
        current_data = [weather_API.get_current() for weather_API in self.weather_APIs]

        return self.aggregate_data(current_data)

    def get_aggregated_hour_forecast(self, day: int, hour: int) -> dict | None:
        hour_forecast_data = [weather_API.get_hour_forecast(day, hour) for weather_API in self.weather_APIs if weather_API.get_hour_forecast(day, hour) is not None]

        return self.aggregate_data(hour_forecast_data)

    def get_aggregated_day_forecast(self, day: int) -> dict | None:
        pass    

    def aggregate_data(self, data: list) -> dict | None:
        if not data:
            return None

        result = {}
        keys = data[0].keys()

        for key in keys:
            values = []

            for d in data:
                values.append(d[key])
            
            if key != rke.CONDITION:
                result[key] = self.get_min_max_mean(values)
            else:
                result[key] = values
        
        result["resources"] = len(data)

        return result

    def get_min_max_mean(self, values: list) -> dict:
        min_value = min(values)
        max_value = max(values)
        mean = sum(values) / len(values)

        return {"min": min_value, "max": max_value, "mean": mean}