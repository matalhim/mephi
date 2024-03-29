import numpy as np
import matplotlib.pyplot as plt


a = np.array([
    [10.8, 0.0475, 0, 0, 0],
    [0.0321, 9.9, 0.0523, 0, 0],
    [0, 0.0369, 9, 0.0570, 0],
    [0, 0, 0.0416, 8.1, 0.0411],
    [0, 0, 0, 0.0341, 10.5]
])

b = np.array([12, 10, 15, 8, 10])

x = np.linalg.solve(a, b)
print('нампи:\n', x)
print('\n')

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


x_run_method = run_method(a, b)
print('метод прогонки:\n', x_run_method)
print('\n')

def matrix_change(a, b):
    n = len(b)
    d = np.zeros((n, n))
    c = np.zeros(n)

    for i in range(n):
        for j in range(n):
            if i != j:
                d[i][j] = -a[i][j] / a[j][j]
        c[i] = b[i] / a[i][i]

    return d, c


d, c = matrix_change(a, b)

def Dx_plus_c(x, d, c):
    result = np.zeros(len(x))
    for i in range(len(d)):
        for j in range(len(x)):
            result[i] += d[i][j] * x[j]

    for i in range(len(result)):
        result[i] += c[i]

    return result


def iteration_method(d, c, n):
    x = [1 for _ in range(len(c))]
    x_values = []
    for _ in range(n):
        x = Dx_plus_c(x, d, c)
        x_values.append(x)

    return x_values



x_iteration_method_values = iteration_method(d, c, 100)
print('метод простой итерации\n', x_iteration_method_values[-1])
print('\n')

err_values = [np.linalg.norm(x - x_iteration) / np.linalg.norm(x) for x_iteration in x_iteration_method_values]
count = range(1, len(err_values) + 1)
plt.plot(count, err_values)

#plt.yscale('log')
plt.xlabel('count')
plt.ylabel('err')
plt.title('err(count)')
plt.grid(True)
#plt.savefig('err(count)')
plt.show()


def g_matrix(n):
  g = np.zeros((n, n))
  for i in range(n):
    for j in range(n):
        g [i][j] = 1 / (i + j + 1)
  print(g)
  print('\nчисло обусловленности: ',np.linalg.cond(g))
  print('\n')

  y = g.dot(np.ones((n)))

  x_g_matrix = iteration_method(g, y, 50)
  print('метод простой итерации\n',x_g_matrix[-1])

  x = np.linalg.solve(g, y)
  print(x)

  err_values = [np.linalg.norm(np.ones((n)) - x_iteration) / np.linalg.norm(np.ones((n))) for x_iteration in x_g_matrix]
  count = range(1, len(err_values) + 1)
  plt.plot(count, err_values)
  plt.xlabel('count')
  plt.ylabel('err')
  plt.title('err(count), n = {}'.format(n))
  plt.grid(True)
  #plt.savefig('err(h), n = {}'.format(n))
  plt.show()
g_matrix(5)
g_matrix(12)

# https://colab.research.google.com/drive/1D_doM9ufVQ2TiWmRNqYxy6EMBI3T97xK?usp=sharing