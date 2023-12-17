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
    time_difference = decor_time - eas_time
    time_differences.append(time_difference)

# Построение гистограммы
plt.hist(time_differences, bins=50, color='blue', edgecolor='black')
plt.title('Гистограмма числа совместных событий', fontsize=18)  # Set title font size
plt.xlabel('Время между событиями: decor_time - eas_time', fontsize=18)  # Set x-axis label font size
plt.ylabel('Число событий', fontsize=18)  # Set y-axis label font size
plt.xticks(fontsize=12)  # Set x-axis tick font size
plt.yticks(fontsize=12)  # Set y-axis tick font size
plt.show()

# Закрытие соединения с MongoDB
client.close()
