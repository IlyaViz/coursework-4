from fastapi import FastAPI
from fastapi import Query
from fastapi import HTTPException
from typing import List
from dotenv import load_dotenv

load_dotenv()

from .external_api.weather_api import WeatherAPI
from .external_api.open_weather_map_api import OpenWeatherMapAPI
from .logic.weather_aggregator import WeatherAggregator
from .external_api.region_helper import RegionHelper


app = FastAPI()

weather_API_classes = (WeatherAPI, OpenWeatherMapAPI)


@app.get("/forecast")
def get_weather_forecast(region: str, API_classes: List[str] = Query(None)) -> dict:
    if not API_classes:
        raise HTTPException(400, "API classes must be provided")

    selected_API_classes = [
        API_class
        for API_class in weather_API_classes
        if API_class.__name__ in API_classes
    ]

    if not selected_API_classes:
        raise HTTPException(400, "No valid API classes provided")

    return WeatherAggregator.get_aggregated_weather(region, selected_API_classes)


@app.get("/partial_city_helper")
def get_partial_city_helper(partial_city: str) -> dict:
    options = RegionHelper.get_options(partial_city)

    return {"options": options}
