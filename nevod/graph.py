from pymongo import MongoClient
import matplotlib.pyplot as plt

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
coincidences_coll = db['coincidences_1000']

# Агрегация для подсчета количества документов с одинаковым delta_time
pipeline = [
    {
        '$group': {
            '_id': '$delta_time',
            'count': {'$sum': 1}
        }
    }
]

result = list(coincidences_coll.aggregate(pipeline))
delta_times = [abs(doc['_id']) for doc in result]
counts = [doc['count'] for doc in result]

plt.bar(delta_times, counts)
plt.xlabel('Delta Time (event_time_ns_coll - eas_event_time_ns)')
plt.ylabel('Число файлов')
plt.title('График числа файлов по Delta Time')
plt.grid(True)
plt.show()
