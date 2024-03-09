import requests as req
import os as os
from dotenv import load_dotenv

load_dotenv()

SHEETY_API_ENDPOINT = os.environ["SHEETY_API_ENDPOINT"]
SHEETY_BEARER_TOKEN = os.environ["SHEETY_BEARER_TOKEN"]


class Users():

    def __init__(self):
        self.url = f"{SHEETY_API_ENDPOINT}/users"
        self.headers = {
            "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}",
            'Content-Type': 'application/json',
        }

    def sign_up(self):
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

        if email == email2:
            res = req.post(url=self.url, headers=self.headers, json=data)
            res.raise_for_status()
            print(res)
            print("You're in the club! :)")
        else:
            print("Your emails do not match. Please try again.")

    def get_users(self):
        res = req.get(url=self.url, headers=self.headers)
        res.raise_for_status()
        data = res.json()["users"]
        users = [u["email"] for u in data]
        return users


# Users().sign_up()
