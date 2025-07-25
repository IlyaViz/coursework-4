WeatherStatusData = dict[str, int | str]
DifferentTimeIndicatorData = dict[str, int | float]

WeatherStatusesData = dict[str, WeatherStatusData]

TimeData = dict[str, int | float | DifferentTimeIndicatorData | WeatherStatusesData]

TimesData = list[TimeData]

UsedData = dict[str, int | TimesData]
