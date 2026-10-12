import { useState } from "react";

function WeatherSearch() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!city.trim()) {
      setMessage("Please enter a destination.");
      setWeather(null);
      return;
    }

    setLoading(true);
    setMessage("");
    setWeather(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5001/weather/${encodeURIComponent(city)}`
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Could not fetch weather data.");
        return;
      }

      setWeather(data);
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="weather-section" id="weather">
      <div className="weather-card">
        <div>
          <p className="tagline">Weather check</p>
          <h2>Check destination weather</h2>
          <p className="weather-intro">
            Search for a city and TripWise will show the current weather
            information for your destination.
          </p>
        </div>

        <form className="weather-form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="e.g. Paris"
            value={city}
            onChange={(event) => setCity(event.target.value)}
          />
          <button className="primary-button weather-button" type="submit">
            Check Weather
          </button>
        </form>

        {loading && <p className="weather-message">Loading weather...</p>}
        {message && <p className="weather-message">{message}</p>}

        {weather && (
          <div className="weather-result">
            <h3>{weather.city || city}</h3>

            <div className="weather-details">
              {weather.temperature !== undefined && (
                <div>
                  <span>Temperature</span>
                  <strong>{weather.temperature}°C</strong>
                </div>
              )}

              {weather.description && (
                <div>
                  <span>Condition</span>
                  <strong>{weather.description}</strong>
                </div>
              )}

              {weather.good_weather !== undefined && (
                <div>
                  <span>Outdoor suitability</span>
                  <strong>
                    {weather.good_weather ? "Good weather" : "Bad weather"}
                  </strong>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

export default WeatherSearch;
