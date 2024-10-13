from ..external_api.weather_api_base import WeatherAPIBase
from ..enums.result_key_enum import ResultKeyEnum as rke


class WeatherAggregator():
    def __init__(self, weather_API_classes: tuple[WeatherAPIBase], region: str, days: int) -> None:
        self.weather_APIs = []

        for weather_API_class in weather_API_classes:
            weather_API = weather_API_class(region)
            
            if weather_API.update_data(days):
                self.weather_APIs.append(weather_API)

    def get_aggregated_current(self) -> dict:
        current_data = [weather_API.get_current() for weather_API in self.weather_APIs]

        result = {num: data for num, data in enumerate(current_data)}

        return result

    def get_aggregated_forecast(self, day: int, hour: int) -> dict:
        forecast_data = [weather_API.get_forecast(day, hour) for weather_API in self.weather_APIs]

        result = {num: data for num, data in enumerate(forecast_data)}

        return result
