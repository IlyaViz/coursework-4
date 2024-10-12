from fastapi import FastAPI
from dotenv import load_dotenv
from .logic.weather_aggregator import WeatherAggregator
from .external_api.weather_api import WeatherAPI
from .external_api.open_weather_map_api import OpenWeatherMapAPI


load_dotenv()

weather_API_classes = [WeatherAPI, OpenWeatherMapAPI]

app = FastAPI()

@app.get("/current/")
def get_current(region: str):
    weather_aggregator = WeatherAggregator(weather_API_classes, region)

    return weather_aggregator.get_aggregated_current()

@app.get("/forecast/")
def get_forecast(region: str, day_index: int, hour: int):
    weather_aggregator = WeatherAggregator(weather_API_classes, region)

    return weather_aggregator.get_aggregated_forecast(day_index, hour)




