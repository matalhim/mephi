import pandas as pd
from pymongo import MongoClient


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
print(df_coordinates)


client = MongoClient('mongodb://localhost:27017/')
db = client['nevod']
collection = db['events']



def calculate_x_axis(document, df_coordinates):
    x_axis_sum = 0
    y_axis_sum = 0
    station_count = 0
    for direction in document.get('eas_event_direction', []):
        cluster = direction.get('cluster')
        for station_key in direction.get('stations', {}):
            station_number = int(station_key[-1])
            df_station = df_coordinates[(df_coordinates['cluster'] == cluster) & (df_coordinates['ds'] == station_number)]

            if not df_station.empty:
                x_axis_sum += df_station['x'].values[0]
                y_axis_sum = df_station['y'].values[0]
                station_count += 1
    return x_axis_sum / station_count, y_axis_sum / station_count

for document in collection.find({}):
    x_axis, y_axis = calculate_x_axis(document, df_coordinates)
    collection.update_one({'_id': document['_id']}, {'$set': {'axis.x_axis': x_axis, 'axis.y_axis': y_axis}})



client.close()