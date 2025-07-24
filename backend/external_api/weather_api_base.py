from abc import ABC, abstractmethod


class WeatherAPIBase(ABC):
    @classmethod
    @abstractmethod
    async def get_weather(cls, coordinates: tuple[float, float]) -> dict:
        pass

    @classmethod
    @abstractmethod
    def _get_daily_data(cls, data: dict) -> dict:
        pass

    @classmethod
    @abstractmethod
    def _get_hourly_data(cls, data: dict) -> dict:
        pass
