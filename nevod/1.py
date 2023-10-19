import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit

# Чтение данных из файла
data = pd.read_table(r"D:\test_python\data\1.dat")
parameter = data['A_2']

# Определение функции Гаусса
def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-((x - mean) / 4 / stddev) ** 2)

# Инициализация начальных параметров для аппроксимации
binwidth = 1
y, x, _ = plt.hist(parameter, bins=np.arange(min(parameter), max(parameter)+binwidth, binwidth), edgecolor="k", color="r")
params, _ = curve_fit(gaussian, x[:-1], y, p0=[100, 20, 5])

# Генерация значений для кривой Гаусса
x_range = np.linspace(20, max(parameter), 100)
y_gaussian = gaussian(x_range, *params)

# Построение гистограммы
plt.hist(parameter, bins=np.arange(min(parameter), max(parameter) + binwidth, binwidth), edgecolor="blue", color="black")
plt.grid()
plt.xlabel('q, pc')
plt.ylabel('N')
plt.title('N(Q)')

# Построение кривой Гаусса
plt.plot(x_range, y_gaussian, 'r-', label='Gaussian Fit')
plt.legend()

# Отображение пика Гауссиана и его значение
meon_peak = params[1]
plt.vlines(meon_peak, 0, max(y_gaussian), color='red', linestyle='--')
plt.text(100, 40, f'mean_peak = {meon_peak}')

# Отображение графика
plt.show()
