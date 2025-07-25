WeatherStatusData = dict[str, str | int]

DayData = dict[str, int | float | WeatherStatusData]
HourData = dict[str, int | str | float | WeatherStatusData]

HourlyData = list[HourData]

DayWholeData = dict[str, int | str | float | DayData | HourlyData]

DailyData = list[DayWholeData]

UsedData = dict[str, DailyData]
