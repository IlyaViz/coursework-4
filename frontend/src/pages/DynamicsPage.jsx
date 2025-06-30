import { LineChart, XAxis, Line, ResponsiveContainer, YAxis } from "recharts";
import { useEffect, useState } from "react";
import { useForecastContext } from "../contexts/ForecastContext";
import SelectButton from "../components/SelectButton";
import generateServiceColor from "../utils/serviceColorGenerator";
import INDICATOR_TO_ICON_CONSTANTS from "../constants/indicatorToIconConstants";
import UNITS from "../constants/units";

const getMinMaxDates = (data) => {
  const dates = Object.keys(data);

  return [dates[0], dates[dates.length - 1]];
};

const getIndicators = (data) => {
  const [firstDate] = getMinMaxDates(data);
  const firstHour = Object.keys(data[firstDate].hours)[0];

  return Object.keys(data[firstDate].hours[firstHour]);
};

const DynamicsPage = () => {
  const [dailyPeriod, setDailyPeriod] = useState([null, null]);
  const [indicator, setIndicator] = useState(null);

  const { city, forecast, loadingForecast, errorForecast } =
    useForecastContext();

  useEffect(() => {
    if (forecast) {
      const [minDate, maxDate] = getMinMaxDates(forecast);
      const indicators = getIndicators(forecast);

      setDailyPeriod([minDate, maxDate]);
      setIndicator(indicators[0]);
    }
  }, [forecast]);

  if (loadingForecast) {
    return <h1 className="text-center">Loading...</h1>;
  }

  if (errorForecast) {
    return <h1 className="text-center">No data available for {city}</h1>;
  }

  if (!forecast || !dailyPeriod[0] || !dailyPeriod[1] || !indicator) {
    return <h1 className="text-center">Processing...</h1>;
  }
  const data = [];

  Object.entries(forecast).forEach(([date, dateData]) => {
    if (date >= dailyPeriod[0] && date <= dailyPeriod[1]) {
      Object.entries(dateData.hours).forEach(([hour, hourData]) => {
        data.push({
          time: `${date} ${hour}`,
          ...hourData[indicator],
        });
      });
    }
  });

  const [minDate, maxDate] = getMinMaxDates(forecast);
  const indicators = getIndicators(forecast);

  return (
    <div className="flex flex-col">
      <div className="flex justify-center">
        <ResponsiveContainer width="75%" height={400}>
          <LineChart data={data}>
            <XAxis dataKey="time" />
            <YAxis
              label={{ value: `${UNITS[indicator]}`, angle: -90, dx: -25 }}
              domain={["dataMin - 2", "dataMax + 2"]}
              tickFormatter={(value) => Math.round(value)}
            />

            {Object.keys(data[0])
              .filter((key) => key !== "time" && key !== "average")
              .map((key) => (
                <Line
                  key={key}
                  type="monotone"
                  dataKey={key}
                  stroke={`${generateServiceColor(key)}`}
                />
              ))}

            <Line type="monotone" dataKey="average" stroke="#4ade80" />
          </LineChart>
        </ResponsiveContainer>

        <div className="flex flex-col justify-center gap-2 ml-4 -translate-y-5">
          {indicators.map(
            (ind) =>
              ind !== "condition icon" && (
                <SelectButton
                  key={ind}
                  onClick={() => setIndicator(ind)}
                  selected={indicator === ind}
                >
                  {INDICATOR_TO_ICON_CONSTANTS[ind]}
                </SelectButton>
              )
          )}
        </div>
      </div>

      <div className="flex justify-center">
        <label htmlFor="start-date">Start date:</label>
        <input
          type="date"
          id="start-date"
          value={dailyPeriod[0]}
          min={minDate}
          max={dailyPeriod[1]}
          onChange={(e) => setDailyPeriod([e.target.value, dailyPeriod[1]])}
        />

        <label htmlFor="end-date">End date:</label>
        <input
          type="date"
          id="end-date"
          value={dailyPeriod[1]}
          min={dailyPeriod[0]}
          max={maxDate}
          onChange={(e) => setDailyPeriod([dailyPeriod[0], e.target.value])}
        />
      </div>
    </div>
  );
};

export default DynamicsPage;
