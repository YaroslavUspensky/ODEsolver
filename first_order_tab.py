from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import e, pi
import sympy as sp

from error_panels import *
from kernel.equation import Equation
from config import *


label_font = QFont(LABELS_FONT, LABELS_FONTSIZE)
field_font = QFont(FIELDS_FONT, FIELDS_FONTSIZE)

class FirstOrderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.solution = None  # contains a solution of given equation with current interval and initial condition

        self.input = FirstOrderInput()

        # "SOLVE" Button
        self.solve_btn = QPushButton("РЕШИТЬ")
        self.solve_btn.setFont(QFont("Calibri", 16))
        self.solve_btn.clicked.connect(self.solve)
        self.solve_btn.setStyleSheet("QPushButton {background-color: " + SOLVE_BTN_COLOR +
                                     "; color: black; border: none}")


        self.plot = Plot()
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
        f, x0, x1, y0, n, method = self.parse_input()
        if f is None:
            return
        if x0 is None or x1 is None:
            return
        if y0 is None:
            return
        if n is None:
            return

        eq = Equation(f)
        self.solution = eq.solve(method, (x0, x1), y0, n, get_solution=True)

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
        :return: f, x0, x1, y0, n, method
        """
        # dy/dx = f
        f_str = self.input.right_side.text()

        f_str = f_str.replace('e', str(e))
        f_str = f_str.replace('pi', str(pi))

        try:
            x, y = sp.symbols('x y')
            f_sym= sp.sympify(f_str)
            f_func = sp.lambdify((x, y), f_sym, 'numpy')
        except sp.SympifyError:
            invalid_f_input()
            return None, 0, 0, 0, 0, 0


        interval_str = self.input.interval_input.text()
        a = interval_str.split(',')

        try:
            x0 = float(a[0][1:])
            x1 = float(a[1][:-1])
        except ValueError:
            invalid_interval_input()
            return 0, None, None, 0, 0, 0



        y0_str = self.input.y0_input.text()
        try:
            y0 = float(y0_str)
        except ValueError:
            invalid_y0_input()
            return 0, 0, 0, None, 0, 0


        n_str = self.input.n_input.text()
        try:
            n = int(n_str)
        except ValueError:
            invalid_add_settings()
            return 0, 0, 0, 0, None, 0

        method = self.input.method_input.currentText()

        return f_func, x0, x1, y0, n, method

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


class FirstOrderInput(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Equation
        equation_frame = QFrame(self)
        equation_layout = QVBoxLayout(equation_frame)
        equation_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)

        equation_txt = QLabel("Введите уравнение:", equation_frame)
        equation_txt.setFont(label_font)
        equation_txt.setMaximumHeight(LABELS_MAXHEIGHT)

        equation_subframe = QFrame(equation_frame)
        equation_sublayout = QHBoxLayout(equation_subframe)
        self.left_side = QLabel("y'=", equation_subframe)
        self.left_side.setFont(field_font)
        self.right_side = QLineEdit(equation_subframe)
        self.right_side.setFont(field_font)
        self.right_side.setPlaceholderText("f(x, y)")

        equation_sublayout.addWidget(self.left_side)
        equation_sublayout.addWidget(self.right_side)
        equation_layout.addWidget(equation_txt)
        equation_layout.addWidget(equation_subframe)



        # Interval
        interval_frame = QFrame(self)
        interval_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        interval_layout = QVBoxLayout(interval_frame)

        interval_txt = QLabel("Введите интервал поиска решения (x0, x1):", interval_frame)
        interval_txt.setFont(label_font)
        interval_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.interval_input = QLineEdit(self)
        self.interval_input.setFont(field_font)
        self.interval_input.setPlaceholderText("(x0, x1)")
        self.interval_input.setMaximumHeight(FIELDS_MAXHEIGHT)

        interval_layout.addWidget(interval_txt)
        interval_layout.addWidget(self.interval_input)



        # y0
        y0_frame = QFrame(self)
        y0_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        y0_layout = QVBoxLayout(y0_frame)

        y0_txt = QLabel("Введите начальное условие y0 = y(x0):", y0_frame)
        y0_txt.setFont(label_font)
        y0_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.y0_input = QLineEdit(self)
        self.y0_input.setFont(field_font)
        self.y0_input.setPlaceholderText("y0 = y(x0)")
        self.y0_input.setMaximumHeight(FIELDS_MAXHEIGHT)

        y0_layout.addWidget(y0_txt)
        y0_layout.addWidget(self.y0_input)



        # Additional settings
        add_settings = QGroupBox("Расширенные настройки")
        add_settings.setFont(label_font)
        add_settings_layout = QGridLayout(add_settings)

        n_txt = QLabel("Число разбиений сетки: ", self)
        n_txt.setFont(label_font)
        self.n_input = QLineEdit("10000", self)
        self.n_input.setFont(field_font)
        method_txt = QLabel("Метод: ", self)
        method_txt.setFont(label_font)
        self.method_input = QComboBox(self)
        self.method_input.addItems(["erk4", "erk3", "erk2", "erk1", "euler"])
        self.method_input.setFont(field_font)

        add_settings_layout.addWidget(n_txt, 0, 0)
        add_settings_layout.addWidget(self.n_input, 0, 1)
        add_settings_layout.addWidget(method_txt, 1, 0)
        add_settings_layout.addWidget(self.method_input, 1, 1)

        add_settings.setLayout(add_settings_layout)
        add_settings.setCheckable(True)
        add_settings.setChecked(False)


        self.layout.addWidget(equation_frame)
        self.layout.addWidget(interval_frame)
        self.layout.addWidget(y0_frame)
        self.layout.addWidget(add_settings)

        self.setLayout(self.layout)


class Plot(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.select_axes = QComboBox(self)
        self.select_axes.setFont(label_font)
        self.select_axes.addItems(["xy", "yy'", "xy'"])

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout.addWidget(self.select_axes)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)

        self.setLayout(self.layout)
