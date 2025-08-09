from abc import ABC, abstractmethod
from typing import Any
from ..types.general_weather_api_types import ForecastData, DailyData, HourlyData


class WeatherAPIBase(ABC):
    @classmethod
    @abstractmethod
    async def get_weather(cls, coordinates: tuple[float, float]) -> ForecastData:
        pass

    @classmethod
    @abstractmethod
    def _get_daily_data(cls, data: Any) -> DailyData:
        pass

    @classmethod
    @abstractmethod
    def _get_hourly_data(cls, data: Any) -> HourlyData:
        pass
