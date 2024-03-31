import numpy as np
x_list = [1, 2, 4, 6, 9, 10]
y_list = [1, 4, 13, 28, 16, 20]
#x_list = [1, 2, 10]
#y_list = [1, 4, 13]


def calculate_difference(x, y):
  f_list = np.zeros(len(x))
  n =len(x)

  for k in range(2, n + 1):
    f= 0
    for j in range(k):
      denominator = 1
      for i in range(k):
        if i != j:
          denominator *= (x[j] - x[i])
      f += (y[j] / denominator)
    f_list[k-2] = f
  return f_list

f_difference = calculate_difference(x_list, y_list)

def caluclate_newton_pol(x_list, y_list, f, x):
  p = y_list[0]
  for j in range(1, len(x_list)):
    denominator = 1
    for i in range(j):
      denominator *= (x - x_list[i])
    p += denominator * f[j-1]
  return p


p = caluclate_newton_pol(x_list, y_list, f_difference, 2.5)

import matplotlib.pyplot as plt
x_values = np.linspace(min(x_list), max(x_list), 100)
y_values = []
for x in x_values:
  y_values.append(caluclate_newton_pol(x_list, y_list, f_difference, x))



plt.plot(x_values, y_values, label='Интерполяционный многочлен Ньютона')
plt.scatter(x_list, y_list, color='red', label='исходные точки')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
#plt.savefig('newton.png', dpi=2000)


print('x: {}\ny: {}'.format(x_list, y_list))

h_list = [x_list[i+1] - x_list[i] for i in range(len(x_list)-1)]
c_list = np.zeros(len(x_list))

n = len(y_list) - 2
A = np.zeros((n, n))
for i in range(n):
    if i > 0:
        A[i, i-1] = h_list[i-1]
    A[i, i] = 2 * (h_list[i] + h_list[i+1])
    if i < n-1:
        A[i, i+1] = h_list[i+1]

b = np.zeros(n)
for i in range(1, n+1):
    b[i-1] = 6 * ((y_list[i+1] - y_list[i]) / h_list[i]) - 6 * ((y_list[i] - y_list[i-1]) / h_list[i-1])

print(A)
print(b)

def run_method(a, b):
    n = len(b)

    x = [0 for _ in range(n)]
    alpha = [0 for _ in range(n)]
    beta = [0 for _ in range(n)]
    gamma = [0 for _ in range(n)]

    gamma[0] = a[0][0]
    alpha[0] = -a[0][1] / gamma[0]
    beta[0] = b[0] / gamma[0]

    for i in range(1, n-1):
        gamma[i] = a[i][i] + a[i][i-1] * alpha[i-1]
        alpha[i] = -a[i][i+1] / gamma[i]
        beta[i] = (b[i] - a[i][i-1] * beta[i-1]) / gamma[i]

    gamma[n-1] = a[n-1][n-1] + a[n-1][n-2] * alpha[n-2]
    beta[n-1] = (b[n-1] - a[n-1][n-2] * beta[n-2]) / gamma[n-1]

    x[n-1] = beta[n-1]
    for i in range(n - 2, -1, -1):
        x[i] = alpha[i] * x[i + 1] + beta[i]

    return x


c = run_method(A, b)
#c = np.linalg.solve(A, b)
print(c)

c.append(0)
c.insert(0, 0)
print(c)

a = np.zeros(len(c)-1)
b = np.zeros(len(c)-1)
d = np.zeros(len(c)-1)
h = h_list

for i in range(1, len(c)):
    a[i-1] = y_list[i]
    b[i-1] = ((y_list[i] - y_list[i-1]) / h_list[i-1]) + (c[i] * h_list[i-1] / 3) + (c[i-1] * h_list[i-1] / 6)
    d[i-1] = (c[i] - c[i-1]) / h_list[i-1]

def calculate_s(a, b, c, d, x, x_i):
  s = a + b * (x-x_i) + (c * (x-x_i) ** 2)/2 + (d * (x-x_i) ** 3)/6
  return s

s_values = []
x_values = []
for i in range(1, len(x_list)):
    x_i_values = np.linspace(x_list[i-1], x_list[i], 1000)
    x_values += list(x_i_values)
    for x in x_i_values:
        s = calculate_s(a[i-1], b[i-1], c[i], d[i-1], x, x_list[i])
        s_values.append(s)

print(len(s_values))

print(len(s_values))

plt.plot(x_values, s_values, label='Кубический сплайн')
plt.scatter(x_list, y_list, color='red', label='исходные точки')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
#plt.savefig('cubic_spline.png', dpi=2000)

from scipy.interpolate import CubicSpline
from scipy.interpolate import lagrange

polynom = lagrange(x_list, y_list)
spline = CubicSpline(x_list, y_list)

x_values = np.linspace(min(x_list), max(x_list), 100)
y_values_spline = spline(x_values)
y_values_linear = np.interp(x_values, x_list, y_list)
y_values_polynom = polynom(x_values)

plt.plot(x_values, y_values_spline, color='green', label='сплайн')
plt.plot(x_values, y_values_linear, color='blue', label='линейно')
plt.plot(x_values, y_values_polynom, color='orange', label='полином')
plt.scatter(x_list, y_list, color='red', label='исходные точки')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
#plt.savefig('interpolation', dpi=2000)

#https://colab.research.google.com/drive/1NMjwlhDKGj-OXN1EWM0iV0Opof6N_kau?usp=sharing