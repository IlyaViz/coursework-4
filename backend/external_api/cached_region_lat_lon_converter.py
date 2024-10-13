import requests
import os


class CachedRegionLatLonConverter():
    cache = {}
    
    @classmethod
    def convert(cls, region: str) -> tuple[int, int] | None:
        if cls.cache.get(region, 0) != 0:
            return cls.cache[region]

        API_key = os.environ["GEOCODE_API_KEY"]
        url = f"https://geocode.maps.co/search?q={region}&api_key={API_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                
                cls.cache[region] = (lat, lon)

                return (lat, lon)
