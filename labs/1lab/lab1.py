import numpy as np
import matplotlib.pyplot as plt

def df_dx_right(f, x, delta_x):
    return (f(x + delta_x) - f(x)) / delta_x

def df_dx_left(f, x, delta_x):
    return (f(x) - f(x - delta_x)) / delta_x

def df_dx_center(f, x, delta_x):
    return (f(x + delta_x) - f(x - delta_x)) / (2 * delta_x)

def err_calculate(analytical, counting):
    return abs(analytical - counting)

def f(x):
    return x**2 - np.exp(x)

def df_dx(x):
    return 2*x - np.exp(x)

analytical = df_dx(2)
x = 2
start = 0.1
end = 1e-14
num_points = 10000
h_values = np.logspace(np.log10(start), np.log10(end), num=num_points)
#h_values = np.linspace(start, end, num=num_points, endpoint=True)


err_r_values, err_l_values, err_c_values = [], [], []

for h in h_values:
    right = df_dx_right(f, x, h)
    left = df_dx_left(f, x, h)
    center = df_dx_center(f, x, h)

    err_r_values.append(err_calculate(analytical, right))
    err_l_values.append(err_calculate(analytical, left))
    err_c_values.append(err_calculate(analytical, center))

plt.figure()
plt.loglog(h_values, err_r_values, label='right', color='red')
plt.loglog(h_values, err_l_values, label='left', color='blue')
plt.loglog(h_values, err_c_values, label='center', color='green')
plt.xlabel('h')
plt.ylabel('err')
plt.title('err(h)')
plt.legend()
plt.grid(True)
plt.savefig('err(h)')

