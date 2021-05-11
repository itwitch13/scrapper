from pymongo import MongoClient
from dbConfig import *
import json


class MongoDatabase:
    def __init__(self):
        url = 'mongodb+srv://{}:{}@{}.net/{}?retryWrites=true&w=majority'\
            .format(db_user, db_password, db_cluster, db_name)
        self.client = MongoClient(url)
        self.db = self.client[db_name]

    def upload_dataframe(self, df_data):
        collection = self.db[db_collection]

        records = json.loads(df_data.T.to_json()).values()
        collection.insert_many(records)

        self.client.close()
