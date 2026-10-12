import { useState } from "react";

function MysteryTrip({ user, setLatestTripId, refreshTrips }) {
  const [mysteryTrip, setMysteryTrip] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleMysteryTrip() {
    if (!user) {
      setMessage("Please log in before creating a mystery trip.");
      return;
    }

    setLoading(true);
    setMessage("");
    setMysteryTrip(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5001/users/${user.user_id}/itinerary/random`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Could not create a mystery trip.");
        return;
      }

      localStorage.setItem("lastTripId", data.trip_id);
      setLatestTripId(data.trip_id);

      if (refreshTrips) {
        refreshTrips();
      }

      setMysteryTrip(data);
      setMessage(data.message || "Mystery trip created successfully!");
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mystery-section" id="mystery-trip">
      <div className="mystery-card">
        <p className="tagline">Mystery trip</p>
        <h2>Feeling spontaneous?</h2>
        <p>
          Let TripWise choose a random destination and create a surprise
          itinerary for you.
        </p>

        <button
          className="primary-button mystery-button"
          onClick={handleMysteryTrip}
          disabled={loading}
        >
          {loading ? "Creating mystery trip..." : "Create Mystery Trip"}
        </button>

        {message && <p className="form-message">{message}</p>}

        {mysteryTrip && (
          <div className="mystery-result">
            <h3>{mysteryTrip.destination}</h3>
            <p>{mysteryTrip.number_days} day mystery itinerary created.</p>
            <p>
              This trip is now selected, so you can view it in Your Trips or use
              it for itinerary actions.
            </p>
          </div>
        )}
      </div>
    </section>
  );
}

export default MysteryTrip;
