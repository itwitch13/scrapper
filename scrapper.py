import csv
import pandas as pd

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from mongo import MongoDatabase


class Scrapper:
    def __init__(self):
        self.data_page = []
        self.all_info = []
        self.db = MongoDatabase()

    def get_page_number(self):
        page_number = 1
        self.get_page_data(page_number)
        pages = self.data_page.findAll("ul", {"class": "pager"})

        for page in pages:
            page_number = int(page.select('li')[-2].text.strip())

        return page_number

    def get_page_data(self, page_number):
        # mieszkania w Krakowie od 30m²
        self.number_page_url = 'https://www.otodom.pl/sprzedaz/nowe-mieszkanie/krakow/?search%5Bfilter_float_m%3Afrom%5D=30&search%5Bregion_id%5D=6&search%5Bcity_id%5D=38&nrAdsPerPage=72&page={}'.format(page_number)
        # mieszkania w Krakowie od 30-50m², 2-3 pokoi, max 8.500zł/m²
        self.page_url = 'https://www.otodom.pl/sprzedaz/nowe-mieszkanie/krakow/?search%5Bfilter_float_price_per_m%3Ato%5D=8500&search%5Bfilter_float_m%3Afrom%5D=35&search%5Bfilter_float_m%3Ato%5D=50&search%5Bfilter_enum_rooms_num%5D%5B0%5D=2&search%5Bfilter_enum_rooms_num%5D%5B1%5D=3&search%5Bregion_id%5D=6&search%5Bcity_id%5D=38&nrAdsPerPage=72&page={}'.format(page_number)
        client = uReq(self.page_url)
        self.data_page = soup(client.read(), "html.parser")
        client.close()

    def get_flat_info(self):
        offer_items = self.data_page.findAll("div", {"class": "offer-item-details"})
        flat_locations = self.data_page.find_all("header", {"class": "offer-item-header"})

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

                    self.all_info.append({
                        "Krakow": location.replace('Kraków, ', ''),
                        "zł/m²": int(price_per_meter.replace(',', '.')),
                        "zł": float(price.replace(',', '.')),
                        "m²": float(area.replace(',', '.')),
                        "pokoje": int(rooms)
                    })

    def run(self):
        page_numbers = self.get_page_number()

        for page in range(1, page_numbers):
            self.get_page_data(page)
            self.get_flat_info()

        df = pd.DataFrame(self.all_info)
        self.db.upload_dataframe(df)

        headers = self.all_info[0].keys()
        with open('./flat_info.csv', 'w', newline='') as output_file:
            all_info_file = csv.DictWriter(output_file, headers)
            all_info_file.writeheader()
            all_info_file.writerows(self.all_info)



scrapper = Scrapper()
scrapper.run()