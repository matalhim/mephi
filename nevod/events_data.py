from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Загрузка данных из коллекций
coincidences_1000 = db.coincidences_1000.find()
decor_events_info = db.decor_events_info
eas_events_corners = db['eas_events_direction']

# Создание новой коллекции events_data
events_data = db['events']
events_data.delete_many({})

# Обработка данных из coincidences_1000
for coincidence in coincidences_1000:
    coll_file_id = coincidence['coll_file_id']
    event_file_id = coincidence['event_file_id']

    # Поиск соответствующей записи в decor_events_info
    decor_event_info = decor_events_info.find_one({'id_nevod_decor': coll_file_id})

    # Поиск соответствующей записи в eas_events_corners
    eas_events_corner = eas_events_corners.find_one({'_id': event_file_id})

    # Проверка наличия нужных записей
    if decor_event_info is not None and eas_events_corner is not None:
        # Создание новой записи для events_data
        new_event_data = {
            'eas_event_id': event_file_id,
            'decor_event_id': coll_file_id,
            'decor_time': decor_event_info['event_time_ns'],
            'eas_time': eas_events_corner['eas_event_time_ns'],
            'decor_Theta': decor_event_info['Theta'],
            'decor_Phi': decor_event_info['Phi'],
            'eas_event_direction': eas_events_corner['data_list']
        }

        # Запись в коллекцию events_data
        events_data.insert_one(new_event_data)

# Закрытие соединения с MongoDB
client.close()
