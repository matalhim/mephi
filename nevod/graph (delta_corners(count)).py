import plotly.graph_objects as go
from pymongo import MongoClient
from scipy.stats import norm
from scipy.optimize import curve_fit

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['nevod']
collection = db['events_data']

# Собираем статистику для decor_Theta - average_eas_theta
theta_diff_count_map = {}

# Собираем статистику для decor_Phi - average_eas_phi
phi_diff_count_map = {}

data_theta = []
data_phi = []

for document in collection.find():
    decor_Theta = document["decor_Theta"]
    average_eas_theta = document["average_eas_theta"]
    theta_diff = round(decor_Theta - average_eas_theta)  # Округляем до целых
    data_theta.append(theta_diff)

    decor_Phi = document["decor_Phi"]
    average_eas_phi = document["average_eas_phi"]
    phi_diff = round(decor_Phi - average_eas_phi)  # Округляем до целых
    data_phi.append(phi_diff)

    if theta_diff not in theta_diff_count_map:
        theta_diff_count_map[theta_diff] = 1
    else:
        theta_diff_count_map[theta_diff] += 1

    if phi_diff not in phi_diff_count_map:
        phi_diff_count_map[phi_diff] = 1
    else:
        phi_diff_count_map[phi_diff] += 1

client.close()  # Закрываем соединение с базой данных

# Оценка параметров нормального распределения для theta
mu_theta, std_theta = norm.fit(data_theta)

# Создание аппроксимационной кривой для theta
x_theta = list(range(int(min(data_theta)), int(max(data_theta)) + 1))
y_theta = [norm.pdf(i, mu_theta, std_theta) for i in x_theta]

# График для decor_Theta - average_eas_theta
theta_diff_fig = go.Figure()

# Добавление гистограммы
theta_diff_fig.add_trace(go.Bar(
    x=list(theta_diff_count_map.keys()),
    y=list(theta_diff_count_map.values()),
    name='Histogram'
))

# Добавление аппроксимации
theta_diff_fig.add_trace(go.Scatter(
    x=x_theta,
    y=y_theta,
    mode='lines',
    name='Approximation'
))

theta_diff_fig.update_layout(
    xaxis_title='R_difference = Rounded(decor_Theta - average_eas_theta)',
    yaxis_title='Number of Files',
    title='Dependency of R_difference (decor_Theta - average_eas_theta) on the Number of Files',
    width=800,
    height=600
)

theta_diff_fig.show(renderer="browser")

# Оценка параметров нормального распределения для phi
mu_phi, std_phi = norm.fit(data_phi)

# Создание аппроксимационной кривой для phi
x_phi = list(range(int(min(data_phi)), int(max(data_phi)) + 1))
y_phi = [norm.pdf(i, mu_phi, std_phi) for i in x_phi]

# График для decor_Phi - average_eas_phi
phi_diff_fig = go.Figure()

# Добавление гистограммы
phi_diff_fig.add_trace(go.Bar(
    x=list(phi_diff_count_map.keys()),
    y=list(phi_diff_count_map.values()),
    name='Histogram'
))

# Добавление аппроксимации
phi_diff_fig.add_trace(go.Scatter(
    x=x_phi,
    y=y_phi,
    mode='lines',
    name='Approximation'
))

phi_diff_fig.update_layout(
    xaxis_title='R_difference = Rounded(decor_Phi - average_eas_phi)',
    yaxis_title='Number of Files',
    title='Dependency of R_difference (decor_Phi - average_eas_phi) on the Number of Files',
    width=800,
    height=600
)

phi_diff_fig.show(renderer="browser")
