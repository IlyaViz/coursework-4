import os
import requests
from ..enums.result_key_enum import CurrentAndHourResultKeyEnum as cahrke
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
        return self.parse_info(self.data["current"])

    def get_hour_forecast(self, day: int, hour: int) -> dict | None:
        hour_infos = []  
        hours = []

        for hour_info in self.data["list"]:
            if int(hour_info["dt_txt"].split()[0].split("-")[2]) == day:
                hour_infos.append(hour_info)

                current_hour = hour_info["dt_txt"].split()[1].split(":")[0]
                hours.append(int(current_hour))
                
                if int(current_hour) == hour:
                    return self.parse_info(hour_info)

        if hours:
            closest_hour = get_closest_num(hours, hour)

            if abs(hour - closest_hour) > 1:
                return None

            for hour_info in hour_infos:
                if int(hour_info["dt_txt"].split()[1].split(":")[0]) == closest_hour:
                    return self.parse_info(hour_info)

    def get_day_forecast(self, day: int) -> dict | None:
        pass

    def parse_info(self, info: dict) -> dict:
        result = {}
        result[cahrke.TEMPERATURE_C] = info["main"]["temp"]
        result[cahrke.WIND_KM] = info["wind"]["speed"]
        result[cahrke.PRESSURE_MB] = info["main"]["pressure"]
        result[cahrke.HUMIDITY] = info["main"]["humidity"]
        result[cahrke.CONDITION] = info["weather"][0]["main"]

        return result   