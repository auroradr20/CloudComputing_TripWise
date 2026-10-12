# Defining the application factory.
import os 
from flask import Flask
from backend.db import init_app
from backend.routes.trips import trips_bp
from backend.routes.users import users_bp
from backend.services.weather import weather_bp
from backend.routes.itinerary import itinerary_bp
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # the instance folder exists 
    os.makedirs(app.instance_path, exist_ok=True)

    app.register_blueprint(users_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(itinerary_bp)
    init_app(app)
    
    return app

