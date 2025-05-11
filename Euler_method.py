import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Callable


def euler(f: Callable[..., float], interval: Tuple[float, float], y0: float, n: int = 10000, plot=True):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Эйлера.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида y' = f(x, y).
        Должна принимать два аргумента: x (float) и y (float),
        и возвращать значение производной (float).

    interval : tuple of float
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : float
        Начальное значение y(x0) для выделения частного решения.

    n : int
        Количество разбиений сетки.

    plot : bool, optional
        Если True, строит график решения (по умолчанию True).

    Возвращает
    -------
    list of tuple
        Список пар (x, y) - точек численного решения ОДУ.
        Длина списка будет n+1 (включая начальную точку).
    """

    h = (interval[1] - interval[0]) / n

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    Y[0] = y0

    for i in range(n-1):
        Y[i+1] = Y[i] + h * f(X[i], Y[i])


    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()

    return np.vstack([X, Y]).T
