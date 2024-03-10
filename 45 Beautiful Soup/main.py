import requests as req
import operator
from bs4 import BeautifulSoup

res = req.get("https://news.ycombinator.com/")
html = res.text

soup = BeautifulSoup(html, "html.parser")

tags = soup.select(".titleline a")
titles = []
links = []
i = 0
while i < len(tags):
    titles.append(tags[i].getText())
    links.append(tags[i].get("href"))
    i += 2

points = soup.select(".subtext")
points = [
    0 if
    point.find(class_="score") is None else
    int(point.find(class_="score").getText().split()[0]) for point in points
]
articles = []
for i in range(i // 2):
    articles.append({
        "title": titles[i],
        "link": links[i],
        "points": points[i],
    }
    )

x = max(articles, key=lambda a: a["points"])
print(x)
