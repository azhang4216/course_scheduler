import googlemaps
from addresses import addresses
import os
from dotenv import load_dotenv

load_dotenv()
GMAPS_API_KEY = os.getenv('GMAPS_API_KEY')
map_client = googlemaps.Client(GMAPS_API_KEY)


def walk_distance_time(building1, building2):
    if building1 not in addresses or building2 not in addresses:
        raise ValueError("Building Address(es) given are not in addresses.py")

    response = map_client.directions(addresses[building1], addresses[building2], "walking")[0]['legs'][0]
    return response['distance']['text'], response['duration']['text']


# print(walk_distance_time("Mathematics Building", "Milbank Hall"))
# print(walk_distance_time("Mathematics Building", "Pupin Laboratories"))
