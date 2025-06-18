import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import useFetch from "../hooks/useFetch";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const HomePage = () => {
  const [URL, setURL] = useState("");

  const navigate = useNavigate();

  let shouldFetchLocation = URL !== "";

  const {
    data: locationData,
    loading: loadingLocation,
    error: errorLocation,
  } = useFetch(URL, shouldFetchLocation);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const { latitude, longitude } = position.coords;

        setURL(
          `${BACKEND_URL}/convert_coordinates?lat=${latitude}&lon=${longitude}`
        );
      });
    }
  }, []);

  useEffect(() => {
    if (locationData) {
      const { region } = locationData;

      navigate(`/${region}`);
    }
  }, [locationData, navigate]);

  if (loadingLocation) {
    return <h1 className="text-center">Loading you location...</h1>;
  }

  if (errorLocation) {
    return <h1 className="text-center">Error while getting your city</h1>;
  }

  return (
    <h1 className="text-center">Allow your location for automatic fetch</h1>
  );
};

export default HomePage;
