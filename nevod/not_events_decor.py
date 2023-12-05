from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Создание коллекции not_events_decor_info
db.create_collection("not_events_decor_info")

# Выполнение запроса
pipeline = [
    {
        '$lookup': {
            'from': 'events_data',
            'localField': 'id_nevod_decor',
            'foreignField': 'decor_event_id',
            'as': 'matching_events'
        }
    },
    {
        '$match': {
            'matching_events': {'$eq': []}
        }
    },
    {
        '$project': {
            '_id': 1,
            'NRUN': 1,
            'NEvent': 1,
            'NtrackX': 1,
            'NtrackY': 1,
            'Ntrack': 1,
            'Theta': 1,
            'Phi': 1,
            'IdEv': 1,
            'Nview': 1,
            'id_nevod_decor': 1,
            'event_time_ns': 1
        }
    }
]

result = db.decor_events_info.aggregate(pipeline)

# Сохранение результатов в коллекцию not_events_decor_info
db.not_events_decor_info.insert_many(result)

# Закрытие соединения
client.close()
