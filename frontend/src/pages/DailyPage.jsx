import { useForecastContext } from "../contexts/ForecastContext";
import { useParams } from "react-router";

const DailyPage = () => {
  const { forecastData } = useForecastContext();
  const { date } = useParams();

  if (!forecastData) {
    return <div>No data available for the selected date.</div>;
  }

  const hourlyData = forecastData[date].hours;

  console.log(hourlyData);

  return (
    <div className="flex">
      {Object.entries(hourlyData).map(([hour, indicators]) => (
        <div key={hour}>
          <h1>{hour}</h1>

          {Object.entries(indicators).map(([indicator, services]) => (
            <div key={indicator}>
              <h1>{indicator}</h1>

              {Object.entries(services).map(
                ([service, value]) =>
                  service !== "average" && (
                    <div key={service}>
                      <p>{value}</p>
                    </div>
                  )
              )}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default DailyPage;
