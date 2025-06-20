from fastapi import HTTPException
from ..enums.hour_result_key_enum import HourResultKeyEnum as hrke
from ..enums.day_result_key_enum import DayResultKeyEnum as drke
from ..enums.result_type_key_enum import ResultTypeKeyEnum as rtke
from ..external_api.weather_api_base import WeatherAPIBase
from ..external_api.region_helper import RegionHelper


class WeatherAggregator:
    @classmethod
    async def get_aggregated_weather(
        cls, region: str, API_classes: list[WeatherAPIBase]
    ) -> dict | None:
        coordinates = await RegionHelper.convert_to_coordinates(region)

        if coordinates is None:
            raise HTTPException(404, "Region doesn't exist")

        results = {
            API_class.__name__: await API_class.get_weather(coordinates)
            for API_class in API_classes
        }

        aggregated_result = cls._aggregate_weather(results)

        return aggregated_result

    @classmethod
    def _aggregate_weather(cls, data: dict) -> dict:
        result = {}

        template_API_result = data[list(data.keys())[0]]

        for day in template_API_result[rtke.DAILY]:
            if not cls._check_dicts_have_time_key(
                [d[rtke.DAILY] for d in data.values()], day
            ):
                continue

            result[day] = {}
            result[day]["indicators"] = {}

            for key in drke:
                result[day]["indicators"][key] = {}

                for API_class in data:
                    value = data[API_class][rtke.DAILY][day][key]

                    result[day]["indicators"][key][API_class] = value

                if (
                    not isinstance(value, str)
                    and len(result[day]["indicators"][key]) > 1
                ):
                    result[day]["indicators"][key]["average"] = round(
                        sum(result[day]["indicators"][key].values())
                        / len(result[day]["indicators"][key]),
                        2,
                    )

            result[day]["hours"] = {}

            for time in template_API_result[rtke.HOURLY]:
                date, hour = time.split(" ")

                if date != day:
                    continue

                if not cls._check_dicts_have_time_key(
                    [d[rtke.HOURLY] for d in data.values()], time
                ):
                    continue

                result[day]["hours"][hour] = {}

                for key in hrke:
                    result[day]["hours"][hour][key] = {}

                    for API_class in data:
                        value = data[API_class][rtke.HOURLY][time][key]

                        result[day]["hours"][hour][key][API_class] = value

                    if (
                        not isinstance(value, str)
                        and len(result[day]["hours"][hour][key]) > 1
                    ):
                        result[day]["hours"][hour][key]["average"] = round(
                            sum(result[day]["hours"][hour][key].values())
                            / len(result[day]["hours"][hour][key]),
                            2,
                        )

        return result

    @staticmethod
    def _check_dicts_have_time_key(dicts: list[dict], key: str) -> bool:
        for d in dicts:
            if key not in d:
                return False

        return True
