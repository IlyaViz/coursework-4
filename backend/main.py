from fastapi import FastAPI
from dotenv import load_dotenv
from .logic.cached_weather_aggregator import CachedWeatherAggregator
from .external_api.weather_api import WeatherAPI
from .external_api.open_weather_map_api import OpenWeatherMapAPI


load_dotenv()

weather_API_classes = (WeatherAPI, OpenWeatherMapAPI)

app = FastAPI()

@app.get("/current/")
def get_current(region: str):
    weather_aggregator = CachedWeatherAggregator.get_weather_aggregator(weather_API_classes, region)

    return weather_aggregator.get_aggregated_current()

@app.get("/forecast/hour")
def get_hour_forecast(region: str, day: int, hour: int):
    weather_aggregator = CachedWeatherAggregator.get_weather_aggregator(weather_API_classes, region)

    return weather_aggregator.get_aggregated_hour_forecast(day, hour)

@app.get("/forecast/day")
def get_day_forecast(region: str, day: int):
    weather_aggregator = CachedWeatherAggregator.get_weather_aggregator(weather_API_classes, region)

    return weather_aggregator.get_aggregated_day_forecast(day)


