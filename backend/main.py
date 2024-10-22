from fastapi import FastAPI
from fastapi import Query
from fastapi import HTTPException
from dotenv import load_dotenv
from .logic.cached_weather_aggregator import CachedWeatherAggregator
from .external_api.weather_api import WeatherAPI
from .external_api.open_weather_map_api import OpenWeatherMapAPI


app = FastAPI()

load_dotenv()

weather_API_classes = (WeatherAPI, OpenWeatherMapAPI)

def get_selected_weather_API_classes(selected_weather_API_class_names: list[str]) -> tuple:
    if not selected_weather_API_class_names:
        raise HTTPException(status_code=404, detail="Enter at least one API")

    return tuple([weather_API_class for weather_API_class in weather_API_classes if weather_API_class.__name__ in selected_weather_API_class_names])

@app.get("/weather_API_class_names/")
def get_weather_API_class_names():
    return [weather_API_class.__name__ for weather_API_class in weather_API_classes]

@app.get("/current/")
def get_current(region: str, API: list[str] = Query(None)):
    selected_weather_API_classes = get_selected_weather_API_classes(API)

    weather_aggregator = CachedWeatherAggregator.get_weather_aggregator(selected_weather_API_classes, region)

    return weather_aggregator.get_aggregated_current()

@app.get("/forecast/hour")
def get_hour_forecast(region: str, day: int, hour: int, API: list[str] = Query(None)):
    selected_weather_API_classes = get_selected_weather_API_classes(API)

    weather_aggregator = CachedWeatherAggregator.get_weather_aggregator(selected_weather_API_classes, region)

    return weather_aggregator.get_aggregated_hour_forecast(day, hour)

@app.get("/forecast/day")
def get_day_forecast(region: str, day: int, API: list[str] = Query(None)):
    selected_weather_API_classes = get_selected_weather_API_classes(API)

    weather_aggregator = CachedWeatherAggregator.get_weather_aggregator(selected_weather_API_classes, region)

    return weather_aggregator.get_aggregated_day_forecast(day)


