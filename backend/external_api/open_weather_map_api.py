import os
import requests
from ..enums.result_key_enum import ResultKeyEnum as rke
from .cached_region_lat_lon_converter import CachedRegionLatLonConverter
from .weather_api_base import WeatherAPIBase
from ..utils.get_closest_number import get_closest_num


class OpenWeatherMapAPI(WeatherAPIBase):
    def update_data(self, days: int) -> bool:
        API_key = os.environ["OPEN_WEATHER_MAP_API_KEY"]
        pos = CachedRegionLatLonConverter.convert(self.region)

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

    def get_forecast(self, day: int, hour: int) -> dict | None:
        hour_infos = []  
        hours = []

        for hour_info in self.data["list"]:
            if int(hour_info["dt_txt"].split()[0].split("-")[2]) == day:
                hour_infos.append(hour_info)

                current_hour = hour_info["dt_txt"].split()[1].split(":")[0]
                hours.append(int(current_hour))
                
                if int(current_hour) == hour:
                    return self.parse_same_part_of_data(hour_info)

        if hours:
            closest_hour = get_closest_num(hours, hour)

            if abs(hour - closest_hour) > 1:
                return None

            for hour_info in hour_infos:
                if int(hour_info["dt_txt"].split()[1].split(":")[0]) == closest_hour:
                    return self.parse_same_part_of_data(hour_info)

    def parse_same_part_of_data(self, part: dict) -> dict:
        result = {}
        result[rke.TEMPERATURE_C] = part["main"]["temp"]
        result[rke.WIND_KM] = part["wind"]["speed"]
        result[rke.PRESSURE_MB] = part["main"]["pressure"]
        result[rke.HUMIDITY] = part["main"]["humidity"]
        result[rke.CONDITION] = part["weather"][0]["main"]

        return result   