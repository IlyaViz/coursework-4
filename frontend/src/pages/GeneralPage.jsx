import { useForecastContext } from "../contexts/ForecastContext";
import ForecastBlock from "../components/ForecastBlock";

const GeneralPage = () => {
  const { city, forecast, loadingForecast, errorForecast } =
    useForecastContext();

  if (loadingForecast) {
    return <h1 className="text-center">Loading...</h1>;
  }

  if (errorForecast) {
    return <h1 className="text-center">No data available for {city}</h1>;
  }

  if (!forecast) {
    return <h1 className="text-center">Processing...</h1>;
  }

  console.log(forecast, loadingForecast, errorForecast);

  return <ForecastBlock forecast={forecast} onClickBaseLink={city} />;
};

export default GeneralPage;
