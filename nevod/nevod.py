from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

delta_time = 1000
batch_size = 1000

time_range_stage = {
    '$addFields': {
        'start_range': {'$subtract': ['$event_time_ns', delta_time]},
        'end_range': {'$add': ['$event_time_ns', delta_time]}
    }
}

ё
coincidences_coll = db['coincidences_1000']

pipeline = [
    {
        '$group': {
            '_id': '$event_time_ns'
        }
    }
]
unique_event_time_ns_values = [doc['_id'] for doc in db['coll'].aggregate(pipeline)]

batches = [unique_event_time_ns_values[i:i+batch_size] for i in range(0, len(unique_event_time_ns_values), batch_size)]

for batch in batches:
    pipeline = [
        time_range_stage,
        {
            '$match': {
                'event_time_ns': {'$in': batch}
            }
        },
        {
            '$lookup': {
                'from': 'event',
                'let': {
                    'start_range': '$start_range',
                    'end_range': '$end_range'
                },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    { '$gte': ['$eas_event_time_ns', '$$start_range'] },
                                    { '$lte': ['$eas_event_time_ns', '$$end_range'] }
                                ]
                            }
                        }
                    }
                ],
                'as': 'event_matches'
            }
        }
    ]

    cursor = db['coll'].aggregate(pipeline)


    for doc in cursor:
        if doc['event_matches']:

            coincidence_doc = {
                'coll_file_id': doc['_id'],
                'event_file_id': doc['event_matches'][0]['_id'],
                'event_time_ns_coll': doc['event_time_ns'],
                'eas_event_time_ns': doc['event_matches'][0]['eas_event_time_ns'],
                'delta_time': doc['event_time_ns'] - doc['event_matches'][0]['eas_event_time_ns']
            }
            coincidences_coll.insert_one(coincidence_doc)

            print("Документ из coll:")
            print(doc)
            print("Совпадающие документы из event:")
            for match in doc['event_matches']:
                print(match)
            print("-------------------------------")

# Импортируется библиотека MongoClient из PyMongo, чтобы устанавливать соединение с MongoDB.
#
# Устанавливается соединение с базой данных MongoDB 'nevod'
#
# Задаются переменные delta_time и batch_size.
# delta_time определяет временной интервал, в пределах которого ищутся совпадения между документами,
# а batch_size определяет размер пакетов (пачек) уникальных значений 'event_time_ns' для обработки пакетами.
#
# Создается переменная time_range_stage, которая содержит оператор агрегации '$addFields' ($addFields: Добавление новых полей в документ).
# оператор добавляет два новых поля в документы: 'start_range' и 'end_range'.
# 'start_range' вычисляется как разница между 'event_time_ns' и delta_time,
# а 'end_range' - как сумма 'event_time_ns' и delta_time.
# Это позволяет создать временной диапазон для каждого документа.
#
# Создается коллекция 'coincidences1', в которую будут записываться найденные совпадения (в базе данных nevod).
#
# Затем создается пайплайн для агрегации данных. Первый этап пайплайна группирует документы по полю 'event_time_ns' с помощью оператора '$group' ( Группировка документов по заданным полям),
# чтобы найти уникальные значения 'event_time_ns'. Эти уникальные значения сохраняются в переменной unique_event_time_ns_values.
#
# Далее выполняется разделение уникальных значений 'event_time_ns' на пакеты размером batch_size. Это позволяет обрабатывать данные частями для уменьшения нагрузки на сервер MongoDB.
#
# Затем начинается итерация по каждому пакету значений 'event_time_ns'.
#
# Для каждого пакета строится новый пайплайн для агрегации данных. Пайплайн включает в себя:
#
# time_range_stage, чтобы определить временной диапазон для каждого документа.
# Оператор '$match', который фильтрует документы, у которых 'event_time_ns' входит в текущий пакет.
# Оператор '$lookup', который связывает текущий документ из коллекции 'coll' с документами из коллекции 'event' на основе временного диапазона.
# Выполняется агрегация сформированного пайплайна с использованием метода aggregate.
#
# Для каждого документа, найденного в результате агрегации, проверяется наличие совпадений в поле 'event_matches'.
#
# Если есть совпадения, то создается новый документ 'coincidence_doc' с данными о совпадении, и этот документ добавляется в коллекцию 'coincidences1'.
#
# Выводятся информация о текущем документе из коллекции 'coll' и совпадающих документах из коллекции 'event'.
#
# Процесс повторяется для каждого пакета уникальных значений 'event_time_ns'.