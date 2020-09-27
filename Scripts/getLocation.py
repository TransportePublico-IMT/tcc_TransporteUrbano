import os
from os.path import dirname, join

import geopy.distance
import googlemaps
import pandas as pd
from dotenv import load_dotenv
from geopy.geocoders import GoogleV3

# Create .env file path.
dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)
API = os.getenv("GOOGLE_MAPS")

geolocator = GoogleV3(api_key=API)

print(type(geolocator))


def getAdress(nome):
    name = nome

    try:
        location = geolocator.geocode(name)
        endereco = [location.address, location.latitude, location.longitude]
    except Exception as e:
        print("Sem endereco", e)
        endereco = [None, None, None]
    return endereco
