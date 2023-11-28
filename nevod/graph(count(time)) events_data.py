import matplotlib.pyplot as plt
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Загрузка данных из коллекции events_data
events_data = db.events_data.find()

# Инициализация списка для хранения разницы времени
time_differences = []

# Обработка данных из events_data
for event_data in events_data:
    decor_time = event_data.get('decor_time', 0)
    eas_time = event_data.get('eas_time', 0)

    # Вычисление разницы между decor_time и eas_time
    time_difference = abs(decor_time - eas_time)
    time_differences.append(time_difference)

# Построение гистограммы
plt.hist(time_differences, bins=50, color='blue', edgecolor='black')
plt.title('Гистограмма разницы времени между decor_time и eas_time')
plt.xlabel('Разница времени (ns)')
plt.ylabel('Число событий')
plt.show()

# Закрытие соединения с MongoDB
client.close()
