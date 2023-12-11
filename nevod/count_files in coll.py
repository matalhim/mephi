from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = db['coincidences_1000']

# Получение числа документов в коллекции
num_documents = collection.count_documents({})

print(f"Число документов в коллекции: {num_documents}")
