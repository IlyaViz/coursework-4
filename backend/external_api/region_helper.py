import requests
import os


API_key = os.environ["GEOCODE_API_KEY"]


class RegionHelper:
    @staticmethod
    def convert(region: str) -> tuple[float, float] | None:
        url = f"https://geocode.maps.co/search?q={region}&api_key={API_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])

                return (lat, lon)

    @staticmethod
    def get_options(partial_city: str) -> list[str]:
        url = f"https://geocode.maps.co/search?q={partial_city}&api_key={API_key}"
        response = requests.get(url)

        result = []

        if response.status_code != 200:
            return result

        data = response.json()

        for option in data:
            result.append(option["display_name"])

        return result
