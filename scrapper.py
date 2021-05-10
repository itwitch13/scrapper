from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from mongo import MongoDatabase


class Scrapper:
    def __init__(self):
        self.page_url = "https://www.otodom.pl/sprzedaz/nowe-mieszkanie/krakow/?search%5Bregion_id%5D=6&search%5Bcity_id%5D=38"
        self.data_page = []

    def prepareMongo(self):
        self.db = MongoDatabase()

    def getPageData(self):
        client = uReq(self.page_url)
        self.data_page = soup(client.read(), "html.parser")
        client.close()

    def getFlatInfo(self):
        offer_items = self.data_page.findAll("div", {"class": "offer-item-details"})
        flat_locations = self.data_page.find_all("header", {"class": "offer-item-header"})

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

    def run(self):
        self.getPageData()
        self.getFlatInfo()


scrapper = Scrapper()
scrapper.run()