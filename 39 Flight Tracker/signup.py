import requests as req
import os as os
from dotenv import load_dotenv

load_dotenv()

SHEETY_API_ENDPOINT = os.environ["SHEETY_API_ENDPOINT"]
SHEETY_BEARER_TOKEN = os.environ["SHEETY_BEARER_TOKEN"]

print("Welcome to Liam's Flight Club!")
print("We find the best flight deals and email you.")
f_name = input("What's your first name? ")
l_name = input("What's your last name? ")
email = input("What is your email? ")
email2 = input("Type your email again. ")

data = {
    "user": {
        "firstName": f_name,
        "lastName": l_name,
        "email": email,
    }
}
headers = {
    "Authorization": SHEETY_BEARER_TOKEN
}

if email == email2:
    res = req.post(f"{SHEETY_API_ENDPOINT}/users", json=data, headers=headers)
    res.raise_for_status()
    print(res)
    print("You're in the club! :)")
else:
    print("Your emails do not match. Please try again.")
