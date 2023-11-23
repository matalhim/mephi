from pymongo import MongoClient
from datetime import datetime, timedelta

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Создание новой коллекции eas_events_data
eas_events_data_collection = db['eas_events_data']

# Получение данных из nevod_eas_events
nevod_eas_events_cursor = db['nevod_eas_events'].find()

# Для каждого документа в nevod_eas_events
for nevod_eas_event in nevod_eas_events_cursor:
    # Получение списка id из list_of_ids
    list_of_ids = nevod_eas_event.get('list_of_ids', [])

    # Формирование запроса для neas_db
    query = {'_id': {'$in': list_of_ids}}

    # Поиск соответствующих документов в neas_db
    neas_db_events = list(db['neas_db'].find(query))

    # Добавление данных в новую коллекцию
    eas_events_data = nevod_eas_event
    eas_events_data['data_list'] = neas_db_events
    eas_events_data_collection.insert_one(eas_events_data)

# Закрытие соединения
client.close()
