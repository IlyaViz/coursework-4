import os
from .weather_api_base import WeatherAPIBase
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from ..enums.result_type_key_enum import ResultTypeKeyEnum as rtke
from .async_client import async_client


API_KEY = os.environ.get("WEATHER_API_KEY")


class WeatherAPI(WeatherAPIBase):
    @classmethod
    async def get_weather(cls, coordinates: tuple[float, float]) -> dict[rtke, dict]:
        lat, lon = coordinates
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={lat},{lon}&days=14"

        response = await async_client.get(url)

        if response.status_code != 200:
            return {}

        data = response.json()

        result = {}

        result[rtke.DAILY] = cls._get_daily_data(data)
        result[rtke.HOURLY] = cls._get_hourly_data(data)

        return result

    @classmethod
    def _get_daily_data(cls, data: dict) -> dict[str, dict]:
        result = {}

        for day in data["forecast"]["forecastday"]:
            date = day["date"]

            result[date] = {
                drke.MIN_TEMPERATURE: day["day"]["mintemp_c"],
                drke.MAX_TEMPERATURE: day["day"]["maxtemp_c"],
                drke.AVERAGE_HUMIDITY: day["day"]["avghumidity"],
                drke.MAX_WIND: day["day"]["maxwind_kph"],
                drke.CONDITION: day["day"]["condition"]["text"],
            }

        return result

    @classmethod
    def _get_hourly_data(cls, data: dict) -> dict[str, dict]:
        result = {}

        for day in data["forecast"]["forecastday"]:
            for hour in day["hour"]:
                time = hour["time"]

                result[time] = {
                    hrke.TEMPERATURE: hour["temp_c"],
                    hrke.WIND: hour["wind_kph"],
                    hrke.PRESSURE: hour["pressure_mb"],
                    hrke.HUMIDITY: hour["humidity"],
                    hrke.CONDITION: hour["condition"]["text"],
                }

        return result
