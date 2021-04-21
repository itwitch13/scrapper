from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import pandas as pd

# URl to web scrap from.
# in this example we web scrap graphics cards from Newegg.com
page_url = "https://www.otodom.pl/sprzedaz/nowe-mieszkanie/krakow/?search%5Bregion_id%5D=6&search%5Bcity_id%5D=38"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

print(page_soup.h1)

# finds each product from the store page
offer_items = page_soup.findAll("div", {"class": "offer-item-details"})
flat_locations = page_soup.find_all("header", {"class": "offer-item-header"})

# flat_locations = offer_items.findAll("p", {"class": "text-nowrap"})
# flat_details = offer_items.findAll("ul", {"class": "params"})
for flat, offer_detail in zip(flat_locations, offer_items):
    location = flat.find_all("p", {"class": "text-nowrap"})
    flat_details = offer_detail.findAll("ul", {"class": "params"})
    prizes_m = []
    area = []
    rooms = []
    for details in flat_details:
        print(details)
        # prizes = details.find_ll("li", {"class": "offer-item-price"})
        prizes_m.append(details.find("li", {"class": "hidden-xs offer-item-price-per-m"}))
        area.append(details.find("li", {"class": "hidden-xs offer-item-area"}))
        rooms.append(details.find("li", {"class": "offer-item-rooms hidden-xs"}))
        # detail = [detail.text for detail in details]
        # print(prizes_m, area, rooms)

