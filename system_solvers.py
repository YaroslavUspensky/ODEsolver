import numpy as np
from typing import Callable, Iterable


def s_euler(f: Callable, interval: Iterable[float], y0: Iterable[float], n: int = 10000):
    """
    Решает системы обыкновенных дифференциальных уравнений (ОДУ) методом Эйлера.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида **y'** = f(x, **y**), где **y** -- вектор-столбец, а f -- соответственно вектор-функция.
        Должна принимать два аргумента: x (float) и y_i (float),
        и возвращать значение производной (float) для i-ой компоненты вектора **y**.

    interval : tuple of float
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : tuple of float
        Начальное значение вектора **y**(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    ----------
    list of tuple
        Список строк (x, y_1, y_2, ...) - точек численного решения системы ОДУ.
        Длина списка будет n+1 (включая начальную точку).
    """

    h = (interval[1] - interval[0]) / n
    dim = len(y0)

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros((dim, n))
    for k in range(dim):
        Y[k, 0] = y0[k]

    for k in range(dim):
        for i in range(n - 1):
            Y[k, i + 1] = Y[k, i] + h * f(X[i], Y[k, i])

    return np.vstack([X, Y]).T


def s_erk1(f: Callable[..., float], interval: Iterable[float], y0: float, n: int = 10000):
    """
    Решает системы обыкновенных дифференциальных уравнений (ОДУ) методом Рунге-Кутты 1-го порядка.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида **y'** = f(x, **y**), где **y** -- вектор-столбец, а f -- соответственно вектор-функция.
        Должна принимать два аргумента: x (float) и y_i (float),
        и возвращать значение производной (float) для i-ой компоненты вектора **y**.

    interval : tuple of float
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : tuple of float
        Начальное значение вектора **y**(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    ----------
    list of tuple
        Список строк (x, y_1, y_2, ...) - точек численного решения системы ОДУ.
        Длина списка будет n+1 (включая начальную точку).
    """

    h = (interval[1] - interval[0]) / n
    dim = len(y0)

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros((dim, n))
    for k in range(dim):
        Y[k, 0] = y0[k]

    b = 1
    c = .5

    for k in range(dim):
        for i in range(n-1):
            Y[k, i+1] = Y[k, i] + h * b * f(X[i] + h*c, Y[k, i])

    return np.vstack([X, Y]).T


def s_erk2(f: Callable[..., float], interval: Iterable[float], y0, n: int = 10000):
    """
    Решает системы обыкновенных дифференциальных уравнений (ОДУ) методом Рунге-Кутты 2-го порядка.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида **y'** = f(x, **y**), где **y** -- вектор-столбец, а f -- соответственно вектор-функция.
        Должна принимать два аргумента: x (float) и y_i (float),
        и возвращать значение производной (float) для i-ой компоненты вектора **y**.

    interval : tuple of float
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : tuple of float
        Начальное значение вектора **y**(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    ----------
    list of tuple
        Список строк (x, y_1, y_2, ...) - точек численного решения системы ОДУ.
        Длина списка будет n+1 (включая начальную точку).
    """

    h = (interval[1] - interval[0]) / n
    dim = len(y0)

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    for k in range(dim):
        Y[k, 0] = y0[k]

    B = np.array([.25, .75])
    c2 = 2/3
    a2 = 2/3

    # 0  | 0  0
    # c2 | a2 0
    # ===|======
    #    | b1 b2

    for k in range(dim):
        for i in range(n-1):
            w1 = f(X[i], Y[k, i])
            w2 = f(X[i] + h * c2, Y[k, i] + h * a2 * w1)

            W = np.array([w1, w2])
            Y[k, i+1] = Y[k, i] + h * (B @ W)

    return np.vstack([X, Y]).T


def s_erk3(f: Callable[..., float], interval: Iterable[float], y0, n: int=10000):
    """
    Решает системы обыкновенных дифференциальных уравнений (ОДУ) методом Рунге-Кутты 1-го порядка.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида **y'** = f(x, **y**), где **y** -- вектор-столбец, а f -- соответственно вектор-функция.
        Должна принимать два аргумента: x (float) и y_i (float),
        и возвращать значение производной (float) для i-ой компоненты вектора **y**.

    interval : tuple of float
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : tuple of float
        Начальное значение вектора **y**(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    ----------
    list of tuple
        Список строк (x, y_1, y_2, ...) - точек численного решения системы ОДУ.
        Длина списка будет n+1 (включая начальную точку).
    """

    h = (interval[1] - interval[0]) / n
    dim = len(y0)

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    for k in range(dim):
        Y[k, 0] = y0[k]


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


    for k in range(dim):
        for i in range(n-1):
            w1 = f(X[i], Y[k, i])
            w2 = f(X[i] + h * c2, Y[k, i] + h * a2 * w1)
            w3 = f(X[i] + h * c3, Y[k, i] + h * a31 * w1 + h * a32 * w2)

            W = np.array([w1, w2, w3])

            Y[k, i+1] = Y[k, i] + h * (B @ W)

    return np.vstack([X, Y]).T


def s_erk4(f: Callable[..., float], interval: Iterable[float], y0, n: int=10000):
    """
    Решает системы обыкновенных дифференциальных уравнений (ОДУ) методом Рунге-Кутты 1-го порядка.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида **y'** = f(x, **y**), где **y** -- вектор-столбец, а f -- соответственно вектор-функция.
        Должна принимать два аргумента: x (float) и y_i (float),
        и возвращать значение производной (float) для i-ой компоненты вектора **y**.

    interval : tuple of float
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : tuple of float
        Начальное значение вектора **y**(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    ----------
    list of tuple
        Список строк (x, y_1, y_2, ...) - точек численного решения системы ОДУ.
        Длина списка будет n+1 (включая начальную точку).
    """

    h = (interval[1] - interval[0]) / n
    dim = len(y0)

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    for k in range(dim):
        Y[k, 0] = y0[k]

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

    for k in range(dim):
        for i in range(n-1):
            w1 = f(X[i], Y[k, i])
            w2 = f(X[i] + h * c2, Y[k, i] + h * a2 * w1)
            w3 = f(X[i] + h * c3, Y[k, i] + h * a3 * w2)
            w4 = f(X[i] + h * c4, Y[k, i] + h * a4 * w3)

            W = np.array([w1, w2, w3, w4])
            Y[k, i+1] = Y[k, i] + h * (B @ W)

    return np.vstack([X, Y]).T
