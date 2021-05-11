from pymongo import MongoClient
from dbConfig import *


class MongoDatabase:
    def __init__(self):
        url = 'mongodb+srv://{}:{}@{}.net/{}?retryWrites=true&w=majority'\
            .format(db_user, db_password, db_cluster, db_name)
        print(url)

        self.db = MongoClient(url)
        self.connect()

    def connect(self):
        print(self.db.list_databases())
        self.db.close()

MongoDatabase()