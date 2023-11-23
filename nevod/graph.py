from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def gaussian(x, A, mu, sigma):
    return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
coincidences_coll = db['coincidences_1000']

# Агрегация для подсчета количества документов с одинаковым delta_time
pipeline = [
    {
        '$group': {
            '_id': '$delta_time',
            'count': {'$sum': 1}
        }
    }
]

result = list(coincidences_coll.aggregate(pipeline))
delta_times = [abs(doc['_id']) for doc in result]
counts = [doc['count'] for doc in result]

# Аппроксимация гистограммы
params, covariance = curve_fit(gaussian, delta_times, counts, p0=[max(counts), np.mean(delta_times), np.std(delta_times)])

# Найти параметры
A, mu, sigma = params

# Найти максимум аппроксимации
maximum_time = round(mu)

# Нарисовать гистограмму
plt.bar(delta_times, counts, align='center', alpha=0.5)
plt.xlabel('Время между событиями\ndelta_time = event_time - eas_event_time, нс', fontsize=20)
plt.ylabel('Число событий', fontsize=20)
plt.title('Гистограмма числа совместных событий', fontsize=24)

# Ограничение графика до 800 нс
plt.xlim(0, 800)

# Показать максимум
plt.vlines(maximum_time, 0, max(counts), color='blue', linestyle='--', label=f'Наиболее вероятная разница (delta_time={maximum_time})')
plt.legend(loc='upper right', fontsize=20)


plt.grid(True)
plt.show()
