import Hero from "../components/Hero";
import FeatureCard from "../components/FeatureCard";
import AuthForm from "../components/AuthForm";
import TripForm from "../components/TripForm";
import WeatherSearch from "../components/WeatherSearch";
import ItineraryGenerator from "../components/ItineraryGenerator";
import YourTrips from "../components/YourTrips";
import MysteryTrip from "../components/MysteryTrip";
import Footer from "../components/Footer";

function Home({ user, setUser, latestTripId, setLatestTripId, tripsRefreshKey, refreshTrips, }) {
  return (
    <main>
      <Hero user={user} />

      <section className="features-section" id="features">
        <h2>Everything you need for your trip</h2>
        <p className="section-intro">
          TripWise brings your travel details together in one place.
        </p>

        <div className="features-grid">
          <FeatureCard
            title="Create Trips"
            description="Save your destination, dates, number of travelers, and preferences."
          />

          <FeatureCard
            title="Check Weather"
            description="View weather information for your destination before planning activities."
          />

          <FeatureCard
            title="Generate Itineraries"
            description="Create a clear day-by-day travel plan with suggested activities."
          />
        </div>
      </section>

      <AuthForm user={user} setUser={setUser} />

      <TripForm
        user={user}
        setLatestTripId={setLatestTripId}
        refreshTrips={refreshTrips}
      />

      <MysteryTrip
        user={user}
        setLatestTripId={setLatestTripId}
        refreshTrips={refreshTrips}
      />

      <YourTrips
        user={user}
        latestTripId={latestTripId}
        setLatestTripId={setLatestTripId}
        tripsRefreshKey={tripsRefreshKey}
      />

      <WeatherSearch />

      <ItineraryGenerator latestTripId={latestTripId} />

      <Footer />
    </main>
  );
}

export default Home;
