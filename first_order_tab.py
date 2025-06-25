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


class FirstOrderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.solution = None  # contains solution of given equation with current interval and initial condition

        self.input = FirstOrderInput()

        # "SOLVE" Button
        self.solve_btn = QPushButton("SOLVE")
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
        ax.plot(eq.solution[0], eq.solution[1])
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        self.plot.canvas.draw()

    def parse_input(self):
        # dy/dx = f
        f_str = self.input.right_side.text()

        f_str = f_str.replace('e', str(e))
        f_str = f_str.replace('pi', str(pi))

        try:
            x, y = sp.symbols('x y')
            f_sym= sp.sympify(f_str)
            f_func = sp.lambdify((x, y), f_sym, 'numpy')
        except sp.SympifyError as error:
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

        method_idx = self.input.method_input.currentText()

        return f_func, x0, x1, y0, n, method_idx

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
        self.equation_frame = QFrame(self)
        self.equation_layout = QVBoxLayout(self.equation_frame)
        self.equation_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)

        equation_txt = QLabel("Введите уравнение:", self)
        equation_txt.setFont(QFont(LABELS_FONT, LABELS_FONTSIZE))
        equation_txt.setMaximumHeight(LABELS_MAXHEIGHT)

        self.equation_subframe = QFrame(self.equation_frame)
        self.equation_sublayout = QHBoxLayout(self.equation_subframe)
        self.left_side = QLabel("y'=")
        self.left_side.setFont(QFont(FIELDS_FONT, FIELDS_TXTSIZE))
        self.right_side = QLineEdit(self)
        self.right_side.setFont(QFont(FIELDS_FONT, FIELDS_TXTSIZE))
        self.right_side.setPlaceholderText("f(x, y)")

        self.equation_sublayout.addWidget(self.left_side)
        self.equation_sublayout.addWidget(self.right_side)
        self.equation_layout.addWidget(equation_txt)
        self.equation_layout.addWidget(self.equation_subframe)



        # Interval
        self.interval_frame = QFrame(self)
        self.interval_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.interval_layout = QVBoxLayout(self.interval_frame)

        interval_txt = QLabel("Введите интервал поиска решения (x0, x1):", self)
        interval_txt.setFont(QFont(LABELS_FONT, LABELS_FONTSIZE))
        interval_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.interval_input = QLineEdit(self)
        self.interval_input.setFont(QFont(FIELDS_FONT, FIELDS_TXTSIZE))
        self.interval_input.setPlaceholderText("(x0, x1)")
        self.interval_input.setMaximumHeight(FIELDS_MAXHEIGHT)

        self.interval_layout.addWidget(interval_txt)
        self.interval_layout.addWidget(self.interval_input)



        # y0
        self.y0_frame = QFrame(self)
        self.y0_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.y0_layout = QVBoxLayout(self.y0_frame)

        y0_txt = QLabel("Введите начальное условие y0 = y(x0):", self)
        y0_txt.setFont(QFont(LABELS_FONT, LABELS_FONTSIZE))
        y0_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.y0_input = QLineEdit(self)
        self.y0_input.setFont(QFont(FIELDS_FONT, FIELDS_TXTSIZE))
        self.y0_input.setPlaceholderText("y0 = y(x0)")
        self.y0_input.setMaximumHeight(FIELDS_MAXHEIGHT)

        self.y0_layout.addWidget(y0_txt)
        self.y0_layout.addWidget(self.y0_input)



        # Additional settings
        self.add_settings = QGroupBox("Расширенные настройки")
        self.add_settings.setFont(QFont(LABELS_FONT, LABELS_FONTSIZE))
        self.add_settings_layout = QGridLayout(self.add_settings)

        n_txt = QLabel("Число разбиений сетки: ", self)
        n_txt.setFont(QFont(LABELS_FONT, LABELS_FONTSIZE))
        self.n_input = QLineEdit("10000", self)
        self.n_input.setFont(QFont(FIELDS_FONT, FIELDS_TXTSIZE))
        method_txt = QLabel("Метод: ", self)
        method_txt.setFont(QFont(LABELS_FONT, LABELS_FONTSIZE))
        self.method_input = QComboBox(self)
        self.method_input.addItems(["erk4", "erk3", "erk2", "erk1", "euler"])
        self.method_input.setFont(QFont(FIELDS_FONT, FIELDS_TXTSIZE))



        self.add_settings_layout.addWidget(n_txt, 0, 0)
        self.add_settings_layout.addWidget(self.n_input, 0, 1)
        self.add_settings_layout.addWidget(method_txt, 1, 0)
        self.add_settings_layout.addWidget(self.method_input, 1, 1)

        self.add_settings.setLayout(self.add_settings_layout)
        self.add_settings.setCheckable(True)
        self.add_settings.setChecked(False)


        self.layout.addWidget(self.equation_frame)
        self.layout.addWidget(self.interval_frame)
        self.layout.addWidget(self.y0_frame)
        self.layout.addWidget(self.add_settings)

        self.setLayout(self.layout)


class Plot(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.select_axes = QComboBox(self)
        self.select_axes.setFont(QFont(LABELS_FONT, LABELS_FONTSIZE))
        self.select_axes.addItems(["xy", "yy'", "xy'"])

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout.addWidget(self.select_axes)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)

        self.setLayout(self.layout)
