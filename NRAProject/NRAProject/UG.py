import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog)
from PyQt5.QtGui import (QPainter, QPen)
from PyQt5.QtCore import Qt


class Example(QDialog):

    def __init__(self, Dialog):
        super(Example, self).__init__()

        # resize设置宽高，move设置位置
        Dialog.resize(400, 300)
        Dialog.move(100, 100)
        Dialog.setWindowTitle("画直线")

        # setMouseTracking设置为False，否则不按下鼠标时也会跟踪鼠标事件
        self.setMouseTracking(False)

        # 用于存储所画线的坐标[0,1,2,3]从（0,1）到（2,3）的直线
        self.pos = []

        # 用于判断移动时是鼠标左键移动还是右键
        self.leftButtonFlag = False
        self.rightButtonFlag = False

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        # 画线
        if len(self.pos) != 0:
            for x in self.pos:
                painter.drawLine(x[0], x[1], x[2], x[3])
        print(self.pos, self.leftButtonFlag, self.rightButtonFlag)
        painter.end()

    def mouseMoveEvent(self, e):
        '''
         按住鼠标移动事件：更新pos的值
         调用update()函数在这里相当于调用paintEvent()函数
         每次update()时，之前调用的paintEvent()留下的痕迹都会清空
        '''
        if self.leftButtonFlag:
            self.pos[-1][2] = e.pos().x()
            self.pos[-1][3] = e.pos().y()
            self.update()
        else:
            pass

    def mousePressEvent(self, e):
        # 如果移动的鼠标是左键，则实时更新pos中第第三四个值的目标（直线第二个点的X Y 坐标）
        if e.button() == Qt.LeftButton:
            self.leftButtonFlag = True
            self.pos.append([e.pos().x(), e.pos().y(), e.pos().x(), e.pos().y()])
        # self.update()
        if e.button() == Qt.RightButton:
            self.rightButtonFlag = True

    def mouseReleaseEvent(self, e):
        # 鼠标松开时的事件
        if e.button() == Qt.RightButton:
            self.rightButtonFlag = False
            if len(self.pos) != 0:
                self.pos.pop(-1)
                self.update()
        if e.button() == Qt.LeftButton:
            self.leftButtonFlag = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pyqt_learn = Example()
    pyqt_learn.show()
    app.exec_()
