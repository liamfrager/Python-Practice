import requests as req
import json
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup

listings = []
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
result_count = int(soup.select_one('.result-count').getText().split()[0])
results_per_page = 40

for page in range(result_count // results_per_page + 1):
    url = 'https://www.zillow.com/async-create-search-page-state'
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": FILTERED_ZILLOW_URL
    }
    body = {
        "searchQueryState": {
            "pagination": {
                "currentPage": page + 1
            },
            "isMapVisible": True,
            "mapBounds": {
                "west": -73.56813354320504,
                "east": -70.88197631664254,
                "south": 43.389321957717485,
                "north": 44.312293759349835
            },
            "regionSelection": [
                {
                    "regionId": 1539,
                    "regionType": 4
                }
            ],
            "filterState": {
                "sortSelection": {
                    "value": "pricea"
                },
                "isCondo": {
                    "value": False
                },
                "isLotLand": {
                    "value": False
                },
                "isAllHomes": {
                    "value": True
                },
                "isApartment": {
                    "value": False
                },
                "isManufactured": {
                    "value": False
                },
                "isApartmentOrCondo": {
                    "value": False
                }
            },
            "isListVisible": True
        },
        "wants": {
            "cat1": ["listResults"],
            "cat2": ["total"]
        },
        "requestId": 2
    }
    res = req.put(
        url=url,
        headers=headers,
        data=json.dumps(body)
    )

    data = json.loads(res.content.decode('utf-8')
                      )['cat1']['searchResults']['listResults']

    for listing in data:
        listing = {
            'address': listing['address'] if 'address' in listing else None,
            'link': listing['detailUrl'] if 'detailUrl' in listing else None,
            'beds': listing['beds'] if 'beds' in listing else None,
            'baths': listing['baths'] if 'baths' in listing else None,
            'sqft': listing['area'] if 'area' in listing else None,
            'price': listing['unformattedPrice'] if 'unformattedPrice' in listing else None,
        }
        listings.append(listing)

listings = pd.DataFrame(listings)

listings.to_csv(f'Zillow-Homes-{date.today()}.csv')
