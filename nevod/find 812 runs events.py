from pymongo import MongoClient

def create_decor_events_info(db_name='nevod'):
    # Подключение к базе данных
    client = MongoClient('mongodb://localhost:27017')
    db = client[db_name]

    # Коллекция из 810-814 runs
    runs_collection = db['810-814 runs']

    # Коллекция nevod_decor
    nevod_decor_collection = db['nevod_decor']

    # Новая коллекция для хранения информации
    decor_events_info_collection = db['decor_events_info']

    # Очищаем коллекцию decor_events_info перед вставкой новых данных
    decor_events_info_collection.delete_many({})

    # Агрегационный запрос
    for record in nevod_decor_collection.find():
        matching_runs = runs_collection.find({'NEvent': record['event_number']})

        for matching_run in matching_runs:
            # Заменяем IdEv на значение из nevod_decor
            matching_run['IdEv'] = record.get('IdEv', None)

            # Добавляем поля из nevod_decor
            matching_run['id_nevod_decor'] = record['_id']
            matching_run['event_time_ns'] = record.get('event_time_ns', None)

            # Вставляем документ с измененным IdEv и добавленными полями
            decor_events_info_collection.insert_one(matching_run)

    # Закрываем соединение
    client.close()

# Вызываем функцию для создания коллекции decor_events_info
create_decor_events_info()
