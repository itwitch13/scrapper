from pymongo import MongoClient
from dbConfig import *
import json


class MongoDatabase:
    def __init__(self):
        self.start_mongo_cloud()
        self.start_mongo_local()

    def start_mongo_cloud(self):
        url = 'mongodb+srv://{}:{}@{}.net/{}?retryWrites=true&w=majority' \
            .format(db_user, db_password, db_cluster, db_name)
        self.client_cloud = MongoClient(url)
        self.db_cloud = self.client_cloud[db_name]

    def start_mongo_local(self):
        self.client_local = MongoClient('localhost', 27017)
        self.db_local = self.client_local[db_name]

    def upload_dataframe_to_cloud(self, df_data):
        print("upload data to mongo cloud")
        collection = self.db_cloud[db_collection]
        records = json.loads(df_data.T.to_json()).values()
        collection.insert_many(records)

        self.client_cloud.close()

    def upload_dataframe_to_local(self, df_data):
        print("upload data to mongo local")
        collection = self.db_local[db_collection]
        records = json.loads(df_data.T.to_json()).values()
        collection.insert_many(records)
        # self.db_local.db_collection.insert_many(df_data.to_dict('records'))

        self.client_local.close()
