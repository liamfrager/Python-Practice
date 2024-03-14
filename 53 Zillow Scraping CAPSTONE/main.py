from bs4 import BeautifulSoup
import requests as req
import pandas as pd

ZILLOW = "https://appbrewery.github.io/Zillow-Clone/"
res = req.get(ZILLOW)


soup = BeautifulSoup(res.text, "html.parser")

listings = soup.select(".StyledPropertyCardDataWrapper")
listings = [
    {
        "address": listing.select_one("address").getText().replace(" | ", "").strip(),
        "rent": int(listing.select_one(".PropertyCardWrapper__StyledPriceLine").getText().replace("/mo", "").split("+")[0].replace(",", "")[1:]),
        "link": listing.select_one("a")['href'],
    }
    for listing in listings
]

listings = pd.DataFrame(listings)

listings.to_csv('sf-ca-for-rent.csv')

print(listings)
