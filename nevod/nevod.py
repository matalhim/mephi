from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

delta_time = 300
batch_size = 1000

time_range_stage = {
    '$addFields': {
        'start_range': {'$subtract': ['$event_time_ns', delta_time]},
        'end_range': {'$add': ['$event_time_ns', delta_time]}
    }
}


coincidences_coll = db['coincidences']

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
                'event_file_id': doc['event_matches'][0]['_id'],  # Первое совпадение
                'event_time_ns_coll': doc['event_time_ns'],
                'eas_event_time_ns': doc['event_matches'][0]['eas_event_time_ns']  # Первое совпадение
            }
            coincidences_coll.insert_one(coincidence_doc)

            print("Документ из coll:")
            print(doc)
            print("Совпадающие документы из event:")
            for match in doc['event_matches']:
                print(match)
            print("-------------------------------")
