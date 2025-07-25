import os
import httpx
import json
import logging
from ..resources.async_client import async_client
from ..resources.async_redis import AsyncRedis
from ..constants.redis_cache import COORDINATES_CACHE_TIME, PARTIAL_CITY_CACHE_TIME
from ..exceptions.external_api_exceptions import APIResponseException


logger = logging.getLogger(__name__)

API_KEY = os.environ["GEOCODE_API_KEY"]


class RegionHelper:
    @staticmethod
    async def convert_to_coordinates(region: str) -> tuple[float, float]:
        cached_coordinates = await AsyncRedis.safe_get(
            f"cache:region_helper:convert_to_coordinates:{region}"
        )

        if cached_coordinates:
            return json.loads(cached_coordinates)

        url = f"https://geocode.maps.co/search?q={region}&api_key={API_KEY}"

        try:
            response = await async_client.get(url)

            if response.status_code != 200:
                logger.error(f"Failed to fetch coordinates for region '{region}'")

                raise APIResponseException(
                    f"Failed to fetch coordinates for region '{region}'"
                )

            data = response.json()

            if not data:
                logger.error(f"No coordinates found for region '{region}'")

                raise APIResponseException(
                    f"No coordinates found for region '{region}'"
                )

            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])

            coordinates = (lat, lon)

            await AsyncRedis.safe_set(
                f"cache:region_helper:convert_to_coordinates:{region}",
                json.dumps(coordinates),
                ex=COORDINATES_CACHE_TIME,
            )

            return (lat, lon)
        except APIResponseException as e:
            raise
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")

            raise APIResponseException(f"Connection error: {e}")
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {e}")

            raise APIResponseException(f"Timeout error: {e}")

    @staticmethod
    async def get_options(partial_city: str) -> list[str]:
        cached_options = await AsyncRedis.safe_get(
            f"cache:region_helper:get_options:{partial_city}"
        )

        if cached_options:
            return json.loads(cached_options)

        url = f"https://geocode.maps.co/search?q={partial_city}&api_key={API_KEY}"

        result = []

        try:
            response = await async_client.get(url)

            if response.status_code != 200:
                logger.error(
                    f"Failed to fetch options for partial city '{partial_city}'"
                )

                raise APIResponseException(
                    f"Failed to fetch options for partial city '{partial_city}'"
                )

            data = response.json()

            for option in data:
                result.append(option["display_name"])

            await AsyncRedis.safe_set(
                f"cache:region_helper:get_options:{partial_city}",
                json.dumps(result),
                ex=PARTIAL_CITY_CACHE_TIME,
            )

            return result
        except APIResponseException as e:
            raise
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")

            raise APIResponseException(f"Connection error: {e}")
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {e}")

            raise APIResponseException(f"Timeout error: {e}")

    @staticmethod
    async def convert_to_region(coordinates: tuple[float, float]) -> str:
        cached_region = await AsyncRedis.safe_get(
            f"cache:region_helper:convert_to_region:{coordinates}"
        )

        if cached_region:
            return json.loads(cached_region)

        lat, lon = coordinates
        url = f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}&api_key={API_KEY}"

        try:
            response = await async_client.get(url)

            if response.status_code != 200:
                logger.error(f"Failed to fetch region for coordinates '{coordinates}'")

                raise APIResponseException(
                    f"Failed to fetch region for coordinates '{coordinates}'"
                )

            data = response.json()

            if "display_name" not in data:
                logger.error(f"No display name found for coordinates '{coordinates}'")

                raise APIResponseException(
                    f"No display name found for coordinates '{coordinates}'"
                )

            await AsyncRedis.safe_set(
                f"cache:region_helper:convert_to_region:{coordinates}",
                json.dumps(data["display_name"]),
                ex=COORDINATES_CACHE_TIME,
            )

            return data["display_name"]
        except APIResponseException as e:
            raise
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}")

            raise APIResponseException(f"Connection error: {e}")
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error: {e}")

            raise APIResponseException(f"Timeout error: {e}")
