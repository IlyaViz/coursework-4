import { useForecastContext } from "../contexts/ForecastContext";
import { useParams } from "react-router";
import ForecastBlock from "../components/ForecastBlock";
import useSyncCityParams from "../hooks/useSyncCityParams";

const DailyPage = () => {
  useSyncCityParams();

  const { forecastData } = useForecastContext();
  const { date } = useParams();

  if (!forecastData) {
    return <div>No data available for the selected date</div>;
  }

  const hourlyData = forecastData[date].hours;

  return <ForecastBlock forecastData={hourlyData} />;
};

export default DailyPage;
