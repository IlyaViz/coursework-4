import ConditionalLink from "./ConditionalLink";
import generateServiceColor from "../utils/serviceColorGenerator";

const ForecastBlock = ({ forecastData, onClickBaseLink }) => {
  console.log(forecastData);

  return (
    <div className="flex justify-around gap-4">
      {Object.entries(forecastData).map(([time, data]) => (
        <ConditionalLink
          to={`/${onClickBaseLink}/${time}`}
          condition={onClickBaseLink}
          key={time}
        >
          <div key={time} className="p-1 bg-blue-400 rounded-xl">
            <div className="flex items-center justify-between">
              <h1 className="w-full text-4xl text-center text-white">{time}</h1>

              <div className="flex flex-col m-1">
                <img
                  src="https://as2.ftcdn.net/v2/jpg/01/17/28/51/1000_F_117285131_W2qjuUEEBPP2nPJHxosDk62mj4B6KvIg.jpg"
                  className="w-16"
                />
                <img
                  src="https://as2.ftcdn.net/v2/jpg/01/17/28/51/1000_F_117285131_W2qjuUEEBPP2nPJHxosDk62mj4B6KvIg.jpg"
                  className="w-16"
                />
                <img
                  src="https://as2.ftcdn.net/v2/jpg/01/17/28/51/1000_F_117285131_W2qjuUEEBPP2nPJHxosDk62mj4B6KvIg.jpg"
                  className="w-16"
                />
              </div>
            </div>

            <div className="flex justify-center gap-2 m-1 bg-blue-300">
              {Object.entries(data.indicators ? data.indicators : data).map(
                ([indicator, services]) => (
                  <div
                    key={indicator}
                    className="flex flex-col items-center w-24"
                  >
                    {indicator}

                    {Object.entries(services).map(
                      ([service, temp]) =>
                        service !== "average" && (
                          <div
                            key={service}
                            style={{
                              backgroundColor: generateServiceColor(service),
                            }}
                            className="w-full text-center rounded-lg"
                          >
                            <p>{temp}</p>
                          </div>
                        )
                    )}

                    <p className="w-full mt-2 mb-1 text-center bg-green-400">
                      {services.average}
                    </p>
                  </div>
                )
              )}
            </div>
          </div>
        </ConditionalLink>
      ))}
    </div>
  );
};

export default ForecastBlock;
