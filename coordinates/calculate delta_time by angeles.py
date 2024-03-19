import pandas as pd
import numpy as np

csv_file_path = "coordinates_data.csv"
df_coordinates = pd.read_csv(csv_file_path, sep=r'\s+')
df_coordinates = df_coordinates[df_coordinates['cluster'] == 8]
print(df_coordinates)
print('\n')


theta = np.deg2rad(37)
phi = np.deg2rad(155)
c = 0.299792458

def calculate_eas_flatness_coefficients(theta, phi, *coordinates):
    x, y, z = coordinates
    a = np.sin(theta) * np.cos(phi)
    b = np.sin(theta) * np.sin(phi)
    c = -np.cos(theta)
    d = -x*a - y*b - z*c
    return a, b, c, d


def calculate_ds_distance(coefficients,*coordinates):
    a, b, c, d = coefficients
    x, y, z = coordinates

    d = np.abs(a*x + b*y + c*z + d) / np.sqrt(a**2 + b**2 + c**2)
    return d


coefficients = calculate_eas_flatness_coefficients(
    theta, phi,
    df_coordinates.iloc[0]['x'], df_coordinates.iloc[0]['y'], df_coordinates.iloc[0]['z'])

delta_times = [0]


for i in range(1, len(df_coordinates)):
    ds_distance = calculate_ds_distance(
        coefficients,
        df_coordinates.iloc[i]['x'], df_coordinates.iloc[i]['y'], df_coordinates.iloc[i]['z'])
    time_diff = ds_distance / c
    delta_times.append(time_diff)
for i in range(len(delta_times)):
    print(df_coordinates.iloc[i])
    print(delta_times[i])
    print('\n')
print(delta_times)


min_result = float('inf')
for theta in range(0, 90):
    theta = np.deg2rad(theta)
    for phi in range(0, 360):
        phi = np.deg2rad(phi)
        result = 0
        for i in range(1, len(df_coordinates)):
            coefficients = calculate_eas_flatness_coefficients(
                theta, phi,
                df_coordinates.iloc[0]['x'], df_coordinates.iloc[0]['y'], df_coordinates.iloc[0]['z'])
            ds_distance = calculate_ds_distance(
                coefficients,
                df_coordinates.iloc[i]['x'], df_coordinates.iloc[i]['y'], df_coordinates.iloc[i]['z'])
            result += np.abs(ds_distance**2 - (delta_times[i] * c)**2)
            if result > 1e-5:
                break
        if result < min_result:
            min_result = result
            best_theta = theta
            best_phi = phi

print('end\n')
print(min_result)
print(best_theta*180/np.pi, best_phi*180/np.pi)

for i in range(1, len(df_coordinates)):
    coefficients = calculate_eas_flatness_coefficients(
        38, 155,
        df_coordinates.iloc[0]['x'], df_coordinates.iloc[0]['y'], df_coordinates.iloc[0]['z'])
    ds_distance = calculate_ds_distance(
        coefficients,
        df_coordinates.iloc[i]['x'], df_coordinates.iloc[i]['y'], df_coordinates.iloc[i]['z'])
    result += np.abs(ds_distance ** 2 - (delta_times[i] * c) **2)
print(result)