from pymongo import MongoClient

def create_decor_events_info(db_name='nevod'):
    # Подключение к базе данных
    client = MongoClient('mongodb://localhost:27017')
    db = client[db_name]

    # Коллекция из 810-814 runs
    runs_collection = db['812 runs']

    # Коллекция nevod_decor
    nevod_decor_collection = db['nevod_decor']

    # Новая коллекция для хранения информации
    decor_events_info_collection = db['decor_events_info_812_1']

    # Очищаем коллекцию decor_events_info перед вставкой новых данных
    decor_events_info_collection.delete_many({})

    # Агрегационный запрос с фильтром по NRUN
    for record in runs_collection.find():
        matching_runs = nevod_decor_collection.find({'event_number': record['NEvent']})

        for matching_run in matching_runs:
            # Заменяем IdEv на значение из nevod_decor

            # Добавляем поля из nevod_decor
            matching_run['NEvent'] = record.get('NEvent')
            matching_run['NRUN'] = record.get('NRUN')
            matching_run['NtrackX'] = record.get('NtrackX')
            matching_run['NtrackY'] = record.get('NtrackY')
            matching_run['Theta'] = record.get('Theta')
            matching_run['Phi'] = record.get('Phi')
            matching_run['Phi'] = record.get('Phi')
            matching_run['Nview'] = record.get('Nview')


            # Вставляем документ с измененным IdEv и добавленными полями
            decor_events_info_collection.insert_one(matching_run)

    # Закрываем соединение
    client.close()

# Вызываем функцию для создания коллекции decor_events_info
create_decor_events_info()
