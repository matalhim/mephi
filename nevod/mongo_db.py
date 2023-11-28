from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, host='localhost', port=27017, db_name='nevod'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]

    def disconnect(self):
        if self.client:
            self.client.close()


mongo_connection = MongoDBConnection()

mongo_connection.connect()
