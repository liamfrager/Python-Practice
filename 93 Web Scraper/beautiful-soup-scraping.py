from bs4 import BeautifulSoup
import requests as req
from datetime import date
import pandas as pd

FILTERED_ZILLOW_URL = 'https://www.zillow.com/belknap-county-nh/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-72.11738030664063%2C%22east%22%3A-70.77430169335938%2C%22south%22%3A43.093159751955696%2C%22north%22%3A43.95446692684302%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A1539%2C%22regionType%22%3A4%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22pricea%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'

res = req.get(
    url=FILTERED_ZILLOW_URL,
    headers={
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
)
zillow_page = res.content

soup = BeautifulSoup(zillow_page, "html.parser")

data = soup.select('#grid-search-results ul li .property-card-data')

listings = []
for listing in data:
    price = listing.select_one(
        'span', {'data-test': 'property-card-price'}).getText().replace('$', '').replace(',', '')
    link = listing.select_one(
        'a', {'data-test': 'property-card-link'})['href']
    address = listing.select_one(
        'address', {'data-test': 'property-card-addr'}).getText()
    beds, baths, sqft = [0 if item.getText(
    ) == '--' else item.getText().replace(',', '') for item in listing.select('ul li b')]
    listing = {
        'address': address,
        'link': link,
        'beds': beds,
        'baths': baths,
        'sqft': sqft,
        'price': price
    }
    listings.append(listing)

listings = pd.DataFrame(listings)

listings.to_csv(f'{date.today()}-homes.csv')
