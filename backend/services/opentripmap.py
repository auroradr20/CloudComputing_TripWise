import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OPENTRIPMAP_API_KEY = os.getenv('OPENTRIPMAP_API_KEY')

OPENTRIPMAP_KINDS = [
    "foods",
    "museums",
    "cultural",
    "cinemas",
    "religion",
    "gardens_and_parks",
    "natural",
    "beaches",
    "nature_reserves",
    "mountain_peaks",
    "geological_formations",
    "sport",
    "shops",
    "historic",
    "architecture"
]

def get_activity_type(kinds: str):
    """
    Convert activity kinds from the API to our app's activity types.
    """
    if not kinds:
        return 'other'
    
    kind_list = kinds.split(',')

    for k in kind_list:
        if k == "foods":
            return "restaurant"
        
        if k == "museums":
            return "museum"
        
        if k == "cultural":
            return "culture"
        
        if k == "cinemas":
            return "cinema"
        
        if k == "religion":
            return "religion"
        
        if k in ["gardens_and_parks"]:
            return "park"
        
        if k in ["natural", "beaches", "nature_reserves"]:
            return "nature"
        
        if k in ["mountain_peaks", "geological_formations"]:
            return "hiking"
        
        if k == "sport":
            return "sport"
        
        if k == "shops":
            return "shopping"
        
        if k in ["historic", "architecture"]:
            return "sightseeing"

    return 'other'

def get_coordinates(destination: str):
    '''
    Convert a destination into coordinates using OpenTripMap API.
    '''

    if not OPENTRIPMAP_API_KEY:
        raise ValueError('OPENTRIP_API_KEY is missing.')
    url = "https://api.opentripmap.com/0.1/en/places/geoname"

    parameters = {
        'name': destination,
        'apikey': OPENTRIPMAP_API_KEY
    }

    response = requests.get(url, params=parameters, timeout=10)

    if response.status_code != 200:
        raise Exception(f"OpenTripMap request failed: {response.text}")

    data = response.json()

    if 'lat' not in data or 'lon' not in data:
        raise ValueError(f"No coordinates found for this destination: {destination}")


    return data['lat'], data['lon']


def get_places(destination: str, limit: int = 40):
    """
    Get places from OpenTripMap for a given destination and category.
    """

    if not OPENTRIPMAP_API_KEY:
        raise ValueError('API is missing.')

    lat, lon = get_coordinates(destination)

    url = "https://api.opentripmap.com/0.1/en/places/radius"

    parameters = {
        "radius": 7000,
        "lat": lat,
        "lon": lon,
        "kinds": ",".join(OPENTRIPMAP_KINDS),
        "rate": "3",
        "format": "json",
        "limit": limit,
        "apikey": OPENTRIPMAP_API_KEY
    }

    response = requests.get(url, params=parameters, timeout=10)

    if response.status_code != 200:
        raise Exception(f"OpenTripMap request failed: {response.text}")
    
    data = response.json()

    places = []

    for item in data:
        name = item.get('name')
        kinds = item.get('kinds', '')
        activity_type = get_activity_type(kinds)

        if name and activity_type != 'other':
            places.append({
                "name": name,
                "address": destination,
                "category": kinds.split(','),
                "activity_type": activity_type
            })

    return places 
