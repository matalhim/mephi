from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Коллекция eas_events_data
eas_events_data_collection = db['eas_events_data']

# Фильтр
query = {
    'data_list': {'$exists': True, '$not': {'$size': 0}},
}

# Находим документы, соответствующие условиям
filtered_data = eas_events_data_collection.find(query)

# Обновляем документы, удаляя объекты из списка data_list без direction или неопределенным углом theta
for document in filtered_data:
    new_data_list = [obj for obj in document['data_list'] if (obj.get('direction') and obj.get('direction', {}).get('theta')) is not None]

    # Обновляем документ в коллекции
    eas_events_data_collection.update_one(
        {'_id': document['_id']},
        {'$set': {'data_list': new_data_list}}
    )
# удаление документов с путсым data_list
eas_events_data_collection.delete_many({'data_list': {'$exists': True, '$size': 0}})
client.close()
