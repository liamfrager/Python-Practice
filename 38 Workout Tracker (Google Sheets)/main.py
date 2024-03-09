import requests as req
import datetime as dt
import os as os
from dotenv import load_dotenv

load_dotenv()

NUTRITIONIX_APP_ID = os.environ["NUTRITIONIX_APP_ID"]
NUTRITIONIX_API_KEY = os.environ["NUTRITIONIX_API_KEY"]
NUTRITIONIX_API_URL = os.environ["NUTRITIONIX_API_URL"]
SHEETY_API_URL = os.environ["SHEETY_API_URL"]
SHEETY_BEARER_TOKEN = os.environ["SHEETY_BEARER_TOKEN"]

nutritionix_headers = {
    'Content-Type': 'application/json',
    'x-app-id': NUTRITIONIX_APP_ID,
    'x-app-key': NUTRITIONIX_API_KEY
}

nutritionix_body = {
    "query": input("What did you do for your workout?: "),
    "gender": "male",
    "age": 23,
}

res = req.post(url=NUTRITIONIX_API_URL,
               headers=nutritionix_headers, json=nutritionix_body)
res.raise_for_status()
data = res.json()

now = dt.datetime.now()

for exercise in data["exercises"]:
    sheety_body = {
        "workout": {
            "date": now.strftime("%b %d, %Y"),
            "time": now.strftime("%I:%M %p"),
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheety_headers = {
        "Authorization": SHEETY_BEARER_TOKEN
    }

try:
    res = req.post(url=SHEETY_API_URL,
                   headers=sheety_headers, json=sheety_body)
    res.raise_for_status()
except:
    print("Error: Could not update spreadsheet.")
else:
    print("Your spreadsheet has been updated!")
