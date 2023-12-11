import math
from pymongo import MongoClient

def angle_between_vectors(theta1, phi1, theta2, phi2):
    # Преобразуем углы из градусов в радианы
    theta1_rad = math.radians(theta1)
    phi1_rad = math.radians(phi1)
    theta2_rad = math.radians(theta2)
    phi2_rad = math.radians(phi2)

    # Вычисляем косинус угла между векторами
    cos_angle = math.sin(theta1_rad) * math.sin(theta2_rad) * math.cos(phi1_rad - phi2_rad) + math.cos(theta1_rad) * math.cos(theta2_rad)

    # Используем обратный косинус для получения угла в радианах
    angle_rad = math.acos(cos_angle)

    # Преобразуем угол обратно в градусы
    angle_deg = math.degrees(angle_rad)

    return angle_deg

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = db['events_data']

# Получаем все документы из коллекции
documents = collection.find()

# Обновляем каждый документ в коллекции
for document in documents:
    theta1 = document['decor_Theta']
    phi1 = document['decor_Phi']
    theta2 = document['average_eas_theta']
    phi2 = document['average_eas_phi']

    # Вычисляем угол между векторами
    alpha = angle_between_vectors(theta1, phi1, theta2, phi2)

    # Записываем результат в новое поле "angle_alpha" для каждого документа
    collection.update_one({"_id": document["_id"]}, {"$set": {"angle_alpha": alpha}})

print("Углы успешно вычислены и записаны в коллекцию.")
