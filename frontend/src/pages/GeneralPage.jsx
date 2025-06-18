import { useForecastContext } from "../contexts/ForecastContext";
import ForecastBlock from "../components/ForecastBlock";

const GeneralPage = () => {
  const { city, forecastData } = useForecastContext();

  if (!forecastData) {
    return <div>No data for current city</div>;
  }

  return <ForecastBlock forecastData={forecastData} onClickBaseLink={city} />;
};

export default GeneralPage;
