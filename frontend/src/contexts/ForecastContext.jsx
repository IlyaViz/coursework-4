import { createContext, useContext, useEffect, useState } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const ForecastContext = createContext();

const ForecastProvider = ({ children }) => {
  const [city, setCity] = useState("");
  const [availableAPIs, setAvailableAPIs] = useState([]); 
  const [usedAPIs, setUsedAPIs] = useState([]);
  const [forecastData, setForecastData] = useState(null);

  useEffect(() => {
    async function fetchForecast() {
      if (!city || usedAPIs.length === 0) {
        return;
      }

      const params = new URLSearchParams();

      params.append("region", city);
      usedAPIs.forEach((API) => {
        params.append("API_classes", API);
      });

      const response = await fetch(
        `${BACKEND_URL}/forecast?${params.toString()}`
      );

      if (!response.ok) {
        return;
      }

      const data = await response.json();

      console.log(data);

      setForecastData(data);
    }

    fetchForecast();
  }, [city, usedAPIs]);

  useEffect(() => {
    const fetchAPIs = async () => {
      const response = await fetch(`${BACKEND_URL}/api_classes`);

      console.log(`${BACKEND_URL}/api_classes`);
      if (!response.ok) {
        return;
      }

      const data = await response.json();
      const APIClasses = data.api_classes;

      setAvailableAPIs(APIClasses);
      setUsedAPIs(APIClasses);
    };

    fetchAPIs();
  }, []);

  return (
    <ForecastContext.Provider
      value={{
        city,
        forecastData,
        usedAPIs,
        availableAPIs,
        setCity,
        setUsedAPIs,
      }}
    >
      {children}
    </ForecastContext.Provider>
  );
};

const useForecastContext = () => useContext(ForecastContext);

export { ForecastProvider, useForecastContext };
