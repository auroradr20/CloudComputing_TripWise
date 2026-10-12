from flask import request
from flask import Blueprint, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

Weather_API_KEY = os.getenv("WEATHER_API_KEY")
weather_bp = Blueprint('weather', __name__)

"""This module defines a Flask Blueprint for handling weather-related routes. 
It includes a route to fetch weather information for a specified city. 
The route uses the Open-Meteo Geocoding API to get the latitude and longitude of the city, 
and then it uses the Open Weather API to retrieve the current weather conditions. 
The response includes the city name, temperature in Celsius, and a description of the weather."""

@weather_bp.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    geo_url=(
         "https://geocoding-api.open-meteo.com/v1/search"f"?name={city}"
    )

    """Fetches weather information for a specified city."""

    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data or not geo_data["results"]:
        return jsonify({"error": f"No coordinates found for this city: {city}"}), 404

    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]

    """Fetches weather information using the Open Weather API based on the latitude and longitude obtained from the geocoding API."""

    headers = {
	"x-rapidapi-key": Weather_API_KEY,
	"x-rapidapi-host": "open-weather13.p.rapidapi.com",
	"Content-Type": "application/json"
    }
    weather_url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "lang": "EN"
    }

    """Makes a GET request to the Open Weather API to retrieve the current weather conditions for the specified city, 
    and returns a JSON response containing the city name, temperature in Celsius, and a description of the weather."""

    weather_response = requests.get(weather_url, params=params, headers=headers)

    if weather_response.status_code != 200:
        return jsonify({
            "error": "Failed to get weather data",
        "details": weather_response.text
        }), weather_response.status_code

    w_data = weather_response.json()
    current = w_data["list"][0]
    temperature = round(
    current["main"]["temp"] - 273.15,1
    )
    description = current["weather"][0]["description"]

    return jsonify({
    "city": city,
    "temperature": temperature,
    "description": description,
    "good_weather": weather_good(description)
    })   


@weather_bp.route('/weather/<city>/forecast', methods=['GET'])
def get_forecast(city):
    """Fetches a 5-day weather forecast for a specified city."""

    geo_url=(
         "https://geocoding-api.open-meteo.com/v1/search"f"?name={city}"
    )

    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data or not geo_data["results"]:
        return jsonify({"error": f"No coordinates found for this city: {city}"}), 404

    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]

    headers = {
    "x-rapidapi-key": Weather_API_KEY,
    "x-rapidapi-host": "open-weather13.p.rapidapi.com",
    "Content-Type": "application/json"
    }

    weather_url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "lang": "EN"
    }

    weather_response = requests.get(weather_url, params=params, headers=headers)

    if weather_response.status_code != 200:
        return jsonify({
            "error": "Failed to get weather data",
            "details": weather_response.text
        }), weather_response.status_code

    w_data = weather_response.json()
    forecast = []
    for item in w_data["list"]:
        if item["dt_txt"].endswith("12:00:00"):
            forecast.append({
                "date": item["dt_txt"],
                "description": item["weather"][0]["description"],
                "good_weather": weather_good(item["weather"][0]["description"])
            })
    return jsonify({
        "city": city,
        "forecast": forecast
    })

def weather_good(description:str)->bool:
    """
    good weather = returns True
    bad weather = returns False
    """
    weather = description.lower().strip()
    bad_weather = ["drizzle","rain","snow","showers","shower","thunderstorm","hail","haze","smoke","dust","mist","fog","sleet"]
    for word in bad_weather:
        if word in weather:
            return False
        
    return True

def get_weather_good(city:str)->bool:
    """
    This function is a copy paste from get_weather, but it returns the result of weather_good() only
    """
    geo_url=(
         "https://geocoding-api.open-meteo.com/v1/search"f"?name={city}"
    )

    """Fetches weather information for a specified city."""

    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()
    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]

    """Fetches weather information using the Open Weather API based on the latitude and longitude obtained from the geocoding API."""

    headers = {
	"x-rapidapi-key": Weather_API_KEY,
	"x-rapidapi-host": "open-weather13.p.rapidapi.com",
	"Content-Type": "application/json"
    }
    weather_url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "lang": "EN"
    }

    """Makes a GET request to the Open Weather API to retrieve the current weather conditions for the specified city, 
    and returns a JSON response containing the city name, temperature in Celsius, and a description of the weather."""

    weather_response = requests.get(weather_url, params=params, headers=headers)
    w_data = weather_response.json()
    current = w_data["list"][0]
    temperature = round(
    current["main"]["temp"] - 273.15,1
    )
    description = current["weather"][0]["description"]

    return weather_good(description)

