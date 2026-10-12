# Project Title
    TripWise
## Brief description of the project
This project is a travel planning web application. The application allows users to create an account, log in, create trips, check weather information for a destination, and generate an itinerary with suggested activities and places to visit.
The goal of the project is to make travel planning easier by helping users organise trip details and receive activity suggestions based on their destination, group type and activity preferences. 
- The backend is built with Flask.
- The database is SQLite.
- The application uses blueprints to organise routes.
- Passwords are hashed before they are stored in the database.

## Frontend mockup
## Team members
1. Aurora Dragnoi, cpf995
2. Ioana Martiniuc, iav230
3. XING CHEN, sil039
4. YILE YE, qod519

## Installation details
* Open the project folder:
    cd group-20

* Create and activate a virtual environment.
- On Windows:
    python -m venv .venv
    .venv\Scripts\activate
- On macOS/Linux:
    python3 -m venv .venv
    source .venv/bin/activate

* Install the required dependencies:
    pip install -r requirements.txt

* Create a .env file in the root folder of the project and add the API keys:
    OPENTRIPMAP_API_KEY=your_opentripmap_api_key_here
    WEATHER_API_KEY=your_weather_api_key_here

* Initialise the database:
    flask --app backend.app:create_app init-db
* Run the Flask application:
    flask --app backend.app:create_app run --debug
* The backend should then run locally at:
    http://127.0.0.1:5000

## Architecture
group-20/ 
│ 
├── backend/ 
│   ├── app.py 
│   ├── db.py 
│   ├── schema.sql 
│   │
│   ├── routes/ 
│   │   ├── itinerary.py 
│   │   ├── trips.py 
│   │   ├── users.py 
│   │ 
│   └── services/ 
│       └── opentripmap.py 
│       └── weather.py
├── frontend/ 
│ 
├── .gitignore 
├── README.md 
└── requirements.txt

    backend/app.py 
Creates the Flask application, registers the blueprints, and connects the database setup.
    backend/db.py
Handles the SQLite database connection and database initialisation.
    backend/schema.sql
Defines the database tables used by the application.
    backend/routes/users.py
Contains the user registration, login, username change, and password change.
    backend/routes/trips.py
Contains the routes for creating, viewing, updating, and deleting trips.
    backend/routes/itinerary.py
Contains the routes for generating, viewing, updating, and deleting itinerary items.
    backend/services/opentripmap.py
Handles communication with the OpenTripMap API and formats activity suggestions.
    backend/services/weather.py
Uses an external API to retrieve weather information for a destination.

## APIs
*   OpenTripMap API
Used to retrieve suggested places and activities for a destination.
*   Open-Meteo Geocoding API
Used to find the latitude and longitude of a city.
*   Open Weather API
Used to retrieve weather information and forecasts.