from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke


IndicatorResults = dict[str, int | float | str]

Indicators = dict[drke | hrke, IndicatorResults]

HourlyData = dict[str, Indicators]

DayWholeData = dict[str, Indicators | HourlyData]

AggregatedData = dict[str, DayWholeData]
