import json
from .weather_api_base import WeatherAPIBase
from ..enums.result_type_key_enum import ResultTypeKeyEnum as rtke
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from ..resources.async_client import async_client
from ..resources.async_redis import AsyncRedis
from ..constants.redis_cache import WEATHER_API_CACHE_TIME
from ..constants.wmo_code_to_icon import WMO_TO_WEATHER_ICON


class OpenMeteoAPI(WeatherAPIBase):
    @classmethod
    async def get_weather(cls, coordinates: tuple[float, float]) -> dict:
        cached_data = await AsyncRedis.safe_get(
            f"cache:open_meteo_api:get_weather:{coordinates}"
        )

        if cached_data:
            return json.loads(cached_data)

        lat, lon = coordinates
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=sunset,sunrise,weather_code,temperature_2m_max,temperature_2m_min,wind_speed_10m_max&hourly=pressure_msl,weather_code,temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=auto"

        try:
            response = await async_client.get(url)

            if response.status_code != 200:
                return {}

            data = response.json()

            result = {}

            result[rtke.DAILY] = cls._get_daily_data(data)
            result[rtke.HOURLY] = cls._get_hourly_data(data)

            await AsyncRedis.safe_set(
                f"cache:open_meteo_api:get_weather:{coordinates}",
                json.dumps(result),
                ex=WEATHER_API_CACHE_TIME,
            )

            return result
        except Exception as e:
            print(f"Error fetching weather data from OpenMeteo: {e}")

            return {}

    @classmethod
    def _get_daily_data(cls, data: dict) -> dict[str, dict]:
        result = {}

        for day_index, day in enumerate(data["daily"]["time"]):
            result[day] = {
                drke.MIN_TEMPERATURE: data["daily"]["temperature_2m_min"][day_index],
                drke.MAX_TEMPERATURE: data["daily"]["temperature_2m_max"][day_index],
                drke.WIND: data["daily"]["wind_speed_10m_max"][day_index],
                drke.CONDITION_ICON: cls._get_weather_icon(data, day),
            }

        return result

    @classmethod
    def _get_hourly_data(cls, data: dict) -> dict[str, dict]:
        result = {}

        for time_index, dt in enumerate(data["hourly"]["time"]):
            day, time = dt.split("T")
            key = f"{day} {time}"

            result[key] = {
                hrke.TEMPERATURE: data["hourly"]["temperature_2m"][time_index],
                hrke.HUMIDITY: data["hourly"]["relative_humidity_2m"][time_index],
                hrke.WIND: data["hourly"]["wind_speed_10m"][time_index],
                hrke.PRESSURE: data["hourly"]["pressure_msl"][time_index],
                hrke.CONDITION_ICON: cls._get_weather_icon(data, day, time),
            }

        return result

    @classmethod
    def _get_weather_icon(cls, data, day, time=None):
        day_index = data["daily"]["time"].index(day)

        if time is None:
            weather_code = str(data["daily"]["weather_code"][day_index])

            return WMO_TO_WEATHER_ICON[weather_code]["day"]["image"]

        time_index = data["hourly"]["time"].index(f"{day}T{time}") if time else None
        sunrise = data["daily"]["sunrise"][day_index]
        sunset = data["daily"]["sunset"][day_index]
        weather_code = str(data["hourly"]["weather_code"][time_index])

        if sunrise <= time < sunset:
            icon = WMO_TO_WEATHER_ICON[weather_code]["day"]["image"]
        else:
            icon = WMO_TO_WEATHER_ICON[weather_code]["night"]["image"]

        return icon
