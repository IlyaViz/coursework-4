import os
import requests
from .weather_api_base import WeatherAPIBase
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke


class WeatherAPI(WeatherAPIBase):
    def update_data(self, days: int) -> bool:
        API_key = os.environ["WEATHER_API_KEY"]
        
        lat, lon = self.coordinates
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_key}&q={lat},{lon}&days={days}"
        response = requests.get(url)

        if response.status_code == 200:
            self.data = response.json() 
            
            return True
        
        return False

    def get_current(self) -> dict:
        return self.parse_hour_info(self.data["current"])

    def get_hour_forecast(self, day: int, hour: int) -> dict | None:
        for day_info in self.data["forecast"]["forecastday"]:
            if self.get_day(day_info) == day:
                for hour_info in day_info["hour"]:
                    if self.get_hour(hour_info) == hour:
                        return self.parse_hour_info(hour_info)

    def get_day_forecast(self, day: int) -> dict | None:
        for day_info in self.data["forecast"]["forecastday"]:
            if self.get_day(day_info) == day:
                result = {}

                result[drke.MIN_TEMPERATURE] = day_info["day"]["mintemp_c"]
                result[drke.MAX_TEMPERATURE] = day_info["day"]["maxtemp_c"]
                result[drke.AVERAGE_HUMIDITY] = day_info["day"]["avghumidity"]
                result[drke.MAX_WIND] = day_info["day"]["maxwind_kph"]
                result[drke.CONDITION] = day_info["day"]["condition"]["text"]
            
                return result

    def parse_hour_info(self, info: dict) -> dict:
        result = {}

        result[hrke.TEMPERATURE] = info["temp_c"]
        result[hrke.WIND] = info["wind_kph"]
        result[hrke.PRESSURE] = info["pressure_mb"]
        result[hrke.HUMIDITY] = info["humidity"]
        result[hrke.CONDITION] = info["condition"]["text"]

        return result
    
    def get_day(self, day_info: dict) -> int:
        return int(day_info["date"].split("-")[2])
    
    def get_hour(self, hour_info: dict) -> int:
        return int(hour_info["time"].split()[1].split(":")[0])