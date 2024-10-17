from enum import Enum


class ResultKeyEnum(Enum):
    TEMPERATURE_C = "temperature"
    PRESSURE_MB = "pressure"
    HUMIDITY = "humidity"
    WIND_KM = "wind speed"
    CONDITION = "condition"
