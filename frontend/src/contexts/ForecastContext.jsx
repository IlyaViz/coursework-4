import { createContext, useContext, useEffect, useState } from "react";

const ForecastContext = createContext();

const ForecastProvider = ({ children }) => {
  const [city, setCity] = useState("");
  const [coords, setCoords] = useState({ lat: null, lon: null });
  const [forecastData, setForecastData] = useState(null);

  useEffect(() => {
    async function fetchForecast() {
      // TODO
      const testData = {
        kiev: {
          "2023-10-01": {
            indicators: {
              temperature: {
                average: 20,
                service1: 19,
                service2: 21,
              },
              humidity: {
                average: 60,
                service1: 58,
                service2: 62,
              },
            },
            hours: {
              "09:00": {
                temperature: {
                  average: 18,
                  service1: 17,
                  service2: 19,
                },
                humidity: {
                  average: 10,
                  service1: 64,
                  service2: 66,
                },
              },
              "15:00": {
                temperature: {
                  average: 22,
                  service1: 21,
                  service2: 23,
                },
                humidity: {
                  average: 55,
                  service1: 54,
                  service2: 56,
                },
              },
              "21:00": {
                temperature: {
                  average: 16,
                  service1: 15,
                  service2: 17,
                },
                humidity: {
                  average: 70,
                  service1: 69,
                  service2: 71,
                },
              },
            },
          },
          "2023-10-02": {
            indicators: {
              temperature: {
                average: 21,
                service1: 20,
                service2: 22,
              },
              humidity: {
                average: 58,
                service1: 57,
                service2: 59,
              },
            },
            hours: {
              "09:00": {
                temperature: {
                  average: 19,
                  service1: 18,
                  service2: 20,
                },
                humidity: {
                  average: 63,
                  service1: 62,
                  service2: 64,
                },
              },
              "15:00": {
                temperature: {
                  average: 23,
                  service1: 22,
                  service2: 24,
                },
                humidity: {
                  average: 53,
                  service1: 52,
                  service2: 54,
                },
              },
              "21:00": {
                temperature: {
                  average: 17,
                  service1: 16,
                  service2: 18,
                },
                humidity: {
                  average: 90,
                  service1: 67,
                  service2: 69,
                },
              },
            },
          },
        },
        lviv: {
          "2023-10-01": {
            indicators: {
              temperature: {
                average: 17,
                service1: 16,
                service2: 18,
              },
              humidity: {
                average: 67,
                service1: 66,
                service2: 68,
              },
            },
            hours: {
              "09:00": {
                temperature: {
                  average: 15,
                  service1: 14,
                  service2: 16,
                },
                humidity: {
                  average: 70,
                  service1: 69,
                  service2: 71,
                },
              },
              "15:00": {
                temperature: {
                  average: 19,
                  service1: 18,
                  service2: 20,
                },
                humidity: {
                  average: 65,
                  service1: 64,
                  service2: 66,
                },
              },
              "21:00": {
                temperature: {
                  average: 14,
                  service1: 13,
                  service2: 15,
                },
                humidity: {
                  average: 72,
                  service1: 71,
                  service2: 73,
                },
              },
            },
          },
          "2023-10-02": {
            indicators: {
              temperature: {
                average: 18,
                service1: 17,
                service2: 19,
              },
              humidity: {
                average: 65,
                service1: 64,
                service2: 66,
              },
            },
            hours: {
              "09:00": {
                temperature: {
                  average: 16,
                  service1: 15,
                  service2: 17,
                },
                humidity: {
                  average: 68,
                  service1: 67,
                  service2: 69,
                },
              },
              "15:00": {
                temperature: {
                  average: 20,
                  service1: 19,
                  service2: 21,
                },
                humidity: {
                  average: 63,
                  service1: 62,
                  service2: 64,
                },
              },
              "21:00": {
                temperature: {
                  average: 15,
                  service1: 14,
                  service2: 16,
                },
                humidity: {
                  average: 70,
                  service1: 69,
                  service2: 71,
                },
              },
            },
          },
        },
      };

      setForecastData(testData[city]);
    }

    fetchForecast();
  }, [city]);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setCoords({
          lat: position.coords.latitude,
          lon: position.coords.longitude,
        });
      });
    }
  }, []);

  return (
    <ForecastContext.Provider
      value={{ city, setCity, forecastData, setForecastData }}
    >
      {children}
    </ForecastContext.Provider>
  );
};

const useForecastContext = () => useContext(ForecastContext);

export { ForecastProvider, useForecastContext };
