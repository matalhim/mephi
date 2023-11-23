from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Получение коллекций
nevod_eas = db['nevod_eas']
coincidences_1000 = db['coincidences_1000']
nevod_eas_events = db['nevod_eas_events']

# Получение списка event_file_id из coincidences_1000
event_file_ids = coincidences_1000.distinct('event_file_id')

# Фильтрация и запись данных из nevod_eas в новую коллекцию
for event_file_id in event_file_ids:
    eas_event = nevod_eas.find_one({'_id': event_file_id})
    if eas_event:
        nevod_eas_events.insert_one(eas_event)

# Закрытие соединения
client.close()
