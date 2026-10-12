-- define the db tables
DROP TABLE IF EXISTS Itineraries;
DROP TABLE IF EXISTS Trips;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Trips(
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    destination TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    nr_people INTEGER,
    is_random INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id)
        REFERENCES Users (id)
);

CREATE TABLE Itineraries(
    itinerary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL,
    day_number INTEGER NOT NULL,
    activity_nr INTEGER NOT NULL,
    activity TEXT NOT NULL,
    address TEXT,
    activity_type TEXT,
    status TEXT NOT NULL,
    FOREIGN KEY (trip_id)
        REFERENCES Trips (trip_id)
);