from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from mongo import MongoDatabase
import pandas as pd


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
        all = []
        for flat, offer_detail in zip(flat_locations, offer_items):
            location = flat.select('p.text-nowrap')[0].text.split(': ')[1]
            flat_details = offer_detail.findAll("ul", {"class": "params"})

            for details in flat_details:
                price = details.select('li.offer-item-price')[0].text.strip()
                if 'zł' in price:
                    price = price.split('zł')[0].replace(' ', '')
                    price_per_meter = details.select('li.hidden-xs.offer-item-price-per-m')[0].text.split('zł/m')[0].replace(' ', '')
                    area = details.select('li.hidden-xs.offer-item-area')[0].text.split('m')[0].replace(' ', '')
                    rooms = details.select('li.offer-item-rooms.hidden-xs')[0].text.split(' ')[0]

                    all.append({
                        "Krakow": location.replace('Kraków, ', ''),
                        "zł/m²": int(price_per_meter.replace(',', '.')),
                        "zł": float(price.replace(',', '.')),
                        "m²": float(area.replace(',', '.')),
                        "pokoje": int(rooms)
                    })

        df = pd.DataFrame(all)
        print(df)

    def run(self):
        self.getPageData()
        self.getFlatInfo()


scrapper = Scrapper()
scrapper.run()