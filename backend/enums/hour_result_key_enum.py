from enum import Enum


class HourResultKeyEnum(str, Enum):
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"
    HUMIDITY = "humidity"
    WIND = "wind speed"
    CONDITION = "condition"
