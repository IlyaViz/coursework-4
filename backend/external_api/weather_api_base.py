from abc import ABC, abstractmethod


class WeatherAPIBase(ABC):
    def __init__(self, region: str) -> None:
        self.region = region
        self.data = {}

    @abstractmethod
    def update_data(self, days: int) -> bool:
        pass

    @abstractmethod
    def get_current(self) -> dict:
        pass

    @abstractmethod
    def get_hour_forecast(self, day: int, hour: int) -> dict | None:
        pass

    @abstractmethod
    def get_day_forecast(self, day: int) -> dict | None:
        pass
    