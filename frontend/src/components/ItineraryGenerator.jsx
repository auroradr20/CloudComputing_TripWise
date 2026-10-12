import { useEffect, useState } from "react";

function ItineraryGenerator({ latestTripId }) {
  const [itineraryData, setItineraryData] = useState(null);
  const [summary, setSummary] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function fetchItinerary(tripId) {
    if (!tripId) {
      setMessage("Create or select a trip first.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/trips/${tripId}/itinerary`
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Could not fetch itinerary.");
        return;
      }

      setItineraryData(data);
      setMessage("");
      await fetchSummary(tripId);
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  }

  async function fetchSummary(tripId) {
    if (!tripId) {
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/trips/${tripId}/itinerary/summary`
      );

      const data = await response.json();

      if (!response.ok) {
        return;
      }

      setSummary(data);
    } catch (error) {
      console.log("Could not fetch itinerary summary.");
    }
  }

  useEffect(() => {
    if (latestTripId) {
      fetchItinerary(latestTripId);
    }
  }, [latestTripId]);

  async function handleStatusChange(itineraryId, status) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/itinerary/${itineraryId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ status }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Could not update activity.");
        return;
      }

      setItineraryData((previousData) => ({
        ...previousData,
        itinerary: previousData.itinerary.map((item) =>
          item.itinerary_id === itineraryId ? { ...item, status } : item
        ),
      }));

      if (latestTripId) {
        await fetchSummary(latestTripId);
      }

      setMessage(data.message || `Activity ${status}.`);
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    }
  }

  async function handleReplaceActivity(itineraryId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/itinerary/${itineraryId}/replace`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Could not replace activity.");
        return;
      }

      if (latestTripId) {
        await fetchItinerary(latestTripId);
      }

      setMessage(data.message || "Activity replaced successfully.");
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    }
  }

  async function handleDeleteActivity(itineraryId) {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this activity?"
    );

    if (!confirmDelete) {
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/itinerary/${itineraryId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Could not delete activity.");
        return;
      }

      setItineraryData((previousData) => ({
        ...previousData,
        itinerary: previousData.itinerary.filter(
          (item) => item.itinerary_id !== itineraryId
        ),
      }));

      if (latestTripId) {
        await fetchSummary(latestTripId);
      }

      setMessage(data.message || "Activity deleted successfully.");
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    }
  }

  function groupByDay(itinerary) {
    return itinerary.reduce((days, item) => {
      if (!days[item.day_number]) {
        days[item.day_number] = [];
      }

      days[item.day_number].push(item);
      return days;
    }, {});
  }

  const groupedItinerary = itineraryData
    ? groupByDay(itineraryData.itinerary)
    : {};

  return (
    <section className="itinerary-section" id="itinerary">
      <div className="itinerary-header">
        <p className="tagline">Your itinerary</p>
        <h2>View your travel plan</h2>
        <p>
          Select a trip from Your Trips to view its itinerary. You can accept,
          decline, replace, or delete activities from here.
        </p>

        {!latestTripId && (
          <p className="itinerary-warning">
            Create or select a trip first to view an itinerary.
          </p>
        )}
      </div>

      <div className="itinerary-form">
        <div className="form-actions">
          <button
            className="secondary-button form-button"
            type="button"
            disabled={loading || !latestTripId}
            onClick={() => fetchItinerary(latestTripId)}
          >
            {loading ? "Loading..." : "Refresh Itinerary"}
          </button>

          {message && <p className="form-message">{message}</p>}
        </div>
      </div>

            {summary && (
        <div className="summary-grid">
          <div className="summary-card">
            <span>Total activities</span>
            <strong>{summary.total_activities}</strong>
          </div>

          <div className="summary-card">
            <span>Pending</span>
            <strong>{summary.pending}</strong>
          </div>

          <div className="summary-card">
            <span>Accepted</span>
            <strong>{summary.accepted}</strong>
          </div>

          <div className="summary-card">
            <span>Declined</span>
            <strong>{summary.declined}</strong>
          </div>
        </div>
      )}

      {itineraryData && (
        <div className="itinerary-results">
          <h3>{itineraryData.destination} itinerary</h3>

          {itineraryData.itinerary.length === 0 ? (
            <p className="empty-trips-message">
              This trip does not have itinerary activities yet.
            </p>
          ) : (
            Object.entries(groupedItinerary).map(([dayNumber, activities]) => (
              <div className="day-card" key={dayNumber}>
                <h4>Day {dayNumber}</h4>

                <div className="activity-list">
                  {activities.map((item) => (
                    <div className="activity-card" key={item.itinerary_id}>
                      <div className="activity-info">
                        <span className="activity-number">
                          Activity {item.activity_nr}
                        </span>
                        <h5>{item.activity}</h5>
                        <p>{item.address || "No address available"}</p>

                        {item.status && (
                          <p className={`activity-status ${item.status}`}>
                            Status: {item.status}
                          </p>
                        )}
                      </div>

                      <div className="activity-side">
                        <span className="activity-type">
                          {item.activity_type}
                        </span>

                        <div className="activity-actions">
                          {item.status === "pending" && (
                            <>
                              <button
                                type="button"
                                className="accept-button"
                                onClick={() =>
                                  handleStatusChange(
                                    item.itinerary_id,
                                    "accepted"
                                  )
                                }
                              >
                                Accept
                              </button>

                              <button
                                type="button"
                                className="decline-button"
                                onClick={() =>
                                  handleStatusChange(
                                    item.itinerary_id,
                                    "declined"
                                  )
                                }
                              >
                                Decline
                              </button>
                            </>
                          )}

                          <button
                            type="button"
                            className="replace-button"
                            onClick={() =>
                              handleReplaceActivity(item.itinerary_id)
                            }
                          >
                            Replace
                          </button>

                          <button
                            type="button"
                            className="delete-activity-button"
                            onClick={() =>
                              handleDeleteActivity(item.itinerary_id)
                            }
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </section>
  );
}

export default ItineraryGenerator;