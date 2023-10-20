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

# Округление максимума до целых
maximum_index = np.argmax(gaussian(delta_times, A, mu, sigma))
maximum_time = round(delta_times[maximum_index])

# Нарисовать аппроксимацию
x = np.linspace(min(delta_times), max(delta_times), 1000)
y = gaussian(x, A, mu, sigma)
plt.plot(x, y, 'r', label='Аппроксимация')

maximum_value = y[maximum_index]
plt.vlines(delta_times[maximum_index], 0, maximum_value, color='blue', linestyle='--', label=f'Максимум (delta_time={maximum_time})')

# Нарисовать график гистограммы
plt.bar(delta_times, counts, align='center', alpha=0.5)
plt.xlabel('Delta Time (event_time_ns_coll - eas_event_time_ns)')
plt.ylabel('Число файлов')
plt.title('Гистограмма числа файлов по Delta Time')

plt.legend(loc='upper right')

plt.grid(True)
plt.show()
