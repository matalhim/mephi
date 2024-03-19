import pandas as pd
import numpy as np
from pymongo import MongoClient
from scipy.optimize import minimize


client = MongoClient('mongodb://localhost:27017/')
db = client['nevod']
collection = db['events']


x_values = [-25.359, -37.609, -37.609, -25.359, -25.359, -37.609, -37.609, -25.359, 6.479, -6.872,
            -6.872, 6.479, 37.369, 22.469, 22.469, 37.369, 37.369, 22.977, 22.977, 37.367, 6.915, -2.794,
            -2.794, 6.915, -9.541, -20.557, -20.557, -9.541, 42.14, 26.94, 26.94, 42.14, -25.359, -37.255, -37.255, -25.359]
y_values = [5.885, 5.885, -7.315, -7.315, 37.335, 37.335, 24.135, 24.135, 12.65, 12.65, -12.63, -12.63, 10.956, 10.956,
            -3.952, -3.952, 45.572, 45.572, 28.482, 28.482, -56.16, -56.16, -70.539, -70.539, 53.623, 64.708, 53.623, 42.539,
            -16.802, -16.802, -32.102, -32.102, -25.745, -25.745, -39.545, -39.545]
z_values = [-6.684, -6.684, -6.684, -6.684, -6.684, -6.684, -6.684, -6.684, 0, 0, 0, 0,
            -14.946, -15.266, -15.346, -15.076, -16.166, -16.461, -16.111, -16.511, -16.151, -15.911, -15.931, -16.101,
            -17.031, -17.796, -17.501, -16.931, -15.136, -15.456, -15.456, -14.686, -7.329, -7.364, -7.339, -7.279]

assert len(x_values) == len(y_values) == len(z_values)

data = {
    'cluster': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9,9],

    'ds': [1, 2, 3, 4, 1, 2, 3, 4,1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4],
    'x': x_values,
    'y': y_values,
    'z': z_values
}


df_coordinates = pd.DataFrame(data)

event_data = collection.find_one({}, {'eas_event_direction': 1})

events_list = []


for direction in event_data['eas_event_direction']:
    cluster = direction['cluster']
    if cluster == 8:
        for station, station_data in direction['stations'].items():
            station_number = int(station.split('_')[1])
            time = station_data['t_std']
            events_list.append({'cluster': cluster, 'ds': station_number, 'time': time})
df_events = pd.DataFrame(events_list)
df_events= df_events.sort_values(by='time') #станции по порядку срабатывания
print(df_events)

coordinates = []

for index, row in df_events.iterrows():
    cluster = row['cluster']
    station = row['ds']
    station_coordinates = df_coordinates[(df_coordinates['cluster'] == cluster) & (df_coordinates['ds'] == station)][['x', 'y', 'z']].values
    coordinates.append(station_coordinates)

coordinates = np.array(coordinates) #координаты станций по порядку срабатывания
print(coordinates)


c = 0.299792458

distances = []

for i in range(len(coordinates) - 1):
    time_diff = df_events.iloc[i+1]['time'] - df_events.iloc[i]['time']
    distance = time_diff * c
    distances.append(distance)

distances = np.array(distances) # расстояния между соседними срабатываниями
print(distances)




def calculate_eas_flatness_coefficients(theta_degrees, phi_degrees, coordinates):
    theta = np.deg2rad(theta_degrees)
    phi = np.deg2rad(phi_degrees)
    x, y, z = coordinates
    a = np.sin(theta) * np.cos(phi)
    b = np.sin(theta) * np.sin(phi)
    c = -np.cos(theta)
    d = -x*a - y*b - z*c
    return a, b, c, d

def calculate_ds_distance(coefficients,coordinates):
    a, b, c, d = coefficients
    x, y, z = coordinates

    d = np.abs(a*x + b*y + c*z + d) / np.sqrt(a**2 + b**2 + c**2)
    return d


min_result = float('inf')
best_theta = None
best_phi = None

for theta in range(0, 90):
    for phi in range(0, 360):
        result = 0
        for i in range(len(coordinates)-1):
            coefficients = calculate_eas_flatness_coefficients(theta, phi, *coordinates[i])
            ds_distance = calculate_ds_distance(coefficients, *coordinates[i+1])
            result += np.abs(ds_distance**2 - distances[i]**2)
        if result < min_result:
            min_result = result
            best_theta = theta
            best_phi = phi

print(best_theta, best_phi)


coefficients = calculate_eas_flatness_coefficients(90, 30, *[[1,1,1]])
ds_distance = calculate_ds_distance(coefficients, *[[0, 0, 0]])
print(ds_distance)