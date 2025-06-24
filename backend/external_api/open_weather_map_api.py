import os
import json
from datetime import datetime
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from ..enums.result_type_key_enum import ResultTypeKeyEnum as rtke
from .weather_api_base import WeatherAPIBase
from ..resources.async_client import async_client
from ..resources.async_redis import AsyncRedis
from ..constants.redis_cache import WEATHER_API_CACHE_TIME


API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")


class OpenWeatherMapAPI(WeatherAPIBase):
    @classmethod
    async def get_weather(cls, coordinates: tuple[float, float]) -> dict[rtke, dict]:
        cached_data = await AsyncRedis.safe_get(
            f"cache:open_weather_map_api:get_weather:{coordinates}"
        )

        if cached_data:
            return json.loads(cached_data)

        lat, lon = coordinates
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&exclude=minutely"

        try:
            response = await async_client.get(url)

            if response.status_code != 200:
                return {}
                
            data = response.json()

            result = {}

            result[rtke.DAILY] = cls._get_daily_data(data)
            result[rtke.HOURLY] = cls._get_hourly_data(data)

            await AsyncRedis.safe_set(
                f"cache:open_weather_map_api:get_weather:{coordinates}",
                json.dumps(result),
                ex=WEATHER_API_CACHE_TIME,
            )

            return result
        except:
            return {}

    @classmethod
    def _get_daily_data(cls, data: dict) -> dict[str, dict]:
        result = {}

        for day in data["daily"]:
            dt = day["dt"]
            date = datetime.fromtimestamp(dt).strftime("%Y-%m-%d")

            result[date] = {
                drke.MIN_TEMPERATURE: day["temp"]["min"],
                drke.MAX_TEMPERATURE: day["temp"]["max"],
                drke.AVERAGE_HUMIDITY: day["humidity"],
                drke.MAX_WIND: day["wind_speed"] * 3.6,
                drke.CONDITION: day["weather"][0]["main"],
            }

        return result

    @classmethod
    def _get_hourly_data(cls, data: dict) -> dict[str, dict]:
        result = {}

        for hour in data["hourly"]:
            dt = hour["dt"]
            time = datetime.fromtimestamp(dt).strftime("%Y-%m-%d %H:00")

            result[time] = {
                hrke.TEMPERATURE: hour["temp"],
                hrke.WIND: hour["wind_speed"] * 3.6,
                hrke.PRESSURE: hour["pressure"],
                hrke.HUMIDITY: hour["humidity"],
                hrke.CONDITION: hour["weather"][0]["main"],
            }

        return result
