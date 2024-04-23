import pandas as pd
import numpy as np
import sys
import json

num_cluster = int(sys.argv[1])
json_cluster_dict = sys.argv[2]
cluster_dict = json.loads(json_cluster_dict)
C = 0.299792458

df = pd.read_csv('coordinates_data.csv', sep='\\s+')
cluster_data = {}
for index, row in df.iterrows():
    cluster = row['cluster']
    x = row['x']
    y = row['y']
    if cluster in cluster_data:
        cluster_data[cluster]['x'].append(x)
        cluster_data[cluster]['y'].append(y)
    else:
        cluster_data[cluster] = {'x': [x], 'y': [y]}

x_list = cluster_data[num_cluster]['x']
x_values = []
y_list = cluster_data[num_cluster]['y']
y_values = []
ds_times = []
for ds_i, time in cluster_dict.items():
    i = int(ds_i.split("_")[1])
    x_values.append(x_list[i-1])
    y_values.append(y_list[i-1])
    ds_times.append(time)


ds_delta_times = [round(ds_time - min(ds_times), 3) for ds_time in ds_times]
len_list = len(ds_delta_times)
i = 0

# Используем цикл while для итерации по индексам списка ds_delta_times
while i < len_list:
    if ds_delta_times[i] > 100:
        del ds_delta_times[i]
        del x_values[i]
        del y_values[i]
        # Уменьшаем длину списка и индекс, чтобы избежать сдвига индексов после удаления элемента
        len_list -= 1
    else:
        # Если элемент не удаляется, переходим к следующему индексу
        i += 1



def calculate_O(times, x, y):
    sum_list = [0 for _ in range(3)]
    for i in range(len(times)):
        sum_list[0] += times[i] * x[i]
        sum_list[1] += times[i] * y[i]
        sum_list[2] += times[i]
    omega = np.array([C * sum for sum in sum_list])
    return omega

def calculate_M(times, x, y):
    matrix = np.zeros((3, 3))
    for i in range(len(times)):
        matrix[0][0] += x[i] ** 2
        matrix[1][1] += y[i] ** 2
        matrix[2][2] += 1
        matrix[0][1] += x[i] * y[i]
        matrix[0][2] += x[i]
        matrix[1][2] += y[i]
    matrix[1][0] = matrix[0][1]
    matrix[2][0] = matrix[0][2]
    matrix[2][1] = matrix[1][2]
    return matrix





omega = calculate_O(ds_delta_times, x_values, y_values)
M = calculate_M(ds_delta_times, x_values, y_values)
inverse_M = np.linalg.inv(M)
O = np.dot(inverse_M, omega)

c = - np.sqrt(1 - O[0] ** 2 - O[1] ** 2)
n = [-O[0], -O[1], -c]
len_n = np.linalg.norm(n)

theta_rad = np.arccos(n[2] / round(len_n, 0))
theta_deg = np.degrees(theta_rad)

phi_rad = np.arctan2(n[1], n[0])
phi_deg = np.degrees(phi_rad)
if phi_deg < 0:
    phi_deg = 360 + phi_deg


result = {"theta": theta_deg, "phi": phi_deg}
print(json.dumps(result))