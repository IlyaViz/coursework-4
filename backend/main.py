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
) -> dict:
    if not API_classes:
        raise HTTPException(400, "API classes must be provided")

    selected_API_classes = [
        API_class
        for API_class in weather_API_classes
        if API_class.__name__ in API_classes
    ]

    if not selected_API_classes:
        raise HTTPException(400, "No valid API classes provided")

    return await WeatherAggregator.get_aggregated_weather(region, selected_API_classes)


@app.get("/partial_city_helper")
async def get_partial_city_helper(partial_city: str) -> dict:
    options = await RegionHelper.get_options(partial_city)

    return {"options": options}


@app.get("/convert_coordinates")
async def convert_coordinates(lat: float, lon: float) -> dict:
    region = await RegionHelper.convert_to_region((lat, lon))

    if region is None:
        raise HTTPException(404, "Coordinates do not correspond to a valid region")

    return {"region": region}


@app.get("/API_classes")
def get_API_classes() -> dict:
    API_classes = [cls.__name__ for cls in weather_API_classes]

    return {"API_classes": API_classes}