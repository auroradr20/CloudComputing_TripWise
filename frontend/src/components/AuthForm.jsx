import { useState } from "react";

function AuthForm({ user, setUser }) {
  const [mode, setMode] = useState("login");
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!formData.username || !formData.password) {
      setMessage("Please enter a username and password.");
      return;
    }

    setLoading(true);
    setMessage("");

    const endpoint = mode === "login" ? "login" : "register";

    try {
      const response = await fetch(`http://127.0.0.1:5000/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.error || "Something went wrong.");
        return;
      }

      const loggedInUser = {
        user_id: data.user_id,
        username: data.username,
      };

      setUser(loggedInUser);
      localStorage.setItem("tripwiseUser", JSON.stringify(loggedInUser));

      setMessage(data.message || "Success!");
      setFormData({ username: "", password: "" });
    } catch (error) {
      setMessage("Could not connect to the backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    setUser(null);
    localStorage.removeItem("tripwiseUser");
    localStorage.removeItem("lastTripId");
    setMessage("You have been logged out.");
  }

  if (user) {
    return (
      <section className="auth-section" id="auth">
        <div className="auth-card logged-in-card">
          <p className="tagline">Account</p>
          <h2>Welcome, {user.username}</h2>
          <p>
            You are logged in. You can now create trips and generate itineraries.
          </p>

          <button className="secondary-button auth-button" onClick={handleLogout}>
            Log out
          </button>

          {message && <p className="auth-message">{message}</p>}
        </div>
      </section>
    );
  }

  return (
    <section className="auth-section" id="auth">
      <div className="auth-card">
        <p className="tagline">Account</p>
        <h2>{mode === "login" ? "Log in" : "Create an account"}</h2>
        <p className="auth-intro">
          Log in or create an account to save your trips, view your plans, and generate personalized itineraries whenever you need them.
        </p>

        <div className="auth-tabs">
          <button
            type="button"
            className={mode === "login" ? "auth-tab active" : "auth-tab"}
            onClick={() => {
              setMode("login");
              setMessage("");
            }}
          >
            Login
          </button>

          <button
            type="button"
            className={mode === "register" ? "auth-tab active" : "auth-tab"}
            onClick={() => {
              setMode("register");
              setMessage("");
            }}
          >
            Register
          </button>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="auth-username">Username</label>
            <input
              id="auth-username"
              name="username"
              type="text"
              placeholder="e.g. testuser"
              value={formData.username}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="auth-password">Password</label>
            <input
              id="auth-password"
              name="password"
              type="password"
              placeholder="At least 8 chars, 1 uppercase, 1 digit"
              value={formData.password}
              onChange={handleChange}
            />
          </div>

          <button className="primary-button auth-button" type="submit">
            {loading
              ? "Loading..."
              : mode === "login"
              ? "Log in"
              : "Register"}
          </button>

          {message && <p className="auth-message">{message}</p>}
        </form>
      </div>
    </section>
  );
}

export default AuthForm;