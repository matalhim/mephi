import numpy as np
import matplotlib.pyplot as plt

# Создаем массив значений x для x > 10
x1 = np.linspace(10.01, 30, 400)
y1 = np.cosh(x1 - 0.5 * np.log((x1 + 10) / (x1 - 10)))

# Создаем массив значений x для x < 10
x2 = np.linspace(-30, 9.99, 400)
y2 = np.cosh(x2 - 0.5 * np.log((x2 + 10) / (x2 - 10)))

# Строим графики
plt.figure(figsize=(12, 4))

plt.subplot(121)  # Первый график для x > 10
plt.plot(x1, y1)
plt.xlabel('x')
plt.ylabel('cosh(x - 1/2ln((x+10)/(x-10)))')
plt.title('График для x > 10')
plt.grid(True)

plt.subplot(122)  # Второй график для x < 10
plt.plot(x2, y2)
plt.xlabel('x')
plt.ylabel('cosh(x - 1/2ln((x+10)/(x-10)))')
plt.title('График для x < 10')
plt.grid(True)

plt.tight_layout()

# Отображаем графики
plt.show()
