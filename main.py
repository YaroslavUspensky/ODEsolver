import sys
from PyQt5.QtWidgets import *

from first_order_tab import FirstOrderTab
from high_order_tab import HighOrderTab
from slope_field_tab import SlopeFieldTab
from config import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.main_layout = QGridLayout()

        self.tabs = QTabWidget(self)
        self.first_order_tab = FirstOrderTab()
        self.high_order_tab = HighOrderTab()
        self.slope_field_tab = SlopeFieldTab()

        self.tabs.addTab(self.first_order_tab, "First order ODE")
        self.tabs.addTab(self.high_order_tab, "High order ODE")
        self.tabs.addTab(self.slope_field_tab, "Slope field")

        self.main_layout.addWidget(self.tabs)

        # self.main_layout.setColumnStretch(1, PLOT_WIDTH_RATIO)
        # self.main_layout.setColumnStretch(0, 10 - PLOT_WIDTH_RATIO)


        self.main_widget.setLayout(self.main_layout)

        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle("ODESolver")
        self.setCentralWidget(self.main_widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
