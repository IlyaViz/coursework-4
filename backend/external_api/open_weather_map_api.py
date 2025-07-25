import os
import json
import httpx
import logging
from datetime import datetime
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from ..enums.result_type_key_enum import ResultTypeKeyEnum as rtke
from .weather_api_base import WeatherAPIBase
from ..resources.async_client import async_client
from ..resources.async_redis import AsyncRedis
from ..constants.redis_cache import WEATHER_API_CACHE_TIME
from ..exceptions.external_api_exceptions import APIResponseException
from ..types.general_weather_api_types import DailyData, HourlyData, ForecastData
from ..types.open_weather_map_api_types import UsedData


logger = logging.getLogger(__name__)

API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")


class OpenWeatherMapAPI(WeatherAPIBase):
    @classmethod
    async def get_weather(cls, coordinates: tuple[float, float]) -> ForecastData:
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
                logger.error(
                    f"Failed to fetch weather data for coordinates {coordinates}"
                )

                raise APIResponseException(
                    f"Failed to fetch weather data for coordinates {coordinates}"
                )

            data = response.json()
            data = {
                "daily": data["daily"],
                "hourly": data["hourly"],
                "timezone_offset": data["timezone_offset"],
            }

            result = {}

            result[rtke.DAILY] = cls._get_daily_data(data)
            result[rtke.HOURLY] = cls._get_hourly_data(data)

            await AsyncRedis.safe_set(
                f"cache:open_weather_map_api:get_weather:{coordinates}",
                json.dumps(result),
                ex=WEATHER_API_CACHE_TIME,
            )

            return result
        except APIResponseException as e:
            raise
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")

            raise APIResponseException(f"Connection error: {e}")
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {e}")

            raise APIResponseException(f"Timeout error: {e}")

    @classmethod
    def _get_daily_data(cls, data: UsedData) -> DailyData:
        result = {}

        for day in data["daily"]:
            dt = day["dt"] + data["timezone_offset"]
            date = datetime.fromtimestamp(dt).strftime("%Y-%m-%d")

            result[date] = {
                drke.MIN_TEMPERATURE: day["temp"]["min"],
                drke.MAX_TEMPERATURE: day["temp"]["max"],
                drke.HUMIDITY: day["humidity"],
                drke.WIND: round(day["wind_speed"] * 3.6, 2),
                drke.CONDITION_ICON: f"https://openweathermap.org/img/wn/{day['weather'][0]['icon']}@2x.png",
            }

        return result

    @classmethod
    def _get_hourly_data(cls, data: UsedData) -> HourlyData:
        result = {}

        for hour in data["hourly"]:
            dt = hour["dt"] + data["timezone_offset"]
            time = datetime.fromtimestamp(dt).strftime("%Y-%m-%d %H:00")

            result[time] = {
                hrke.TEMPERATURE: hour["temp"],
                hrke.WIND: round(hour["wind_speed"] * 3.6, 2),
                hrke.PRESSURE: hour["pressure"],
                hrke.HUMIDITY: hour["humidity"],
                hrke.CONDITION_ICON: f"https://openweathermap.org/img/wn/{hour['weather'][0]['icon']}@2x.png",
            }

        return result
