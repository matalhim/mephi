import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import Counter

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = db['events_data']

# Размерность массива eas_events_corners, которую вы хотите использовать в фильтре
min_dimension = 5

# Получаем углы alpha из каждого документа и округляем до целых
angles = [round(document['angle_alpha']) for document in collection.find({'$expr': {'$gte': [{'$size': '$eas_events_corners'}, min_dimension]}}) if 'angle_alpha' in document]

# Считаем количество вхождений каждого угла
angle_counts = Counter(angles)

# Создаем диаграмму
angles = list(angle_counts.keys())
counts = list(angle_counts.values())

# Построение гистограммы
plt.bar(angles, counts, align='center')
plt.xlabel('Угол Alpha (градусы)')
plt.ylabel('Число файлов')
plt.title('Диаграмма угла Alpha от числа файлов')

# Вычисляем квантиль Q2 (медиана)
q2 = np.percentile(angles, 50)

# Вычисляем квантиль, до которого лежит 67% данных
q67 = np.percentile(angles, 67)

print(f"Медиана (Q2): {q2}")
print(f"Квантиль 67%: {q67}")
# Добавление вертикальной линии в точке q67
plt.axvline(x=q67, color='red', linestyle='--', label='Квантиль 67%\nугол alpha = {})'.format(round(q67, 2)))

# Вывод легенды
plt.legend()

# Показать гистограмму
plt.show()

print(f"Медиана (Q2): {q2}")
print(f"Квантиль 67%: {q67}")
