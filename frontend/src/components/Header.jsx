import { useLocation, useNavigate } from "react-router";
import { useForecastContext } from "../contexts/ForecastContext";

const Header = () => {
  const { city } = useForecastContext();

  const navigate = useNavigate();

  const location = useLocation();

  const backable = location.pathname !== `/${city}`;

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      navigate(`/${e.target.value}`);
    }
  };

  return (
    <header className="flex justify-around">
      <div>
        {backable && <button onClick={() => navigate(-1)}>Go back</button>}
      </div>

      <div className="flex flex-col items-center">
        <div>
          <input
            className="border border-black"
            type="text"
            onKeyUp={handleKeyDown}
          />

          <div className="hidden">Options</div>
        </div>

        <div>Checkboxes</div>

        <h1>Weather for {city}</h1>

        <div>
          <button onClick={() => navigate(`/${city}`)}>Forecast</button>
          <button onClick={() => navigate(`/${city}/dynamics`)}>
            Dynamics
          </button>
        </div>
      </div>

      <div>Services</div>
    </header>
  );
};

export default Header;
