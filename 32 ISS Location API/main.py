import requests as req
from datetime import datetime
import smtplib
import time

# # KANYE QUOTES
# API_URL = "https://api.kanye.rest"

# res = req.get(API_URL)
# res.raise_for_status()
# print(res.json()['quote'])


SUNRISE_SUNSET_API_URL = "https://api.sunrise-sunset.org/json"
ISS_API_URL = "http://api.open-notify.org/iss-now.json"
LAT = 43.584290
LNG = -71.207748
MY_EMAIL = "liam.frager@gmail.com"
MY_PASSWORD = "ywssmwtppzrikwer"


def iss_is_overhead():
    res = req.get(ISS_API_URL)
    res.raise_for_status()
    data = res.json()
    ISS_LAT = float(data['iss_position']['latitude'])
    ISS_LNG = float(data['iss_position']['longitude'])
    return LAT - 5 <= ISS_LAT <= LAT + 5 and LNG - 5 <= ISS_LNG <= LNG + 5


def is_night():
    res = req.get(SUNRISE_SUNSET_API_URL, params={
        "lat": LAT,
        "lng": LNG,
        "formatted": 0
    })
    res.raise_for_status()
    data = res.json()['results']
    sunrise = data['sunrise'].split("T")[1].split("+")[0].split(":")
    sunrise_min = int(sunrise[0]) * 60 + int(sunrise[1])
    sunset = data['sunset'].split("T")[1].split("+")[0].split(":")
    sunset_min = int(sunset[0]) * 60 + int(sunset[1])
    now = datetime.now().hour * 60 + datetime.now().minute
    return now > sunset_min or now < sunrise_min


while True:
    time.sleep(60)
    if is_night() and iss_is_overhead():
        print('go outside!')
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject: The ISS is overhead!\n\nGo outside right now to see the International Space Station overhead!"
            )
        break
