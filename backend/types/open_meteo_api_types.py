TimeData = list[str]
IndicatorData = list[int | float]

PeriodData = dict[str, TimeData | IndicatorData]

UsedData = dict[str, PeriodData]
