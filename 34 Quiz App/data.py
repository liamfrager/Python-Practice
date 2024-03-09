import requests as req

API_URL = "https://opentdb.com/api.php"
PARAMS = {
    "amount": 10,
    "category": 9,
    "type": "boolean",
}
res = req.get(API_URL, params=PARAMS)
question_data = res.json()["results"]
