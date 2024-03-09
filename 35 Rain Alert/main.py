import requests as req

API_URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = "28a5cc9e3d8ce301ee048245f6c9a280"
API_PARAMS = {
    "lat": 43.584290,
    "lon": -71.207748,
    "cnt": 4,
    "appid": API_KEY
}

res = req.get(API_URL, params=API_PARAMS)
res.raise_for_status()
data = res.json()
codes = [
    forecast['weather'][0]['id']
    for forecast in data['list']
    if forecast['weather'][0]['id'] < 600
]
if len(codes) > 0:
    print("It's going to rain!")
else:
    print("No rain today.")
