from ..enums.result_type_key_enum import ResultTypeKeyEnum as rtke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke


DayData = dict[drke, str | float | int]
HourData = dict[hrke, str | float | int]

DailyData = dict[str, DayData]
HourlyData = dict[str, HourData]

ForecastData = dict[rtke, DailyData | HourlyData]
