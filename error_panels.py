from PyQt5.QtWidgets import QMessageBox


def invalid_f_input():
    panel = QMessageBox()
    panel.setIcon(QMessageBox.Critical)
    panel.setWindowTitle("ODESolver: ошибка")
    panel.setText("Уравнение введено некорректно")
    panel.setStandardButtons(QMessageBox.Ok)
    retval = panel.exec_()

def invalid_interval_input():
    panel = QMessageBox()
    panel.setIcon(QMessageBox.Critical)
    panel.setWindowTitle("ODESolver: ошибка")
    panel.setText("Интервал введен некорректно")
    panel.setStandardButtons(QMessageBox.Ok)
    retval = panel.exec_()

def invalid_y0_input():
    panel = QMessageBox()
    panel.setIcon(QMessageBox.Critical)
    panel.setWindowTitle("ODESolver: ошибка")
    panel.setText("Начальное условие введено некорректно")
    panel.setStandardButtons(QMessageBox.Ok)
    retval = panel.exec_()


def invalid_add_settings():
    panel = QMessageBox()
    panel.setIcon(QMessageBox.Critical)
    panel.setWindowTitle("ODESolver: ошибка")
    panel.setText("Дополнительные настройки введены некорректно")
    panel.setStandardButtons(QMessageBox.Ok)
    retval = panel.exec_()

