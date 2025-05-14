from fastapi import FastAPI
from fastapi import Query
from fastapi import HTTPException
from dotenv import load_dotenv
from .logic.cached_weather_aggregator import CachedWeatherAggregator
from .external_api.weather_api import WeatherAPI
from .external_api.open_weather_map_api import OpenWeatherMapAPI
from .logic.weather_aggregator import WeatherAggregator


load_dotenv()

app = FastAPI()

weather_API_classes = (WeatherAPI, OpenWeatherMapAPI)


def get_weather_aggregator(
    selected_weather_API_class_names: list[str], region: str
) -> WeatherAggregator:
    if not selected_weather_API_class_names:
        raise HTTPException(status_code=404, detail="Enter at least one API")

    selected_weather_API_classes = tuple(
        [
            weather_API_class
            for weather_API_class in weather_API_classes
            if weather_API_class.__name__ in selected_weather_API_class_names
        ]
    )

    return CachedWeatherAggregator.get_weather_aggregator(
        selected_weather_API_classes, region
    )


@app.get("/weather_API_class_names/")
def get_weather_API_class_names():
    return [weather_API_class.__name__ for weather_API_class in weather_API_classes]


@app.get("/current/")
def get_current(region: str, API_class_names: list[str] = Query(None)):
    weather_aggregator = get_weather_aggregator(API_class_names, region)

    return weather_aggregator.get_aggregated_current()


@app.get("/forecast/hour")
def get_hour_forecast(
    region: str, day: int, hour: int, API_class_names: list[str] = Query(None)
):
    weather_aggregator = get_weather_aggregator(API_class_names, region)

    return weather_aggregator.get_aggregated_hour_forecast(day, hour)


@app.get("/forecast/day")
def get_day_forecast(region: str, day: int, API_class_names: list[str] = Query(None)):
    weather_aggregator = get_weather_aggregator(API_class_names, region)

    return weather_aggregator.get_aggregated_day_forecast(day)
