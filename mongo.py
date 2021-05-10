from pymongo import MongoClient
from dbConfig import *


class MongoDatabase:
    def __init__(self):
        url = "mongodb+srv://{}:{}@{}.net/{}?retryWrites=true&w=majority"\
            .format(db_user, db_password, db_cluster, db_name)
        self.db = MongoClient(db_name, host=url)

    def connect(self):
        pass
