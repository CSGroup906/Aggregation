import sys
import cgitb

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from scene import GraphicScene
from view import GraphicView
from NRAProject.MainWindow import Ui_MainWindow

cgitb.enable(format("text"))


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui_init()
        #

    def ui_init(self):
        self.setMinimumWidth(1000)
        self.setMinimumHeight(800)
        # self.setWindowTitle("Graphics Demo")

        self.scene = GraphicScene(self)
        self.view = GraphicView(self.scene, self)

        # 添加Button
        self.button = QtWidgets.QPushButton(self.view)
        self.button.setGeometry(QtCore.QRect(250, 190, 75, 23))
        self.setCentralWidget(self.view)
        self.button.clicked.connect(self.click)
    def click(self):
        self.view.is_delete = True


def demo_run():
    app = QApplication(sys.argv)
    demo = MainWindow()
    # compatible with Mac Retina screen.
    # app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    # app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # show up
    demo.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    demo_run()
