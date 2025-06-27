import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from typing import Tuple


def high_order_solve(order: int, F: str, interval: Tuple, y_0: Tuple, n=100000, alpha=(1+1j)/2):
    """
    F(x, y, y', y'', ...) = 0
    :param order: порядок уравнения
    :param F: уравнение порядка (order), в общем случае не разрешенно относительно старшей производной
    :param interval: интервал поиска решения
    :param y_0: начальное условие на функцию y и ее производные до order порядка включительно (в порядке возрастания)
    :param n: число разбиений сетки
    :param alpha: параметр схемы Розенброка
    :return: столбцы X и Y, где Y содержит вычисленные точки функции Y и ее первой производной
    """

    common = [f"y_{i}" for i in range(1, order+1)]

    left_side_str = ["y"] + common
    right_side_str = common + [F]

    # ls  d/dx->  rs
    # y           y_1
    # y_1         y_2
    # ...         ...
    # y_(n-1)     y_n


    def jacoby_matrix():
        jmatrix = sp.matrices.zeros(dim, dim)

        for i in range(dim):
            for j in range(dim):
                jmatrix[i, j] = sp.diff(r_sym[i], l_sym[j], 1)

        return jmatrix

    h = (interval[1] - interval[0]) / n

    dim = len(right_side_str)  # - Число уравнений в системе
    m = dim-1 # - Число дифференциальных уравнений в системе
    x = sp.symbols('x')
    l_sym = []
    r_sym = []
    for i in range(dim):
        l_sym.append(sp.symbols(left_side_str[i]))
        r_sym.append(sp.sympify(right_side_str[i]))


    X = np.linspace(interval[0], interval[1], n)
    Y = np.zeros((dim, n))
    # Y[0] = y, Y[1] = y', Y[2] = y'', ...

    # Using initial conditions
    for i in range(dim):
        Y[i][0] = y_0[i]


    J = jacoby_matrix()
    A = sp.matrices.Matrix(np.diag([1 if k<=m-1 else 0 for k in range(dim)])) - alpha * h * J


    A_func = [[] for i in range(dim)]
    r_func = []

    for i in range(dim):
        r_func.append(sp.lambdify([x] + l_sym, r_sym[i], 'numpy'))
        for j in range(dim):
            A_func[i].append(sp.lambdify([x] + l_sym, A[i, j], 'numpy'))

    # A_func * w_1 = right_side_func

    for i in range(1, n):
        r_num = np.zeros(dim, dtype=np.complex64)
        A_num = np.zeros_like(A_func, dtype=np.complex64)

        # evaluating functions
        # for k in range(dim):
        #     r_num[k] = r_func[k](X[i-1]+0.5*h, *[Y[l][i-1] for l in range(dim)])
        #     for j in range(dim):
        #         A_num[k][j] = A_func[k][j](X[i-1], *[Y[l][i-1] for l in range(dim)])

        for j in range(dim):
            r_num[j] = r_func[j](X[i-1]+0.5*h, *[Y[l][i-1] for l in range(dim)])
            for k in range(dim):
                A_num[j][k] = A_func[j][k](X[i-1], *[Y[l][i-1] for l in range(dim)])

        # find w_1
        w_1 = np.linalg.solve(A_num, r_num)


        for j in range(dim):
            Y[j][i] = Y[j][i-1] + h * np.real(w_1[j])

    return X, Y[0], Y[1]
