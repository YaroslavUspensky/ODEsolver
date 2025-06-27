from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import pi
import sympy as sp

from kernel.high_ord_solver import high_order_solve
from config import *
from error_panels import *


label_font = QFont(LABELS_FONT, LABELS_FONTSIZE)
field_font = QFont(FIELDS_FONT, FIELDS_FONTSIZE)


class HighOrderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.solution = None  # contains a solution of given equation with current interval and initial condition

        self.input = HighOrderInput()

        # "SOLVE" Button
        self.solve_btn = QPushButton("РЕШИТЬ")
        self.solve_btn.setFont(QFont("Calibri", 16))
        self.solve_btn.clicked.connect(self.solve)
        self.solve_btn.setStyleSheet("QPushButton {background-color: " + SOLVE_BTN_COLOR +
                                     "; color: black; border: none}")

        self.plot = HighOrderPlot()
        self.plot.select_axes.currentIndexChanged.connect(self.change_axes)

        self.layout.addWidget(self.input, 0, 0)
        self.layout.addWidget(self.solve_btn, 1, 0)
        self.layout.addWidget(self.plot, 0, 1)

        self.layout.setColumnStretch(1, PLOT_WIDTH_RATIO)
        self.layout.setColumnStretch(0, 10 - PLOT_WIDTH_RATIO)

        self.setLayout(self.layout)
        if SHOW_BORDERS:
            self.setStyleSheet("border: 2px solid grey")

    def solve(self):
        try:
            order, F_str, x0, x1, y0, n, alpha = self.parse_input()
        except TypeError:
            return

        self.solution = high_order_solve(order, F_str, (x0, x1), y0, n, alpha)

        self.plot.select_axes.setCurrentIndex(0)
        self.plot.figure.clear()
        ax = self.plot.figure.add_subplot(111)
        ax.plot(self.solution[0], self.solution[1])
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        self.plot.canvas.draw()

    def parse_input(self):
        """
        :return: order, F_str, x0, x1, y0, n, alpha
        """

        # get order
        order_str = self.input.order_input.text()
        try:
            order = int(order_str)
        except ValueError:
            invalid_order_input()
            return None


        # get F
        F_str = self.input.F_input.text()
        F_str = F_str.replace("pi", str(pi))
        try:
            x, y = sp.symbols('x y')
            vars = [x, y]
            for i in range(1, order+1):
                vars.append(sp.symbols(f'y_{i}'))
            F_sym = sp.sympify(F_str)
            F_func = sp.lambdify(vars, F_sym, 'numpy')
        except sp.SympifyError:
            invalid_f_input()
            return None


        # get interval
        interval_str = self.input.interval_input.text()
        interval_str = interval_str.replace("pi", str(pi))
        a = interval_str.split(',')
        try:
            x0 = float(sp.sympify(a[0][1:]))
            x1 = float(sp.sympify(a[1][:-1]))
        except ValueError:
            invalid_interval_input()
            return None


        # get y0
        y0_str = self.input.y0_input.text()
        y0_str = y0_str.replace("pi", str(pi))
        b = y0_str[1:-1].split(',')
        y0 = []
        try:
            for i in range(order+1):
                y0.append(float(sp.sympify(b[i])))
            if abs(F_func(x0, *y0)) > EPS:
                invalid_y0_substitute()
                return None

        except ValueError or IndexError:
            invalid_y0_input()
            return None


        # get n
        n_str = self.input.n_input.text()
        try:
            n = int(n_str)
        except ValueError:
            invalid_add_settings()
            return None


        # get alpha
        alpha_idx = self.input.alpha_input.currentIndex()
        if alpha_idx == 0:
            alpha = .5
        elif alpha_idx == 1:
            alpha = 1
        else:
            alpha = (1 + 1j) / 2

        return order, F_str, x0, x1, y0, n, alpha

    def change_axes(self):
        if self.solution is None:
            return

        axes_idx = self.plot.select_axes.currentIndex()
        if axes_idx == 0:
            self.plot.figure.clear()
            ax = self.plot.figure.add_subplot(111)
            ax.plot(self.solution[0], self.solution[1])
            ax.grid(True)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            self.plot.canvas.draw()
        elif axes_idx == 1:
            self.plot.figure.clear()
            ax = self.plot.figure.add_subplot(111)
            ax.plot(self.solution[1], self.solution[2])
            ax.grid(True)
            ax.set_xlabel("y")
            ax.set_ylabel("y'")
            self.plot.canvas.draw()
        else:
            self.plot.figure.clear()
            ax = self.plot.figure.add_subplot(111)
            ax.plot(self.solution[0], self.solution[2])
            ax.grid(True)
            ax.set_xlabel("x")
            ax.set_ylabel("y'")
            self.plot.canvas.draw()


