from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import e, pi


from error_panels import *
from kernel.solvers import *
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


        self.plot = FirstOrderPlot()
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
            f_str, f, x0, x1, y0, n, method, alpha = self.parse_input()
        except TypeError:
            return

        if method == "erk4":
            self.solution = erk4(f, (x0, x1), y0, n)
        elif method == "erk3":
            self.solution = erk3(f, (x0, x1), y0, n)
        elif method == "erk2":
            self.solution = erk2(f, (x0, x1), y0, n)
        elif method == "erk1":
            self.solution = erk1(f, (x0, x1), y0, n)
        elif method == "ros1":
            self.solution = ros1(f_str, (x0, x1), y0, alpha, n)

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
        :return: f_str, f, x0, x1, y0, n, method, alpha
        """

        # get f
        f_str = self.input.f_input.text()
        f_str = f_str.replace('pi', str(pi))
        try:
            x, y = sp.symbols('x y')
            f_sym= sp.sympify(f_str)
            f_func = sp.lambdify((x, y), f_sym, 'numpy')
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
        try:
            y0 = float(sp.sympify(y0_str))
        except ValueError:
            invalid_y0_input()
            return None


        # get n
        n_str = self.input.n_input.text()
        try:
            n = int(n_str)
        except ValueError:
            invalid_add_settings()
            return None


         # get method and alpha
        method = self.input.method_input.currentText()
        if method == "ros1":
            alpha_idx = self.input.alpha_input.currentIndex()
            if alpha_idx == 0:
                alpha = .5
            elif alpha_idx == 1:
                alpha = 1
            else:
                alpha = (1 + 1j)/2
        else:
            alpha = -1


        return f_str, f_func, x0, x1, y0, n, method, alpha

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
        self.f_input = None
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


        # Additional settings

        self.method_input = None
        self.alpha_input = None

        add_settings = self.init_additional_settings()
        add_settings.setCheckable(True)
        add_settings.setChecked(False)

        self.layout.addWidget(equation_frame)
        self.layout.addWidget(interval_frame)
        self.layout.addWidget(y0_frame)
        self.layout.addWidget(n_frame)
        self.layout.addWidget(add_settings)

        self.setLayout(self.layout)

    def init_equation_input(self):
        equation_frame = QFrame(self)
        equation_layout = QVBoxLayout(equation_frame)
        equation_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)

        equation_txt = QLabel("Введите уравнение:", equation_frame)
        equation_txt.setFont(label_font)
        equation_txt.setMaximumHeight(LABELS_MAXHEIGHT)

        equation_subframe = QFrame(equation_frame)
        equation_sublayout = QHBoxLayout(equation_subframe)
        left_side = QLabel("y'=", equation_subframe)
        left_side.setFont(field_font)
        left_side.setMinimumHeight(FIELDS_MINHEIGHT)

        self.f_input = QLineEdit(equation_subframe)
        self.f_input.setFont(field_font)
        self.f_input.setPlaceholderText("f(x, y)")
        self.f_input.setMinimumHeight(FIELDS_MINHEIGHT)

        equation_sublayout.addWidget(left_side)
        equation_sublayout.addWidget(self.f_input)
        equation_layout.addWidget(equation_txt)
        equation_layout.addWidget(equation_subframe)

        return equation_frame

    def init_interval_input(self):
        interval_frame = QFrame(self)
        interval_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
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
        y0_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        y0_layout = QVBoxLayout(y0_frame)

        y0_txt = QLabel("Введите начальное условие y0 = y(x0):", y0_frame)
        y0_txt.setFont(label_font)
        y0_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.y0_input = QLineEdit(y0_frame)
        self.y0_input.setFont(field_font)
        self.y0_input.setPlaceholderText("y0 = y(x0)")
        self.y0_input.setMinimumHeight(FIELDS_MINHEIGHT)

        y0_layout.addWidget(y0_txt)
        y0_layout.addWidget(self.y0_input)

        return y0_frame

    def init_n_input(self):
        n_frame = QFrame(self)
        n_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
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

    def init_additional_settings(self):
        add_settings = QGroupBox("Расширенные настройки")
        add_settings.setFont(label_font)
        add_settings_layout = QGridLayout(add_settings)

        method_txt = QLabel("Метод: ", add_settings)
        method_txt.setFont(label_font)
        self.method_input = QComboBox(add_settings)
        self.method_input.setFont(field_font)
        self.method_input.addItems(["erk4", "erk3", "erk2", "erk1", "ros1"])
        self.method_input.currentIndexChanged.connect(self.enable_alpha_select)

        alpha_txt = QLabel("Параметр alpha (для схемы ros1)", add_settings)
        alpha_txt.setFont(label_font)
        self.alpha_input = QComboBox(add_settings)
        self.alpha_input.addItems(["0.5", "1", "(1 + j)/2"])
        self.alpha_input.setFont(field_font)
        self.alpha_input.setEnabled(False)

        add_settings_layout.addWidget(method_txt, 0, 0)
        add_settings_layout.addWidget(self.method_input, 0, 1)
        add_settings_layout.addWidget(alpha_txt, 2, 0)
        add_settings_layout.addWidget(self.alpha_input, 2, 1)

        add_settings.setLayout(add_settings_layout)

        return add_settings

    def enable_alpha_select(self):
        m = self.method_input.currentText()
        if m == "ros1":
            self.alpha_input.setEnabled(True)
        else:
            self.alpha_input.setEnabled(False)


class FirstOrderPlot(QWidget):
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
