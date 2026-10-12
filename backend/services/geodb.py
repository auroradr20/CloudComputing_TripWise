import random 
import requests

def get_random_destination():
    """
    Get a random city with a population of at least 500000 people from GeoDB API.
    """

    url = "http://geodb-free-service.wirefreethought.com/v1/geo/cities"

    params = {
        'minPopulation': 500000,
        'limit': 10,
        'offset': random.randint(0, 1000)
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception("Request failed.")
    
    data = response.json()
    cities = data.get('data', [])

    if not cities:
        raise ValueError("No cities found.")
    
    city = random.choice(cities)

    return city['city']