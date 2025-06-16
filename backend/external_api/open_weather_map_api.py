import os
import requests
from datetime import datetime
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from .weather_api_base import WeatherAPIBase


API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")


class OpenWeatherMapAPI(WeatherAPIBase):
    @classmethod
    def get_weather(cls, coordinates: tuple[float, float]) -> dict:
        lat, lon = coordinates
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&exclude=minutely"
        response = requests.get(url)

        if response.status_code != 200:
            return {}

        data = response.json()

        result = {}

        result["daily"] = cls._get_daily_data(data)
        result["hourly"] = cls._get_hourly_data(data)

        return result

    @classmethod
    def _get_daily_data(cls, data: dict) -> dict:
        result = {}

        for day in data["daily"]:
            dt = day["dt"]
            date = datetime.fromtimestamp(dt).strftime("%Y-%m-%d")

            result[date] = {
                drke.MIN_TEMPERATURE: day["temp"]["min"],
                drke.MAX_TEMPERATURE: day["temp"]["max"],
                drke.AVERAGE_HUMIDITY: day["humidity"],
                drke.MAX_WIND: day["wind_speed"],
                drke.CONDITION: day["weather"][0]["main"],
            }

        return result

    @classmethod
    def _get_hourly_data(cls, data: dict) -> dict:
        result = {}

        for hour in data["hourly"]:
            dt = hour["dt"]
            time = datetime.fromtimestamp(dt).strftime("%Y-%m-%d %H:00")

            result[time] = {
                hrke.TEMPERATURE: hour["temp"],
                hrke.WIND: hour["wind_speed"],
                hrke.PRESSURE: hour["pressure"],
                hrke.HUMIDITY: hour["humidity"],
                hrke.CONDITION: hour["weather"][0]["main"],
            }

        return result
