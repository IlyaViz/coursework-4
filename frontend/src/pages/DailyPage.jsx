import { useForecastContext } from "../contexts/ForecastContext";
import { useParams } from "react-router";
import ForecastBlock from "../components/ForecastBlock";

const DailyPage = () => {
  const { forecast, loadingForecast, errorForecast, city } =
    useForecastContext();

  const { date } = useParams();

  if (loadingForecast) {
    return <h1 className="text-center">Loading...</h1>;
  }

  if (errorForecast) {
    return <h1 className="text-center">No data available for {city}</h1>;
  }

  if (!forecast) {
    return <h1 className="text-center">Processing...</h1>;
  }

  const hourlyData = forecast[date].hours;

  return <ForecastBlock forecast={hourlyData} />;
};

export default DailyPage;
