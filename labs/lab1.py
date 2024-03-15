import numpy as np
import matplotlib.pyplot as plt

def df_dx_right(f, x, delta_x):
  return (f(x + delta_x) - f(x)) / delta_x

def df_dx_left(f, x, delta_x):
 return (f(x) - f(x- delta_x)) / delta_x

def df_dx_center(f, x, delta_x):
 return (f(x + delta_x) - f(x - delta_x)) / (2 * delta_x)


def err_calculate(analytical, counting):
    return abs(analytical - counting)

def f(x): return x**2 - np.exp(x)


analytical = 2**2 - np.exp(2)
x=2
delta_x = 0.1

right = df_dx_right(f, x, delta_x)
left = df_dx_left(f, x, delta_x)
center = df_dx_center(f, x, delta_x)

err_right = err_calculate(analytical, right)
err_left = err_calculate(analytical, left)
err_center = err_calculate(analytical, center)
print(analytical, right, left, center)
print('right: ', err_right)
print('left: ', err_left)
print('center: ', err_center)


start = 0.1
end = 1e-14
num_points = 1000
h_values = np.linspace(start, end, num=num_points, endpoint=True)

r_values, l_values, c_values = [], [], []
err_r_values, err_l_values, err_c_values = [], [], []

for h in h_values:
    r_values.append(df_dx_right(f, x, h))
    l_values.append(df_dx_left(f, x, h))
    c_values.append(df_dx_center(f, x, h))

    err_r_values.append(err_calculate(analytical, df_dx_right(f, x, h)))
    err_l_values.append(err_calculate(analytical, df_dx_left(f, x, h)))
    err_c_values.append(err_calculate(analytical, df_dx_center(f, x, h)))

plt.figure()
plt.loglog(h_values, err_r_values, label='right', color='red')
plt.loglog(h_values, err_l_values, label='left', color='blue')
plt.loglog(h_values, err_c_values, label='center', color='green')
plt.xlabel('h')
plt.ylabel('err')
plt.title('err(h)')
plt.legend()
plt.grid(True)
plt.savefig('err(h).png')
