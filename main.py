import googlemaps
from datetime import datetime

api_key = 'AIzaSyC4ANo16mXKpsOptseCbBkZgmahkpTjXVk'
gmaps = googlemaps.Client(key=api_key)
geocode_result = gmaps.geocode('Palermo, Buenos Aires')


