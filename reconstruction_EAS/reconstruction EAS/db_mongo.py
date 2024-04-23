import pymongo
def get_database_connection(database):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    return client[database]
