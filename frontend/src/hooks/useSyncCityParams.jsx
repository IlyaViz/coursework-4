import { useEffect } from "react";
import { useParams } from "react-router";
import { useForecastContext } from "../contexts/ForecastContext";

const useSyncCityParams = () => {
  const { city } = useParams();

  const { setCity } = useForecastContext();

  useEffect(() => {
    setCity(city);
  }, [city]);
};

export default useSyncCityParams;
