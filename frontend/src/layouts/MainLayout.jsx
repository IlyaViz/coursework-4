import { Outlet, useParams } from "react-router";
import { useForecastContext } from "../contexts/ForecastContext";
import Header from "../components/Header";

const MainLayout = () => {
  const { city } = useParams();

  const { setCity } = useForecastContext();

  if (city) {
    setCity(city);
  }

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
