import { LineChart, XAxis, Line, ResponsiveContainer, YAxis } from "recharts";
import { useEffect, useState } from "react";
import { useForecastContext } from "../contexts/ForecastContext";
import SelectButton from "../components/SelectButton";
import generateServiceColor from "../utils/serviceColorGenerator";

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

  const { forecastData } = useForecastContext();

  useEffect(() => {
    if (forecastData) {
      const [minDate, maxDate] = getMinMaxDates(forecastData);
      const indicators = getIndicators(forecastData);

      setDailyPeriod([minDate, maxDate]);
      setIndicator(indicators[0]);
    }
  }, [forecastData]);

  if (!forecastData || dailyPeriod[0] === null || indicator === null) {
    return <div>No data available for dynamics.</div>;
  }

  const data = [];

  Object.entries(forecastData).forEach(([date, dateData]) => {
    if (date >= dailyPeriod[0] && date <= dailyPeriod[1]) {
      Object.entries(dateData.hours).forEach(([hour, hourData]) => {
        data.push({
          time: `${date} ${hour}`,
          ...hourData[indicator],
        });
      });
    }
  });

  const [minDate, maxDate] = getMinMaxDates(forecastData);
  const indicators = getIndicators(forecastData);

  return (
    <div className="flex flex-col">
      <div className="flex justify-center">
        <ResponsiveContainer width="75%" height={400}>
          <LineChart data={data}>
            <XAxis dataKey="time" />
            <YAxis label={{ value: indicator, angle: -90, dx: -20 }} />
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

        <div className="flex flex-col justify-center gap-2 -translate-y-5">
          {indicators.map((ind) => (
            <SelectButton
              key={ind}
              onClick={() => setIndicator(ind)}
              selected={indicator === ind}
            >
              {ind}
            </SelectButton>
          ))}
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
