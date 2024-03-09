import requests as req

SHEETY_API_ENDPOINT = "https://api.sheety.co/9bf8cf781d9f9676f8f8d29389c7b8af/flightDeals/users"
SHEETY_BEARER_TOKEN = "Bearer FlIgHt SeCrEtS"

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
    res = req.post(SHEETY_API_ENDPOINT, json=data, headers=headers)
    res.raise_for_status()
    print(res)
    print("You're in the club! :)")
else:
    print("Your emails do not match. Please try again.")
