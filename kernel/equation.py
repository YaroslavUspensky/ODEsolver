import matplotlib.pyplot as plt
from kernel.solvers import *
from kernel.slope_field import slope_field



class Equation:
    def __init__(self, equation: Callable):
        self.f = equation
        self.solution = None
        # x  | y  | y'
        # x0 | y0 | y'(x0)

        # self.stiffness = False

    def solve(self, method: str, interval: Tuple[float, float], y0: float, n: int = 10000, get_solution=False):
        if method == "euler":
            self.solution = euler(self.f, interval, y0, n)
        elif method == "erk1":
            self.solution = erk1(self.f, interval, y0, n)
        elif method == "erk2":
            self.solution = erk2(self.f, interval, y0, n)
        elif method == "erk3":
            self.solution = erk3(self.f, interval, y0, n)
        elif method == "erk4":
            self.solution = erk4(self.f, interval, y0, n)
        elif method == "rosenbrock":
            self.solution = ros1(self.f, interval, y0, n)

        if get_solution:
            return self.solution

    def plot(self, axes="xy") -> None:
        """
        Строит график частного решения данного уравнения. Для начала используйте метод solve!
        :param axes: оси, в которых будет построен график решения. Возможные варианты:
                    xy, yy', xy'
        """
        if axes == "xy":
            plt.plot(self.solution[0], self.solution[1])
        elif axes == "yy'":
            plt.plot(self.solution[1], self.solution[2])
        elif axes == "xy'":
            plt.plot(self.solution[0], self.solution[2])

        plt.grid()
        plt.show()

    def slope_field(self, rect: Tuple[float, float, float, float], nx: int, ny: int, plot=False) -> None:
        """
        Строит поле направленностей на заданном прямоугольнике
        :param rect: координаты прямоугольника (в формате (x1, x2, y1, y2))
                    в пределах которого будет постороено поле направленности
        :param nx: число векторов по x
        :param ny: число векторов по y
        """
        X, Y, U, V = slope_field(self.f, rect, nx, ny)

        xstep = (rect[1] - rect[0]) / nx
        ystep = (rect[3] - rect[2]) / ny

        plt.quiver(X, Y, U, V, angles='xy')
        plt.xlim(rect[0] - xstep/2, rect[1] + xstep)
        plt.ylim(rect[2] - ystep, rect[3] + ystep)
        plt.grid()
        plt.show()


    # def isoclines(self, rect, level, n=10000):
    #     eps = 1E-6
    #
    #     X = np.linspace(rect[0], rect[1], n)
    #     Y = np.zeros_like(X)
    #
    #     for i in range(n-1):
    #         derivative_value = self.f(X[i], Y[i])

