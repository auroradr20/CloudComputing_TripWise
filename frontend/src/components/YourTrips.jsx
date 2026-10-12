import { useEffect, useState } from "react";

function YourTrips({ user, latestTripId, setLatestTripId, tripsRefreshKey }) {
  const [trips, setTrips] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function fetchTrips() {
    if (!user) {
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/trips/");
      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Could not fetch trips.");
        return;
      }

      const userTrips = data.filter((trip) => trip.user_id === user.user_id);
      setTrips(userTrips);
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchTrips();
  }, [user, tripsRefreshKey]);

  function handleSelectTrip(tripId) {
    setLatestTripId(tripId);
    localStorage.setItem("lastTripId", tripId);
    setMessage("Trip selected. Scroll down to view its itinerary.");

    setTimeout(() => {
      document.getElementById("itinerary")?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  }

  async function handleDeleteTrip(tripId) {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this trip?"
    );

    if (!confirmDelete) {
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:5000/trips/${tripId}`, {
        method: "DELETE",
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Could not delete trip.");
        return;
      }

      setTrips((previousTrips) =>
        previousTrips.filter((trip) => trip.trip_id !== tripId)
      );

      if (String(latestTripId) === String(tripId)) {
        setLatestTripId(null);
        localStorage.removeItem("lastTripId");
      }

      setMessage(data.message || "Trip deleted successfully.");
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    }
  }

  if (!user) {
    return (
      <section className="your-trips-section" id="your-trips">
        <div className="your-trips-card">
          <p className="tagline">Your trips</p>
          <h2>Your saved trips</h2>
          <p>Please log in to view your trips.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="your-trips-section" id="your-trips">
      <div className="your-trips-card">
        <div className="section-heading">
          <p className="tagline">Your trips</p>
          <h2>Your saved trips</h2>
          <p>
            View your saved trips, open their itineraries, or delete trips you no longer need.

          </p>
        </div>

        <button className="secondary-button refresh-button" onClick={fetchTrips}>
          {loading ? "Loading..." : "Refresh Trips"}
        </button>

        {message && <p className="form-message">{message}</p>}

        {trips.length === 0 && !loading ? (
          <p className="empty-trips-message">
            You do not have any saved trips yet.
          </p>
        ) : (
          <div className="trips-grid">
            {trips.map((trip) => (
              <div
                className={`saved-trip-card ${
                  String(latestTripId) === String(trip.trip_id) ? "selected" : ""
                }`}
                key={trip.trip_id}
              >
                <h3>{trip.destination}</h3>

                <p>
                  {trip.start_date} → {trip.end_date}
                </p>

                <p>{trip.nr_people} traveler(s)</p>

                <div className="trip-card-actions">
                  <button
                    className="primary-button small-button"
                    onClick={() => handleSelectTrip(trip.trip_id)}
                  >
                    View Itinerary
                  </button>

                  <button
                    className="delete-button"
                    onClick={() => handleDeleteTrip(trip.trip_id)}
                  >
                    Delete
                  </button>
                </div>

                {String(latestTripId) === String(trip.trip_id) && (
                  <p className="selected-trip-label">Selected trip</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

export default YourTrips;