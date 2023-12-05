from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = db['events_data']

def calculate_average(lst, key):
    return sum(item[key] for item in lst) / len(lst) if len(lst) > 0 else 0

for document in collection.find():
    average_theta = calculate_average(document["eas_events_corners"], "theta")
    average_phi = calculate_average(document["eas_events_corners"], "phi")

    collection.update_one(
        {"_id": document["_id"]},
        {
            "$set": {
                "average_eas_theta": average_theta,
                "average_eas_phi": average_phi
            }
        }
    )

client.close()
