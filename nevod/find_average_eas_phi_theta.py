from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = db['events_data']

def calculate_average(lst, key):
    return sum(item[key] for item in lst) / len(lst) if len(lst) > 0 else 0

def calculate_median(lst, key):
    sorted_values = sorted(item[key] for item in lst)
    length = len(sorted_values)
    if length % 2 == 0:  # Если количество элементов четное
        return (sorted_values[length // 2 - 1] + sorted_values[length // 2]) / 2
    else:  # Если количество элементов нечетное
        return sorted_values[length // 2]

for document in collection.find():
    average_theta = calculate_average(document["eas_events_corners"], "theta")
    average_phi = calculate_average(document["eas_events_corners"], "phi")
    median_theta = calculate_median(document["eas_events_corners"], "theta")
    median_phi = calculate_median(document["eas_events_corners"], "phi")

    collection.update_one(
        {"_id": document["_id"]},
        {
            "$set": {
                "average_eas_theta": average_theta,
                "average_eas_phi": average_phi,
                "median_eas_theta": median_theta,
                "median_eas_phi": median_phi
            }
        }
    )

client.close()