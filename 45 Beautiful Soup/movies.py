import requests as req
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

res = req.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

movies = [movie.getText()
          for movie in soup.find_all(name="h3", class_="title")][::-1]

with open("top_movies.txt", mode="w") as file:
    for movie in movies:
        file.write(f"{movie}\n")
