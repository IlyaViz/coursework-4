import requests
import os


def region_lat_lon_convert(region: str) -> tuple[int, int] | None:
    API_key = os.environ["OPEN_WEATHER_MAP_API_KEY"]
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={region}&appid={API_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data[0]["lat"], data[0]["lon"]