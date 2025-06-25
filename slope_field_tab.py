from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.colors import hsv_to_rgb
import numpy as np
import sympy as sp

from error_panels import *
from kernel.slope_field import slope_field
from config import *


label_font = QFont(LABELS_FONT, LABELS_FONTSIZE)
field_font = QFont(FIELDS_FONT, FIELDS_FONTSIZE)


class SlopeFieldTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        self.input = SlopeFieldInput()

        self.build_btn = QPushButton("ПОСТРОИТЬ")
        self.build_btn.setFont(QFont("Calibri", 16))
        self.build_btn.clicked.connect(self.build)
        self.build_btn.setStyleSheet("QPushButton {background-color: " + SOLVE_BTN_COLOR +
                                     "; color: black; border: none}")

        self.sf_plot = SlopeFieldPlot()

        self.layout.addWidget(self.input, 0, 0)
        self.layout.addWidget(self.build_btn, 1, 0)
        self.layout.addWidget(self.sf_plot, 0, 1)

        self.layout.setColumnStretch(1, PLOT_WIDTH_RATIO)
        self.layout.setColumnStretch(0, 10 - PLOT_WIDTH_RATIO)

        self.setLayout(self.layout)
        if SHOW_BORDERS:
            self.setStyleSheet("border: 2px solid grey")

    def build(self):
        f, x1, x2, y1, y2, nx, ny = self.parse_input()

        if f is None:
            return
        if x1 is None or x2 is None:
            return
        if y1 is None or y2 is None:
            return
        if nx is None or ny is None:
            return

        x, y, u, v = slope_field(f, (x1, x2, y1, y2), nx, ny)
        xstep = (x2-x1)/nx
        ystep = (y2-y1)/ny

        self.sf_plot.figure.clear()
        ax = self.sf_plot.figure.add_subplot(111)
        angles = np.arctan(v/u)
        colors = self.angle_to_color(angles)

        ax.quiver(x, y, u, v, color=colors.reshape(-1, 3), angles='xy')
        ax.set_xlim(x1 - xstep/2, x2 + xstep)
        ax.set_ylim(y1 - ystep, y2 + ystep)
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        self.sf_plot.canvas.draw()

    def parse_input(self):
        """
        :return: f, x1, x2, y1, y2, nx, ny
        """

        # dy/dx = f
        f_str = self.input.right_side.text()
        f_str = f_str.replace('e', str(np.e))
        f_str = f_str.replace('pi', str(np.pi))
        try:
            x, y = sp.symbols('x y')
            f_sym = sp.sympify(f_str)
            f_func = sp.lambdify((x, y), f_sym, 'numpy')
        except sp.SympifyError:
            invalid_f_input()
            return None, 0, 0, 0, 0, 0, 0


        x_interval_str = self.input.x_interval_input.text()
        a = x_interval_str.split(',')

        try:
            x1 = float(a[0][1:])
            x2 = float(a[1][:-1])
        except ValueError:
            invalid_interval_input()
            return 0, None, None, 0, 0, 0, 0

        y_interval_str = self.input.y_interval_input.text()
        b = y_interval_str.split(',')

        try:
            y1 = float(b[0][1:])
            y2 = float(b[1][:-1])
        except ValueError:
            invalid_interval_input()
            return 0, 0, 0, None, None, 0, 0

        nx_str = self.input.nx_input.text()
        ny_str = self.input.ny_input.text()
        try:
            nx = int(nx_str)
            ny = int(ny_str)
        except ValueError:
            invalid_n_vectors()
            return 0, 0, 0, 0, 0, None, None

        return f_func, x1, x2, y1, y2, nx, ny

    @staticmethod
    def angle_to_color(angles):
        h = (angles + np.pi) / (2*np.pi) * 0.6 + 0.1
        h = 1 - h
        s = np.ones_like(h)
        v = np.ones_like(h)
        return hsv_to_rgb(np.stack([h, s, v], axis=-1))

class SlopeFieldInput(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Equation
        equation_frame = QFrame(self)
        equation_layout = QVBoxLayout(equation_frame)

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



        # Rect
        rect_frame = QFrame(self)
        rect_layout = QVBoxLayout(rect_frame)

        x_interval_txt = QLabel("Введите интервал по x:", rect_frame)
        x_interval_txt.setFont(label_font)
        x_interval_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.x_interval_input = QLineEdit(rect_frame)
        self.x_interval_input.setFont(field_font)
        self.x_interval_input.setPlaceholderText("(x1, x2)")

        y_interval_txt = QLabel("Введите интервал по y:", rect_frame)
        y_interval_txt.setFont(label_font)
        y_interval_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.y_interval_input = QLineEdit(rect_frame)
        self.y_interval_input.setFont(field_font)
        self.y_interval_input.setPlaceholderText("(y1, y2)")

        rect_layout.addWidget(x_interval_txt)
        rect_layout.addWidget(self.x_interval_input)
        rect_layout.addWidget(y_interval_txt)
        rect_layout.addWidget(self.y_interval_input)

        # nx and ny
        n_frame = QFrame(self)
        n_layout = QVBoxLayout(n_frame)

        nx_txt = QLabel("Введите число векторов по x:", rect_frame)
        nx_txt.setFont(label_font)
        nx_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.nx_input = QLineEdit(rect_frame)
        self.nx_input.setFont(field_font)
        self.nx_input.setPlaceholderText("nx")

        ny_txt = QLabel("Введите число векторов по y:", rect_frame)
        ny_txt.setFont(label_font)
        ny_txt.setMaximumHeight(LABELS_MAXHEIGHT)
        self.ny_input = QLineEdit(rect_frame)
        self.ny_input.setFont(field_font)
        self.ny_input.setPlaceholderText("ny")

        n_layout.addWidget(nx_txt)
        n_layout.addWidget(self.nx_input)
        n_layout.addWidget(ny_txt)
        n_layout.addWidget(self.ny_input)


        self.layout.addWidget(equation_frame)
        self.layout.addWidget(rect_frame)
        self.layout.addWidget(n_frame)
        self.setLayout(self.layout)


class SlopeFieldPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)

        self.setLayout(self.layout)
