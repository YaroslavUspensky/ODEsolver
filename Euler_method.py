import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Callable


def euler(f: Callable[..., float], segment: Tuple[float, float], y0: float, n: int = 10000, plot=True):
    """
    Функция находит численное решение ОДУ заданного в нормальной форме:
    dy/dx = f(x, y).

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

    for i in range(n-1):
        Y[i+1] = Y[i] + h * f(X[i], Y[i])


    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()


    return X, Y
