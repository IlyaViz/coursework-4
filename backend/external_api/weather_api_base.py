from abc import ABC, abstractmethod
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke


class WeatherAPIBase(ABC):
    def __init__(self, coordinates: tuple) -> None:
        self._coordinates = coordinates
        self._data = {}

    @abstractmethod
    def update_data(self, days: int) -> bool:
        pass

    @abstractmethod
    def get_current(self) -> dict[hrke]:
        pass

    @abstractmethod
    def get_hour_forecast(self, day: int, hour: int) -> dict[hrke] | None:
        pass

    @abstractmethod
    def get_day_forecast(self, day: int) -> dict[drke] | None:
        pass
