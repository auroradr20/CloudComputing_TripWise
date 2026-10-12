# TripWise Cloud Deployment

Name: Aurora Dragnoi 
Student Number: 50455539


## Project Description

TripWise is a travel planning web application that helps users organise trips and generate itinerary suggestions. The application allows users to create an account, log in, create trips, check weather information for a destination, and generate an itinerary with suggested activities and places to visit.

For this cloud computing project, the original TripWise web application was containerized and deployed using Docker and Docker Swarm. The goal of this version is to demonstrate cloud computing concepts such as containerization, service orchestration, scalability, replication, and deployment automation.

The application includes the following main features:

- User registration and login
- Trip creation and trip management
- Itinerary generation based on destination
- Activity filtering by preferences, group type, and intensity
- Weather information for a destination
- Random trip / mystery trip generation

## Technologies Used

- Frontend: React with Vite
- Backend: Flask
- Database: SQLite
- APIs: OpenTripMap API, Open-Meteo Geocoding API, Open Weather API
- Containerization: Docker
- Orchestration: Docker Swarm

## Project Structure

```text
CloudComputing_TripWise/
│
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── schema.sql
│   ├── Dockerfile
│   │
│   ├── routes/
│   │   ├── itinerary.py
│   │   ├── trips.py
│   │   └── users.py
│   │
│   └── services/
│       ├── opentripmap.py
│       ├── weather.py
│       └── geodb.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── index.html
│   ├── public/
│   └── src/
│
├── docker-compose.yml
├── docker-stack.yml
├── .dockerignore
├── .gitignore
├── README.md
└── requirements.txt
```

## Main Backend Files

`backend/app.py` creates the Flask application, registers the blueprints, and connects the database setup.

`backend/db.py` handles the SQLite database connection and database initialization.

`backend/schema.sql` defines the database tables used by the application.

`backend/routes/users.py` contains the user registration, login, username change, and password change routes.

`backend/routes/trips.py` contains the routes for creating, viewing, updating, and deleting trips.

`backend/routes/itinerary.py` contains the routes for generating, viewing, updating, replacing, and deleting itinerary items.

`backend/services/opentripmap.py` handles communication with the OpenTripMap API and formats activity suggestions.

`backend/services/weather.py` retrieves weather information for a destination.

`backend/services/geodb.py` supports random destination generation.

## APIs Used

### OpenTripMap API

Used to retrieve suggested places and activities for a destination.

### Open-Meteo Geocoding API

Used to find the latitude and longitude of a city.

### Open Weather API

Used to retrieve weather information and forecasts.

## Environment Variables

Create a `.env` file in the root folder of the project:

```env
OPENTRIPMAP_API_KEY=your_opentripmap_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

The `.env` file is ignored by Git and should not be committed.

## Running the Project Locally Without Docker

Open the project folder:

```bash
cd CloudComputing_TripWise
```

Create and activate a virtual environment.

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required backend dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
flask --app backend.app:create_app init-db
```

Run the Flask backend:

```bash
flask --app backend.app:create_app run --debug --port 5001
```

The backend runs locally at:

```text
http://127.0.0.1:5001
```

To run the frontend, open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs locally at:

```text
http://localhost:5173
```

## Running the Project with Docker Compose

Make sure Docker Desktop is running.

From the project root folder, build and start the containers:

```bash
docker compose up --build
```

The frontend will be available at:

```text
http://localhost:5173
```

The backend will be available at:

```text
http://localhost:5001
```

To stop the containers, press:

```text
CTRL + C
```

## Running the Project with Docker Swarm

This project also includes a Docker Swarm deployment file to demonstrate orchestration and service replication.

Initialize Docker Swarm:

```bash
docker swarm init
```

Build the Docker images:

```bash
docker compose build
```

Tag the images for the Swarm stack:

```bash
docker tag cloudcomputing_tripwise-backend:latest tripwise-backend:latest
docker tag cloudcomputing_tripwise-frontend:latest tripwise-frontend:latest
```

Deploy the stack:

```bash
docker stack deploy -c docker-stack.yml tripwise
```

Check the running services:

```bash
docker service ls
```

Expected result:

```text
tripwise_backend     2/2
tripwise_frontend    1/1
```

The backend is deployed with 2 replicas to demonstrate scalability and availability. The frontend is deployed with 1 replica because the Vite development server caused dependency-loading issues when scaled to multiple replicas.

Open the application at:

```text
http://localhost:5173
```

## Stopping the Docker Swarm Deployment

Remove the deployed stack:

```bash
docker stack rm tripwise
```

To leave Swarm mode:

```bash
docker swarm leave --force
```

## Notes

- The project uses SQLite for simplicity.
- The database is stored locally in the `instance/` folder.
- The `.env` file is required for API keys.
- The application should be tested locally before running it with Docker or Docker Swarm.