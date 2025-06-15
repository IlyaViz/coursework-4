import { useForecastContext } from "../contexts/ForecastContext";
import { Link } from "react-router";

const GeneralPage = () => {
  const { city, forecastData } = useForecastContext();

  if (!forecastData) {
    return <div>No data for current city</div>;
  }

  return (
    <div className="flex justify-around">
      {Object.entries(forecastData).map(([date, data]) => (
        <Link to={`/${city}/${date}`}>
          <div key={date}>
            <h1>{date}</h1>

            {Object.entries(data.indicators.temperature).map(
              ([service, temp]) =>
                service !== "average" && (
                  <div key={service}>
                    <p>Temperature: {temp}°C</p>
                  </div>
                )
            )}

            <p>Average temperature: {data.indicators.temperature.average}°C</p>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default GeneralPage;
