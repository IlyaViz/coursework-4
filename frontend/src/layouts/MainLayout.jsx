import { Outlet, useNavigate, useParams } from "react-router";
import { useEffect } from "react";
import { useForecastContext } from "../contexts/ForecastContext";
import Header from "../components/Header";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const MainLayout = () => {
  const { city: cityParam } = useParams();

  const { city, setCity } = useForecastContext();

  const navigate = useNavigate();

  useEffect(() => {
    if (cityParam && cityParam !== city) {
      setCity(cityParam);
    }
  }, [cityParam, city, setCity]);

  useEffect(() => {
    if (navigator.geolocation && !city && !cityParam) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const response = await fetch(
          `${BACKEND_URL}/convert_coordinates?lat=${position.coords.latitude}&lon=${position.coords.longitude}`
        );

        if (!response.ok) {
          return;
        }

        const data = await response.json();

        navigate(`/${data.region}`);
      });
    }
  }, [city, cityParam, navigate]);

  return (
    <div className="main-layout">
      <Header />

      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default MainLayout;
