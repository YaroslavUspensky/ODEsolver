import numpy as np
from typing import Callable, Tuple


def slope_field(f: Callable[..., float], rect: Tuple[float, float, float, float], nx: int, ny: int):
    """
    Строит поле направленностей на заданном прямоугольнике
    :param f: правая часть уравнения y'=f(x, y)
    :param rect: координаты прямоугольника (в формате (x1, x2, y1, y2))
                в пределах которого будет постороено поле направленности
    :param nx: число векторов по x
    :param ny: число векторов по y
    """

    X = np.linspace(rect[0], rect[1], nx)
    Y = np.linspace(rect[2], rect[3], ny)

    U = np.zeros((ny, nx))
    V = np.zeros((ny, nx))

    xstep = (rect[1] - rect[0]) / nx
    ystep = (rect[3] - rect[2]) / ny

    arrow_len = np.sqrt((xstep) ** 2 + (ystep) ** 2) / 2

    for i in range(ny):
        for j in range(nx):
            derivative_value = f(X[j], Y[i])
            U[i, j] = arrow_len * np.sqrt(1 / (1 + derivative_value ** 2))
            if derivative_value >= 0:
                V[i, j] = arrow_len * np.sqrt(derivative_value ** 2 / (1 + derivative_value ** 2))
            else:
                V[i, j] = - arrow_len * np.sqrt(derivative_value ** 2 / (1 + derivative_value ** 2))

    return X, Y, U, V
