from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

delta_time = 300

sorted_documents = list(db['coincidences'].find({
    '$where': f"Math.abs(this.event_time_ns_coll - this.eas_event_time_ns) > {delta_time}"
}).sort('event_time_ns_coll', 1))

for doc in sorted_documents:
    print("Документ:")
    print(doc)
