from pymongo import MongoClient
import matplotlib.pyplot as plt

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

sorted_documents = list(db['coincidences'].find().sort('event_time_ns_coll', 1))

delta_numbers = []


for doc in sorted_documents:
    delta_number = doc['event_time_ns_coll'] - doc['eas_event_time_ns']
    delta_numbers.append(delta_number)

plt.scatter(range(len(delta_numbers)), delta_numbers, s=10)
plt.xlabel('Номер документа')
plt.ylabel('Delta Number (event_time_ns_coll - eas_event_time_ns)')
plt.title('Точечный график Delta Number от номера документа')
plt.grid(True)
plt.show()
