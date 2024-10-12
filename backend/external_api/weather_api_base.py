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
    def get_forecast(self, day: int, hour: int) -> dict:
        pass
    
    @abstractmethod
    def parse_same_part_of_data(self, part: dict) -> dict:
        pass

