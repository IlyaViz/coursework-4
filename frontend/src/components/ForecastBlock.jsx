import ConditionalLink from "./ConditionalLink";
import generateServiceColor from "../utils/serviceColorGenerator";

const ForecastBlock = ({ forecast, onClickBaseLink }) => {
  return (
    <div className="grid grid-cols-1 gap-y-5 lg:grid-cols-2 xl:grid-cols-3 justify-items-center">
      {Object.entries(forecast).map(([time, data]) => (
        <ConditionalLink
          to={`/${onClickBaseLink}/${time}`}
          condition={onClickBaseLink}
          key={time}
        >
          <div key={time} className="p-1 bg-blue-400 rounded-xl">
            <div className="flex items-center justify-between">
              <h1 className="w-full text-4xl text-center text-white">{time}</h1>

              <div className="flex flex-col m-1">
                {Object.entries(
                  data.indicators
                    ? data.indicators["condition icon"]
                    : data["condition icon"]
                ).map(([service, icon]) => (
                  <img src={icon} key={service} style={{backgroundColor: generateServiceColor(service)}}/>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 justify-items-center sm:grid-cols-4">
              {Object.entries(data.indicators ? data.indicators : data).map(
                ([indicator, services]) =>
                  indicator !== "condition icon" && (
                    <div
                      key={indicator}
                      className="flex flex-col items-center w-24"
                    >
                      <h1 className="text-center">{indicator}</h1>

                      {Object.entries(services).map(
                        ([service, value]) =>
                          service !== "average" && (
                            <div
                              key={service}
                              style={{
                                backgroundColor: generateServiceColor(service),
                              }}
                              className="w-full text-center rounded-lg"
                            >
                              <p>{value}</p>
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
