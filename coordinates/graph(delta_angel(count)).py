import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('angeles_data.csv')
calculate_theta = np.array(data['calculate_theta'].values)
calculate_phi = np.array(data['calculate_phi'].values)

exp_theta = np.array(data['exp_theta'].values)
exp_phi = np.array(data['exp_phi'].values)

def angle_between_vectors(theta1, phi1, theta2, phi2):
    # Преобразуем углы из градусов в радианы
    theta1_rad = np.radians(theta1)
    phi1_rad = np.radians(phi1)
    theta2_rad = np.radians(theta2)
    phi2_rad = np.radians(phi2)

    # Вычисляем косинус угла между векторами
    cos_angle = np.sin(theta1_rad) * np.sin(theta2_rad) * np.cos(phi1_rad - phi2_rad) + np.cos(theta1_rad) * np.cos(theta2_rad)

    # Используем обратный косинус для получения угла в радианах
    angle_rad = np.arccos(cos_angle)

    # Преобразуем угол обратно в градусы
    angle_deg = np.degrees(angle_rad)

    return angle_deg

angles = angle_between_vectors(calculate_theta, calculate_phi, exp_theta, exp_phi)
data['angles'] = angles
for col in data.columns:
    data[col] = data[col].apply(lambda x: str(x).rjust(20))

# Сохранение DataFrame в CSV файл
data.to_csv('angeles_data.csv', index=False)


rounded_angles = [round(angle) for angle in angles]

# Получение уникальных значений и их количества
unique_values, value_counts = zip(*sorted((val, rounded_angles.count(val)) for val in set(rounded_angles)))

# Построение гистограммы
plt.figure(figsize=(10, 6))
plt.bar(unique_values, value_counts, color='blue', alpha=0.6)
plt.xlabel('Пространственный угол (округленный до целого)', fontsize=18)
plt.ylabel('Число событий', fontsize=18)
plt.title('Гистограмма углов между векторами', fontsize=18)
plt.show()