import sys

from PyQt5.QtWidgets import QMainWindow, QFileDialog
from NRAProject.MainWindow import Ui_MainWindow

from PaintWindow import PaintWindow
from analyze.main import MainWindow


class ActionWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(ActionWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.action_Open.triggered.connect(self.openFile)

    def openFile(self):
        # try-except解决弹出打开文件点取消后界面无响应的问题
        try:
            fileName = QFileDialog.getOpenFileName(self, "选取文件", "./", "xml Files (*.xml)")[0]
            pt = PaintWindow()
            pt.setTitle(fileName.split('/')[-1])
            pt.show()
            print(fileName)

        except IOError:
            pass
