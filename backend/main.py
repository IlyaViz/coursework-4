import logging
from fastapi import FastAPI
from fastapi import Query
from fastapi import HTTPException
from typing import List
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from .external_api.weather_api import WeatherAPI
from .external_api.open_weather_map_api import OpenWeatherMapAPI
from .external_api.open_meteo_api import OpenMeteoAPI
from .logic.weather_aggregator import WeatherAggregator
from .external_api.region_helper import RegionHelper
from .exceptions.external_api_exceptions import APIResponseException
from .types.weather_aggregator_types import AggregatedData


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log", mode="w")],
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

weather_API_classes = (WeatherAPI, OpenWeatherMapAPI, OpenMeteoAPI)


@app.get("/forecast")
async def get_weather_forecast(
    region: str, API_classes: List[str] = Query(None)
) -> AggregatedData:
    if not API_classes:
        logger.error(f"No API classes provided for region '{region}'")

        raise HTTPException(400, "API classes must be provided")

    selected_API_classes = [
        API_class
        for API_class in weather_API_classes
        if API_class.__name__ in API_classes
    ]

    if not selected_API_classes:
        logger.error(
            f"No valid API classes provided for region '{region}' with classes {API_classes}"
        )

        raise HTTPException(400, "No valid API classes provided")

    try:
        result = await WeatherAggregator.get_aggregated_weather(
            region, selected_API_classes
        )
    except APIResponseException as e:
        raise HTTPException(500, f"Weather aggregation failed: {e}")

    logger.info(f"Weather forecast for region '{region}' retrieved successfully")

    return result


@app.get("/partial_city_helper")
async def get_partial_city_helper(partial_city: str) -> dict[str, list[str]]:
    try:
        options = await RegionHelper.get_options(partial_city)
    except APIResponseException as e:
        raise HTTPException(500, f"Failed to fetch options for '{partial_city}': {e}")

    logger.info(f"Options for partial city '{partial_city}' retrieved successfully")

    return {"options": options}


@app.get("/convert_coordinates")
async def convert_coordinates(lat: float, lon: float) -> dict[str, str]:
    try:
        region = await RegionHelper.convert_to_region((lat, lon))
    except APIResponseException as e:
        raise HTTPException(500, f"Failed to convert coordinates: {e}")

    logger.info(
        f"Coordinates ({lat}, {lon}) converted to region '{region}' successfully"
    )

    return {"region": region}


@app.get("/API_classes")
def get_API_classes() -> dict[str, list[str]]:
    API_classes = [cls.__name__ for cls in weather_API_classes]

    return {"API_classes": API_classes}
