import pandas as pd
import numpy as np
import sys
import json

def find_first_last_ds(lst):
    min_index = lst.index(min(lst))
    max_index = lst.index(max(lst))
    return min_index, max_index

def calculate_radius_vector(coordinates):
    x, y, z = coordinates
    return np.sqrt(x**2 + y**2 + z**2)


find_phi = lambda x, y: np.arctan2(y, x)


coordinates = [[42.14, -16.802, -15.136], [26.94, -16.802, -15.456], [26.94, -32.102, -15.456], [42.14, -32.102, -14.686]]
exp_times = json.loads(sys.argv[1:][0])
#exp_times = [2358.19, 2328.071, 2348.558, 2369.739]
#exp_times = [2350.748, 2333.186, 2366.12]
#exp_times = list(map(float, sys.argv[1:]))
#exp_times = {"1": 2350.748, "2":2333.186, "3": 2366.12}


#exp_intervals = [t - exp_times[0] for t in exp_times]
th_intervals = []
exp_intervals = []
#print(exp_intervals)

new_coordinates = []
for key, value in exp_times.items():
    new_coordinates.append(coordinates[int(key)-1])
    exp_intervals.append(value - next(iter(exp_times.values())))


coordinates = new_coordinates

theta = np.deg2rad(19)  #37.933791518328654
phi = np.deg2rad(173)    #155.37658139743183
c = 0.299792458

first_ds, last_ds = find_first_last_ds(exp_intervals)
vector = [coordinates[last_ds][i] - coordinates[first_ds][i] for i in range(3)]
if find_phi(vector[0], vector[1]) >= 0:
    phi_range = np.arange(180, 360, 1)
else:
    phi_range = np.arange(0, 180, 1)


def calculate_eas_coefficients(theta, phi, coordinates):
    x, y, z = coordinates
    a = np.sin(theta) * np.cos(phi)
    b = np.sin(theta) * np.sin(phi)
    c = -np.cos(theta)
    d = -x * a - y * b - z * c
    return a, b, c, d


def calculate_ds_distance(coefficients, coordinates):
    a, b, c, d = coefficients
    x, y, z = coordinates

    d = np.abs(a * x + b * y + c * z + d) / np.sqrt(a ** 2 + b ** 2 + c ** 2)
    return d


coefficients_eas_front = calculate_eas_coefficients(theta, phi, coordinates[0])

for coordinate in coordinates:
    ds_distance = calculate_ds_distance(coefficients_eas_front, coordinate)
    th_intervals.append(ds_distance / c)

min_delta_time = float('inf')


for theta in np.arange(20, 90, 1):
    theta = np.deg2rad(theta)
    for phi in phi_range:
        phi = np.deg2rad(phi)
        delta_time = 0
        for i in range(1, len(exp_intervals)):
            coefficients = calculate_eas_coefficients(theta, phi, coordinates[0])
            ds_distance = calculate_ds_distance(coefficients, coordinates[i])
            delta_time += np.abs((ds_distance / c) ** 2 - (exp_intervals[i]) ** 2)

        if delta_time < min_delta_time:
            min_delta_time = delta_time
            best_theta = theta
            best_phi = phi


result = {"theta": round(np.rad2deg(best_theta)), "phi": round(np.rad2deg(best_phi))}
print(json.dumps(result))