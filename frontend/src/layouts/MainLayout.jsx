import { Outlet } from "react-router";
import { ForecastProvider } from "../contexts/ForecastContext";
import Header from "../components/Header";

const MainLayout = () => {
  return (
    <ForecastProvider>
      <div className="main-layout">
        <Header />

        <main>
          <Outlet />
        </main>
      </div>
    </ForecastProvider>
  );
};

export default MainLayout;
