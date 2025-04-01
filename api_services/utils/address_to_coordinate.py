import requests
import logging
import os
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

def address_to_coordinate(address):
    """
    Retrieve latitude and longitude for a given address using the Google Geocoding API.
    
    Parameters:
        address (str): The address to be geocoded.
        
    Returns:
        tuple: (latitude, longitude) if successful; otherwise, (None, None).
    """
    # Retrieve API key from environment variables (replace with your secure method)
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    
    try:
        response = requests.get(url, params={'address': address, 'key': api_key}, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses (status code != 200)
        
        data = response.json()
        results = data.get('results')
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            logger.warning("No geocoding results found for address: %s", address)
            return None, None

    except requests.exceptions.RequestException as e:
        logger.error("Geocode API request failed: %s", e)
        return None, None
