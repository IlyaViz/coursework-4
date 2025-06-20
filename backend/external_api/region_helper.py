import httpx
import os


API_KEY = os.environ["GEOCODE_API_KEY"]


class RegionHelper:
    @staticmethod
    async def convert_to_coordinates(region: str) -> tuple[float, float] | None:
        url = f"https://geocode.maps.co/search?q={region}&api_key={API_KEY}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code == 200:
                data = await response.json()

                if data:
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])

                    return (lat, lon)

    @staticmethod
    async def get_options(partial_city: str) -> list[str]:
        url = f"https://geocode.maps.co/search?q={partial_city}&api_key={API_KEY}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            result = []

            if response.status_code != 200:
                return result

            data = await response.json()

            for option in data:
                result.append(option["display_name"])

            return result

    @staticmethod
    async def convert_to_region(coordinates: tuple[float, float]) -> str | None:
        lat, lon = coordinates
        url = f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}&api_key={API_KEY}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code == 200:
                data = await response.json()

                return data["display_name"]

            return None
