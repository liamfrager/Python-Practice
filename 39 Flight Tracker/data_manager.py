import requests as req

# Sheety
API_URL_GET = "https://api.sheety.co/9bf8cf781d9f9676f8f8d29389c7b8af/flightDeals/prices"
API_URL_POST = "https://api.sheety.co/9bf8cf781d9f9676f8f8d29389c7b8af/flightDeals/prices"

# Tequila Kiwi
API_URL = "https://api.tequila.kiwi.com/v2/search"
API_KEY = "TzYyKDwitVMVvSAAB0yeRV7iMunxLex5"


class DataManager:

    # def update_iata_codes(self):
    #     res = req.get(API_URL_GET)
    #     res.raise_for_status()
    #     data = res.json()["prices"]
    #     cities = [x["city"] for x in data]
    #     for city in cities:

    #     # res = req.post(API_URL_POST, )

    # def get_iata_code(self, city_name):
    #     headers = {
    #         "apikey": API_KEY
    #     }
    #     params = {
    #         "term": city_name,
    #         "location_types": "city",
    #         "limit": 1,
    #     }
    #     res = req.get(API_URL, params=params, headers=headers)
    #     res.raise_for_status()
    #     print(res.json()["data"])

    def get_locations(self):
        res = req.get(API_URL_GET)
        res.raise_for_status()
        return res.json()["prices"]
