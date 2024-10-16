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
        forecast_data = [weather_API.get_hour_forecast(day, hour) for weather_API in self.weather_APIs if weather_API.get_hour_forecast(day, hour) is not None]

        return self.aggregate_data(forecast_data)

    def get_aggregated_day_forecast(self, day: int, hour: int) -> dict | None:
        pass    

    def aggregate_data(self, data: list) -> dict | None:
        if not data:
            return None

        result = {}
        result[rke.TEMPERATURE_C] = self.get_mean_with_chance([d[rke.TEMPERATURE_C] for d in data])
        result[rke.WIND_KM] = self.get_mean_with_chance([d[rke.WIND_KM] for d in data])
        result[rke.PRESSURE_MB] = self.get_mean_with_chance([d[rke.PRESSURE_MB] for d in data])
        result[rke.HUMIDITY] = self.get_mean_with_chance([d[rke.HUMIDITY] for d in data])
        result[rke.CONDITION] = [d[rke.CONDITION] for d in data]
        
        result["resources"] = len(data)

        return result

    def get_mean_with_chance(self, values: list) -> tuple:
        #CHAT GPT formula
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        stddev = math.sqrt(variance)
        chance = max(0, min(100, (1 - stddev / max(abs(mean), 1)) * 100)) 

        return (round(mean, 1), int(chance))