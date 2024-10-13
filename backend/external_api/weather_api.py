import os
import requests
from .weather_api_base import WeatherAPIBase
from ..enums.result_key_enum import ResultKeyEnum as rke


class WeatherAPI(WeatherAPIBase):
    def update_data(self, days: int) -> bool:
        API_key = os.environ["WEATHER_API_KEY"]
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_key}&q={self.region}&days={days}"
        response = requests.get(url)

        if response.status_code == 200:
            self.data = response.json() 
            
            return True
        
        return False

    def get_current(self) -> dict:
        return self.parse_same_part_of_data(self.data["current"])

    def get_forecast(self, day: int, hour: int) -> dict | None:
        for day_info in self.data["forecast"]["forecastday"]:
            if int(day_info["date"].split("-")[2]) == day:
                for hour_info in day_info["hour"]:
                    if int(hour_info["time"].split()[1].split(":")[0]) == hour:
                        return self.parse_same_part_of_data(hour_info)

    def parse_same_part_of_data(self, part: dict) -> dict:
        result = {}
        result[rke.TEMPERATURE_C] = part["temp_c"]
        result[rke.WIND_KM] = part["wind_kph"]
        result[rke.PRESSURE_MB] = part["pressure_mb"]
        result[rke.HUMIDITY] = part["humidity"]
        result[rke.CONDITION] = part["condition"]["text"]

        return result