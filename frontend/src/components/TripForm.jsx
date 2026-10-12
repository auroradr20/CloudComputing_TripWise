import { useState } from "react";

const activityOptions = [
  { value: "restaurant", label: "Food" },
  { value: "museum", label: "Museums" },
  { value: "culture", label: "Culture" },
  { value: "cinema", label: "Cinema" },
  { value: "religion", label: "Religion" },
  { value: "park", label: "Parks" },
  { value: "nature", label: "Nature" },
  { value: "hiking", label: "Hiking" },
  { value: "sport", label: "Sport" },
  { value: "shopping", label: "Shopping" },
  { value: "sightseeing", label: "Sightseeing" },
];

function TripForm({ user, setLatestTripId, refreshTrips }) {
  const today = new Date().toISOString().split("T")[0];

  const [formData, setFormData] = useState({
    destination: "",
    startDate: "",
    endDate: "",
    travelers: "",
    groupType: "",
    dayIntensity: "normal",
    vibe: "",
    includeFood: true,
    preferences: [],
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  function handlePreferenceChange(event) {
    const { value, checked } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      preferences: checked
        ? [...previousData.preferences, value]
        : previousData.preferences.filter((preference) => preference !== value),
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!user) {
      setMessage("Please log in before creating a trip.");
      return;
    }

    if (
      !formData.destination ||
      !formData.startDate ||
      !formData.endDate ||
      !formData.travelers
    ) {
      setMessage("Please fill in destination, dates, and travelers.");
      return;
    }

    if (formData.startDate < today) {
      setMessage("The start date cannot be in the past.");
      return;
    }

    if (formData.endDate < formData.startDate) {
      setMessage("The end date cannot be before the start date.");
      return;
    }

    const tripPayload = {
      user_id: user.user_id,
      destination: formData.destination,
      start_date: formData.startDate,
      end_date: formData.endDate,
      nr_people: Number(formData.travelers),
    };

    const itineraryPayload = {
      day_intensity: formData.dayIntensity,
      group_type: formData.groupType,
      include_food: formData.includeFood,
      vibe: formData.vibe,
      activity_types: formData.preferences,
    };

    setLoading(true);
    setMessage("");

    try {
      const tripResponse = await fetch("http://127.0.0.1:5000/trips/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(tripPayload),
      });

      const tripData = await tripResponse.json();

      if (!tripResponse.ok) {
        setMessage(tripData.error || "Could not create trip.");
        return;
      }

      const itineraryResponse = await fetch(
        `http://127.0.0.1:5000/trips/${tripData.trip_id}/itinerary/generate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(itineraryPayload),
        }
      );

      const itineraryData = await itineraryResponse.json();

      if (!itineraryResponse.ok) {
        setMessage(
          itineraryData.error ||
            "Trip was created, but the itinerary could not be generated."
        );

        localStorage.setItem("lastTripId", tripData.trip_id);
        setLatestTripId(tripData.trip_id);

        if (refreshTrips) {
          refreshTrips();
        }

        return;
      }

      localStorage.setItem("lastTripId", tripData.trip_id);
      setLatestTripId(tripData.trip_id);

      if (refreshTrips) {
        refreshTrips();
      }

      setMessage(
        "Trip and itinerary created successfully! Scroll down to Your Trips. If you do not see it immediately, press Refresh Trips."
      );

      setTimeout(() => {
        document.getElementById("your-trips")?.scrollIntoView({ behavior: "smooth" });
      }, 300);

      setFormData({
        destination: "",
        startDate: "",
        endDate: "",
        travelers: "",
        groupType: "",
        dayIntensity: "normal",
        vibe: "",
        includeFood: true,
        preferences: [],
      });
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="form-section" id="trip-form">
      <div className="trip-panel">
        <div className="section-heading">
          <p className="tagline">Trip details</p>
          <h2>Create your trip</h2>
          <p>
            Choose your destination, travel dates, and preferences once.
            TripWise will create your itinerary automatically.
          </p>

          {!user && (
            <p>
              Please log in or register first so TripWise can save your trip to
              your account.
            </p>
          )}
        </div>

        <form className="trip-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="destination">Destination</label>
              <input
                id="destination"
                name="destination"
                type="text"
                placeholder="e.g. Paris"
                value={formData.destination}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="travelers">Number of travelers</label>
              <input
                id="travelers"
                name="travelers"
                type="number"
                min="1"
                placeholder="e.g. 2"
                value={formData.travelers}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="groupType">Group type</label>
              <select
                id="groupType"
                name="groupType"
                value={formData.groupType}
                onChange={handleChange}
              >
                <option value="">Select group type</option>
                <option value="solo">Solo</option>
                <option value="couple">Couple</option>
                <option value="friends">Friends</option>
                <option value="family">Family</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="dayIntensity">Day intensity</label>
              <select
                id="dayIntensity"
                name="dayIntensity"
                value={formData.dayIntensity}
                onChange={handleChange}
              >
                <option value="lazy">Lazy</option>
                <option value="normal">Normal</option>
                <option value="busy">Busy</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="vibe">Trip vibe</label>
              <select
                id="vibe"
                name="vibe"
                value={formData.vibe}
                onChange={handleChange}
              >
                <option value="">No vibe preference</option>
                <option value="chill">Chill</option>
                <option value="adventure">Adventure</option>
                <option value="cultural">Cultural</option>
                <option value="social">Social</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="startDate">Start date</label>
              <input
                id="startDate"
                name="startDate"
                type="date"
                min={today}
                value={formData.startDate}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="endDate">End date</label>
              <input
                id="endDate"
                name="endDate"
                type="date"
                min={formData.startDate || today}
                value={formData.endDate}
                onChange={handleChange}
              />
            </div>
          </div>

          <label className="food-toggle">
            <input
              type="checkbox"
              name="includeFood"
              checked={formData.includeFood}
              onChange={handleChange}
            />
            Include food places
          </label>

          <div className="form-group">
            <label>Activity preferences</label>
            <p className="helper-text">
              Choose one or more activity types for your itinerary.
            </p>

            <div className="preferences-grid">
              {activityOptions.map((option) => (
                <label
                  className={`preference-chip ${
                    formData.preferences.includes(option.value) ? "selected" : ""
                  }`}
                  key={option.value}
                >
                  <input
                    type="checkbox"
                    value={option.value}
                    checked={formData.preferences.includes(option.value)}
                    onChange={handlePreferenceChange}
                  />
                  <span>{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="form-actions">
            <button className="primary-button form-button" type="submit">
              {loading ? "Creating itinerary..." : "Create Trip & Itinerary"}
            </button>

            {message && <p className="form-message">{message}</p>}
          </div>
        </form>
      </div>
    </section>
  );
}

export default TripForm;