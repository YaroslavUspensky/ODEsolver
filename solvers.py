import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Iterable


def euler(f: Callable[..., float], interval: Iterable[float], y0: float, n: int = 10000, plot=True):
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

    n : int, optional
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


def erk1(f: Callable[..., float], interval: Iterable[float], y0: float, n: int = 10000, plot=True):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Рунге-Кутты 1-го порядка.

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

    n : int, optional
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

    b = 1
    c = .5

    for i in range(n-1):
        Y[i+1] = Y[i] + h * b * f(X[i] + h*c, Y[i])

    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()

    return np.vstack([X, Y]).T


def erk2(f: Callable[..., float], interval: Iterable[float], y0, n: int = 10000, plot=True):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Рунге-Кутты 2-го порядка.

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

    n : int, optional
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

    B = np.array([.25, .75])
    c2 = 2/3
    a2 = 2/3

    # 0  | 0  0
    # c2 | a2 0
    # ===|======
    #    | b1 b2

    for i in range(n-1):
        w1 = f(X[i], Y[i])
        w2 = f(X[i] + h * c2, Y[i] + h * a2 * w1)

        W = np.array([w1, w2])
        Y[i+1] = Y[i] + h * (B @ W)

    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()

    return np.vstack([X, Y]).T


def erk3(f: Callable[..., float], interval: Iterable[float], y0, n: int=10000, plot=True):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Рунге-Кутты 3-го порядка.

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

    n : int, optional
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


    B = np.array([1/6, 2/3, 1/6])
    c2 = .5
    c3 = 1.

    a2 = .5
    a31 = -1.
    a32 = 2.

    # 0  | 0   0   0
    # c2 | a2  0   0
    # c3 | a31 a32 0
    # ===|===========
    #    | b1  b2  b3


    for i in range(n-1):
        w1 = f(X[i], Y[i])
        w2 = f(X[i] + h * c2, Y[i] + h * a2 * w1)
        w3 = f(X[i] + h * c3, Y[i] + h * a31 * w1 + h * a32 * w2)

        W = np.array([w1, w2, w3])

        Y[i+1] = Y[i] + h * (B @ W)

    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()

    return np.vstack([X, Y]).T


def erk4(f: Callable[..., float], interval: Iterable[float], y0, n: int=10000, plot=True):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Рунге-Кутты 4-го порядка.

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

    n : int, optional
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

    B = np.array([1/6, 1/3, 1/3, 1/6])
    c2 = .5
    c3 = .5
    c4 = 1.

    a2 = .5
    a3 = .5
    a4 = 1

    # 0  | 0  0  0  0
    # c2 | a2 0  0  0
    # c3 | 0  a3 0  0
    # c4 | 0  0  a4 0
    # ===|===========
    #    | b1 b2 b3 b4

    for i in range(n-1):
        w1 = f(X[i], Y[i])
        w2 = f(X[i] + h * c2, Y[i] + h * a2 * w1)
        w3 = f(X[i] + h * c3, Y[i] + h * a3 * w2)
        w4 = f(X[i] + h * c4, Y[i] + h * a4 * w3)

        W = np.array([w1, w2, w3, w4])
        Y[i+1] = Y[i] + h * (B @ W)

    if plot:
        plt.plot(X, Y)
        plt.grid()
        plt.show()

    return np.vstack([X, Y]).T