class HighOrderInput(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Order
        self.order_input = None
        order_frame = self.init_order_input()

        # Equation
        self.F_input = None
        equation_frame = self.init_equation_input()


        # Interval
        self.interval_input = None
        interval_frame = self.init_interval_input()


        # y0
        self.y0_input = None
        y0_frame = self.init_y0_input()


        # n
        self.n_input = None
        n_frame = self.init_n_input()

        # alpha
        self.alpha_input = None
        alpha_frame = self.init_alpha_input()


        self.layout.addWidget(order_frame)
        self.layout.addWidget(equation_frame)
        self.layout.addWidget(interval_frame)
        self.layout.addWidget(y0_frame)
        self.layout.addWidget(n_frame)
        self.layout.addWidget(alpha_frame)

        self.setLayout(self.layout)

    def init_order_input(self):
        order_frame = QFrame(self)
        order_layout = QVBoxLayout(order_frame)

        order_txt = QLabel("Порядок уравнения", order_frame)
        order_txt.setFont(label_font)
        order_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.order_input = QLineEdit(order_frame)
        self.order_input.setFont(field_font)
        self.order_input.setMinimumHeight(FIELDS_MINHEIGHT)

        order_layout.addWidget(order_txt)
        order_layout.addWidget(self.order_input)

        return order_frame

    def init_equation_input(self):
        equation_frame = QFrame(self)
        equation_layout = QVBoxLayout(equation_frame)
        equation_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)

        equation_txt = QLabel("Введите уравнение:", equation_frame)
        equation_txt.setFont(label_font)
        equation_txt.setMaximumHeight(LABELS_MAXHEIGHT)

        equation_subframe = QFrame(equation_frame)
        equation_sublayout = QHBoxLayout(equation_subframe)
        left_side = QLabel("0 =", equation_subframe)
        left_side.setFont(field_font)
        left_side.setMinimumHeight(FIELDS_MINHEIGHT)

        self.F_input = QLineEdit(equation_subframe)
        self.F_input.setFont(field_font)
        self.F_input.setPlaceholderText("F(x, y, y', y'', ...)")
        self.F_input.setMinimumHeight(FIELDS_MINHEIGHT)

        equation_sublayout.addWidget(left_side)
        equation_sublayout.addWidget(self.F_input)
        equation_layout.addWidget(equation_txt)
        equation_layout.addWidget(equation_subframe)

        return equation_frame

    def init_interval_input(self):
        interval_frame = QFrame(self)
        interval_layout = QVBoxLayout(interval_frame)

        interval_txt = QLabel("Введите интервал поиска решения (x0, x1):", interval_frame)
        interval_txt.setFont(label_font)
        interval_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.interval_input = QLineEdit(self)
        self.interval_input.setFont(field_font)
        self.interval_input.setPlaceholderText("(x0, x1)")
        self.interval_input.setMinimumHeight(FIELDS_MINHEIGHT)

        interval_layout.addWidget(interval_txt)
        interval_layout.addWidget(self.interval_input)

        return interval_frame

    def init_y0_input(self):
        y0_frame = QFrame(self)
        y0_layout = QVBoxLayout(y0_frame)

        y0_txt = QLabel("Введите начальное условие y0 = y(x0):", y0_frame)
        y0_txt.setFont(label_font)
        y0_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.y0_input = QLineEdit(self)
        self.y0_input.setFont(field_font)
        self.y0_input.setPlaceholderText("y0 = y(x0)")
        self.y0_input.setMinimumHeight(FIELDS_MINHEIGHT)

        y0_layout.addWidget(y0_txt)
        y0_layout.addWidget(self.y0_input)

        return y0_frame

    def init_n_input(self):
        n_frame = QFrame(self)
        n_layout = QVBoxLayout(n_frame)

        n_txt = QLabel("Число разбиений сетки: ", n_frame)
        n_txt.setFont(label_font)
        n_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.n_input = QLineEdit("10000", n_frame)
        self.n_input.setFont(field_font)
        self.n_input.setMinimumHeight(FIELDS_MINHEIGHT)

        n_layout.addWidget(n_txt)
        n_layout.addWidget(self.n_input)

        return n_frame

    def init_alpha_input(self):
        alpha_frame = QFrame(self)
        alpha_layout = QVBoxLayout(alpha_frame)

        alpha_txt = QLabel("Параметр alpha", alpha_frame)
        alpha_txt.setFont(label_font)
        self.alpha_input = QComboBox(alpha_frame)
        self.alpha_input.addItems(["0.5", "1", "(1 + j)/2"])
        self.alpha_input.setFont(field_font)
        self.alpha_input.setMinimumHeight(FIELDS_MINHEIGHT)

        alpha_layout.addWidget(alpha_txt)
        alpha_layout.addWidget(self.alpha_input)

        return alpha_frame


class HighOrderPlot(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.select_axes = QComboBox(self)
        self.select_axes.setFont(label_font)
        self.select_axes.addItems(["xy", "yy'", "xy'"])

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.select_axes)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)
