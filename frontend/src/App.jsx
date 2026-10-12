import { useEffect, useState } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";

function App() {
  const [user, setUser] = useState(null);
  const [latestTripId, setLatestTripId] = useState(null);
  const [tripsRefreshKey, setTripsRefreshKey] = useState(0);

  useEffect(() => {
    const storedUser = localStorage.getItem("tripwiseUser");
    const storedTripId = localStorage.getItem("lastTripId");

    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }

    if (storedTripId) {
      setLatestTripId(storedTripId);
    }
  }, []);

  function refreshTrips() {
    setTripsRefreshKey((previousKey) => previousKey + 1);
  }

  return (
    <div className="app">
      <Navbar user={user} />
      <Home
        user={user}
        setUser={setUser}
        latestTripId={latestTripId}
        setLatestTripId={setLatestTripId}
        tripsRefreshKey={tripsRefreshKey}
        refreshTrips={refreshTrips}
      />
    </div>
  );
}

export default App;
