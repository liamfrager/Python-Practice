import requests as req
from bs4 import BeautifulSoup

date = input("What year would you like to travel to?")
date = "2011-12-04"

url = f"https://www.billboard.com/charts/hot-100/{date}/"

res = req.get(url)
soup = BeautifulSoup(res.text, "html.parser")

songs = soup.select(
    "li ul li h3#title-of-a-story")
songs = [song.getText().strip() for song in songs]

print(songs)
