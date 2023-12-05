import plotly.graph_objects as go
from pymongo import MongoClient
import numpy as np

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = db['events_data']

# Собираем данные для decor_Theta - average_eas_theta, decor_Phi - average_eas_phi и decor_time - eas_time
theta_diff_data = []
phi_diff_data = []
time_diff_data = []

for document in collection.find():
    decor_Theta = document["decor_Theta"]
    average_eas_theta = document["average_eas_theta"]
    theta_diff = round(decor_Theta - average_eas_theta)  # Округляем до целых
    theta_diff_data.append(theta_diff)

    decor_Phi = document["decor_Phi"]
    average_eas_phi = document["average_eas_phi"]
    phi_diff = round(decor_Phi - average_eas_phi)  # Округляем до целых
    phi_diff_data.append(phi_diff)

    decor_time = document["decor_time"]
    eas_time = document["eas_time"]
    time_diff = decor_time - eas_time
    time_diff_data.append(time_diff)

client.close()  # Закрываем соединение с базой данных

# График зависимости decor_Theta - average_eas_theta и decor_Phi - average_eas_phi от decor_time - eas_time
scatter_fig = go.Figure()

scatter_fig.add_trace(go.Scatter(
    x=time_diff_data,
    y=theta_diff_data,
    mode='markers',
    marker=dict(color='blue'),
    name='Theta Difference vs. Time Difference'
))

scatter_fig.add_trace(go.Scatter(
    x=time_diff_data,
    y=phi_diff_data,
    mode='markers',
    marker=dict(color='red'),
    name='Phi Difference vs. Time Difference'
))

scatter_fig.update_layout(
    xaxis_title='Decor_time - Eas_time',
    yaxis_title='Difference',
    title='Dependency of Theta and Phi Differences on Time Difference',
    width=800,
    height=600
)

# Используем show с параметром renderer
scatter_fig.show(renderer="browser")
