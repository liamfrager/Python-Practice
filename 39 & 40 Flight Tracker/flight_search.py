import requests as req

import os as os
from dotenv import load_dotenv

load_dotenv()

# Tequila Kiwi
FLIGHT_API_ENDPOINT = os.environ["FLIGHT_API_ENDPOINT"]
FLIGHT_API_KEY = os.environ["FLIGHT_API_KEY"]


class FlightSearch:
    def search_flights(self, flight_params):
        url = f"{FLIGHT_API_ENDPOINT}/v2/search"
        headers = {
            "apikey": FLIGHT_API_KEY
        }
        res = req.get(url=url,
                      params=flight_params, headers=headers)
        res.raise_for_status()
        return res.json()["data"]
