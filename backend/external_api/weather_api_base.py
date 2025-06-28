from abc import ABC, abstractmethod
from ..enums.result_type_key_enum import ResultTypeKeyEnum as rtke


class WeatherAPIBase(ABC):
    @classmethod
    @abstractmethod
    async def get_weather(cls, coordinates: tuple[float, float]) -> dict:
        pass

    @classmethod
    @abstractmethod
    def _get_daily_data(cls, data: dict) -> dict[str, dict]:
        pass

    @classmethod
    @abstractmethod
    def _get_hourly_data(cls, data: dict) -> dict[str, dict]:
        pass
