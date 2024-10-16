from enum import Enum


class CurrentAndHourResultKeyEnum(Enum):
    TEMPERATURE_C = "temperature"
    PRESSURE_MB = "pressure"
    HUMIDITY = "humidity"
    WIND_KM = "wind speed"
    CONDITION = "condition"
