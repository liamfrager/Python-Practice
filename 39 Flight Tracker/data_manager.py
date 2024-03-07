import requests as req

API_URL = "https://api.sheety.co/9bf8cf781d9f9676f8f8d29389c7b8af/flightDeals/prices"


class DataManager:

    def get_locations(self):
        res = req.get(API_URL)
        res.raise_for_status()
        return res.json()["prices"]
