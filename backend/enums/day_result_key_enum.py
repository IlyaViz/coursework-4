from enum import Enum


class DayResultKeyEnum(str, Enum):
    MIN_TEMPERATURE = "min temperature"
    MAX_TEMPERATURE = "max temperature"
    MAX_WIND = "max wind speed"
    AVERAGE_HUMIDITY = "average humidity"
    CONDITION_ICON = "condition icon"
