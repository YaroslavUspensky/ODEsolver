import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


def solve_euler(f, init_y, segment: Tuple[float, float], n: int = 10000, plot=True):
    """
    Функция находит численное решение ОДУ заданного в нормальной форме:
    dy/dx = f(x, y).

    :param f: функция искомого y и независимой перменной x
    :param init_y: начальное условие на y0
    :param segment: отрезок, на котором ищется решение
    :param plot: если True функция дополнительно выведет график
    :param n: число разбиений сетки
    :return: Последовательность пар точек ({x_i,  y_i})
    """

    h = (segment[1] - segment[0]) / (n+1)

    X = np.linspace(segment[0], segment[1], n+1)
    Y = np.zeros(n+1)
    Y[0] = init_y

    for i in range(n):
        Y[i+1] = Y[i] + h * f(X[i], Y[i])


    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()


    return X, Y

def f(x, y):
    return x-y


print(solve_euler(f, 1, (0, 100), n=100, plot=False))
