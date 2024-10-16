import os
import requests
from .weather_api_base import WeatherAPIBase
from ..enums.result_key_enum import CurrentAndHourResultKeyEnum as cahrke


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
        return self.parse_info(self.data["current"])

    def get_hour_forecast(self, day: int, hour: int) -> dict | None:
        for day_info in self.data["forecast"]["forecastday"]:
            if int(day_info["date"].split("-")[2]) == day:
                for hour_info in day_info["hour"]:
                    if int(hour_info["time"].split()[1].split(":")[0]) == hour:
                        return self.parse_info(hour_info)

    def get_day_forecast(self, day: int) -> dict | None:
        pass

    def parse_info(self, info: dict) -> dict:
        result = {}
        result[cahrke.TEMPERATURE_C] = info["temp_c"]
        result[cahrke.WIND_KM] = info["wind_kph"]
        result[cahrke.PRESSURE_MB] = info["pressure_mb"]
        result[cahrke.HUMIDITY] = info["humidity"]
        result[cahrke.CONDITION] = info["condition"]["text"]

        return result