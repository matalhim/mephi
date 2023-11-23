from pymongo import MongoClient
import pandas as pd
import os

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Коллекция eas_events_corners
eas_events_corners_collection = db['eas_events_corners']

# Получение данных из eas_events_corners
eas_events_corners_cursor = eas_events_corners_collection.find()

# Создание списка для данных
data_list = []

# Для каждого документа в eas_events_corners
for eas_event_corners in eas_events_corners_cursor:
    # Получение _id
    _id = eas_event_corners['_id']

    # Для каждого объекта в data_list
    for obj in eas_event_corners.get('data_list', []):
        # Получение cluster, theta и phi
        cluster = obj.get('cluster')
        theta = obj.get('theta')
        phi = obj.get('phi')

        # Добавление значений в список
        data_list.append((_id, cluster, theta, phi))

# Создание DataFrame с использованием pandas
df = pd.DataFrame(data_list, columns=['id', 'cluster', 'theta', 'phi'])

# Проверка и создание директории
output_directory = r'D:\МИФИ\нирс'
os.makedirs(output_directory, exist_ok=True)

# Сохранение DataFrame в файл Excel
output_path = os.path.join(output_directory, 'clusters_table.xlsx')
df.to_excel(output_path, index=False, engine='openpyxl')

# Закрытие соединения
client.close()
