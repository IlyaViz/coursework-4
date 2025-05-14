from time import time
from ..external_api.weather_api_base import WeatherAPIBase
from ..constants.weather_aggregation_constants import MAX_DAYS, CACHE_TIME
from .weather_aggregator import WeatherAggregator


class CachedWeatherAggregator:
    _cache = {}

    @classmethod
    def get_weather_aggregator(
        cls,
        weather_API_classes: tuple[WeatherAPIBase],
        region: str,
        days: int = MAX_DAYS,
    ) -> WeatherAggregator:
        cls._clean_cache()

        key = (weather_API_classes, region, days)

        if key in cls._cache:
            return cls._cache[key][1]
        else:
            weather_aggregator = WeatherAggregator(weather_API_classes, region, days)
            cls._cache[key] = (time() + CACHE_TIME, weather_aggregator)

            return weather_aggregator

    @classmethod
    def _clean_cache(cls) -> None:
        for key in list(cls._cache):
            if time() >= cls._cache[key][0]:
                del cls._cache[key]
