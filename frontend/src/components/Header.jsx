import { useLocation, useNavigate } from "react-router";
import { useForecastContext } from "../contexts/ForecastContext";
import SelectButton from "./SelectButton";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const Header = () => {
  const { city, setUsedAPIs, availableAPIs, usedAPIs } = useForecastContext();

  const navigate = useNavigate();

  const location = useLocation();

  const backable = location.pathname !== `/${city}`;
  const isDynamicsPage = location.pathname.includes("/dynamics");

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      if (!e.target.value.trim()) return;

      navigate(`/${e.target.value}`);
    }
  };

  const OnAPIButtonClicked = (e) => {
    if (e.target.checked) {
      setUsedAPIs((prev) => [...prev, e.target.id]);
    } else {
      setUsedAPIs((prev) => prev.filter((API) => API !== e.target.id));
    }
  };

  return (
    <header className="flex justify-around mt-5 mb-14">
      <div>
        {backable && <button onClick={() => navigate(-1)}>Go back</button>}
      </div>

      <div className="flex flex-col items-center">
        <div>
          <input
            className="p-0.5 border border-black rounded-lg"
            type="text"
            onKeyUp={handleKeyDown}
            placeholder="City name"
          />

          <div className="hidden">Options</div>
        </div>

        <div className="flex flex-col gap-2 mt-3">
          {availableAPIs.length > 0 ? (
            availableAPIs.map((API) => (
              <div key={API}>
                <input
                  type="checkbox"
                  id={API}
                  className="scale-150"
                  checked={usedAPIs.includes(API)}
                  onChange={OnAPIButtonClicked}
                />
                <label htmlFor={API} className="m-2">
                  {API}
                </label>
              </div>
            ))
          ) : (
            <div>No APIs available</div>
          )}
        </div>

        {city.trim() && (
          <div>
            <h1 className="mt-5 text-2xl">
              Weather for <span className="font-bold">{city}</span>
            </h1>

            <div className="flex gap-1 mt-2">
              <SelectButton
                onClick={() => navigate(`/${city}`)}
                selected={!isDynamicsPage}
              >
                Forecast
              </SelectButton>

              <SelectButton
                onClick={() => navigate(`/${city}/dynamics`)}
                selected={isDynamicsPage}
              >
                Dynamics
              </SelectButton>
            </div>
          </div>
        )}
      </div>

      <div>Services</div>
    </header>
  );
};

export default Header;
