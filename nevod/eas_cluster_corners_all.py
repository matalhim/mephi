from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Коллекция eas_events_data
eas_events_data = db['eas_events_data(1)']

# Новая коллекция
eas_events_corners = db['eas_events_corners(1)']

# Получение данных из eas_events_data
eas_events_data_cursor = eas_events_data.find()

# Для каждого документа в eas_events_data
for eas_event_data in eas_events_data_cursor:
    # Создание нового документа для новой коллекции
    new_document = {
        '_id': eas_event_data['_id'],
        'eas_event_time_ns': eas_event_data.get('eas_event_time_ns'),
        'data_list': [
            {
                'cluster': obj.get('cluster'),
                'direction': {
                    'theta': obj.get('direction', {}).get('theta', None),
                    'phi': obj.get('direction', {}).get('phi', None),
                }
            }
            for obj in eas_event_data.get('data_list', [])
        ]
    }

    # Вставка нового документа в новую коллекцию
    eas_events_corners.insert_one(new_document)

# Закрытие соединения
client.close()
