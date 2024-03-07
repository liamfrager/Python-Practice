import requests as req

API_URL = "https://api.tequila.kiwi.com/v2/search"
API_KEY = "TzYyKDwitVMVvSAAB0yeRV7iMunxLex5"


class FlightSearch:
    def search_flights(self, flight_params):
        headers = {
            "apikey": API_KEY
        }
        res = req.get(API_URL, params=flight_params, headers=headers)
        res.raise_for_status()
        return res.json()["data"]
