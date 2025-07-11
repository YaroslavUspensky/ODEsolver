import numpy as np
import sympy as sp
from typing import Callable, Tuple


def euler(f: Callable[..., float], interval: Tuple[float, float], y0: float, n: int = 10000):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Эйлера.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида y' = f(x, y).
        Должна принимать два аргумента: x (float) и y (float),
        и возвращать значение производной (float).

    interval :
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : float
        Начальное значение y(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    -------
        Кортеж столбцов (x, y, y') - точек численного решения ОДУ.
    """
    h = (interval[1] - interval[0]) / n

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    Yprime = np.zeros(n)
    Y[0] = y0
    Yprime[0] = f(X[0], y0)

    for i in range(n-1):
        Y[i+1] = Y[i] + h * f(X[i], Y[i])
        Yprime[i + 1] = f(X[i], Y[i])

    return X, Y, Yprime


def erk1(f: Callable[..., float], interval: Tuple[float, float], y0: float, n: int = 10000):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Рунге-Кутты 1-го порядка.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида y' = f(x, y).
        Должна принимать два аргумента: x (float) и y (float),
        и возвращать значение производной (float).

    interval :
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : float
        Начальное значение y(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    -------
        Кортеж столбцов (x, y, y') - точек численного решения ОДУ.
    """

    h = (interval[1] - interval[0]) / n

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    Yprime = np.zeros(n)
    Y[0] = y0
    Yprime[0] = f(X[0], y0)

    b = 1
    c = .5

    for i in range(n-1):
        Y[i+1] = Y[i] + h * b * f(X[i] + h*c, Y[i])
        Yprime[i + 1] = f(X[i], Y[i])

    return X, Y, Yprime


def erk2(f: Callable[..., float], interval: Tuple[float, float], y0, n: int = 10000):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Рунге-Кутты 2-го порядка.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида y' = f(x, y).
        Должна принимать два аргумента: x (float) и y (float),
        и возвращать значение производной (float).

    interval :
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : float
        Начальное значение y(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    -------
        Кортеж столбцов (x, y, y') - точек численного решения ОДУ.
    """

    h = (interval[1] - interval[0]) / n

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    Yprime = np.zeros(n)
    Y[0] = y0
    Yprime[0] = f(X[0], y0)

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
        Yprime[i + 1] = w1

    return X, Y, Yprime


def erk3(f: Callable[..., float], interval: Tuple[float, float], y0, n: int=10000):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Рунге-Кутты 3-го порядка.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида y' = f(x, y).
        Должна принимать два аргумента: x (float) и y (float),
        и возвращать значение производной (float).

    interval :
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : float
        Начальное значение y(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    -------
        Кортеж столбцов (x, y, y') - точек численного решения ОДУ.
    """

    h = (interval[1] - interval[0]) / n

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    Yprime = np.zeros(n)
    Y[0] = y0
    Yprime[0] = f(X[0], y0)


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

        Y[i + 1] = Y[i] + h * (B @ W)
        Yprime[i + 1] = w1

    return X, Y, Yprime


def erk4(f: Callable[..., float], interval: Tuple[float, float], y0, n: int=10000):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Рунге-Кутты 4-го порядка.

    Параметры
    ----------
    f : callable
        Функция правой части ОДУ вида y' = f(x, y).
        Должна принимать два аргумента: x (float) и y (float),
        и возвращать значение производной (float).

    interval :
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : float
        Начальное значение y(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    -------
        Кортеж столбцов (x, y, y') - точек численного решения ОДУ.
    """

    h = (interval[1] - interval[0]) / n

    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    Yprime = np.zeros(n)
    Y[0] = y0
    Yprime[0] = f(X[0], y0)

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
        Y[i + 1] = Y[i] + h * (B @ W)
        Yprime[ i+ 1] = w1

    return X, Y, Yprime


def ros1(f_str: str, interval: Tuple[float, float], y0, alpha, n: int=100):
    """
    Решает обыкновенное дифференциальное уравнение (ОДУ) методом Розенброка.

      alpha   | Устойчивость | Точность
        0     |      нет     |   O(h)
       1/2    |       A      |  O(h^2)
        1     |      L1      |   O(h)
    (1 + j)/2 |      L2      |  O(h^2)

    Параметры
    ----------
    f : str
        Строка, содержащая функцию правой части ОДУ вида y' = f(x, y).

    interval :
        Интервал интегрирования в виде (x0, x1), где x0 - начальная точка, x1 - конечная точка.

    y0 : float
        Начальное значение y(x0) для выделения частного решения.

    n : int, optional
        Количество разбиений сетки.

    Возвращает
    -------
        Кортеж столбцов (x, y, y') - точек численного решения ОДУ.
    """

    x, y = sp.symbols('x y')
    f_sym = sp.sympify(f_str)
    f_func = sp.lambdify((x, y), f_sym, 'numpy')

    def derivative():
        dfdy_s = sp.diff(f_sym, y, 1)
        dfdy_f = sp.lambdify((x, y), dfdy_s, 'numpy')
        return dfdy_f

    dfdy_func = derivative()

    h = (interval[1] - interval[0]) / n
    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros(n)
    Yprime = np.zeros(n)
    Y[0] = y0
    Yprime[0] = f_func(X[0], y0)

    alpha = 1
    b1 = 1
    c1 = .5

    for i in range(n-1):
        #Ax = _
        A = (1 - alpha * h * dfdy_func(X[i], Y[i]))
        _ = f_func(X[i] + h * c1, Y[i])

        w1 = _ / A

        Y[i + 1] = Y[i] + h * b1 * w1.real
        Yprime[i + 1] = f_func(X[i], Y[i])

    return X, Y, Yprime
