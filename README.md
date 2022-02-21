# Scrapper - "Analysis of flat prices in Cracow"

The application downloads data from the website www.otodom.pl on the basis of web scrapping, then the most important information about housing offers is captured and saved in the local database (MongoDB) and in the database located within the MongoDB cloud.

- Periodic / on-demand download data
- Generating statistics of flat prices/area/localization

The application has been fully implemented in Python with the use of available libraries: Pandas, BeautifulSoup, MongoClient, Datetime etc.
