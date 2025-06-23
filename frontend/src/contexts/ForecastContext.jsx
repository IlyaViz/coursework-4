import { createContext, useContext, useEffect, useState } from "react";
import useFetch from "../hooks/useFetch";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const ForecastContext = createContext();

const ForecastProvider = ({ children }) => {
  const [city, setCity] = useState("");
  const [availableAPIs, setAvailableAPIs] = useState([]);
  const [usedAPIs, setUsedAPIs] = useState([]);
  const [forecast, setForecast] = useState(null);

  const {
    data: APIClassesData,
    loading: loadingAPIClasses,
    error: errorAPIClasses,
  } = useFetch(`${BACKEND_URL}/API_classes`);

  const forecastParams = new URLSearchParams();

  forecastParams.append("region", city);
  usedAPIs.forEach((API) => {
    forecastParams.append("API_classes", API);
  });

  const forecastURL = `${BACKEND_URL}/forecast?${forecastParams.toString()}`;

  const shouldFetchForecast = city && usedAPIs.length > 0;

  const {
    data: forecastData,
    loading: loadingForecast,
    error: errorForecast,
  } = useFetch(forecastURL, shouldFetchForecast);

  useEffect(() => {
    if (forecastData) {
      setForecast(forecastData);
    }
  }, [forecastData]);

  useEffect(() => {
    if (APIClassesData) {
      const APIClasses = APIClassesData.API_classes;

      setAvailableAPIs(APIClasses);
      setUsedAPIs(APIClasses);
    }
  }, [APIClassesData]);

  return (
    <ForecastContext.Provider
      value={{
        city,
        forecast,
        usedAPIs,
        availableAPIs,
        setCity,
        setUsedAPIs,
        loadingAPIClasses,
        errorAPIClasses,
        loadingForecast,
        errorForecast,
      }}
    >
      {children}
    </ForecastContext.Provider>
  );
};

const useForecastContext = () => useContext(ForecastContext);

export { ForecastProvider, useForecastContext };
