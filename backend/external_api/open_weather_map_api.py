import os
import requests
import statistics
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from .weather_api_base import WeatherAPIBase
from ..utils.get_closest_number import get_closest_num


class OpenWeatherMapAPI(WeatherAPIBase):
    def update_data(self, days: int) -> bool:
        API_key = os.environ["OPEN_WEATHER_MAP_API_KEY"]

        lat, lon = self._coordinates
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            self.data = response.json()
        else:
            return False

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            self.data["current"] = response.json()

            return True

        return False

    def get_current(self) -> dict[hrke]:
        return self._parse_hour_info(self.data["current"])

    def get_hour_forecast(self, day: int, hour: int) -> dict[hrke] | None:
        hour_infos = self._get_hour_infos(day)

        if hour_infos:
            hours = [self._get_hour(hour_info) for hour_info in hour_infos]

            closest_hour = get_closest_num(hours, hour)

            if abs(hour - closest_hour) > 1:
                return None

            return self._parse_hour_info(hour_infos[hours.index(closest_hour)])

    def get_day_forecast(self, day: int) -> dict[drke] | None:
        hour_infos = self._get_hour_infos(day)

        if hour_infos:
            parsed_hour_infos = [
                self._parse_hour_info(hour_info) for hour_info in hour_infos
            ]

            result = {}

            result[drke.MIN_TEMPERATURE] = min(
                [
                    parsed_hour_info[hrke.TEMPERATURE]
                    for parsed_hour_info in parsed_hour_infos
                ]
            )
            result[drke.MAX_TEMPERATURE] = max(
                [
                    parsed_hour_info[hrke.TEMPERATURE]
                    for parsed_hour_info in parsed_hour_infos
                ]
            )
            result[drke.MAX_WIND] = max(
                [parsed_hour_info[hrke.WIND] for parsed_hour_info in parsed_hour_infos]
            )
            result[drke.AVERAGE_HUMIDITY] = round(
                statistics.mean(
                    [
                        parsed_hour_info[hrke.HUMIDITY]
                        for parsed_hour_info in parsed_hour_infos
                    ]
                ),
                1,
            )
            result[drke.CONDITION] = [
                parsed_hour_info[hrke.CONDITION]
                for parsed_hour_info in parsed_hour_infos
            ]

            return result

    def _parse_hour_info(self, info: dict) -> dict[hrke]:
        result = {}

        result[hrke.TEMPERATURE] = info["main"]["temp"]
        result[hrke.WIND] = info["wind"]["speed"] * 3.6
        result[hrke.PRESSURE] = info["main"]["pressure"]
        result[hrke.HUMIDITY] = info["main"]["humidity"]
        result[hrke.CONDITION] = info["weather"][0]["main"]

        return result

    def _get_hour_infos(self, day: int) -> list[dict]:
        return [
            hour_info
            for hour_info in self.data["list"]
            if self._get_day(hour_info) == day
        ]

    def _get_hour(self, hour_info: dict) -> int:
        return int(hour_info["dt_txt"].split()[1].split(":")[0])

    def _get_day(self, hour_info: dict) -> int:
        return int(hour_info["dt_txt"].split()[0].split("-")[2])
