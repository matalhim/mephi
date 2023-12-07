from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Получение коллекций
decor_events_info_collection = db.decor_events_info
events_data_1_collection = db['events_data(1)']
not_events_decor_info_collection = db['not_events_decor_info_1']

# Очищаем коллекцию перед добавлением новых данных
not_events_decor_info_collection.delete_many({})

# Создаем агрегацию с использованием $lookup для соединения двух коллекций
pipeline = [
    {
        "$lookup": {
            "from": "events_data(1)",
            "localField": "id_nevod_decor",
            "foreignField": "decor_event_id",
            "as": "matched_docs"
        }
    },
    {
        "$match": {
            "matched_docs": {"$eq": []}  # Выбираем только те документы, у которых нет совпадений
        }
    },
    {
        "$project": {
            "matched_docs": 0  # Исключаем поле matched_docs из результирующих документов
        }
    }
]

# Выполняем агрегацию и добавляем результаты в новую коллекцию
not_events_decor_info_collection.insert_many(decor_events_info_collection.aggregate(pipeline))
