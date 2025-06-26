from enum import Enum


class DayResultKeyEnum(str, Enum):
    MIN_TEMPERATURE = "min temperature"
    MAX_TEMPERATURE = "max temperature"
    HUMIDITY = "humidity"
    WIND = "wind speed"
    CONDITION_ICON = "condition icon"
