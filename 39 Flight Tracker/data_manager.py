import requests as req
import os as os
from dotenv import load_dotenv

load_dotenv()

# Sheety
SHEETY_API_ENDPOINT = os.environ["SHEETY_API_ENDPOINT"]
SHEETY_BEARER_TOKEN = os.environ["SHEETY_BEARER_TOKEN"]

# Tequila Kiwi
FLIGHT_API_ENDPOINT = os.environ["FLIGHT_API_ENDPOINT"]
FLIGHT_API_KEY = os.environ["FLIGHT_API_KEY"]


class DataManager:
    def __init__(self):
        self.flight_headers = {
            "apikey": FLIGHT_API_KEY
        }
        self.sheety_headers = {
            "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}",
            'Content-Type': 'application/json',
        }

    def update_iata_codes(self):
        res = req.get(f"{SHEETY_API_ENDPOINT}/prices",
                      headers=self.sheety_headers)
        res.raise_for_status()
        data = res.json()["prices"]
        for i in range(len(data)):
            if not data[i]["iataCode"]:
                city = data[i]["city"]
                row = i + 2
                iata_code = self.get_iata_code(city)
                json = {
                    "price": {
                        "iataCode": iata_code,
                    }
                }
                res = req.put(f"{SHEETY_API_ENDPOINT}/prices/{row}",
                              headers=self.sheety_headers, json=json)

    def get_iata_code(self, city_name):
        url = f"{FLIGHT_API_ENDPOINT}/locations/query"
        params = {
            "term": city_name,
        }
        res = req.get(url=url, params=params,
                      headers=self.flight_headers)
        res.raise_for_status()
        return res.json()["locations"][0]["code"]

    def get_locations(self):
        res = req.get(f"{SHEETY_API_ENDPOINT}/prices",
                      headers=self.sheety_headers)
        res.raise_for_status()
        return res.json()["prices"]
