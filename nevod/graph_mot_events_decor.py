import matplotlib.pyplot as plt
from pymongo import MongoClient
from collections import Counter

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']

# Получение данных из коллекции not_events_decor_info
cursor = db.not_events_decor_info_1.find({}, {'Theta': 1, 'Phi': 1})
data = list(cursor)

# Закрытие соединения
client.close()

# Подготовка данных для построения диаграмм
theta_values = [round(entry['Theta']) for entry in data if 'Theta' in entry]
phi_values = [round(entry['Phi']) for entry in data if 'Phi' in entry]

# Подсчет числа файлов для каждого значения Theta и Phi
theta_counts = Counter(theta_values)
phi_counts = Counter(phi_values)

# Построение двух диаграмм на одной странице
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# График для Theta
ax1.bar(theta_counts.keys(), theta_counts.values(), color='blue')
ax1.set_xlabel('Зенитный угол Theta', fontsize=18)
ax1.set_ylabel('Число событий', fontsize=18)
ax1.set_title('Гистограмма числа событий от зенитного угла', fontsize=18)

# График для Phi
ax2.bar(phi_counts.keys(), phi_counts.values(), color='green')
ax2.set_xlabel('Phi', fontsize=18)
ax2.set_ylabel('Number of Files', fontsize=18)
ax2.set_title('Distribution of Phi in not_events_decor_info', fontsize=18)

# Регулировка расположения графиков
plt.tight_layout()

# Отображение обеих диаграмм
plt.show()
