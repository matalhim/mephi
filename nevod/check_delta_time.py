from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = "coincidences_1000"

delta_time = 500

sorted_documents = list(db[collection].find({
    '$where': f"Math.abs(this.event_time_ns_coll - this.eas_event_time_ns) > {delta_time}"
}).sort('event_time_ns_coll', 1))

# for doc in sorted_documents:
#     print("Документ:")
#     print(doc)
print(len(sorted_documents))
