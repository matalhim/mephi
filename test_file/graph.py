import matplotlib.pyplot as plt
import numpy as np

# Заданные значения токов I1, I2, I3, I4 и I5
I1 = 1.9 + 1.9j
I2 = 0.3 - 0.4j
I3 = -0.1 - 1.1j
I4 = 1.5 + 0.9j
I5 = 0.7j

# Создание комплексной плоскости
fig, ax = plt.subplots()
ax.set_aspect('equal')

# Построение векторов
vectors = [I1, I2, I3, I4, I5]
colors = ['k', 'k', 'k', 'k', 'k']

for i in range(len(vectors)):
    ax.quiver(0, 0, vectors[i].real, vectors[i].imag, angles='xy', scale_units='xy', scale=1, color=colors[i])

# Добавление подписей к векторам
label_offset = 0.1  # Расстояние от конца вектора
for i, label in enumerate([r'$I_1$', r'$I_2$', r'$I_3$', r'$I_4$', r'$I_5$']):
    ax.text(vectors[i].real + label_offset, vectors[i].imag + label_offset, label, fontsize=12)

# Установка цен деления на осях
ax.set_xticks(np.arange(-2, 2.1, 0.1))
ax.set_yticks(np.arange(-2, 2.1, 0.1))

# Добавление подписей только для кратных 0.5
ax.set_xticklabels(['' if label != 0.5 * idx else str(label) for idx, label in enumerate(ax.get_xticks())])
ax.set_yticklabels(['' if label != 0.5 * idx else str(label) for idx, label in enumerate(ax.get_yticks())])

# Подписи к осям
ax.text(2.1, -0.1, '1', fontsize=12)
ax.text(-0.1, 2.1, '2', fontsize=12)

# Установка пределов осей
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.grid(True)

# Отображение векторной диаграммы
plt.show()