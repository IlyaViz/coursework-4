from abc import ABC, abstractmethod
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke


class WeatherAPIBase(ABC):
    @classmethod
    @abstractmethod
    def get_weather(cls, coordinates: tuple[float, float]) -> dict:
        pass

    @classmethod
    @abstractmethod
    def _get_daily_data(cls, data: dict) -> dict:
        pass

    @classmethod
    @abstractmethod
    def _get_hourly_data(cls, data: dict) -> dict:
        pass
