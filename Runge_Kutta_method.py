import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Tuple


def erk1(f: Callable[..., float], segment: Tuple[float, float], y0: float, n: int = 10000, plot=True):
    """
    :param f: y' = f(x, y)
    :param segment: [x0, x1] - решение ищется на этом отрезке
    :param y0: y(x0) = y0
    :param n: - число разбиений отрезка, число узлов сетки: n+1
    :param plot: если True, то дополнительно выведется график
    :return: последовательность точек {(x_i, y_i)}
    """
    h = (segment[1] - segment[0]) / n

    X = np.linspace(segment[0], segment[1], n)
    Y = np.zeros(n)
    Y[0] = y0

    b = 1
    c = 0.5

    for i in range(n-1):
        w = f(X[i] + h*c, Y[i])
        Y[i+1] = Y[i] + h * b * w

    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()

    return X, Y


def erk2(f: Callable[..., float], segment: Tuple[float, float], y0, n: int = 10000, plot=True):
    """
        :param f: y' = f(x, y)
        :param segment: [x0, x1] - решение ищется на этом отрезке
        :param y0: y(x0) = y0
        :param n: - число разбиений отрезка, число узлов сетки: n+1
        :param plot: если True, то дополнительно выведется график
        :return: последовательность точек {(x_i, y_i)}
    """
    h = (segment[1] - segment[0]) / n

    X = np.linspace(segment[0], segment[1], n)
    Y = np.zeros(n)
    Y[0] = y0

    B = np.array([.25, .75])
    c1 = 0
    c2 = .666667
    a = .666667

    for i in range(n-1):
        W = np.zeros(2)
        W[0] = f(X[i] + h * c1,
                 Y[i])
        W[1] = f(X[i] + h * c2,
                 Y[i] + h * a * W[0])

        Y[i+1] = Y[i] + h * B @ W

    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()

    return X, Y
