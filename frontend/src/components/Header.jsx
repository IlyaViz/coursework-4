import { useLocation, useNavigate } from "react-router";
import { useState } from "react";
import { useForecastContext } from "../contexts/ForecastContext";
import SelectButton from "./SelectButton";
import generateServiceColor from "../utils/serviceColorGenerator";
import useFetch from "../hooks/useFetch";

const Header = () => {
  const [partialCity, setPartialCity] = useState("");

  const shouldFetchPartialCity = partialCity.trim();

  const {
    data: optionsData,
    loading: loadingCityOptions,
    error: errorCityOptions,
  } = useFetch(
    `partial_city_helper?partial_city=${partialCity}`,
    shouldFetchPartialCity
  );

  const { city, setUsedAPIs, availableAPIs, usedAPIs, forecast } =
    useForecastContext();

  const navigate = useNavigate();

  const location = useLocation();

  const backable = location.pathname !== `/${city}`;
  const isDynamicsPage = location.pathname.includes("/dynamics");
  let resultAPIs = [];

  if (forecast) {
    const firstDay = Object.keys(forecast)[0];
    const indicators = forecast[firstDay].indicators;

    Object.values(indicators).forEach((APIGroup) => {
      Object.keys(APIGroup).forEach((API) => {
        if (!resultAPIs.includes(API)) {
          resultAPIs.push(API);
        }
      });
    });
  }

  const onOptionClick = (option) => {
    setPartialCity("");

    navigate(`/${option}`);
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
        <input
          className="p-0.5 border border-black rounded-lg"
          type="text"
          placeholder="City name"
          onChange={(e) => setPartialCity(e.target.value)}
          value={partialCity}
        />

        <div className="flex flex-col gap-1 mt-1 text-center">
          {loadingCityOptions && <div>Loading...</div>}

          {errorCityOptions && <div>Error: {errorCityOptions}</div>}

          {partialCity.trim() &&
            optionsData?.options.map((option) => (
              <SelectButton key={option} onClick={() => onOptionClick(option)}>
                {option}
              </SelectButton>
            ))}
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

            <div className="flex justify-center gap-1 mt-2">
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

      <div>
        {resultAPIs.map(
          (API) =>
            API !== "average" && (
              <h1
                key={API}
                style={{ backgroundColor: generateServiceColor(API) }}
                className="p-1 text-center"
              >
                {API}
              </h1>
            )
        )}
      </div>
    </header>
  );
};

export default Header;
