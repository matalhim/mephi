import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import Counter

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = db['events_data']

# Размерность массива eas_events_corners, которую вы хотите использовать в фильтре
min_dimension = 2

# Получаем углы alpha и median_alpha из каждого документа и округляем до целых
average_angles = [round(document['angle_alpha']) for document in collection.find(
    {'$expr': {'$gte': [{'$size': '$eas_events_corners'}, min_dimension]}}) if 'angle_alpha' in document]

median_angles = [round(document['median_alpha']) for document in collection.find(
    {'$expr': {'$gte': [{'$size': '$eas_events_corners'}, min_dimension]}}) if 'median_alpha' in document]

# Считаем количество вхождений каждого угла
average_angle_counts = Counter(average_angles)
median_angle_counts = Counter(median_angles)

# Создаем диаграммы
average_angles = list(average_angle_counts.keys())
average_counts = list(average_angle_counts.values())

median_angles = list(median_angle_counts.keys())
median_counts = list(median_angle_counts.values())

# Построение гистограмм для средних и медианных углов
plt.figure(figsize=(10, 6))

# Гистограмма для средних углов
plt.bar(average_angles, average_counts, align='center', color='blue', alpha=0.5, label='Среднее')

# Гистограмма для медианных углов
plt.bar(median_angles, median_counts, align='center', color='orange', alpha=0.5, label='Медиана')

# Вычисляем квантили для обоих наборов данных
q2_average = np.percentile(average_angles, 50)
q2_median = np.percentile(median_angles, 50)

q67_average = np.percentile(average_angles, 67)
q67_median = np.percentile(median_angles, 67)

# Добавляем вертикальные линии для квантилей
plt.axvline(x=q2_average, color='red', linestyle='--', label='Квантиль 50% (среднее)')
plt.axvline(x=q2_median, color='black', linestyle='--', label='Квантиль 50% (медиана)')

plt.axvline(x=q67_average, color='red', linestyle=':', label='Квантиль 67% (среднее)')
plt.axvline(x=q67_median, color='black', linestyle=':', label='Квантиль 67% (медиана)')

plt.xlabel('Пространственный угол alpha (градусы)', fontsize=18)
plt.ylabel('Число событий', fontsize=18)
plt.title('Гистограмма числа совместных событий от пространственного угла', fontsize=18)
plt.legend(fontsize=12)

# Показать гистограмму
plt.show()

# Вывод квантилей
print(f"Квантиль 50% (среднее): {q2_average}")
print(f"Квантиль 50% (медиана): {q2_median}")
print(f"Квантиль 67% (среднее): {q67_average}")
print(f"Квантиль 67% (медиана): {q67_median}")