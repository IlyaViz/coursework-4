import os
import requests
from ..enums.result_key_enum import ResultKeyEnum as rke
from .region_lat_lon_converter import region_lat_lon_convert
from .weather_api_base import WeatherAPIBase
from ..utils.get_closest_number import get_closest_num


class OpenWeatherMapAPI(WeatherAPIBase):
    def update_data(self, days: int) -> bool:
        API_key = os.environ["OPEN_WEATHER_MAP_API_KEY"]
        pos = region_lat_lon_convert(self.region)
        
        if pos is None:
            return False

        lat, lon = pos 
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

    def get_current(self) -> dict:
        return self.parse_same_part_of_data(self.data["current"])

    def get_forecast(self, day: int, hour: int) -> dict:
        result_info = None
        hour_infos = []  
        hours = []
        forecast_list = self.data["list"]
        current_day = forecast_list[0]["dt_txt"].split()[0].split("-")[2]
        target_day = str(int(current_day) + day)

        for info in forecast_list:
            if info["dt_txt"].split()[0].split("-")[2] == target_day:
                hour_infos.append(info)

                current_hour = info["dt_txt"].split()[1].split(":")[0]
                hours.append(int(current_hour))

                if current_hour == hour:
                    result_info = info
                    break

        if result_info is None:
            closest_hour = get_closest_num(hours, hour)

            for info in hour_infos:
                if info["dt_txt"].split()[1].split(":")[0] == str(closest_hour):
                    result_info = info
                    break

        return self.parse_same_part_of_data(result_info)

    def parse_same_part_of_data(self, part: dict) -> dict:
        result = {}
        result[rke.TEMPERATURE_C] = part["main"]["temp"]
        result[rke.WIND_KM] = part["wind"]["speed"]
        result[rke.PRESSURE_MB] = part["main"]["pressure"]
        result[rke.HUMIDITY] = part["main"]["humidity"]
        result[rke.CONDITION] = part["weather"][0]["main"]

        return result