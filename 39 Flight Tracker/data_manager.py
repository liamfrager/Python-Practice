import requests as req
import os as os
from dotenv import load_dotenv

load_dotenv()

# Sheety
SHEETY_API_ENDPOINT = os.environ["SHEETY_API_ENDPOINT"]

# Tequila Kiwi
FLIGHT_API_ENDPOINT = os.environ["FLIGHT_API_ENDPOINT"]
FLIGHT_API_KEY = os.environ["FLIGHT_API_KEY"]


class DataManager:

    def update_iata_codes(self):
        res = req.get(f"{SHEETY_API_ENDPOINT}/prices")
        res.raise_for_status()
        data = res.json()["prices"]
        cities = [x["city"] for x in data]
        for city in cities:
            pass
        # res = req.post(f"{SHEETY_API_ENDPOINT}/prices", )

    def get_iata_code(self, city_name):
        headers = {
            "apikey": FLIGHT_API_KEY
        }
        params = {
            "term": city_name,
            "location_types": "city",
            "limit": 1,
        }
        res = req.get(FLIGHT_API_ENDPOINT, params=params, headers=headers)
        res.raise_for_status()
        print(res.json()["data"])

    def get_locations(self):
        res = req.get(f"{SHEETY_API_ENDPOINT}/prices")
        res.raise_for_status()
        return res.json()["prices"]
