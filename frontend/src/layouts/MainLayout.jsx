import { Outlet, useParams } from "react-router";
import { useEffect } from "react";
import { useForecastContext } from "../contexts/ForecastContext";
import Header from "../components/Header";

const MainLayout = () => {
  const { city: cityParam } = useParams();

  const { city, setCity } = useForecastContext();

  useEffect(() => {
    if (cityParam && cityParam !== city) {
      setCity(cityParam);
    }
  }, [cityParam, city, setCity]);

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
