from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['nevod']
collection = db['events']


for document in collection.find({}):
    for direction in document.get('eas_event_direction', []):
        for station_key in list(direction.get('stations', {})):
            if direction['stations'][station_key].get('a_std') is None:
                del direction['stations'][station_key]
    collection.update_one({'_id': document['_id']}, {'$set': {'eas_event_direction': document['eas_event_direction']}})

client.close()