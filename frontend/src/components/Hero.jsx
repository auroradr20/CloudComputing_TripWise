function Hero({ user }) {
  return (
    <section className="hero" id="home">
      <div className="hero-content">
        <p className="tagline">Welcome to TripWise</p>

        <h1>
          Plan smarter trips without the travel planning stress.
        </h1>

        {user ? (
          <p className="hero-text">
            Welcome back, {user.username}. Create a new trip, explore your saved
            trips, or generate an itinerary for your next destination.
          </p>
        ) : (
          <p className="hero-text">
            Log in or create an account to start planning your trip, save your
            travel details, and generate personalized itineraries.
          </p>
        )}

        <div className="hero-buttons">
          {user ? (
            <>
              <a className="primary-button" href="#trip-form">
                Create a Trip
              </a>
              <a className="secondary-button" href="#your-trips">
                View My Trips
              </a>
            </>
          ) : (
            <>
              <a className="primary-button" href="#auth">
                Log in / Register
              </a>
              <a className="secondary-button" href="#features">
                Explore Features
              </a>
            </>
          )}
        </div>
      </div>
    </section>
  );
}

export default Hero;
