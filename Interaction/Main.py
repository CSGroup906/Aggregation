"""
    Author: JGK
    Time: 2020/11/24 12:04
"""
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

# from MainWindow import Ui_MainWindow
from Interaction.ActionWindow import ActionWindow

import sys


def main():
    app = QApplication(sys.argv)
    w = ActionWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())

    app = QApplication(sys.argv)
    w = ActionWindow()
    w.show()
    sys.exit(app.exec_())
