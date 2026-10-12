function Navbar({ user }) {
  return (
    <nav className="navbar">
      <div className="logo">TripWise</div>

      <div className="nav-links">
        <a href="#features">Features</a>
        <a href="#auth">{user ? user.username : "Login"}</a>
        <a href="#trip-form">Create Trip</a>
        <a href="#mystery-trip">Mystery Trip</a>
        <a href="#your-trips">Your Trips</a>
        <a href="#weather">Weather</a>
        <a href="#itinerary">Itinerary</a>
      </div>
    </nav>
  );
}

export default Navbar;